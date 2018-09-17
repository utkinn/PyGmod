"""
This module contains the :class:`BaseEntity` class.

:class:`BaseEntity` is the base class for :class:`~gmod.entity.Entity` and :class:`~gmod.player.Player` classes.

.. warning::

    :class:`BaseEntity` is not intended for instantination.
"""

from .lua import G, LuaObjectWrapper


class BaseEntity(LuaObjectWrapper):
    """Base class for :class:`~gmod.entity.Entity` and :class:`~gmod.player.Player` classes."""

    def __init__(self, lua_obj):
        self.lua_obj = lua_obj
