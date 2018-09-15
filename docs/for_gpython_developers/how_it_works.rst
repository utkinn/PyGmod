How GPython works
=================

Let's suppose we have a simpliest "Hello World" GPython addon::

    addons\ ─┬─ example\ ─┬─ addon.json
            ...           ├─ python\ ─── __autorun__\ ─── __init__.py

``__init__.py``::

    from gmod import *

    # Greeting the first player
    print('Hello, ' + Player(1).nick + '!')

1. Lua Launcher
---------------

GPython's Lua launcher is a regular Lua addon.
When it's loaded by Garry's Mod's addon system, the launcher activates
``gmcl_gpython_win32.dll`` and ``gmsv_gpython_win32.dll``::

    require 'gpython'

``gmcl_gpython_win32.dll`` is for the *client* and ``gmsv_gpython_win32.dll`` is for the *server*.

2. Realms' DLLs
---------------

These two DLLs call ``gpython_run()`` in ``gpython.dll``.

3. Main GPython DLL: ``gpython.dll``
------------------------------------

``gpython_run()`` does these preparation operations:

Server
^^^^^^

.. _server_cpp_module_routine:

1. Adds :mod:`luastack` module to the builtin initialization table.
2. Initializes Python interpreter.
3. Appends ``garrysmod\gpython\`` to :data:`sys.path`.
4. Calls ``setup()`` in :mod:`luastack` thus setting the global lua stack pointer
   and setting :data:`luastack.IN_GMOD` to ``True``.
5. Redirects I/O to Garry's Mod console with :mod:`gmod.streams`.
6. Adds :doc:`Lua2Python interoperability functions <../lua_reference>` (using Python from Lua).
7. Scans ``addons\`` directory for GPython addons and runs their code.

Client
^^^^^^

Client's routine is the same as server's except the step **2**.

Instead of initializing Python again, a subinterpreter is created and swapped to.

4. GPython wrappers
-------------------

:class:`~gmod.player.Player` is just a wrapper over the corresponding Lua functions,
as much as many other GPython services.

In this example, ``Player(1)`` creates an object that wraps ``Player`` Lua class. ``nick`` is a property that
gets players' nicknames using `Player:Nick() <http://wiki.garrysmod.com/page/Player/Nick>`_ function.

This property looks like this::

    @property
    def nick(self):
        return str(self._player_luaobj['Nick']())

The :class:`~gmod.player.Player` internally uses :class:`gmod.lua.LuaObject` to work with players.

5. :mod:`gmod.lua` module
-------------------------

:mod:`gmod.lua` module is itself a wrapper over :mod:`luastack` module. :mod:`gmod.lua` simplifies the interoperability
with Lua by providing :class:`~gmod.lua.LuaObject` class and :data:`~gmod.lua.G` singleton.

:class:`~gmod.lua.LuaObject` internally uses the :doc:`luastack module<../reference/internal/luastack>`.

6. ``luastack`` module
-------------------------

:doc:`luastack module <../reference/internal/luastack>` manipulates the Lua stack. Lua stack pointer is
`previously set by the C++ module <server_cpp_module_routine>`_.

======

And that's it, our GPython addon is initialized. For me, ``Hello, Protocs!`` will be printed to console.
