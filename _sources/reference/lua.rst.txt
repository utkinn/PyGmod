``pygmod.lua`` - Lua interoperability
=====================================

Access to the Lua environment. Can be used for getting and setting arbitrary variables,
calling Lua functions and manipulating tables and objects.

.. data:: G

    Lua global namespace. Same as ``_G`` in Lua.

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
        should be accessed with the subscription syntax::

            # Won't work
            G._foo
            # Will work
            G['_foo']

.. class:: Table

    Class for representing Lua tables.

    :class:`Table` has a multifunctional constructor::

        # Creating an empty table
        t = Table()

        # Converting a dict to a table
        d = {'a': 1, 'b': 2}
        t = Table(d)

        # Converting an iterable to a table
        i = [1, 2, 3]
        t = Table(i)

    Constructor which takes :class:`int` as argument is intended for internal use.
    More specifically, it wraps a table referenced by :func:`_luastack.reference_create`

    .. note::

        Members which names start with ``_``
        should be accessed with the subscription syntax::

            # Won't work
            Table({"_foo": 1})._foo
            # Will work
            Table({"_foo": 1})['_foo']

    If the undelying table's metatable has ``__call`` function, this object can be called::

        from gmod.api import setmetatable

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

    Runs a string of Lua code.

    ::

        exec_lua("print(jit.version)")
        # "LuaJIT 2.0.4" will be printed to the console

.. function:: eval_lua(code: str) -> object

    Evaluates a Lua expression and returns the result.

    >>> print(eval_lua("function() return 123 end")())
    123

.. exception:: LuaError

    Raised when a Lua error occurs while running some Lua code in Python.
