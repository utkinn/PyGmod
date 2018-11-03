from . import lua


def valid(o):
    """Returns ``True`` if  Entity, Panel, custom table object, etc. is valid, ``False`` otherwise."""
    if not isinstance(o, (lua.LuaObject, lua.LuaObjectWrapper)):
        raise TypeError("valid() accepts LuaObject and LuaObjectWrapper classes and subclasses objects only")
    return bool(lua.G['IsValid'](o))
