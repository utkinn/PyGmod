"""
This module provides tools for Garry's Mod Lua interoperability, for example getting, setting values, indexing tables
and calling functions.
"""

from abc import ABC, abstractmethod

from luastack import LuaStack, Special

__all__ = ['G', 'exec', 'eval', 'table', 'LuaObjectWrapper']

ls = LuaStack()


class Reference:
    def __init__(self, ref):
        self._ref = int(ref)

    def __enter__(self):
        ls.push_ref(self._ref)

    def __exit__(self, exc_type, exc_value, traceback):
        ls.pop(1)


def push_key_or_value(key_or_value):
    """Pushes a Python value of a primitive type or a :class:`LuaObject`."""
    if key_or_value is None:
        ls.push_nil()
    if isinstance(key_or_value, int) or isinstance(key_or_value, float):
        ls.push_number(key_or_value)
    elif isinstance(key_or_value, LuaObject):
        ls.push_ref(key_or_value._ref)
    elif isinstance(key_or_value, str):
        ls.push_string(key_or_value.encode())
    elif isinstance(key_or_value, bytes):
        ls.push_string(key_or_value)
    elif isinstance(key_or_value, bool):
        ls.push_bool(key_or_value)
    elif isinstance(key_or_value, LuaObjectWrapper):
        ls.push_ref(key_or_value.lua_obj._ref)
    else:
        raise TypeError(f'unsupported key/value type: {type(key_or_value)}')


class LuaObject:
    def __init__(self):
        """Creates a :class:`LuaObject` which points to the topmost stack value and pops it."""
        self._ref = ls.create_ref()
        self._context = Reference(self._ref)

    def __del__(self):
        ls.free_ref(self._ref)

    @property
    def type(self):
        """Returns the :class:`luastack.ValueType` of the held value."""
        with self._context:
            return ls.get_type(-1)

    @property
    def type_name(self):
        """Returns the :class:`str` type representation of the held value."""
        with self._context:
            return ls.get_type_name(ls.get_type(-1))

    def __str__(self):
        with self._context:
            return ls.get_string(-1)

    def __int__(self):
        with self._context:
            return int(ls.get_number(-1))

    def __float__(self):
        with self._context:
            return float(ls.get_number(-1))

    def __bool__(self):
        with self._context:
            return ls.get_bool(-1)

    def __setitem__(self, key, value):
        with self._context:
            push_key_or_value(key)
            push_key_or_value(value)
            ls.set_table(-3)

    def __getitem__(self, key):
        with self._context:
            push_key_or_value(key)
            ls.get_table(-2)
            return LuaObject()

    def __call__(self, *args):
        ls.push_ref(self._ref)
        for val in args:
            push_key_or_value(val)
        ls.call(len(args), -1)
        returns = []
        while ls.top():
            returns.insert(0, LuaObject())
        if len(returns) == 1:
            return returns[0]
        elif len(returns) > 1:
            return tuple(returns)


# Lua global table
if ls.IN_GMOD:
    ls.push_special(Special.GLOBAL)
    G = LuaObject()
else:
    G = None


def exec(code):
    """Executes the given Lua code block. Returns nothing.

    ::

        code = 'MsgN("test")'
        lua.exec(code)  # 'test' will be printed to the console
    """
    ls.push_special(Special.GLOBAL)

    ls.get_field(-1, 'RunString')
    ls.push_string(code.encode())  # Arg 1: code
    ls.push_string('GPython lua.exec')  # Arg 2: identifier
    ls.push_bool(True)  # Arg 3: throw error if error occurred during code exec

    ls.call(3, 0)  # Call RunString and pop it from the stack

    ls.pop(1)  # GLOBAL


def eval(expr):
    """Evaluates a single Lua expression. Returns :class:`LuaObject` with evaluation result.

    ::

        expr = 'game.SinglePlayer()'  # Returns "true" if the current session is a single player game
        single_player_luaobj = lua.eval(expr)
        # Remember that we need to convert the evaluation result to bool explicitly
        single_player = bool(single_player_luaobj)

        # Now we can use it
        if single_player:
            ...
    """
    ls.push_special(Special.GLOBAL)

    ls.get_field(-1, 'RunString')
    ls.push_string(f'_gpy_temp = {expr}'.encode())  # Assign expression to temporary var _gpy_temp
    ls.push_string('GPython lua.eval')
    ls.push_bool(True)

    ls.call(3, 0)

    # Grabbing the result from _gpy_temp
    ls.get_field(-1, '_gpy_temp')
    obj = LuaObject()

    # Cleaning up: setting _gpy_temp to nil
    ls.push_nil()
    ls.set_field(-2, '_gpy_temp')

    ls.pop(1)  # GLOBAL
    return obj


def table(iterable):
    """Creates and returns a :class:`LuaObject` of a new Lua table from ``iterable``."""
    ls.create_table()
    ls.push_special(Special.GLOBAL)
    ls.get_field(-1, 'table')
    for v in iterable:
        ls.get_field(-1, 'insert')
        ls.push(1)  # Pushing that new table again
        try:
            push_key_or_value(v)
        except TypeError:  # In case of a value that can't be pushed
            ls.clear()
            raise  # Raising TypeError again
        ls.call(2, 0)
    ls.pop(2)  # Pop the 'table' namespace and the global table

    return LuaObject()  # The new table is grabbed and popped by the LuaObject's constructor


class LuaObjectWrapper(ABC):
    """Abstract class for Lua class wrappers, such as :class:`gmod.entity.Entity`.

    Subclasses must implement a ``lua_obj`` property that should return the wrapped :class:`LuaObject`.
    """

    @property
    @abstractmethod
    def lua_obj(self):
        pass
