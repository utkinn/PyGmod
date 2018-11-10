"""Script that shows a little icon in the top-left corner when an exception happens."""

from . import material, hooks, draw

__all__ = ['setup', 'show']

error_icon = material.Material('pygmod_error.png')
should_draw_icon = False


def show():
    global should_draw_icon
    should_draw_icon = True


def setup():
    @hooks.hook('DrawOverlay')
    def draw_pygmod_error_icon():
        if not should_draw_icon:
            return

        draw.textured_box(10, 10, 16, 16, error_icon)
