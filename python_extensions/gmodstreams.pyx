# distutils: language = c++

import sys, os
from io import StringIO
from luastack import *

class GmodConsoleOut(StringIO):
    def write(self, s):
        push_special(Special.GLOBAL)
        get_field(-1, b'Msg')
        push_string(s.encode())
        call(1, 0)
        pop(1)
    
        return len(s)

cdef public set_stream():
    sys.stdout = GmodConsoleOut()
