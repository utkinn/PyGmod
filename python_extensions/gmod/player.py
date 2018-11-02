"""
This module contains the :class:`Player` class which wraps the Lua ``Player`` class.
"""

from ._base_entity import BaseEntity
from .lua import G


class Player(BaseEntity):
    """Class that wraps the ``Player`` Lua class."""

    @property
    def nick(self):
        return str(self.lua_obj['Nick'](self.lua_obj))


def get_by_userid(userid: int):
    """Returns the :class:`Player` object which refers to the player with the user ID ``userid``.

    *Lua similar:* `Player() <http://wiki.garrysmod.com/page/Global/Player>`_
    """
    return Player(G['Player'](userid))
