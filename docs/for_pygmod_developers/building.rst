Building
========

Requirements for building
-------------------------

1. `Cython <http://cython.org>`_
2. `Visual Studio 2017 <https://visualstudio.microsoft.com>`_

Instructions
------------

#. Copy ``lua_launcher\pygmod_launcher`` directory to ``garrysmod\addons`` directory.
#. Open command prompt, ``cd`` to ``python_extensions`` directory and run ``setup.py build_ext --inplace``.
#. Move all files with ``.py`` and ``.pyd`` extensions
   in ``python_extensions`` directory to ``garrysmod\pygmod`` directory.
#. Copy ``python_extensions\gmod`` directory to ``garrysmod\pygmod\gmod``
   (so there is a bunch of ``.py`` files in ``garrysmod\pygmod\gmod`` directory).
#. Open ``GPython.sln`` with Visual Studio and build the solution.
#. Move ``gmsv_pygmod_win32.dll`` and ``gmcl_pygmod_win32.dll``
   from ``bin_modules\build`` directory to ``garrysmod\lua\bin`` directory.
#. Move ``pygmod.dll`` to Garry's Mod's root directory (where ``hl2.exe`` resides).

------------

Final directory structure should looks like this:

::

    ...\SteamApps\GarrysMod\ ─┬─ hl2.exe
                              ├─ ...
                              ├─ pygmod.dll
                              ├─ garrysmod\ ─┬─ addons\ ─── pygmod_launcher\ ─┬─ addon.json
                              │              │                                └─ lua\ ───── ...
                              │              └─ lua\ ────── bin\ ─────────────┬─ gmsv_pygmod_win32.dll
                              │                                               └─ gmcl_pygmod_win32.dll
                              └─ pygmod\ ────┬─ luastack.cpXX-win32.pyd
                                             ├─ loader.py
                                             └─ gmod\ ─────────────────────────┬─ __init__.py
                                                                               ├─ lua.py
                                                                               ├─ ...
                                                                              ...

.. seealso::

    :doc:`Building documentation <building_docs>`
