"""
Script that shows a little icon in the top-left corner
when an uncaught exception in PyGmod itself or PyGmod addon happens.
"""

import time

from pygmod.gmodapi import Material, surface, hook

__all__ = ['setup', 'show']

error_icon, _ = Material('pygmod_error.png')

# Hide the error icon after n milliseconds
ICON_HIDE_DELAY = 5
should_draw_icon = False
hide_icon_at = 0


def show():
    """
    Shows the error icon in the top-left corner of the screen
    which then disappears after :data:`ICON_HIDE_DELAY` seconds.
    """
    global should_draw_icon, hide_icon_at

    should_draw_icon = True
    hide_icon_at = time.clock() + ICON_HIDE_DELAY


def setup():
    """Registers a ``DrawOverlay`` hook for showing an error icon later."""
    def draw_pygmod_error_icon():
        global should_draw_icon

        if not should_draw_icon:
            return

        surface.SetDrawColor(255, 255, 255, 255)
        surface.SetMaterial(error_icon)
        surface.DrawTexturedRect(20, 20, 32, 32)

        if time.clock() > hide_icon_at:
            should_draw_icon = False

    hook.Add('DrawOverlay', 'pygmod_show_error_icon', draw_pygmod_error_icon)
