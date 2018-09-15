"""
This module contains the :class:`Player` class which wraps the Lua ``Player`` class.
"""

from .lua import G
from .entity import Entity


class Player(Entity):
    """Class that wraps the ``Player`` Lua class."""

    @classmethod
    def get_by_user_id(cls, user_id: int):
        """Returns the :class:`Player` instance with the user ID ``user_id``.

        *Lua similar:* `Player() <http://wiki.garrysmod.com/page/Global/Player>`_
        """
        ply = Player()
        ply.user_id = user_id
        ply.lua_obj = G['Player'](user_id)

        return ply
