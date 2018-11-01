from numbers import Number

from . import lua, net, color as color_module


@net.client
def rounded_box(x, y, w, h, color, corner_radius):
    if any(not isinstance(o, Number) for o in (x, y, w, h)):
        raise TypeError('bounds (x, y, w and h) must be numbers')
    if not isinstance(corner_radius, Number):
        raise TypeError('corner_radius must be a number')

    lc = color_module.get_lua_color(color)
    lua.G['draw']['RoundedBox'](corner_radius, x, y, w, h, lc)
