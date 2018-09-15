"""
This module provides tools for communication between *client* and *server*.
"""

import pickle

from .lua import G
from .realms import CLIENT


class SizeError(Exception):
    """Indicates that there are too many values. Raised by :func:`send` if more than 255 values are passed."""


# def register_net_message_name(name):
#     """Wrapper for GLua's `util.AddNetworkString <http://wiki.garrysmod.com/page/util/AddNetworkString>`_."""
#     if not isinstance(name, str):
#         raise TypeError(f'message name type must be str, not {type(name).__name__}')
#     G['util']['AddNetworkString'](name)


def _write_py2py_netmsg_data(values):
    """Appends the message data for sending from Python and receiving in Python.

    1. Pickles all objects.
    2. Creates a header string which holds data about the pickled objects' lengths.
    3. Writes the header, then the pickled objects.
    """
    values_lst = list(values)  # Creating a copy in case if we got an iterator
    if len(values_lst) > 255:
        raise SizeError('maximal supported appended value quantity is 255. Try putting them all into a list.')

    # header is a string that contains data about the appended data.
    # The format is "x x x ...".
    # Each "x" is the length of an object in bytes.
    header = ''

    # Pickling all values
    pickled_values = [pickle.dumps(v, pickle.HIGHEST_PROTOCOL) for v in values_lst]

    # Adding length data to header
    for v in pickled_values:
        header += ' ' + str(len(v))

    # Writing the header
    G['net']['WriteString'](header)
    # Writing the pickled objects
    for v in pickled_values:
        G['net']['WriteData'](v, len(v))


def send(message_name, *values, addressee=None, lua_receiver=False):
    """Sends a net message to the opposite realm.

    :param str message_name: The message name. Has to be registered with
                             `util.AddNetworkString <http://wiki.garrysmod.com/page/util/AddNetworkString>`_
                             GLua function or :func:`register_net_message_name`.
    :param iterable values: Iterable of values to append to this message.
    :param addressee: Message addressee. Ignored when sending **to** server, but required when sending **from** server.
    :type addressee: Player or iterable[Player] or None
    :param bool lua_receiver: Whether this message is intended to be received by Lua code.
    :raises ValueError: if the addressee is None when sending **from** server.
    :raises SizeError: if more than 255 values are passed and ``lua_receiver`` is ``False``.
    """
    if not isinstance(message_name, str):
        raise TypeError(f'message name type must be str, not {type(name).__name__}')

    G['net']['Start']()

    if lua_receiver:
        # Just writing the values if the message is intended to be received by Lua code
        for v in values:
            G['net']['WriteType'](v)
    else:
        _write_py2py_netmsg_data(values)

    if CLIENT:
        G['net']['SendToServer']()
    else:
        G['net']['Send'](...)  # TODO
