Addon creation tutorial
=======================

In this tutorial you will learn how to create a simple "Hello world" addon with GPython.

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

When GPython sees your addon each time you start a new game in Garry's Mod, GPython runs
``(your addon folder name, "hello_world" in our case)\python\__shared_autorun__\__init__.py``. As you can see,
we have to create ``__init__.py`` in ``__shared_autorun__`` folder to do anything useful.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Open **Notepad**.
2. Paste this::

    print('Hello world!')


3. Go to ``File -> Save as...`` and find ``hello_world\python\__shared_autorun__\`` folder.
4. Open **File type** box and select **All files (\*.\*)** option instead of **Text document (\*.txt)**.
5. Change **Encoding** to **UTF-8**.
6. Type ``__init__.py`` to **File name** field and click **Save**.

.. image:: addon_tutorial_images/init_script.png

3. Seeing it running
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

Congratulations! You just made your first GPython addon.
