import traceback
from code import InteractiveConsole
import sys
from os import path

from pygmod.lua import G
from pygmod.gmodapi import vgui, ScrW, ScrH, CLIENT, concommand

__all__ = ['setup']


class PyGmodReplOut:
    def __init__(self, dhtml):
        self._dhtml = dhtml

    def write(self, s):
        self._dhtml._.Call(f"appendOutput({s!r})")
        return len(s)


class PyGmodREPL(PyGmodReplOut, InteractiveConsole):
    def __init__(self, frame, dhtml):
        InteractiveConsole.__init__(self)
        PyGmodReplOut.__init__(self, dhtml)
        self._frame = frame

    def runcode(self, code):
        try:
            super().runcode(code)
        except SystemExit:  # Closing the console on exit() call
            self._frame._.Close()

    def showtraceback(self):
        self.write(traceback.format_exc())

    def showsyntaxerror(self, filename=None):
        # Code copied from code.py
        exc_type, value, tb = sys.exc_info()
        sys.last_type = exc_type
        sys.last_value = value
        sys.last_traceback = tb
        if filename and exc_type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        lines = traceback.format_exception_only(exc_type, value)
        self.write(''.join(lines))


def create_frame():
    fr = vgui.Create('DFrame')
    fr._.SetTitle('PyGmod REPL')
    fr._.SetPos(ScrW() // 3, ScrH() // 3)
    fr._.SetSize(ScrW() // 2, ScrH() // 2)
    fr._.MakePopup()

    return fr


def create_dhtml(fr):
    dhtml = vgui.Create("DHTML", fr)
    dhtml._.Dock(G.FILL)
    with open(path.join("garrysmod", "pygmod", "html", "repl.html")) as f:
        dhtml._.SetHTML(f.read())
    dhtml._.SetAllowLua(True)

    return dhtml


def add_submit_js_function(dhtml, console):
    def submit(code):
        input_complete = not console.push(code)
        prompt = '>>>' if input_complete else '...'
        dhtml._.Call(f"$('#prompt').text('{prompt}')")

    dhtml._.AddFunction("pygmodRepl", "submit", submit)


def replace_stdout(fr, dhtml):
    original_stdout = sys.stdout
    sys.stdout = PyGmodReplOut(dhtml)

    def on_close(_):
        sys.stdout = original_stdout

    fr.OnClose = on_close


def open_repl(*_):
    fr = create_frame()
    dhtml = create_dhtml(fr)

    cons = PyGmodREPL(fr, dhtml)
    cons.runcode('from pygmod.gmodapi import *')

    add_submit_js_function(dhtml, cons)
    replace_stdout(fr, dhtml)


def setup():
    if CLIENT:
        concommand.Add('python', open_repl)
