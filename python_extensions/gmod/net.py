"""
This module provides the tools for communication between *client* and *server* realms.
"""

import pickle
from collections.abc import Iterable
import base64

from luastack import ValueType, IN_GMOD
from .player import Player
from . import realms, lua

__all__ = ['send', 'receive', 'client', 'server', 'default_receiver']

receivers = {}


def write_py2py_netmsg_data(values):
    """Appends the message data for sending from Python and receiving in Python.

    1. Pickles the ``values`` tuple to :class:`bytes` object.
    2. Encodes the pickle to a Base85 string.
    3. Attaches the Base85 string to the message.
    """
    pickled = pickle.dumps(values, pickle.HIGHEST_PROTOCOL)
    b85encoded = base64.b85encode(pickled)
    lua.G['net']['WriteString'](b85encoded)


def send(message_name, *values, _receiver_=None):
    """Sends a net message to the opposite realm.

    :param str message_name: The message name. Has to be registered with
                             `util.AddNetworkString() <http://wiki.garrysmod.com/page/util/AddNetworkString>`_
                             GLua function.
    :param iterable values: Iterable of values to append to this message.
    :param _receiver_: Message receiver(s). Ignored and can be ``None`` when sending **to** server,
                     but required when sending **from** server.
    :type _receiver_: Player or iterable[Player] or None
    :raises ValueError: if ``receiver`` is ``None`` when sending **from** server.

    *Lua similar:* `net.Start() <http://wiki.garrysmod.com/page/net/Start>`_,
    net.Write...(),
    `net.Send() <http://wiki.garrysmod.com/page/net/Send>`_,
    `net.SendToServer() <http://wiki.garrysmod.com/page/net/SendToServer>`_,
    `net.Broadcast() <http://wiki.garrysmod.com/page/net/Broadcast>`_
    """
    if isinstance(_receiver_, Iterable):
        standardized_receiver = tuple(_receiver_)
        if any(not isinstance(o, Player) for o in standardized_receiver):
            raise TypeError('receivers iterable contain non-Player objects')
    else:
        standardized_receiver = _receiver_

    if not isinstance(message_name, str):
        raise TypeError(f'message name type must be str, not {type(message_name).__name__}')

    if standardized_receiver is None:
        standardized_receiver = default_recv

    if realms.SERVER and not (isinstance(standardized_receiver, Player) or isinstance(standardized_receiver, Iterable)):
        raise ValueError('_receiver_ must be a Player object or an iterable of Player objects '
                         f'when sending messages from server. Got {type(_receiver_).__name__} instead.')

    lua.G['net']['Start'](message_name)

    # if handled_in_lua:
    #     # Just writing the values if the message is intended to be received by Lua code
    #     for v in values:
    #         lua.G['net']['WriteType'](v)
    # else:
    write_py2py_netmsg_data(values)

    if realms.CLIENT:
        lua.G['net']['SendToServer']()
    else:
        if isinstance(standardized_receiver, Player):
            lua.G['net']['Send'](standardized_receiver)
        elif isinstance(standardized_receiver, Iterable):
            lua.G['net']['Send'](lua.table(standardized_receiver))


def received(message):
    receiver = receivers[message]

    # Restoring the object
    lua_player = lua.G['py']['_recv_ply']
    b85encoded = bytes(lua.G['py']['_recv_obj'])
    pickled = base64.b85decode(b85encoded)
    data = pickle.loads(pickled)

    if realms.CLIENT:
        receiver(*data)
    else:
        player = Player(lua_player)
        receiver(*data, player)


def receive(message):
    """Decorator for net message receivers.

    Decorated function is the message receiving callback.
    If data was attached to the message, that data is passed to the callback.
    Message sender as :class:`gmod.player.Player` object is passed after the data,
    if the message was sent from the client.

    Example of sending in the client and receiving in the server::

        if SERVER:
            @net.receive('foo')
            def foo_receiver(a, b, sender):
                print(sender.nick, 'sent:', a, b)

        if CLIENT:
            net.send('foo', 'message', 'received')
            # prints "(nick) sent: message received"

    Server to Client::

        if CLIENT:
            @net.receive('spam')
            def spam_receiver(a):  # <-- No sender argument
                print(a)

        if SERVER:
            net.send('spam', 'eggs', _receiver_=player.get_by_userid(1))

    *Lua similar:* `net.Receive() <http://wiki.garrysmod.com/page/net/Receive>`_,
    net.Read...()
    """

    def decorator(func):
        if message in receivers:
            raise ValueError(f'message {message!r} handler is already registered')

        lua_receiver = lua.eval(f'''
        function(len, ply)
            py._recv_obj = net.ReadString()  -- Actual pickled object
            py._recv_ply = ply

            if CLIENT then
                py._SwitchToClient()
            else
                py._SwitchToServer()
            end

            -- Notifying GPython that message was received; data is ready
            py.Exec("import gmod.net; gmod.net.received({repr(message)})")
        end
        ''')
        lua.G['net']['Receive'](message, lua_receiver)
        receivers[message] = func

        return func

    return decorator


# Default receiver of functions decorated by "client".
# Net messages will be sent to this player when receiver is not specified.
# Context manager "default_receiver" can be used to set the default receiver.
default_recv = None


def select_receiver(kwargs):
    """
    Tries to get the receiver from keyword args dict. If there are no receiver in kwargs, checks the ``default_recv``
    variable. If it is ``None``, raises :class:`TypeError`, otherwise returns the ``default_recv``.
    """
    try:
        return kwargs['_receiver_']
    except KeyError:  # Receiver is not specified in kwargs
        if default_recv is not None:
            # Using the default receiver if it is set
            return default_recv
        else:
            raise TypeError('receiver is not specified and default receiver is not set')


