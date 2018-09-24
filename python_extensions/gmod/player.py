"""
This module contains the :class:`Player` class which wraps the Lua ``Player`` class.
"""

from ._base_entity import BaseEntity
from .lua import G


class Player(BaseEntity):
    """Class that wraps the ``Player`` Lua class."""

    @staticmethod
    def get_by_user_id(user_id: int):
        """Returns the :class:`Player` instance with the user ID ``user_id``.

        *Lua similar:* `Player() <http://wiki.garrysmod.com/page/Global/Player>`_
        """
        return Player(G['Player'](user_id))
