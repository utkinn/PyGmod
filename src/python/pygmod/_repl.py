import traceback
from code import InteractiveConsole
from io import TextIOBase
import sys

from pygmod.gmodapi import vgui, ScrW, ScrH, CLIENT, concommand

__all__ = ['setup']


class PyGmodReplOut(TextIOBase):
    def __init__(self, text_entry):
        self.text_entry = text_entry

    def write(self, s: str):
        te_self = self.text_entry._
        te_self.AppendText(s)
        return len(s)


class PyGmodREPL(InteractiveConsole):
    def __init__(self, frame, text_entry):
        super().__init__()
        self.frame = frame
        self.text_entry = text_entry

    def write(self, data):
        te_self = self.text_entry._
        te_self.InsertColorChange(255, 64, 64, 255)
        te_self.AppendText(data)
        te_self.InsertColorChange(255, 255, 255, 255)

    def runcode(self, code):
        try:
            super().runcode(code)
        except SystemExit:  # Closing the console on exit() call
            self.frame._.Close()

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


def create_output(fr):
    text = vgui.Create('RichText', fr)
    text._.SetPos(7, 25)
    text._.SetSize(ScrW() // 2 - 15, ScrH() // 2 - 65)
    text._.InsertColorChange(255, 255, 255, 255)
    text._.AppendText(
        'Python ' + sys.version + '\n' +
        'Type "help", "copyright", "credits" or "license" for more information.\n'
    )

    def layout(self, *_):
        self._.SetFontInternal('DebugFixed')

    text.PerformLayout = layout

    return text


def replace_stdout(fr, text):
    original_stdout = sys.stdout
    sys.stdout = PyGmodReplOut(text)

    def on_close(_):
        sys.stdout = original_stdout

    fr.OnClose = on_close


def create_prompt_label(fr):
    prompt_lbl = vgui.Create('DLabel', fr)
    prompt_lbl._.SetText('>>>')
    prompt_lbl._.SetPos(7, ScrH() // 2 - 30)

    return prompt_lbl


def create_input_field(fr):
    inp = vgui.Create('DTextEntry', fr)
    inp._.SetPos(35, ScrH() // 2 - 30)
    inp._.SetSize(ScrW() // 2 - 80, 20)
    inp._.SetFont('DebugFixed')
    inp._.RequestFocus()

    return inp


def create_submit_button(fr):
    submit = vgui.Create('DButton', fr)
    submit._.SetPos(ScrW() // 2 - 45, ScrH() // 2 - 30)
    submit._.SetSize(40, 20)
    submit._.SetText('SUBMIT')

    return submit


def open_repl(*_):
    fr = create_frame()
    text = create_output(fr)
    prompt_lbl = create_prompt_label(fr)
    inp = create_input_field(fr)
    submit = create_submit_button(fr)

    cons = PyGmodREPL(fr, text)
    cons.runcode('from pygmod.gmodapi import *')

    replace_stdout(fr, text)

    def enter(*_):
        text._.AppendText(
            ('>>> ' if not cons.buffer else '... ') + inp._.GetText() + '\n')

        input_complete = not cons.push(inp._.GetText())
        prompt_lbl._.SetText('>>>' if input_complete else '. . .')

        inp._.SetText('')
        inp._.RequestFocus()

    inp.OnEnter = submit.DoClick = enter


def setup():
    if CLIENT:
        concommand.Add('python', open_repl)
