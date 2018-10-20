import sys
import os.path
from importlib import import_module
import traceback

# os.path.append('garrysmod\\gpython')

from gmod.realms import REALM
from gmod import streams

__all__ = ['main']


def log(msg, end='\n'):
    print('[GPython]', msg, end=end)


ADDONS_PATH = 'garrysmod\\addons'
SHARED_PACKAGE = '__shared_autorun__'


def handle_exception_in_addon():
    bar = '_' * 50 + '\n'

    print()
    print(bar)
    traceback.print_exc()
    print(bar)


def try_import(addon_dir, pkg):
    try:
        import_module(addon_dir + '.python.' + pkg)
    except ImportError:
        log('Invalid GPython addon "' + addon_dir + '"')
    except:
        handle_exception_in_addon()


def redirect_output():
    streams.setup()
    # sys.stdin = sys.stderr = open('gpython.log', 'w+')


def main():
    redirect_output()

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
