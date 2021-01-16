"""This script drives the PyGmod installer, ``pygmod.pyz``.

Installer format
================

Installer is a ``.zip`` archive with a following structure::

    pygmod.pyz --- common.zip
              |--- win32.zip
              |--- linux32.zip
              `--- __init__.py (this file)

``common.zip``, ``win32.zip`` and ``linux32.zip`` are "bundles".

``common.zip`` contains files which are the same for all platforms
 and all bit-versions of Garry's Mod.
``win32.zip`` contains files for Windows, 32-bit Garry's Mod.
``linux32.zip`` contains files for Linux, 32-bit Garry's Mod.

All files in each bundle are organized in a directory structure
that is relative to the Garry's Mod root folder (``.../steamapps/common/GarrysMod/``).
That is, the bundle root corresponds to ``GarrysMod``,
``bundle_root/addons`` to ``GarrysMod/addons``, etc.
"""

from string import ascii_uppercase
import os
import sys
import traceback
import logging
import itertools
import tempfile
from tkinter import Tk, StringVar
from tkinter.ttk import Label, Button
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo
from zipimport import zipimporter
from zipfile import ZipFile

# Graphical exception handling

def excepthook(exc_class, exc_val, exc_tb):
    """Custom excepthook which shows unhandled exceptions in error message boxes."""
    showerror("Installer error",
              ''.join(traceback.format_exception(exc_class, exc_val, exc_tb)))


sys.excepthook = excepthook


def ensure_inside_zip():
    """Ensures this script is ran inside the ``pyz`` file."""
    # noinspection PyUnresolvedReferences
    inside_zip = isinstance(__loader__, zipimporter)
    if not inside_zip:
        showerror("Installer error", "This script is intended to be ran inside the "
                                     "pyz file, without being extracted. "
                                     "Please run pygmod.pyz directly.")
        exit(1)


def get_drives():
    """Returns a list of all drive root paths on a Windows system."""

    assert os.name == "nt"

    # pylint: disable=import-outside-toplevel
    from ctypes import windll

    drives = []
    drives_bitmask = windll.kernel32.GetLogicalDrives()
    for letter in ascii_uppercase:
        if drives_bitmask & 1:
            drives.append(letter + ":\\")
        drives_bitmask >>= 1

    return drives


def browse(dir_var):
    """
    Asks the user to pick a directory to install PyGmod to and puts the selected
    directory path to :class:`~tkinter.StringVar` ``dir_var``.
    """
    new_dir = askdirectory().replace("/", os.sep)
    if new_dir:
        dir_var.set(new_dir)


def validate_path(path_var):
    """
    Checks whether the path in :class:`~tkinter.StringVar` ``path_var`` is valid.
    If the path is invalid, an error message box is shown and ``False`` is returned.
    If the path is valid, ``True`` is returned.
    """
    valid = os.path.isdir(path_var.get())
    if not valid:
        showerror("Invalid path",
                  "The current path is invalid. Please choose a valid path.")
    return valid


def get_installer_zip():
    """
    Returns :class:`zipfile.ZipFile` for an ``.zip`` file which contains this script.
    """
    return ZipFile(sys.argv[0])


def script_filename():
    """Returns the file name of this script."""
    return __file__.split(os.sep)[-1]


def extract_bundle(destination, bundle):
    """
    Extracts the bundle with a name specified by ``bundle`` to path ``destination``.

    ``bundle`` is one of:

        - "common": files for all OSes and all Garry's Mod bitnesses
        - "win32": files for Windows, 32-bit Garry's Mod
        - "linux32": files for Linux, 32-bit Garry's Mod
    """

    installer_zip = get_installer_zip()
    temp_dir = tempfile.TemporaryDirectory(suffix=bundle, prefix="pygmod")

    bundle_zip = extract_bundle_to_temp(installer_zip, bundle, temp_dir)
    logging.info("Extracting bundle %s", bundle)
    bundle_zip.extractall(destination)


def extract_bundle_to_temp(installer_zip, bundle, temp_dir):
    """
    Extract the bundle zip to a temporary folder
    and return a :class:`zipfile.ZipFile` object for the bundle.
    """
    bundle_filename = bundle + ".zip"
    logging.info("Extracting %s to a temp folder %s", bundle_filename, temp_dir.name)
    installer_zip.extract(bundle_filename, temp_dir.name)
    return ZipFile(os.path.join(temp_dir.name, bundle_filename))


def install(path_var):
    """
    Extracts PyGmod files to the directory contained in :class:`~tkinter.StringVar`
    ``path_var``.
    """
    if not validate_path(path_var):
        return

    extract_bundle(path_var.get(), "common")
    if os.name == "nt":
        extract_bundle(path_var.get(), "win32")
    else:
        extract_bundle(path_var.get(), "linux32")

    showinfo("Success", "PyGmod has been installed successfully.")
    exit()


def find_gmod_dir():
    """
    Attempts to detect the Garry's Mod installation path.
    Returns the path on success and an empty string on failure.
    """

    if os.name == "nt":  # Windows
        guesses = find_gmod_dir_windows()
    else:  # Linux
        guesses = find_gmod_dir_linux()

    for path in guesses:
        logging.debug("Assuming %s", path)
        if os.path.isdir(path):
            logging.debug("Guessed!")
            return path

    logging.info("Couldn't automatically detect Garry's Mod path.")
    return ""


def find_gmod_dir_windows():
    """
    Attempts to detect the Garry's Mod installation path on Windows.

    It tries following locations:

        1. C:\\Program Files (x86)\\Steam\\steamapps\\common\\GarrysMod
        2. <all drives>:\\Steam\\steamapps\\common\\GarrysMod
        3. <all drives>:\\SteamLibrary\\steamapps\\common\\GarrysMod
        4. <all drives>:\\SteamApps\\steamapps\\common\\GarrysMod
    """

    drives = get_drives()

    # Trying to guess between common Garry's Mod installation paths
    common_paths = [
        "Steam\\steamapps\\common\\GarrysMod",
        "SteamLibrary\\steamapps\\common\\GarrysMod",
        "SteamApps\\steamapps\\common\\GarrysMod",
    ]

    guesses = ["C:\\Program Files (x86)\\Steam\\steamapps\\common\\GarrysMod"]
    guesses += ["".join(path) for path in itertools.product(drives, common_paths)]

    return guesses


def find_gmod_dir_linux():
    """
    Attempts to detect the Garry's Mod installation path on Linux.

    There's only one possible path that comes to mind:
    ``~/.steam/steam/steamapps/common/GarrysMod``.
    """
    return [os.path.expanduser("~/.steam/steam/steamapps/common/GarrysMod")]


def main():
    """Main installer function."""
    logging.basicConfig(level=logging.INFO)

    ensure_inside_zip()

    root = Tk()
    root.wm_title("PyGmod installer")

    gmod_dir_var = StringVar(root, find_gmod_dir())
    gmod_dir_label = Label(root, textvariable=gmod_dir_var)
    gmod_dir_label.grid(row=1, column=1, padx=10, pady=10)

    browse_btn = Button(root, text="Browse...", command=lambda: browse(gmod_dir_var))
    browse_btn.grid(row=1, column=2, padx=10)

    install_btn = Button(root, text="Install", command=lambda: install(gmod_dir_var))
    install_btn.grid(row=2, column=1, columnspan=2, ipadx=10, ipady=3, pady=5)

    root.mainloop()


main()
