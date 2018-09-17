"""
This module contains the :class:`Player` class which wraps the Lua ``Player`` class.
"""

from .lua import G
from ._base_entity import BaseEntity


class Player(BaseEntity):
    """Class that wraps the ``Player`` Lua class."""

    @staticmethod
    def get_by_user_id(user_id: int):
        """Returns the :class:`Player` instance with the user ID ``user_id``.

        *Lua similar:* `Player() <http://wiki.garrysmod.com/page/Global/Player>`_
        """
        ply = Player()
        ply.user_id = user_id
        ply.lua_obj = G['Player'](user_id)

        return ply
