"""Script that shows a little icon in the top-left corner when an exception happens."""

from .luanamespace import *
from .lua import luafunction

__all__ = ['setup', 'show']

error_icon, _ = Material('pygmod_error.png')
should_draw_icon = False


def show():
    global should_draw_icon
    should_draw_icon = True


def setup():
    def draw_pygmod_error_icon():
        if not should_draw_icon:
            return

        surface.SetDrawColor(255, 255, 255, 255)
        surface.SetMaterial(error_icon)
        surface.DrawTexturedRect(20, 20, 32, 32)

    hook.Add('DrawOverlay', 'pygmod_show_error_icon', luafunction(draw_pygmod_error_icon))
