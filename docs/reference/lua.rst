``lua`` - Lua interoperability
==============================

.. automodule:: gmod.lua
    :members:

    .. class:: LuaObject

        Proxy to Lua values.

        Can be converted to a Python object with these type conversions:

        #. :class:`int`, :class:`float`
        #. :class:`bool`
        #. :class:`str`

        If this ``LuaObject`` instance is pointing to a callable table or function, you can call it
        with passing arguments of primitive Python types such as :class:`int`, :class:`float`, :class:`bool`,
        :class:`str`, :class:`bytes` and another ``LuaObject``\ s.

        If the callable returns anything, calling of ``LuaObject`` will give another ``LuaObject``\ s which point to
        the returned values.

        The *only* publicly available way of getting ``LuaObject`` instances is indexing the :data:`G` singleton.

        .. warning::

            Do not create ``LuaObject`` instances by yourself. Use the :data:`G` indexation instead.

        Example of using ``LuaObject``\ s::

            chat = G.chat  # Getting 'chat' namespace
            add_text = chat.AddText  # Getting 'chat.AddText' function
            white_color = G.Color(255, 255, 255, 255)

            first_player = G.player.GetAll()[1]

            add_text(white_color, "First player's nick is " + str(first_player.Nick(first_player)))
            # Since Player:Nick() is an equivalent of Player.Nick(Player) (pay attention to the dot instead of the colon),
            # you have to pass the first_player again, otherwise there will be an error.

            # Also, you have to explicitly convert LuaObjects to Python objects.

    .. data:: G

        Lua Global table. Can be indexed to get and set :class:`LuaObject` instances.

        For example::

            MsgN = G.MsgN
            MsgN('Hi there!')

            # Fooling everyone that we are in neither server nor client realm >:-D
            G.CLIENT = False
            G.SERVER = False
