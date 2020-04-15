Building
========

Requirements for building
-------------------------

Windows
~~~~~~~

1. `Visual Studio 2017 or newer <https://visualstudio.microsoft.com>`_.
2. `CMake <https://cmake.org>`_
3. `Python 3 <https://python.org>`_, preferably the latest version.
   You will need a **32-bit** version for the stable Garry's Mod branch (most likely the one you use),
   or a **64-bit** version for the x86-64 Garry's Mod branch.
   
   Make sure you had "Download debugging symbols" and "Download debug binaries" checked when you were installing
   Python. If you're not sure or want to enable them, go to Settings -> Apps -> Python -> Modify.
   Otherwise, building may fail with an error about missing ``python3.X_d.lib``.

Linux
~~~~~

1. **GCC**
2. **CMake**
3. **Python 3 (development version)**

All dependencies can be installed with::

    # Debian-based distributions (Debian, Ubuntu, Mint, Pop!_OS, etc.)
    sudo apt install gcc cmake python3-dev

    # Arch Linux, Manjaro
    sudo pacman -Suy gcc cmake python

A note about 32 and 64 bits
---------------------------

.. highlight:: sh

The regular version of Garry's Mod (its stable branch) is still 32-bit.
This makes compiling and using PyGmod tricky if you:

1. are on Windows and have 64-bit version of Python installed
2. are on 64-bit version of Linux (most likely you are).

This is because Garry's Mod, PyGmod and Python should all have the same bitness for successful compilation and usage.

There are two solutions for this problem: you can either install a 32-bit version of Python, or switch to "x86-64" branch of Garry's Mod.

-  You can switch to the x86-64 branch of Garry's Mod and build a 64-bit version of PyGmod.
   In order to switch to the x86-64 branch, go to Steam -> Library -> Right click on Garry's Mod -> Properties -> Betas -> select "x86-64" in the first dropdown.

   To compile a 64-bit version of PyGmod, use::

       # Windows
       cmake -DBITS=64 . && msbuild PyGmod.sln
       # Linux
       cmake -DBITS=64 . && make

-  If you don't want to switch to "x86-64" branch and you're on Windows, install a 32-bit version of Python from `python.org <https://python.org>`_.
   You should download a "x86 installer", not a "x86-64 installer".

   .. note::
   
       If you have both 32-bit and 64-bit versions of Python installed on your Windows system,
       you may encounter an error about incompatible x86 and x86-64 libraries during the compilation.
       This error could be resolved by specifying Python's installation directory manually, like this::

           cmake -DCMAKE_FIND_ROOT_PATH="C:\Program Files (x86)\Programs\Python38-32" .

       You will have to specify the correct folder for 32-bit or 64-bit version.  
       By default, ``cmake`` will prepare the 32-bit version of PyGmod.

-  If you're on Linux and you don't want to switch to "x86-64" branch, you can install a 32-bit version of Python for just *using* PyGmod::

       # Debian

       # Before installing, you have to enable the i386 repository if you haven't done that already.
       # Use the following command:
       
       sudo dpkg --add-architecture i386 && sudo apt update

       # Install 32-bit Python:
       sudo apt install python3:i386

       # Arch:
       # You'll have to install "lib32-python" from AUR: https://aur.archlinux.org/packages/lib32-python/

   However, actually compiling 32-bit PyGmod on Linux is tricky, though possible. You'll have to play with CMake variables to point it to 32-bit Python libraries (refer to `FindPython3 CMake module documentation <https://cmake.org/cmake/help/latest/module/FindPython3.html>`_ if you want to try to compile 32-bit PyGmod on a host 64-bit Linux).

   To make compiling 32-bit PyGmod simplier, there is a script called ``build_linux_x86.sh`` in ``src/cpp/buildscripts``.
   It will compile 32-bit PyGmod inside a Docker container. Make sure you have Docker installed::

       # Debian:
       sudo apt install docker.io

       # Arch:
       sudo pacman -Suy docker

       # Additional possibly required actions (All distributions):

       # Add yourself to group "docker".
       # Relogin is required for this to take effect.
       sudo usermod -aG docker `whoami`

       # Start docker daemon:
       sudo systemctl start docker

   This script will build PyGmod to work with whatever newest version of Python available on Debian Stable.
   However, this won't necessary be the latest version of Python available at all, thus you might have a version
   discrepancy between the container and your system 
   (for example, at the time of writing, the latest version of Python at all was 3.8, while the latest version on Debian Stable
   was 3.7).

   This might present a problem if you use a rolling-release distribution, such as Arch.
   You can try switching the container base image to ``i386/debian-testing`` in this case.