# TODO: return func results if send was used
def realm_decorator(func, target_realm):
    """Base decorator of :func:`client` and :func:`server`."""

    # Do nothing if we just generate documentation
    if not IN_GMOD:
        return func

    # Net string for calling the function from a different realm
    net_string_call = f'pygmod_net:{func.__module__}.{func.__qualname__} (call)'
    # Net string for returning the results back
    net_string_return = f'pygmod_net:{func.__module__}.{func.__qualname__} (return)'

    add_net_strings_for_decorated_func(net_string_call, net_string_return)

    if target_realm:
        register_call_receiver(func, net_string_call, net_string_return)
    else:
        register_return_receiver(net_string_return)

    def decorated(*args, **kwargs):
        # Just call the function if it is in the same realm
        if target_realm:
            # Removing the receiver argument, so we don't get
            # "TypeError: got an unexpected keyword argument '_receiver_'"
            if '_receiver_' in kwargs:
                del kwargs['_receiver_']

            return func(*args, **kwargs)

        # Sending a net message with the arguments, if the actual function is in a different realm.
        else:
            print('else: diff. realm')
            print('sending net_string_call', realms.REALM)
            if realms.CLIENT:
                send(net_string_call, args, kwargs)
                return _net_decorator_call_returns
            else:
                recv = select_receiver(kwargs)
                send(net_string_call, args, kwargs, _receiver_=recv)
                return _net_decorator_call_returns

    print('reg')
    return decorated


def register_return_receiver(net_string_return):
    r"""Registers the return receiver.

    It receives ``pygmod_net:(``\ *function full name*\ ``) (return)`` net messages which contain the results
    of the function decorated by :func:`realm_decorator`.
    """
    @receive(net_string_return)
    def returner(*args):
        global _net_decorator_call_returns
        print(args)
        _net_decorator_call_returns = args[0]


def register_call_receiver(func, net_string_call, net_string_return):
    r"""Registers the call receiver.

    The call receiver is the net receiver of the net string ``pygmod_net:(``\ *function full name*\ ``) (call)``.
    It calls the underlying function and sends back a ``pygmod_net:(``\ *function full name*\ ``) (return)``
    net message with the function results attached.
    """
    if realms.CLIENT:
        @receive(net_string_call)
        def receiver(args, kwargs):
            print('recv nsc')
            returns = func(*args, **kwargs)
            print('send net_string_return')
            send(net_string_return, returns)
    else:
        @receive(net_string_call)
        def receiver(args, kwargs, sender):
            print('recv nsc')
            returns = func(*args, **kwargs)
            print('sendn et_string_return')
            send(net_string_return, returns, _receiver_=sender)


def add_net_strings_for_decorated_func(net_string_call, net_string_return):
    """
    Calls ``util.AddNetworkString``
    for handling calls of function decorated by :func:`realm_decorator` between realms.
    """
    if realms.SERVER:
        lua.G['util']['AddNetworkString'](net_string_call)
        lua.G['util']['AddNetworkString'](net_string_return)


def client(func):
    """Decorator for *client-side* functions.

    .. warning::
        This decorator is currently broken.

    Functions decorated by :func:`client` act like regular functions when called in the *client* realm.
    When they are called in the *server* realm, a net message is sent from the *server* to the *client*.
    Arguments which were passed to a function are attached to this message.

    Example of shared code::

        @net.client
        def spam(message):
            chat.print(message)
            return 'done'

        if CLIENT:
            # Will print 'eggs' to the client's chat, then will print 'done' to the client's console.
            print(spam('eggs'))
        else:  # Server
            # Receiver has to be specified when calling server-decorated functions.
            # Will print "foo" to the chat of the player with the UserID 1,
            # then will print 'done' to the server console.
            print(spam('foo', receiver=player.get_by_userid(1)))

    .. warning::

        This decorator will work properly only when the decorated function is defined
        in the *shared* realm (__shared_autorun__ package).
    """
    return realm_decorator(func, realms.CLIENT)


def server(func):
    """Decorator for *server-side* functions.

    .. warning::
        This decorator is currently broken.

    Functions decorated by :func:`server` act like regular functions when called in the *server* realm.
    When they are called in the *client* realm, a net message is sent from the *client* to the *server*.
    Arguments which were passed to a function are attached to this message.

    Example of shared code::

        @net.server
        def kill_everyone():
            for p in player.all():
                p.kill()
            return 'everyone was killed!'

        if CLIENT:
            print(kill_everyone())  # Will kill every player and print 'everyone was killed!' to the client's console.
        else:  # Server
            # There is no difference between calling server-decorated functions on client and on server.
            print(kill_everyone())

    .. warning::

        This decorator will work properly only when the decorated function is defined
        in the *shared* realm (__shared_autorun__ package).
    """
    return realm_decorator(func, realms.SERVER)


class default_receiver:
    """Context manager which sets the default receiver, so you don't have to use the ``_receiver_`` argument every time.

    Instead of specifying the receiver on each call::

        recv = player.get_by_userid(1)

        chat.print('spam', _receiver_=recv)
        chat.print('eggs', _receiver_=recv)
        chat.print('foo', _receiver_=recv)
        chat.print('bar', _receiver_=recv)

    you can use :class:`default_receiver`::

        recv = player.get_by_userid(1)
        with net.default_receiver(recv):
            chat.print('spam')
            chat.print('eggs')
            chat.print('foo')
            chat.print('bar')
            # All goes to recv
    """

    def __init__(self, receiver):
        self.receiver = receiver

    def __enter__(self):
        global default_recv
        default_recv = self.receiver

    def __exit__(self, exc_type, exc_val, exc_tb):
        global default_recv
        default_recv = None
