# distutils: language = c++

"""Classes for redirecting IO to Garry's Mod."""

import sys, os
from io import StringIO
from luastack import *


class GmodConsoleOut(StringIO):
    """Output to the Garry's Mod console."""

    def write(self, s):
        """Writes string ``s`` to Garry's Mod console with ``Msg`` Lua function."""
        push_special(Special.GLOBAL)
        get_field(-1, b'Msg')
        push_string(s.encode())
        call(1, 0)
        pop(1)

        return len(s)


class GmodConsoleErr(StringIO):
    """Output to the Garry's Mod console for errors."""

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


cdef public set_streams():
    """Sets ``sys.stdout`` and ``sys.stderr`` to a new GmodConsoleOut instance.
       Being called in ``redirectIO_toGmod()`` in main.cpp of the C++ module."""
    sys.stdout = GmodConsoleOut()
    sys.stderr = GmodConsoleErr()
