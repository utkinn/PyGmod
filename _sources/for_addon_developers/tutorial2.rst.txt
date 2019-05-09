Addon creation tutorial: part 2
===============================

*See* :doc:`Part 1 <tutorial1>` *of the tutorial if you haven't seen it yet.*

In this tutorial we will improve our "Hello, World" addon a bit.

We will make it to print "Hello, X!" to our chat instead of the game console, and there will be our
nickname in place of "X".

First, rename the ``__shared_autorun__`` folder to ``__server_autorun__``, because we don't need the client to
participate in the process anymore. The server will wait for new players and will print "Hello, X!" on
their first spawn.

.. image:: addon_tutorial_images/rename_shared_to_server.png

Then, open the ``__init__.py`` script again.

We have to make two changes here: first, we need to print the text to the chat instead of the game console.
We need to access Garry's Mod Lua somehow. We can use :mod:`pygmod.gmodapi` module for this.
Add this line to the top of the script::

    from pygmod.gmodapi import *

Now we can use any Lua function right away.

We will set a ``PlayerInitialSpawn`` hook with a callback which will print the greeting.

To do so, we need to call `hook.Add() <http://wiki.garrysmod.com/page/hook/Add>`_ with 3 parameters: the event name,
the hook ID and the callback function - a function which is called when the specified event happens.

In our case, the callback function receives one parameter - an object which represents a connected player.

So, we define our callback function::

    from pygmod.gmodapi import *

    def greet(new_player):          # <--
        print('Hello world!')       # <--

and create a hook::

    from pygmod.gmodapi import *

    def greet(new_player):
        print('Hello world!')

    hook.Add('PlayerInitialSpawn', 'greet', greet)  # <--

``Player`` objects have `ChatPrint() <http://wiki.garrysmod.com/page/Player/ChatPrint>`_ method,
which we can use to print text to their chat. In Lua, it would look like this::

    new_player:ChatPrint('Hello world!')
              ^

Notice a colon here. In PyGmod, there is a ``._.`` construction which plays the same role as colon in Lua.

::

    from pygmod.gmodapi import *

    def greet(new_player):
        new_player._.ChatPrint('Hello world!')  # <--

    hook.Add('PlayerInitialSpawn', 'greet', greet)

Now ``Hello world!`` will be printed to the chat. Let's make this greeting personal now: we will greet the player
instead of the world.

Now we get the player's nick with `Nick() <http://wiki.garrysmod.com/page/Player/Nick>`_ method.

::

    from pygmod.gmodapi import *

    def greet(new_player):
        new_player._.ChatPrint('Hello, ' + new_player._.Nick() + '!')  # <--

    hook.Add('PlayerInitialSpawn', 'greet', greet)

We're done here. Save and close the script, launch the game, start a new game and look at the chat.

.. image:: addon_tutorial_images/chat_msg.png

=======

You have finished the tutorial and, I hope, you have understood how to make addons with PyGmod.
If you have questions, you can always `get help at our Discord server <https://discord.gg/aAs4qrj>`_.
