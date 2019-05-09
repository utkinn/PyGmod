How PyGmod works
================

Startup
-------

.. image:: graph.png

API levels
----------

Let's suppose we have a simple "Hello World" PyGmod addon::

    addons\ ─┬─ example\ ─┬─ addon.json
            ...           ├─ python\ ─── __shared_autorun__\ ─── __init__.py

``__init__.py``::

    from gmod.api import *

    if SERVER:
        def greet(new_player):
            new_player._.ChatPrint('Hello, ' + new_player._.Nick() + '!')

        hook.Add('PlayerInitialSpawn', 'greet', greet)
    else:
        print('On client')

1. Lua Launcher
^^^^^^^^^^^^^^^

PyGmod's Lua launcher is a regular Lua addon.
When it's loaded by Garry's Mod's addon system, the launcher activates
``gmcl_pygmod_win32.dll`` and ``gmsv_pygmod_win32.dll``.
``gmcl_pygmod_win32.dll`` is for the *client* and ``gmsv_pygmod_win32.dll`` is for the *server*.

2. Realms' DLLs: ``gmcl_pygmod_win32.dll`` and ``gmsv_pygmod_win32.dll``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These two DLLs call ``pygmod_run()`` in ``pygmod.dll``.

3. Main PyGmod DLL: ``pygmod.dll``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pygmod_run()`` partially initializes PyGmod:

Server
""""""

#. Adds :mod:`_luastack` module to the list of Python builtin modules.
#. Initializes Python interpreter.
#. Appends ``garrysmod\pygmod\`` to :data:`sys.path`.
#. Calls ``init()`` in :mod:`_luastack`, thus setting the internal Lua stack pointer.
#. Adds :doc:`functions for manipulating Python from Lua <../lua_reference>`.
#. Calls ``main()`` in ``loader.py``.
#. Saves the server Python subinterpreter for later use.

Client
""""""

Client's routine is the same as server's except the step **2**.

Instead of initializing Python again, a subinterpreter is created and swapped to.

4. ``loader.py``
^^^^^^^^^^^^^^^^

``loader.py`` finishes the initialization.

#. Redirects I/O to Garry's Mod console with :mod:`gmod._streams` I/O classes.
#. Scans ``addons\`` directory for PyGmod addons and initializes them.

5. :mod:`lua` module
^^^^^^^^^^^^^^^^^^^^

``Player()`` returns :class:`lua.Table` (for now, all userdata are represented as tables).
:mod:`lua` module is itself a wrapper over :mod:`_luastack` module.

6. :mod:`_luastack` module
^^^^^^^^^^^^^^^^^^^^^^^^^^

:doc:`_luastack module <../reference/internal/luastack>` contains functions for direct Lua stack manipulation.
This is the most low-level way of interacting with Lua.
