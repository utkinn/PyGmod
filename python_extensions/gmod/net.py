"""
This module provides tools for communication between *client* and *server*.
"""

import pickle
from collections.abc import Iterable

from .lua import G, table
from .player import Player
from .realms import CLIENT, SERVER


class SizeError(Exception):
    """Indicates that there are too many values. Raised by :func:`send` if more than 255 values are passed."""


def _write_py2py_netmsg_data(values):
    """Appends the message data for sending from Python and receiving in Python.

    Pickles the ``values`` tuple to :class:`bytes` object, then writes its length and himself.
    """
    pickled = pickle.dumps(values, pickle.HIGHEST_PROTOCOL)
    length = len(pickled)
    G['net']['WriteUInt'](length, 32)
    G['net']['WriteData'](pickled, length)


def send(message_name, *values, addressee=None, lua_receiver=False):
    """Sends a net message to the opposite realm.

    :param str message_name: The message name. Has to be registered with
                             `util.AddNetworkString() <http://wiki.garrysmod.com/page/util/AddNetworkString>`_
                             GLua function.
    :param iterable values: Iterable of values to append to this message.
    :param addressee: Message addressee. Ignored when sending **to** server, but required when sending **from** server.
    :type addressee: Player or iterable[Player] or None
    :param bool lua_receiver: Whether this message is intended to be received by Lua code.
    :raises ValueError: if the addressee is None when sending **from** server.
    :raises SizeError: if more than 255 values are passed and ``lua_receiver`` is ``False``.
    """

    if not isinstance(message_name, str):
        raise TypeError(f'message name type must be str, not {type(message_name).__name__}')

    if SERVER and not (isinstance(addressee, Player) or isinstance(addressee, Iterable)):
        raise ValueError('addressee must be a Player object or an iterable of Player objects '
                         f'when sending messages from server. Got {type(addressee).__name__} instead.')

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
        if isinstance(addressee, Player):
            G['net']['Send'](addressee)
        elif isinstance(addressee, Iterable):
            G['net']['Send'](table(addressee))
