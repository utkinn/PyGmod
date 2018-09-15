"""
This module contains the :class:`Entity` class which wraps the Lua ``Entity`` class.
"""

from .lua import G, LuaObjectWrapper


class Entity(LuaObjectWrapper):
    """Class that wraps the ``Entity`` Lua class."""

    @classmethod
    def get_by_index(cls, index: int):
        """Returns the :class:`Entity` instance with the index ``index``.

        *Lua similar:* `Entity() <http://wiki.garrysmod.com/page/Global/Entity>`_
        """
        ent = Entity()
        ent.index = index
        ent.lua_obj = G['Entity'](index)

        return ent
