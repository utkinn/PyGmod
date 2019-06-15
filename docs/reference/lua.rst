``pygmod.lua`` - Lua interoperability
=====================================

This module provides the direct access to the Lua environment, such as getting and setting arbitrary variables,
calling Lua functions and manipulating tables and objects.

.. module:: pygmod.lua
    :synopsis: Lua interoperability

.. data:: G

    A singleton object that represents the Lua global namespace. Same as ``_G`` in Lua. You can use it to get and set
    variables in the Lua environment.

    ::

        MsgN = G.MsgN
        MsgN('Hi there!')

        ply = G.Player(1)
        # Use "._." where you would use ":" in Lua
        ply._.Extinguish()

        # Fooling everyone that we are in neither server nor client realm >:-D
        G.CLIENT = False
        G.SERVER = False

        # Creating variables with exotic names
        G['!!!'] = 123

    .. note::

        Members which names start with ``_``
        should be accessed with the subscription syntax. These names are reserved for internal use.

        ::

            # Won't work
            G._foo
            # Will work
            G['_foo']

.. class:: Table

    Class which represents Lua tables.

    You can create an empty table by passing no arguments to the constructor::

        new = Table()

    You can wrap Python mapping or iterable into a table by passing it to the constructor::

        Table([1, 2, 3])
        Table({"a": 1})

    .. note::

        Members which names start with ``_``
        should be accessed with the subscription syntax. These names are reserved for internal use.

        ::

            # Won't work
            Table({"_foo": 1})._foo
            # Will work
            Table({"_foo": 1})['_foo']

    If the table's metatable has ``__call`` function, this object can be called::

        from pygmod.gmodapi import setmetatable

        tbl = Table()

        def __call(self):
            print("hi")

        setmetatable(tbl, Table({"__call": __call}))
        tbl()  # Prints "hi"

    :class:`Table` objects can be iterated like dictionaries::

        # Iterating through keys
        for k in tbl:
            ...
        for k in tbl.keys():
            ...

        # Iterating through values
        for v in tbl.values():
            ...

        # Iterating through keys and values
        for k, v in tbl.items():
            ...

    A :class:`Table` object can be converted to a dictionary:

    >>> from lua import eval_lua
    >>> tbl = eval_lua("{a = 1, b = 2, c = 3}")
    >>> print(dict(tbl))
    {'a': 1, 'b': 2, 'c': 3}

    .. method:: keys()

        Returns a keys iterator for this table. Same as ``iter(table)``.

        >>> tbl = Table({'a': 1, 'b': 2, 'c': 3})
        >>> for k in tbl.values():
        ...    print(k)
        ...
        a
        b
        c

    .. method:: values()

        Returns a values iterator for this table.

        >>> tbl = Table({'a': 1, 'b': 2, 'c': 3})
        >>> for v in tbl.values():
        ...    print(v)
        ...
        1
        2
        3

    .. method:: items()

        Returns a key-value pairs iterator for this table.

        >>> tbl = Table({'a': 1, 'b': 2, 'c': 3})
        >>> for k, v in tbl.items():
        ...    print(k, v)
        ...
        a 1
        b 2
        c 3


.. function:: exec_lua(code: str) -> None

    Runs a string of Lua code. Raises :exc:`LuaError` on failure.

    ::

        exec_lua("print(jit.version)")
        # "LuaJIT 2.0.4" will be printed to the console

.. function:: eval_lua(code: str) -> object

    Evaluates a Lua expression and returns the result. Raises :exc:`LuaError` on failure.

    >>> print(eval_lua("function() return 123 end")())
    123

.. exception:: LuaError

    Raised when a Lua error occurs while running some Lua code in Python.