Instructions
------------

Common steps for all OSes
~~~~~~~~~~~~~~~~~~~~~~~~~

#. Copy ``src/lua/addons/pygmod_launcher`` to ``garrysmod/addons``.
#. Copy the contents of ``src/lua/lua/includes`` to ``garrysmod/lua/includes``. Confirm the overwriting of ``init.lua``.
#. Copy ``src/python/pygmod`` to ``garrysmod/pygmod``.

Compiling binary modules for Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Open **Developer Command Prompt for VS** (most likely residing in your Start menu, folder **Visual Studio**),
   ``cd`` to ``src\cpp``.
#. Run::

    cmake . && msbuild PyGmod.sln
#. Move ``gmsv_pygmod_win(32/64).dll`` and ``gmcl_pygmod_win(32/64).dll``
   from ``src\cpp`` to ``garrysmod\lua\bin``.
#. Move ``pygmod.dll`` from ``src\cpp`` to Garry's Mod's root directory (where ``hl2.exe`` resides).

Compiling binary modules for Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Open a terminal if you haven't done that already and change the directory to ``src/cpp``.
#. Run::

    cmake . && make

#. Move ``gmsv_pygmod_linux(64).dll`` and ``gmcl_pygmod_linux(64).dll``
   from ``src/cpp`` to ``garrysmod/lua/bin``.
#. Move ``libpygmod.so`` from ``src/cpp`` to ``.../SteamApps/common/GarrysMod/bin``.

------------

Final directory structure should look like this:

Windows
~~~~~~~

.. code-block:: text

    ...\SteamApps\GarrysMod\ ─┬─ hl2.exe
                              ├─ ...
                              ├─ pygmod.dll
                              ├─ garrysmod\ ─┬─ addons\ ─── pygmod_launcher\ ─┬─ addon.json
                              │              │                                └─ lua\ ───── init.lua
                              │              └─ lua\ ────┬─ bin\ ─────────────┬─ gmsv_pygmod_win(32/64).dll
                              │                          │                    └─ gmcl_pygmod_win(32/64).dll
                              │                          └─ includes\ ────────── init.lua (Modified)
                              └─ pygmod\ ────── pygmod\ ──────────────────────┬─ __init__.py
                                                                              ├─ _error_notif.py
                                                                              └─ ...

Linux
~~~~~


.. code-block:: text

    .../SteamApps/GarrysMod/ ─┬─ hl2.sh
                              ├─ ...
                              ├─ bin/ ───────┬─ libpygmod.so
                              │              └─ ...
                              ├─ garrysmod/ ─┬─ addons/ ─── pygmod_launcher/ ─┬─ addon.json
                              │              │                                └─ lua/ ───── init.lua
                              │              └─ lua/ ────┬─ bin/ ─────────────┬─ gmsv_pygmod_linux(64).dll
                              │                          │                    └─ gmcl_pygmod_linux(64).dll
                              │                          └─ includes/ ────────── init.lua (Modified)
                              └─ pygmod/ ────── pygmod/ ──────────────────────┬─ __init__.py
                                                                              ├─ _error_notif.py
                                                                              └─ ...

.. seealso::

    :doc:`Building documentation <building_docs>`
