"""
This module provides Python interactive console (aka REPL) inside Garry's Mod.
The console can be opened by running ``python`` console command.
"""

import traceback
from code import InteractiveConsole
import sys
from os import path
from base64 import b64encode

from pygmod.lua import G
from pygmod.gmodapi import vgui, ScrW, ScrH, CLIENT, concommand

__all__ = ['setup']

# Ignore PyLint warnings about "repl_opened"
# pylint: disable=invalid-name

# Flag of REPL being opened. Used to prevent opening multiple REPLs at once.
repl_opened = False


class PyGmodReplStreamBase:
    """Base class for :class:`PyGmodReplOut` and :class:`PyGmodReplErr`."""

    # pylint: disable=too-few-public-methods

    def __init__(self, dhtml):
        self._dhtml = dhtml

    def write(self, data):
        """Writes ``data`` to the REPL output field."""
        # Encoding the data to Base64 to surely escape it.
        b64_data = b64encode(data.encode()).decode()
        # pylint: disable=no-member
        self._dhtml._.Call(f"appendOutputBase64({b64_data!r}, HighlightMode.{self.HIGHLIGHT_MODE})")
        return len(data)


class PyGmodReplOut(PyGmodReplStreamBase):
    """
    Replacement for :data:`sys.stdout`
    which redirects the output to the currently opened REPL.
    """

    # pylint: disable=too-few-public-methods

    HIGHLIGHT_MODE = "TEXT"


class PyGmodReplErr(PyGmodReplStreamBase):
    """
    Replacement for :data:`sys.stderr`
    which redirects the output to the currently opened REPL.
    """

    # pylint: disable=too-few-public-methods

    HIGHLIGHT_MODE = "ERROR"


class PyGmodREPL(InteractiveConsole):
    """
    Subclass of :class:`code.InteractiveConsole`
    which tunes its functionality to work with the REPL.
    """

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

    def showsyntaxerror(self, filename=None):
        # Code copied from code.py
        exc_type, exc_value, exc_tb = sys.exc_info()
        sys.last_type = exc_type
        sys.last_value = exc_value
        sys.last_traceback = exc_tb
        if filename and exc_type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = exc_value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                exc_value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = exc_value
        lines = traceback.format_exception_only(exc_type, exc_value)
        sys.stderr.write(''.join(lines))
        # PyGmodReplErr.write(self, ''.join(lines))


def create_frame():
    """Creates a ``DFrame`` for the REPL."""
    frame = vgui.Create('DFrame')
    frame._.SetTitle('PyGmod REPL')
    frame._.SetPos(ScrW() // 3, ScrH() // 3)
    frame._.SetSize(ScrW() // 2, ScrH() // 2)
    frame._.MakePopup()

    return frame


def set_frame_close_handler(frame):
    """Sets ``OnClose`` handler of ``DFrame`` ``frame``.

    The handler resets the :data:`repl_opened` flag and restores :data:`sys.stdout`
    and :data:`sys.stderr` to :class:`pygmod._streams.GmodConsoleOut`
    and :class:`pygmod._streams.GmodConsoleErr` respectively.
    """

    def on_close(*_):
        global repl_opened  # pylint: disable=global-statement
        repl_opened = False

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    frame.OnClose = on_close


def create_dhtml(frame):
    """Creates ``DHTML`` element on ``DFrame`` ``frame``."""
    dhtml = vgui.Create("DHTML", frame)
    dhtml._.Dock(G.FILL)
    with open(path.join("garrysmod", "pygmod", "html", "repl.html")) as html:
        dhtml._.SetHTML(html.read())
    dhtml._.SetAllowLua(True)

    return dhtml


def add_functions_to_js(dhtml, console):
    """Installs some functions to ``dhtml``\\ 's JavaScript environment.

    These functions are:

    #. ``pygmodRepl.submit(code)``
        This function receives a ``code`` argument which is a Python code string. The code string
        is pushed to ``console``. The text of th HTML element with id ``prompt`` is changed to
        ``>>>`` or ``...``, depending on whether the Python expression is complete.
    #. ``pygmodRepl.saveStylePreferenceToFile(style)``
        Receives a string ``style`` which is a name of the CSS file of the highlight.js code style
        which was selected by the user. The style name is saved to
        ``garrysmod/data/pygmod_repl_style.txt`` in order to keep the code style
        across REPL sessions.
    #. ``pygmodRepl.loadStylePreferenceFromFile()``
        Returns the style name from ``garrysmod/data/pygmod_repl_style.txt``. If the file doesn't
        exist, returns ``"default"``.
    """

    def submit(code):
        input_complete = not console.push(code)
        prompt = '>>>' if input_complete else '...'
        dhtml._.Call(f"$('#prompt').text('{prompt}')")

    dhtml._.AddFunction("pygmodRepl", "submit", submit)

    def save_style_preference_to_file(style):
        with open(path.join("garrysmod", "data", "pygmod_repl_style.txt"), "w") as style_file:
            style_file.write(style)

    dhtml._.AddFunction("pygmodRepl", "saveStylePreferenceToFile", save_style_preference_to_file)

    def load_style_preference_from_file():
        try:
            with open(path.join("garrysmod", "data", "pygmod_repl_style.txt")) as style_file:
                style = style_file.read()
        except OSError:
            style = "default"
        dhtml._.Call(f"applyStyle({style!r})")

    dhtml._.AddFunction("pygmodRepl", "loadStylePreferenceFromFile",
                        load_style_preference_from_file)


def replace_streams(dhtml):
    """
    Sets :data:`sys.stdout` to a :class:`PyGmodReplOut` instance
    and :data:`sys.stderr` to a :class:`PyGmodReplErr` instance.
    """
    sys.stdout = PyGmodReplOut(dhtml)
    sys.stderr = PyGmodReplErr(dhtml)


def open_repl(*_):
    """Callback for the ``python`` console command which opens the REPL."""
    global repl_opened  # pylint: disable=global-statement

    if repl_opened:
        return

    frame = create_frame()
    dhtml = create_dhtml(frame)

    cons = PyGmodREPL(frame)
    cons.runcode('from pygmod.gmodapi import *')

    add_functions_to_js(dhtml, cons)
    replace_streams(dhtml)
    set_frame_close_handler(frame)

    repl_opened = True


def setup():
    """Registers the ``python`` console command."""
    if CLIENT:
        concommand.Add('python', open_repl)
