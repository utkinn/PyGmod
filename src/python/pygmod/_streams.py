"""Custom I/O classes which redirect I/O to the Garry's Mod console."""

import sys
from io import TextIOBase
from logging import getLogger

from pygmod import lua

__all__ = ["setup"]


class GmodConsoleOutStream(TextIOBase):
    """Base class for Garry's Mod console output streams."""

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return False


class GmodConsoleOut(GmodConsoleOutStream):
    """Class which redirects the standard output (stdout) to the Garry's Mod console.

    Messages from the *client* realm are printed with the yellow color
    and messages from the *server* realm are printed with the blue color,
    just like ``print``, ``Msg`` and other Lua functions do.
    """

    def write(self, s):
        """Writes string ``s`` to Garry's Mod console with ``Msg`` Lua function."""
        lua.G.Msg(s)
        return len(s)


class GmodConsoleErr(GmodConsoleOutStream):
    """Class which redirects the error output (stderr) to the Garry's Mod console.

    All messages are printed with the red color.
    """

    def write(self, s):
        """
        Writes string ``s`` to Garry's Mod console
        with ``MsgC`` Lua function with red color.
        """
        lua.G.MsgC(lua.G.Color(255, 0, 0), s)
        return len(s)


def setup():
    """
    Sets ``sys.stdout`` to a new :class:`GmodConsoleOut` instance
    and ``sys.stderr`` to a new :class:`GmodConsoleErr` instance.
    Being called in ``redirectIOToGmod()`` in ``main.cpp`` of the *C++* module.
    """
    sys.stdout.flush()
    sys.stderr.flush()
    sys.stdout = sys.__stdout__ = GmodConsoleOut()
    sys.stderr = sys.__stderr__ = GmodConsoleErr()
    getLogger("pygmod._streams").debug(
        "sys.stdout and sys.stderr was redirected to Garry's Mod console."
    )
