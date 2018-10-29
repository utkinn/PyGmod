Building
========

Requirements for building
-------------------------

1. `Cython <http://cython.org>`_
2. `Visual Studio 2017 <https://visualstudio.microsoft.com>`_

Instructions
------------

#. Copy ``lua_launcher\gpython_launcher`` directory to ``garrysmod\addons`` directory.
#. Open command prompt, ``cd`` to ``python_extensions`` directory and run ``setup.py build_ext --inplace``.
#. Move all files with ``.py`` and ``.pyd`` extensions
   in ``python_extensions`` directory to ``garrysmod\gpython`` directory.
#. Copy ``python_extensions\gmod`` directory to ``garrysmod\gpython\gmod``
   (so there is a bunch of ``.py`` files in ``garrysmod\gpython\gmod`` directory).
#. Open ``GPython.sln`` with Visual Studio and build the solution.
#. Move ``gmsv_gpython_win32.dll`` and ``gmcl_gpython_win32.dll``
   from ``bin_modules\build`` directory to ``garrysmod\lua\bin`` directory.
#. Move ``gpython.dll`` to Garry's Mod's root directory (where ``hl2.exe`` resides).

------------

Final directory structure should looks like this:

::

    ...\SteamApps\GarrysMod\ ─┬─ hl2.exe
                              ├─ ...
                              ├─ gpython.dll
                              ├─ garrysmod\ ─┬─ addons\ ─── gpython_launcher\ ─┬─ addon.json
                              │              │                                 └─ lua\ ───── ...
                              │              └─ lua\ ────── bin\ ──────────────┬─ gmsv_gpython_win32.dll
                              │                                                └─ gmcl_gpython_win32.dll
                              └─ gpython\ ───┬─ luastack.cpXX-win32.pyd
                                             ├─ loader.py
                                             └─ gmod\ ─────────────────────────┬─ __init__.py
                                                                               ├─ lua.py
                                                                               ├─ ...
                                                                              ...

.. seealso::

    :doc:`Building documentation <building_docs>`
