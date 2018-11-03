"""This module provides tools for creating and executing console commands."""

from typing import Union, Iterable

from . import lua
from .player import Player

callbacks = {}


def ccmd_executed():
    lua.exec('''
    if CLIENT then
        py._SwitchToClient()
    else
        py._SwitchToServer()
    end
    ''')
    ccmd = str(lua.G['py']['_ccmd_ccmd'])
    ccmd_sender = Player(lua.G['py']['_ccmd_ply'])
    ccmd_args = str(lua.G['py']['_ccmd_args'])

    callbacks[ccmd](ccmd_sender, ccmd_args)


def exists(name):
    """Returns ``True`` if the console command with the name ``name`` was registered
    by Lua `concommand.Add() <http://wiki.garrysmod.com/page/concommand/Add>`_ or by :class:`ConCmd` class constructor.
    """
    if not isinstance(name, str):
        raise TypeError('name must be str')

    if name in callbacks:
        return True

    lua.G['py']['_cmd'] = name

    lua.exec(f'''
    py._cmd_exists = false
    local ccmds = concommand.GetTable()
    for k, _ in pairs(ccmds) do
        if py._cmd == k then
            py._cmd_exists = true
            break
        end
    end
    ''')

    return bool(lua.G['py']['_cmd_exists'])


class ConCmd:
    """The console command class.

    The callback is a function which will be called when the console command will be executed.
    It must receive 2 arguments:

        - :class:`Player` who executed this command
        - :class:`str` of arguments separated by spaces.

    *Lua similar:* `concommand.Add() <http://wiki.garrysmod.com/page/concommand/Add>`_
    """

    def __init__(self, name: str, callback):
        if not isinstance(name, str):
            raise TypeError('name must be str')

        self.name = name
        self._callback = callback
        self.removed = False

        self._register()

    def _register(self):
        if exists(self.name):
            raise ValueError('concommand "' + self.name + '" was already registered')

        callbacks[self.name] = self._callback

        cb = lua.eval('''
        function(ply, ccmd, _, args)
            if CLIENT then
                py._SwitchToClient()
            else
                py._SwitchToServer()
            end
            py._ccmd_ccmd = ccmd
            py._ccmd_ply = ply
            py._ccmd_args = args
            py.Exec('import gmod.concommands; gmod.concommands.ccmd_executed()')
        end
        ''')

        lua.G['concommand']['Add'](self.name, cb)

    @property
    def callback(self):
        """This concommand's callback."""
        return self._callback

    @callback.setter
    def callback(self, val):
        self._callback = val
        callbacks[self.name] = val

    def remove(self):
        """Removes the console command, so it will be not available for executing.

        *Lua similar:* `concommand.Remove() <http://wiki.garrysmod.com/page/concommand/Remove>`_
        """
        del callbacks[self.name]
        lua.G['concommand']['Remove'](self.name)
        self.removed = True

    def readd(self):
        """Adds this concommand again if it was previously removed."""
        if self.removed:
            self._register()


def run(cmd: Union[str, ConCmd], args: Union[str, Iterable[str]] = '') -> None:
    """Runs the console command.

    :param args: space-separated args or iterable of args :class:`str`\ s.

    *Lua similar:* `RunConsoleCommand() <http://wiki.garrysmod.com/page/Global/RunConsoleCommand>`_
    """
    run_func = lua.G['RunConsoleCommand']

    if not isinstance(args, str):
        raise TypeError('args must be str')

    if isinstance(cmd, ConCmd):
        run_func(cmd.name, *args.split())
    elif isinstance(cmd, str):
        run_func(cmd, *args.split())
    else:
        raise TypeError('cmd must be str or ConCmd object')
