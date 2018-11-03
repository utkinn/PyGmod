"""
This module contains the :class:`Player` class which wraps the Lua ``Player`` class.
"""
from . import _base_entity, lua, realms, hooks
from .exceptions import RealmError, NotReadyError

if realms.CLIENT:
    _initpostentity_occurred = False


    @hooks.hook('InitPostEntity')
    def _allow_getlocal():
        global _initpostentity_occurred
        _initpostentity_occurred = True


class Player(_base_entity.BaseEntity):
    """Class that wraps the ``Player`` Lua class."""

    @property
    def nick(self):
        return str(self.lua_obj['Nick'](self.lua_obj))


def get_by_userid(userid: int):
    """Returns the :class:`Player` object which refers to the player with the user ID ``userid``.

    *Lua similar:* `Player() <http://wiki.garrysmod.com/page/Global/Player>`_
    """
    return Player(lua.G['Player'](userid))


def getlocal():
    """Returns the player object of the current client.

    .. note::
        ``getlocal()`` will raise :class:`NotReadyError` if called before the
        `InitPostEntity <http://wiki.garrysmod.com/page/GM/InitPostEntity>`_ event.

    *Lua similar:* `LocalPlayer() <http://wiki.garrysmod.com/page/Global/LocalPlayer>`_
    """
    if realms.SERVER:
        raise RealmError('player.getlocal() is useless in the server realm')
    if not _initpostentity_occurred:
        raise NotReadyError('player.getlocal() is available only after the InitPostEntity event')

    return Player(lua.G['LocalPlayer']())
