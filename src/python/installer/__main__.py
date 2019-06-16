from string import ascii_uppercase
from ctypes import windll
import os
import traceback
import logging
from zipimport import zipimporter
from zipfile import ZipFile

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo
from tkinter.ttk import *


def excepthook(exc_class, exc_val, tb):
    showerror("Installer error",
              ''.join(traceback.format_exception(exc_class, exc_val, tb)))


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
    """Returns a list of all drive root paths on this system."""
    drives = []
    drives_bitmask = windll.kernel32.GetLogicalDrives()
    for letter in ascii_uppercase:
        if drives_bitmask & 1:
            drives.append(letter + ":\\")
        drives_bitmask >>= 1

    return drives


def browse(dir_var):
    new_dir = askdirectory().replace("/", os.sep)
    if new_dir:
        dir_var.set(new_dir)


def validate_path(path_var):
    valid = os.path.isdir(path_var.get())
    if not valid:
        showerror("Invalid path",
                  "The current path is invalid. Please choose a valid path.")
    return valid


def this_zipfile():
    """
    Returns :class:`zipfile.ZipFile` for an ``.zip`` file which contains this script.
    """
    return ZipFile(sys.argv[0])


def script_filename():
    """Returns the file name of this script."""
    return __file__.split(os.sep)[-1]


def extract_pygmod_files(zipfile, destination):
    """
    Extracts all contents of a ``.zip``
    file represented by ``zipfile`` to path ``destination``, except this script.
    """
    files_to_extract = zipfile.namelist()
    logging.debug(script_filename())
    logging.debug(files_to_extract)
    files_to_extract.remove(script_filename())
    for file in files_to_extract:
        logging.info(f"Extracting {file}")
        zipfile.extract(file, destination)


def install(path_var):
    if not validate_path(path_var):
        return

    zipfile = this_zipfile()
    extract_pygmod_files(zipfile, path_var.get())

    showinfo("Success", "PyGmod was installed successfully.")
    exit()


def find_gmod_dir():
    for drive in get_drives():
        assumed_path = os.path.join(drive, "Steam", "steamapps", "common", "GarrysMod")
        logging.debug(f"Assuming {assumed_path}")
        if os.path.isdir(assumed_path):
            logging.debug("Guessed!")
            return assumed_path
        assumed_path = os.path.join(drive, "SteamApps", "steamapps", "common",
                                    "GarrysMod")
        logging.debug(f"Assuming {assumed_path}")
        if os.path.isdir(assumed_path):
            logging.debug("Guessed!")
            return assumed_path
    logging.info("Couldn't automatically detect Garry's Mod path.")
    return ""


def main():
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
