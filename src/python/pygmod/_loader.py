"""
``_loader.py`` is the second part of the initialization system.

Here is what it does:

#. Redirects I/O to Garry's Mod console with :mod:`pygmod._streams` I/O classes.
#. Scans ``addons\\`` directory for PyGmod addons and initializes them.
"""

import sys
from os import path, listdir
from logging import getLogger
from importlib import import_module

from pygmod import _streams, _logging_config

# Redirecting the output to Garry's Mod as early as possible,
# so all possible loader problems will be reported to the Garry's Mod console
_streams.setup()
_logging_config.configure()

from pygmod import lua, _error_notif, _repl

__all__ = ['main']

logger = getLogger("pygmod.loader")

ADDONS_PATH = path.abspath('garrysmod\\addons')
SHARED_PACKAGE_NAME = '__shared_autorun__'


def handle_exception(exc_type, exc_value, tb):
    """Hook for unhandled exceptions that indicate a problem with PyGmod itself."""
    _error_notif.show()
    logger.exception("Unhandled PyGmod exception", exc_info=(exc_type, exc_value, tb))


sys.excepthook = handle_exception


def handle_addon_exception(addon_name):
    """
    Shows a PyGmod error icon with :func:`pygmod._error_notif.show`
    and logs the exception.
    """
    _error_notif.show()
    logger.exception("Exception in addon %r", addon_name)


def try_import(addon_dir, pkg):
    """
    Tries to import a package with name ``f"{addon_dir}.python.{pkg}"``.
    If this package doesn't exist, :exc:`ImportError` is ignored.
    All exceptions which occurred during the package code execution, including
    :exc:`ImportError`\\ s, are logged.

    Returns ``True`` if the module was imported successfully, ``False`` otherwise.
    """
    # noinspection PyBroadException
    try:
        import_module(addon_dir + '.python.' + pkg)
        return True
    # If an optional autorun package is absent, ImportError
    # will be raised. Here we handle it.
    except ImportError as e:
        # However, this ImportError may be unrelated to
        # optional autorun packages and indicate a problem
        # on the side of addon's programmer.
        # These ImportErrors are reraised.
        if not str(e).endswith("autorun__'"):
            handle_addon_exception(addon_dir)
    except BaseException:
        handle_addon_exception(addon_dir)
        return False


def is_pygmod_addon(addons_subdir):
    """Detects whether ``addons_subdir`` is a folder of a PyGmod addon."""
    abspath = path.join(ADDONS_PATH, addons_subdir)
    possible_python_dir = path.join(abspath, "python")
    return path.isdir(possible_python_dir)


def load_addon(addon_dir):
    """
    Imports autorun packages of addon from directory ``addon_dir`` if they exist,
    namely ``__shared_autorun__``,
    then ``__client_autorun__`` or ``__server_autorun__``,
    depending on the current realm.

    Returns ``True`` if at least one autorun package was successfully imported,
    ``False`` otherwise.
    """
    realm_name = 'client' if lua.G.CLIENT else 'server'
    realm_package_name = f'__{realm_name}_autorun__'
    python_dir_path = path.join(ADDONS_PATH, addon_dir, 'python')

    # Temporarily adding the addon code directory to sys.path in order to
    # allow the autorun code to import stuff relative to the code directory (python\).
    sys.path.append(python_dir_path)
    success = any((try_import(addon_dir, SHARED_PACKAGE_NAME),
                   try_import(addon_dir, realm_package_name)))
    # Removing the directory to avoid conflicts
    del sys.path[-1]
    return success


def load_addons():
    """
    Scans the ``addons\\`` directory for PyGmod addons and runs their autorun code.
    """
    logger.info('Loading addons...')

    sys.path.append(ADDONS_PATH)
    # All files and subdirs of addons\
    addons_dir_listing = listdir(ADDONS_PATH)
    # Subdirectories of addons\
    addons_subdirs = (entry for entry in addons_dir_listing
                      if path.isdir(path.join(ADDONS_PATH, entry)))
    pygmod_addons = (entry for entry in addons_subdirs if is_pygmod_addon(entry))

    for addon_dir in pygmod_addons:
        success = load_addon(addon_dir)
        if success:
            logger.info('"' + addon_dir + '" successfully loaded.')

    logger.info('Loading finished')


def main():
    """
    Finishes the PyGmod initialization.

    #. Sets up packages :mod:`pygmod._error_notif` and :mod:`pygmod._repl`.
    #. Initializes PyGmod addons.
    """
    _error_notif.setup()
    _repl.setup()
    load_addons()
