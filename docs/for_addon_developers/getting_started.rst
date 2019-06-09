Getting Started for Addon Developers
====================================

Development of add-ons based on PyGmod looks almost the same as the development of conventional Lua-addons.
You create a subfolder for your addon in the ``addons`` folder and put the code and resources there.
The PyGmod addon structure is almost the same as a regular addon, except for the ``python`` folder,
where the addon Python code is stored.

PyGmod addon structure
----------------------

Comparison of the structure of an usual addon and a PyGmod addon::

    my_lua_addon\ ─┬─ addon.json
                   ├─ lua\ ─────────┬─ autorun\ ─┬─ shared_init.lua
                   │                │            ├─ server\ ────┬─ init.lua
                   │                │            │              └─ ...
                   │                │            └─ client\ ────┬─ cl_init.lua
                   │                │                           └─ ...
                   │                │
                   │                ├─ entities\ ─┬─ myentity\ ─┬─ cl_init.lua
                   │                └─ ...        └─ ...        ├─ init.lua
                   │                                            └─ shared.lua
                   ├─ materials\ ─ ...
                   ├─ sound\ ───── ...
                   └─ ...

    my_pygmod_addon\ ─┬─ addon.json
                      ├─ python\ ───────┬─ __shared_autorun__\ ───────┬─ __init__.py
                      │                 │                             ├─ otherfile.py
                      │                 │                             └─ ...
                      │                 ├─ __client_autorun__\ ───────┬─ __init__.py
                      │                 │                             └─ ...
                      │                 ├─ __server_autorun__\ ───────┬─ __init__.py
                      │                 │                             └─ ...
                      │                 ├─ mypackage\ ────────────────┬─ __init__.py
                      │                 │                             └─ ...
                      │                 └─ folder_with_some_scripts\ ─┬─ spam.py
                      │                                               ├─ eggs.py
                      │                                               └─ ...
                      ├─ lua\ (optional) ─ ...
                      ├─ materials\ ────── ...
                      ├─ sound\ ────────── ...
                      └─ ...

The ``python`` folder
^^^^^^^^^^^^^^^^^^^^^

Consider the structure of the ``python`` folder::

    python\ ───────┬─ __shared_autorun__\ ───────┬─ __init__.py
                   │                             ├─ otherfile.py
                   │                             └─ ...
                   ├─ __client_autorun__\ ───────┬─ __init__.py
                   │                             └─ ...
                   ├─ __server_autorun__\ ───────┬─ __init__.py
                   │                             └─ ...
                   ├─ mypackage\ ────────────────┬─ __init__.py
                   │                             └─ ...
                   └─ folder_with_some_scripts\ ─┬─ spam.py
                                                 ├─ eggs.py
                                                 └─ ...

The ``__*_autorun__`` folders are Python packages, which are executed when a singleplayer game is being loaded,
when a server is being launched or when connecting to a server.

"Python packages" means that these folders should contain the file ``__init__.py``,
where should be the initialization code of these packages.
It is ``__init__.py`` that is executed by the PyGmod addon loader.
The remaining files of the package will be ignored unless you import them inside ``__init__.py``::

    from . import otherfile

The ``__shared_autorun__`` package is initialized 2 times: the first time on the server side, the second on the client side.
``__server_autorun__`` and ``__client_autorun__`` are initialized on the server side and on the client side, respectively,
after ``__shared_autorun__``.

Other packages and scripts can be imported relative to the ``python`` folder::

    import mypackage
    from folder_with_some_scripts import spam, eggs

PyGmod code appearance
----------------------

The PyGmod addons code is plain Python code. For example, you can type something into the Garry's Mod console
with the function :func:`print()`::

    # python\__server_autorun__\__init__.py
    print("Hello from PyGmod!")

.. image:: images/print_example.png

You can use any modules from the standard Python library, thanks to which PyGmod addons have much more
freedom and potential than ordinary Lua addons.

To interact with the game, you need two modules: :mod:`pygmod.gmodapi` and :mod:`pygmod.lua`.

Game interaction: ``pygmod.gmodapi`` and ``pygmod.lua``
-------------------------------------------------------

``pygmod.gmodapi``
^^^^^^^^^^^^^^^^^^

Module :mod:`pygmod.gmodapi` gives access to almost all functions, classes and libraries that are
described in `Garry's Mod Wiki <wiki.garrysmod.com>`_. To use the module, simply import from it what
you need, for example::

    from pygmod.gmodapi import LocalPlayer


You can also import everything::

    from pygmod.gmodapi import *

.. note:: Enum members have to be accessed with :data:`pygmod.lua.G`.

``pygmod.lua``
^^^^^^^^^^^^^^

If your addon also contains Lua code and you need to connect Python code with it, you can use :mod:`pygmod.lua` for this.
It contains an object :data:`~pygmod.lua.G`, with which you can modify the Lua environment.
For example, you can create a global variable that is accessible from Lua::

    from pygmod.lua import G

    G.my_global_var = "My data"

.. note::

    To refer to variables beginning with an underscore ( ``_`` ), use ``G["_underscore_var"]``
    instead of ``G._underscore_var``. Variables beginning with ``_`` are reserved for internal use.

=====

Check out :doc:`Addon development tutorial <tutorial1>` to learn how to create a simple "Hello world" addon.
Then, see :doc:`Module reference <../reference>` to see the list of libraries PyGmod provides to you.
