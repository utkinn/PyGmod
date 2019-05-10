"""
``_loader.py`` is the second part of the initialization system.

Here is what it does:

#. Redirects I/O to Garry's Mod console with :mod:`pygmod._streams` I/O classes.
#. Scans ``addons\\`` directory for PyGmod addons and initializes them.
"""

import sys
from os import path, listdir
from logging import getLogger

from pygmod import _streams, _logging_config

_streams.setup()
_logging_config.configure()

from pygmod import lua, _error_notif, _repl

__all__ = ['main']

logger = getLogger("pygmod.loader")

ADDONS_PATH = 'garrysmod\\addons'
SHARED_PACKAGE = '__shared_autorun__'


def handle_exception(exc_type, exc_value, tb):
    _error_notif.show()
    logger.exception("Unhandled PyGmod exception", exc_info=(exc_type, exc_value, tb))


sys.excepthook = handle_exception


def try_import(addon_dir, pkg):
    # noinspection PyBroadException
    try:
        __import__(addon_dir + '.python.' + pkg)
        return True
    except ImportError:
        pass
    except BaseException:
        _error_notif.show()
        logger.exception("Exception in addon %r", addon_dir)


def main():
    """Finishes the PyGmod initialization."""
    _error_notif.setup()
    _repl.setup()

    logger.info('Loading addons...')

    realm = 'client' if lua.Globals().CLIENT else 'server'
    realm_pkg = f'__{realm}_autorun__'

    sys.path.append(path.abspath(ADDONS_PATH))

    for addon_dir in (d for d in listdir(ADDONS_PATH) if
                      path.isdir(path.join(ADDONS_PATH, d))):
        sys.path.append(path.join(ADDONS_PATH, addon_dir, 'python'))

        success = (
        try_import(addon_dir, SHARED_PACKAGE), try_import(addon_dir, realm_pkg))

        del sys.path[-1]

        if any(success):
            logger.info('"' + addon_dir + '" successfully loaded.')

    logger.info('Loading finished')
