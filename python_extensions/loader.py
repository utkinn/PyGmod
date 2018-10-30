"""
``loader.py`` is the second part of the initialization system.

Here is what it does:

#. Redirects I/O to Garry's Mod console with :mod:`gmod.streams` I/O classes.
#. Patches the ``hook.Call`` Lua function to delegate hook calls to :mod:`gmod.hooks` module.
#. Scans ``addons\`` directory for PyGmod addons and initializes them.
"""

import sys
import os.path
from importlib import import_module
import traceback

# os.path.append('garrysmod\\gpython')

from gmod.realms import REALM
from gmod import lua, streams

__all__ = ['main']


def log(msg, end='\n'):
    print('[PyGmod]', msg, end=end)


ADDONS_PATH = 'garrysmod\\addons'
SHARED_PACKAGE = '__shared_autorun__'


def prepare_and_print_tb():
    # Getting traceback text as a list of strings,
    # string at index 0 is "Traceback (most recent call last):", next strings are the frames.
    # The first frame is this loader's frame where it imports an addon.
    # We don't need this frame because it has no relation to the addon, so we will get rid of it
    # by deleting the string at index 1 from the text list.
    traceback_text = traceback.format_exception(*sys.exc_info())

    # Deleting the loader's frame
    del traceback_text[1]

    # Printing the clean traceback
    for l in traceback_text:
        sys.stderr.write(l)


def handle_exception_in_addon():
    # Constructing a bar of 50 underscores to visually separate tracebacks from other output.
    bar = '_' * 50 + '\n'

    def print_bar():
        print(bar, file=sys.stderr)

    print()
    print_bar()
    prepare_and_print_tb()
    print_bar()


def try_import(addon_dir, pkg):
    try:
        __import__(addon_dir + '.python.' + pkg)
    except ImportError:
        log('Invalid GPython addon "' + addon_dir + '"')
    except:
        handle_exception_in_addon()


def redirect_output():
    streams.setup()
    # sys.stdin = sys.stderr = open('pygmod.log', 'w+')


def patch_hook_call():
    """Patches the ``hook.Call`` Lua function to delegate hook calls to :mod:`gmod.hooks` module."""
    lua.exec('''
    py._watched_events = {}
    
    hook.SilentCall = hook.Call

    local function newCall(eventName, gamemodeTable, ...)
        if isstring(eventName) and py and py._watched_events and py._watched_events[eventName] then
            _py_hook_data = {...}
            _py_n_data = #{...}
            if CLIENT then
                py._SwitchToClient()
            else
                py._SwitchToServer()
            end
            py.Exec('import gmod.hooks; gmod.hooks.event_occurred("'..eventName..'")')
        end

        return hook.SilentCall(eventName, gamemodeTable, ...)
    end

    hook.Call = newCall
    ''')


def main():
    """Finishes the PyGmod initialization."""
    redirect_output()

    patch_hook_call()

    log('Loading addons...')

    realm_pkg = f'__{REALM}_autorun__'

    sys.path.append(os.path.abspath(ADDONS_PATH))

    for addon_dir in (d for d in os.listdir(ADDONS_PATH) if os.path.isdir(os.path.join(ADDONS_PATH, d))):
        log('Loading addon "' + addon_dir + '"... ', end='')

        sys.path.append(os.path.join(ADDONS_PATH, addon_dir, 'python'))

        try_import(addon_dir, SHARED_PACKAGE)
        try_import(addon_dir, realm_pkg)

        del sys.path[-1]

        log('"' + addon_dir + '" successfully loaded.')

    log('Loading finished')
