"""This module contains custom I/O classes which redirect I/O to Garry's Mod."""

import sys
from io import StringIO

from luastack import LuaStack, Special

_ls = LuaStack()


class GmodConsoleOut(StringIO):
    """Class which redirects the standard output (stdout) to the Garry's Mod console.

    Messages from the *client* realm are printed with the yellow color
    and messages from the *server* realm are printed with the blue color,
    just like ``print``, ``Msg`` and other Lua functions do.
    """

    def write(self, s):
        """Writes string ``s`` to Garry's Mod console with ``Msg`` Lua function."""
        _ls.push_special(Special.GLOBAL)
        _ls.get_field(-1, b'Msg')
        _ls.push_string(s.encode())
        _ls.call(1, 0)
        _ls.pop(1)

        return len(s)


class GmodConsoleErr(StringIO):
    """Class which redirects the error output (stderr) to the Garry's Mod console.

    All messages are printed with the red color.
    """

    def write(self, s):
        """Writes string ``s`` to Garry's Mod console with ``MsgC`` Lua function with red color."""
        _ls.push_special(Special.GLOBAL)

        _ls.get_field(-1, b'MsgC')

        # Creating Color structure
        _ls.get_field(-2, b'Color')
        _ls.push_number(255)
        _ls.push_number(0)
        _ls.push_number(0)
        _ls.call(3, 1)

        _ls.push_string(s.encode())
        _ls.call(2, 0)
        _ls.pop(1)

        return len(s)


def setup():
    """
    Sets ``sys.stdout`` to a new :class:`GmodConsoleOut` instance
    and ``sys.stderr`` to a new :class:`GmodConsoleErr` instance.
    Being called in ``redirectIO_toGmod()`` in ``main.cpp`` of the *C++* module.
    """
    sys.stdout = GmodConsoleOut()
    sys.stderr = GmodConsoleErr()
