Building
========

Requirements for building
-------------------------

1. `Visual Studio 2017 or newer <https://visualstudio.microsoft.com>`_
2. `CMake <https://cmake.org>`_
3. `Python <https://python.org>`_, preferably the latest version

Instructions
------------

#. Copy ``src\lua\addons\pygmod_launcher`` to ``garrysmod\addons``.
#. Copy the contents of ``src\lua\lua\includes`` to ``garrysmod\lua\includes``. Confirm the overwriting of ``init.lua``.
#. Copy ``src\python\pygmod`` to ``garrysmod\pygmod``.
#. Open **Developer Command Prompt for VS** (most likely residing in your Start menu, folder **Visual Studio**),
   ``cd`` to ``src\cpp``.
#. Run::

    cmake -G "NMake Makefiles" && nmake
#. Move ``gmsv_pygmod_win32.dll`` and ``gmcl_pygmod_win32.dll``
   from ``src\cpp`` to ``garrysmod\lua\bin``.
#. Move ``pygmod.dll`` from ``src\cpp`` to Garry's Mod's root directory (where ``hl2.exe`` resides).

------------

Final directory structure should looks like this:

::

    ...\SteamApps\GarrysMod\ ─┬─ hl2.exe
                              ├─ ...
                              ├─ pygmod.dll
                              ├─ garrysmod\ ─┬─ addons\ ─── pygmod_launcher\ ─┬─ addon.json
                              │              │                                └─ lua\ ───── init.lua
                              │              └─ lua\ ────┬─ bin\ ─────────────┬─ gmsv_pygmod_win32.dll
                              │                          │                    └─ gmcl_pygmod_win32.dll
                              │                          └─ includes\ ────────┬─ init.lua (Modified)
                                                                              └─ original_init.lua
                              └─ pygmod\ ────── pygmod\ ──────────────────────┬─ __init__.py
                                                                              ├─ _error_notif.py
                                                                              └─ ...

.. seealso::

    :doc:`Building documentation <building_docs>`
