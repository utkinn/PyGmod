"""
This module contains the :class:`BaseEntity` class.

The :class:`BaseEntity` class is the base class for :class:`~gmod.entity.Entity`
and :class:`~gmod.player.Player` classes.

.. warning::

    :class:`BaseEntity` is not intended for public use.
"""

from .lua import LuaObjectWrapper


class BaseEntity(LuaObjectWrapper):
    """Base class for :class:`~gmod.entity.Entity` and :class:`~gmod.player.Player` classes."""

    def __init__(self, lua_obj):
        self._lua_obj = lua_obj

    @property
    def lua_obj(self):
        return self._lua_obj

    @property
    def index(self):
        """Returns the index of this entity."""
        return int(self.lua_obj['EntIndex'](self.lua_obj))
