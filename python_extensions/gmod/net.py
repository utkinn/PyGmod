"""
This module provides the tools for communication between *client* and *server* realms.
"""

import pickle
from collections import defaultdict
from collections.abc import Iterable

from luastack import ValueType
from .player import Player
from . import realms, lua

__all__ = ['send', 'receive', 'client', 'server', 'default_receiver']

receivers = defaultdict(lambda: [])


def write_py2py_netmsg_data(values):
    """Appends the message data for sending from Python and receiving in Python.

    Pickles the ``values`` tuple to :class:`bytes` object, then writes its length and himself.
    """
    pickled = pickle.dumps(values, pickle.HIGHEST_PROTOCOL)
    length = len(pickled)
    lua.G['net']['WriteUInt'](length, 32)
    lua.G['net']['WriteData'](pickled, length)


# def send(message_name, *values, receiver=None, handled_in_lua=False):
def send(message_name, *values, receiver=None):
    """Sends a net message to the opposite realm.

    :param str message_name: The message name. Has to be registered with
                             `util.AddNetworkString() <http://wiki.garrysmod.com/page/util/AddNetworkString>`_
                             GLua function.
    :param iterable values: Iterable of values to append to this message.
    :param receiver: Message receiver(s). Ignored and can be ``None`` when sending **to** server,
                     but required when sending **from** server.
    :type receiver: Player or iterable[Player] or None
    :raises ValueError: if ``receiver`` is ``None`` when sending **from** server.
    """
    if isinstance(receiver, Iterable):
        standardized_receiver = tuple(receiver)
        if any(not isinstance(o, Player) for o in standardized_receiver):
            raise TypeError('receivers iterable contain non-Player objects')
    else:
        standardized_receiver = receiver

    if not isinstance(message_name, str):
        raise TypeError(f'message name type must be str, not {type(message_name).__name__}')

    if standardized_receiver is None:
        standardized_receiver = default_recv

    if realms.SERVER and not (isinstance(standardized_receiver, Player) or isinstance(standardized_receiver, Iterable)):
        raise ValueError('receiver must be a Player object or an iterable of Player objects '
                         f'when sending messages from server. Got {type(receiver).__name__} instead.')

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
    for r in receivers[message]:
        lua_player = lua.G['py']['_recv_ply']
        if lua_player.type == ValueType.NIL:
            player = None
        else:
            player = Player(lua_player)
        data = pickle.loads(bytes(lua.G['py']['_recv_obj']))

        r(*data, player)


def receive(message):
    """Decorator for net message receivers.

    Example of sending in Python and receiving in Python::

        if SERVER:
            G['util']['AddNetworkString']('foo')

            @net.receive('foo')
            def foo_receiver(a, b):
                print(a, b)


        if CLIENT:
            net.send('foo', 'message', 'received', receiver=get_player_by_userid(1))
            # 'message received' will be printed in the console of the player with the UserID 1.
    """
    # Commented part of the documentation:

    # Sending in Lua and receiving in Python::
    #
    #     --- sv_init.lua ---
    #
    #     util.AddNetworkString('foo')
    #
    #     net.Start('foo')
    #         net.WriteString('message')
    #         net.WriteString('received')
    #     net.Send(Player(1))
    #
    #
    #     --- __client_autorun__\\__init__.py ---
    #
    #     from gmod import net
    #
    #     @net.receive('foo')
    #     def foo_receiver(a, b):
    #         print(a, b)

    # End of documentation
    def decorator(func):
        lua_receiver = lua.eval(f'''
        function(_, ply)
            local _recv_len = net.ReadUInt(32)  -- Pickled object length
            py._recv_obj = net.ReadData(_recv_len)  -- Actual pickled object
            py._recv_ply = ply

            -- Notifying GPython that message was received; data is ready
            py.Exec("import gmod.net; gmod.net.received({repr(message)})")
        end
        ''')
        lua.G['net']['Receive'](message, lua_receiver)
        receivers[message].append(func)

        return func

    return decorator


# Default receiver of functions decorated by "client".
# Net messages will be sent to this player when receiver is not specified.
# Context manager "default_receiver" can be used to set the default receiver.
default_recv = None


def select_receiver(kwargs):
    try:
        return kwargs['receiver']
    except KeyError:  # Receiver is not specified in kwargs
        if default_recv is not None:
            # Using the default receiver, if it is set
            return default_recv
        else:
            raise TypeError('receiver is not specified and default receiver is not set')


def realm_decorator(func, target_realm):
    """Base decorator of :func:`client` and :func:`server`."""
    net_string = f'gpython_net:{func.__module__}.{func.__qualname__}'

    if realms.SERVER:
        lua.G['util']['AddNetworkString'](net_string)
    else:
        @receive(net_string)
        def _(args, kwargs):
            func(*args, **kwargs)

    def decorated(*args, **kwargs):
        if target_realm:
            # Removing the receiver argument, so we don't get "TypeError: got an unexpected keyword argument 'receiver'"
            # del kwargs['receiver']
            return func(*args, **kwargs)
        else:
            if realms.CLIENT:
                send(net_string, args, kwargs)
            else:
                recv = select_receiver(kwargs)
                send(net_string, args, kwargs, receiver=recv)

    return decorated


def client(func):
    """Decorator for *client-side* functions.

    Functions decorated by :func:`client` act like regular functions when called in the *client* realm.
    When they are called in the *server* realm, a net message is sent from the *server* to the *client*.
    Arguments which were passed to a function are attached to this message.

    Example of shared code::

        @net.client
        def spam(message):
            chat.print(message)


        if CLIENT:
            spam('eggs')  # Will print 'eggs' to the client's chat.
        else:  # Server
            # Receiver has to be specified when calling server-decorated functions.
            # Will print "foo" to the chat of the player with the UserID 1.
            spam('foo', receiver=player.get_by_userid(1))

    .. warning::

        This decorator will work properly only when the decorated function is defined
        in the *shared* realm (__shared_autorun__ package).
    """
    return realm_decorator(func, realms.CLIENT)


def server(func):
    """Decorator for *client-side* functions.

    Functions decorated by :func:`client` act like regular functions when called in the *client* realm.
    When they are called in the *server* realm, a net message is sent from the *server* to the *client*.
    Arguments which were passed to a function are attached to this message.

    Example of shared code::

        @net.server
        def kill_everyone():
            for p in player.all():
                p.kill()


        if CLIENT:
            kill_everyone()  # Will kill every player
        else:  # Server
            # There is no difference between calling server-decorated functions on client and on server.
            kill_everyone()

    .. warning::

        This decorator will work properly only when the decorated function is defined
        in the *shared* realm (__shared_autorun__ package).
    """
    return realm_decorator(func, realms.SERVER)


class default_receiver:
    """Context manager which sets the default receiver.

    Instead of specifying the receiver on each call::

        recv = player.get_by_userid(1)

        chat.print('spam', receiver=recv)
        chat.print('eggs', receiver=recv)
        chat.print('foo', receiver=recv)
        chat.print('bar', receiver=recv)

    you can use :class:`default_receiver`::

        recv = player.get_by_userid(1)
        with net.default_receiver(recv):
            chat.print('spam')
            chat.print('eggs')
            chat.print('foo')
            chat.print('bar')
    """

    def __init__(self, receiver):
        self.receiver = receiver

    def __enter__(self):
        global default_recv
        default_recv = self.receiver

    def __exit__(self, exc_type, exc_val, exc_tb):
        global default_recv
        default_recv = None
