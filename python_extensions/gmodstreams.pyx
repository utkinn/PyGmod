# distutils: language = c++

import sys, os
from io import StringIO
from luastack import *

class GmodConsoleOut(StringIO):
    """Output to Garry's Mod console."""

    def write(self, s):
        """Writes string ``s`` to Garry's Mod console with ``Msg`` Lua function."""
        push_special(Special.GLOBAL)
        get_field(-1, b'Msg')
        push_string(s.encode())
        call(1, 0)
        pop(1)

        return len(s)

cdef public set_stream():
    """Sets ``sys.stdout`` to a new GmodConsoleOut instance."""
    sys.stdout = GmodConsoleOut()
