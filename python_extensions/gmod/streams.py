"""This module contains custom I/O classes which redirect I/O to Garry's Mod."""

import sys, os
from io import StringIO
from luastack import *


class GmodConsoleOut(StringIO):
    """Class which redirects the standard output (stdout) to the Garry's Mod console.

    Messages from the *client* realm are printed with the yellow color
    and messages from the *server* realm are printed with the blue color,
    just like ``print``, ``Msg`` and other Lua functions do.
    """

    def write(self, s):
        """Writes string ``s`` to Garry's Mod console with ``Msg`` Lua function."""
        push_special(Special.GLOBAL)
        get_field(-1, b'Msg')
        push_string(s.encode())
        call(1, 0)
        pop(1)

        return len(s)


class GmodConsoleErr(StringIO):
    """Class which redirects the error output (stderr) to the Garry's Mod console.

    All messages are printed with the red color.
    """

    def write(self, s):
        """Writes string ``s`` to Garry's Mod console with ``MsgC`` Lua function with red color."""
        push_special(Special.GLOBAL)

        get_field(-1, b'MsgC')

        # Creating Color structure
        get_field(-2, b'Color')
        push_number(255)
        push_number(0)
        push_number(0)
        call(3, 1)

        push_string(s.encode())
        call(2, 0)
        pop(1)

        return len(s)


def setup():
    """
    Sets ``sys.stdout`` to a new :class:`GmodConsoleOut` instance
    and ``sys.stderr`` to a new :class:`GmodConsoleErr` instance.
    Being called in ``redirectIO_toGmod()`` in ``main.cpp`` of the *C++* module.
    """
    sys.stdout = GmodConsoleOut()
    sys.stderr = GmodConsoleErr()
