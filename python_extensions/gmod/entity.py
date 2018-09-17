"""
This module contains the :class:`Entity` class which wraps the Lua ``Entity`` class.
"""

from ._base_entity import BaseEntity
from .lua import G, LuaObjectWrapper


class Entity(BaseEntity):
    """Class that wraps the ``Entity`` Lua class."""

    @staticmethod
    def get_by_index(index: int):
        """Returns the :class:`Entity` instance with the index ``index``.

        *Lua similar:* `Entity() <http://wiki.garrysmod.com/page/Global/Entity>`_
        """

        return Entity(G['Entity'](index))
