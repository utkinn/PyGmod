from . import concommands, realms, screen
from .derma.frame import Frame


def open_repl(player, args):
    fr = Frame()
    fr.title = 'PyGmod REPL'
    fr.pos = (c // 3 for c in screen.getsize())
    fr.size = (c // 2 for c in screen.getsize())
    fr.popup()


def setup():
    if realms.SERVER:
        return
    concommands.ConCmd('python', open_repl)
