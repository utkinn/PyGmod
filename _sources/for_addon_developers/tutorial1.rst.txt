Addon creation tutorial: part 1
===============================

In this tutorial you will learn how to create a simple "Hello world" addon with PyGmod.

1. Create addon folders
-----------------------

Open the folder where your Garry's Mod is installed. It's path approximately looks like
``...\SteamApps\GarrysMod\``.

If you don't know where your Garry's Mod copy is installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Open **Steam**.
2. Go to **Library** tab.

.. image:: addon_tutorial_images/library_tab.png

3. Right-click **Garry's Mod** and select **Properties** option.

.. image:: addon_tutorial_images/properties_option.png

4. Select **Local files** tab and click **Browse local files...** button. Your Garry's Mod folder will be opened.

.. image:: addon_tutorial_images/browse_local_files.png

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to ``garrysmod\addons\`` folder.

.. image:: addon_tutorial_images/garrysmod_addons.png

Create a new folder here. Let's name it ``hello_world``.

.. image:: addon_tutorial_images/hello_world_folder.png

Open it and create ``python`` folder. Then, in ``python`` folder, create ``__shared_autorun__`` folder.

The folder structure should look like:

.. image:: addon_tutorial_images/addon_folder_structure.png

2. Create the initialization script
-----------------------------------

When PyGmod sees your addon each time you start a new game in Garry's Mod, PyGmod runs
``(your addon folder name, "hello_world" in our case)\python\__shared_autorun__\__init__.py``.
So, we have to create a file ``__init__.py`` in ``__shared_autorun__`` folder.

A note about the game states
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyGmod runs autorun scripts for each **game realm**.

Garry's Mod game session consists of two realms: the **client** realm and the **server** realm.

The **client** state is basically your game client. It handles things such as visual rendering.
It can communicate with **server** state via the net library as an example.

The **server** state handles things on the server; it's the only state used on Dedicated Servers.
This handles things like telling entities what to do, controlling weapons/players and all game logic
(what happens when and how in game modes).

First, PyGmod runs ``__shared_autorun__.__init__`` and ``__server_autorun__.__init__`` for the **server**, then it runs
``__shared_autorun__.__init__`` and ``__client_autorun__.__init__`` for the **client**. As you can see,
``__shared_autorun__.__init__`` is ran two times: in the **server** and in the **client**.

Realms are independent, so, for example, if you create a global variable in the client realm, you won't be able
to access it from the server realm. You can use Garry's Mod's
`net library <http://wiki.garrysmod.com/page/Net_Library_Usage>` to establish communication between the realms.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Open **Notepad**.
2. Paste this code::

    print('Hello world!')

3. Go to ``File -> Save as...`` and find ``hello_world\python\__shared_autorun__\`` folder.
4. Open **File type** box and select **All files (\*.\*)** option instead of **Text document (\*.txt)**.
5. Change **Encoding** to **UTF-8**.
6. Type ``__init__.py`` in **File name** field and click **Save**.

.. image:: addon_tutorial_images/init_script.png

3. See it works
--------------------

1. Launch **Garry's Mod**.
2. Go to **Settings**, **Keyboard** tab. Click **Advanced...**

.. image:: addon_tutorial_images/gmod_advanced.png

3. Tick **Enable developer console** flag.
4. Start a new game and wait for it to load.
5. Press ``~`` key (just below ``Esc``). You will see ``Hello world!`` printed two times:
   first time with the blue color, second time with the yellow color.

.. image:: addon_tutorial_images/hello_world_msgs.png

.. note::

    Most likely you won't see ``Hello, world!`` messages going one after another.
    You might have to look closely to find them among other console messages.

=============

Congratulations! You just made your first PyGmod addon.
Proceed to the :doc:`Part 2 of the tutorial <tutorial2>`.
