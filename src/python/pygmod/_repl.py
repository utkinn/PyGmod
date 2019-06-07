import traceback
from code import InteractiveConsole
import sys
from os import path
from base64 import b64encode

from pygmod.lua import G
from pygmod.gmodapi import vgui, ScrW, ScrH, CLIENT, concommand

__all__ = ['setup']

# Flag of REPL being opened. Used to prevent opening multiple REPLs at once.
repl_opened = False


class PyGmodReplOut:
    def __init__(self, dhtml):
        self._dhtml = dhtml

    def write(self, s):
        # Encoding the output to Base64 to surely escape it.
        b64_data = b64encode(s.encode()).decode()
        self._dhtml._.Call(f"appendOutputBase64({b64_data!r}, HighlightMode.TEXT)")
        return len(s)


class PyGmodReplErr:
    def __init__(self, dhtml):
        self._dhtml = dhtml

    def write(self, s):
        # Encoding the output to Base64 to surely escape it.
        b64_data = b64encode(s.encode()).decode()
        self._dhtml._.Call(f"appendOutputBase64({b64_data!r}, HighlightMode.ERROR)")
        return len(s)


class PyGmodREPL(InteractiveConsole):
    def __init__(self, frame):
        InteractiveConsole.__init__(self)
        self._frame = frame

    def runcode(self, code):
        try:
            super().runcode(code)
        except SystemExit:  # Closing the console on exit() call
            self._frame._.Close()

    def showtraceback(self):
        sys.stderr.write(traceback.format_exc())
        # PyGmodReplErr.write(self, )

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
        sys.stderr.write(''.join(lines))
        # PyGmodReplErr.write(self, ''.join(lines))


def create_frame():
    fr = vgui.Create('DFrame')
    fr._.SetTitle('PyGmod REPL')
    fr._.SetPos(ScrW() // 3, ScrH() // 3)
    fr._.SetSize(ScrW() // 2, ScrH() // 2)
    fr._.MakePopup()

    return fr


def set_frame_close_handler(fr):
    def on_close(*_):
        global repl_opened
        repl_opened = False

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    fr.OnClose = on_close


def create_dhtml(fr):
    dhtml = vgui.Create("DHTML", fr)
    dhtml._.Dock(G.FILL)
    with open(path.join("garrysmod", "pygmod", "html", "repl.html")) as f:
        dhtml._.SetHTML(f.read())
    dhtml._.SetAllowLua(True)

    return dhtml


def add_functions_to_js(dhtml, console):
    def submit(code):
        input_complete = not console.push(code)
        prompt = '>>>' if input_complete else '...'
        dhtml._.Call(f"$('#prompt').text('{prompt}')")

    dhtml._.AddFunction("pygmodRepl", "submit", submit)

    def save_style_preference_to_file(style):
        with open(path.join("garrysmod", "data", "pygmod_repl_style.txt"), "w") as f:
            f.write(style)

    dhtml._.AddFunction("pygmodRepl", "saveStylePreferenceToFile", save_style_preference_to_file)

    def load_style_preference_from_file():
        try:
            with open(path.join("garrysmod", "data", "pygmod_repl_style.txt")) as f:
                return f.read()
        except OSError:
            return "default"

    dhtml._.AddFunction("pygmodRepl", "loadStylePreferenceFromFile", load_style_preference_from_file)

    dhtml._.Call("loadStyleFromPreference()")


def replace_stdout(dhtml):
    sys.stdout = PyGmodReplOut(dhtml)


def replace_stderr(dhtml):
    sys.stderr = PyGmodReplErr(dhtml)


def open_repl(*_):
    global repl_opened

    if repl_opened:
        return

    fr = create_frame()
    dhtml = create_dhtml(fr)

    cons = PyGmodREPL(fr)
    cons.runcode('from pygmod.gmodapi import *')

    add_functions_to_js(dhtml, cons)
    replace_stdout(dhtml)
    replace_stderr(dhtml)
    set_frame_close_handler(fr)

    repl_opened = True


def setup():
    if CLIENT:
        concommand.Add('python', open_repl)
