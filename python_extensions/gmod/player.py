"""
This module contains the :class:`Player` class which wraps the Lua ``Player`` class.
"""

from ._base_entity import BaseEntity
from .lua import G


class Player(BaseEntity):
    """Class that wraps the ``Player`` Lua class."""
    ...


def get_by_userid(userid: int):
    """Returns the :class:`Player` instance with the user ID ``userid``.

    *Lua similar:* `Player() <http://wiki.garrysmod.com/page/Global/Player>`_
    """
    return Player(G['Player'](userid))
