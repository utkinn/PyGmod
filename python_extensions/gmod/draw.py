from numbers import Number
from typing import Union, Tuple

from . import lua, net, color as color_module, typecheck, material as material_module

__all__ = ['textured_box', 'rounded_box']


@net.client
def textured_box(x, y, w, h, material,
                 color: Union[color_module.Color, Tuple[int, int, int, int]] = color_module.Color(255, 255, 255)):
    """Draws a textured box.

    :arg x: the X coordinate of the upper-left corner of the box.
    :arg y: the Y coordinate of the upper-left corner of the box.
    :arg w: the box width, in other words, the X coordinate of the lower-right corner of the box.
    :arg h: the box height, in other words, the Y coordinate of the lower-right corner of the box.
    :arg color: the box fill color.
    :arg material: the box material.

    *Lua similar:* `surface.DrawTexturedRect() <http://wiki.garrysmod.com/page/surface/DrawTexturedRect>`_
    """
    typecheck.check_iter((x, y, w, h), int)
    typecheck.check(material, material_module.Material)

    lc = color_module.get_lua_color(color)
    lua.G.surface.SetDrawColor(lc)
    lua.G.surface.SetMaterial(material)
    lua.G.surface.DrawTexturedRect(x, y, w, h)


@net.client
def rounded_box(x, y, w, h, color: Union[color_module.Color, Tuple[int, int, int, int]], corner_radius):
    """Draws a rounded filled box.

    :arg x: the X coordinate of the upper-left corner of the box.
    :arg y: the Y coordinate of the upper-left corner of the box.
    :arg w: the box width, in other words, the X coordinate of the lower-right corner of the box.
    :arg h: the box height, in other words, the Y coordinate of the lower-right corner of the box.
    :arg color: the box fill color.
    :arg corner_radius: the radius of the rounded corners, works best with a multiple of 2.

    *Lua similar:* `draw.RoundedBox() <http://wiki.garrysmod.com/page/draw/RoundedBox>`_
    """

    if any(not isinstance(o, Number) for o in (x, y, w, h)):
        raise TypeError('bounds (x, y, w and h) must be numbers')
    if not isinstance(corner_radius, Number):
        raise TypeError('corner_radius must be a number')

    lc = color_module.get_lua_color(color)
    lua.G['draw']['RoundedBox'](corner_radius, x, y, w, h, lc)
