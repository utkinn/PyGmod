from collections.abc import Iterable

from . import lua


def _check_component_type(*comps):
    if any(not isinstance(o, int) for o in comps):
        raise TypeError('color components must be int')


class Color:
    """
    The color class which is used in various client functions, such as functions in modules :mod:`gmod.chat`
    and :mod:`gmod.draw`.

    ``Color`` constructor requires four color components: *red*, *green*, *blue* and *alpha* (transparency).

    *Lua similar:* `Color() <http://wiki.garrysmod.com/page/Global/Color>`_
    """
    def __init__(self, r, g, b, a):
        _check_component_type(r, g, b, a)
        self.r = r
        self.g = g
        self.b = b
        self.a = a


def get_lua_color(col):
    if isinstance(col, Color):
        comps = (col.r, col.g, col.b, col.a)
        _check_component_type(*comps)
        return lua.G['Color'](*comps)
    elif isinstance(col, Iterable):
        r, g, b, a = col
        _check_component_type(r, g, b, a)
        return lua.G['Color'](r, g, b, a)
    else:
        raise TypeError('color must be Color or iterable of ints')
