Building
========

This article describes the process of building PyGmod from source code. You may want to do this if you're developing on PyGmod itself.
If all you want is to use or develop PyGmod addons, refer to `"How to use PyGmod" </getting_started.html#how-to-use-it>`_ guide instead.

Requirements for building
-------------------------

Windows requirements
~~~~~~~~~~~~~~~~~~~~

1. `Visual Studio 2017 or newer <https://visualstudio.microsoft.com>`_ with C++ workload selected
2. `CMake <https://cmake.org>`_
3. `Python 3 <https://python.org>`_, preferably the latest version
4. `Git <https://git-scm.com>`_

Linux requirements
~~~~~~~~~~~~~~~~~~

1. **GCC**
2. **CMake**
3. **Python 3**
4. **Git**
5. All dependencies for building Python from source. See `this AskUbuntu answer <https://askubuntu.com/a/21551/900983>`_ for a list of dependencies.
   `This article in Python Developer Guide <https://devguide.python.org/setup/#install-dependencies>`_ will also help.

    .. note::

        If you're going to build a 32-bit version, you'll need to get 32-bit (aka i386) version of dependencies,
        which is a bit tricky if you're using a 64-bit version of your Linux distribution.

        On Debian-based distributions (Ubuntu, Linux Mint), follow `this guide on Debian Wiki <https://wiki.debian.org/Multiarch/HOWTO>`_
        to install i386 packages.

        On Arch-based distributions (Manjaro), you'll have to `enable Multilib <https://wiki.archlinux.org/index.php/official_repositories#Enabling_multilib>`_
        and look for ``lib32-*`` packages. You may find some of them in AUR as well.

Instructions
------------

Building on Windows
~~~~~~~~~~~~~~~~~~~

#. Open **Developer Command Prompt for VS** (most likely residing in your Start menu, folder **Visual Studio**).
#. Run:

    .. code-block:: doscon

        > cd pygmod_dir\src

    substituting *pygmod_dir* with the full path to PyGmod source tree, for example, ``C:\Users\user\Downloads\PyGmod``.

#. Depending on what version of PyGmod you want to build, run:

    .. code-block:: doscon

        Release build for stable 32-bit Garry's Mod branch:
        > cmake -A Win32 . && msbuild -m PyGmod.sln -p:Configuration=Release

        Debug build for stable 32-bit Garry's Mod branch:
        > cmake -A Win32 -DCMAKE_BUILD_TYPE=Debug . && msbuild -m PyGmod.sln -p:Configuration=Debug

        Release build for x86-64 Garry's Mod branch:
        > cmake -A x64 . && msbuild -m PyGmod.sln -p:Configuration=Release

        Debug build for x86-64 Garry's Mod branch:
        > cmake -A x64 -DCMAKE_BUILD_TYPE=Debug . && msbuild -m PyGmod.sln -p:Configuration=Debug

    Debug builds are intended for aiding to track down bugs in the C++ part of PyGmod.
    These builds are generally less optimized and not distributable as they're linked against debug versions of Visual C++ runtime
    which ship with Visual Studio only.

#. After a few minutes, a ``.pyz`` file should appear in ``src\installer-build`` directory. This is the PyGmod installer.
   You can run it to install the freshly compiled version of PyGmod.

Building on Linux
~~~~~~~~~~~~~~~~~

#. Open a terminal in ``pygmod_dir/src``, where ``pygmod_dir`` being the PyGmod source tree root.
#. Depending on what version of PyGmod you want to build, run:

    .. code-block:: console

        Release build for stable 32-bit Garry's Mod branch:
        $ cmake . && make

        Debug build for stable 32-bit Garry's Mod branch:
        $ cmake -DCMAKE_BUILD_TYPE=Debug . && make

        Release build for x86-64 Garry's Mod branch:
        $ cmake -DBITS=64 . && make

        Debug build for x86-64 Garry's Mod branch:
        $ cmake -DCMAKE_BUILD_TYPE=Debug -DBITS=64 . && make

#. After a few minutes, a ``.pyz`` file should appear in ``src\installer-build`` directory. This is the PyGmod installer.
   You can run ``python3 pygmod-linuxXX.pyz`` to install the freshly compiled version of PyGmod.

.. seealso::

    :doc:`Building documentation <building_docs>`
