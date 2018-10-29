"""
This module provides tools for Garry's Mod Lua interoperability, for example getting, setting values, indexing tables
and calling functions.
"""

from abc import ABC, abstractmethod
from numbers import Number

from luastack import LuaStack, Special, IN_GMOD, ValueType

__all__ = ['G', 'exec', 'eval', 'table', 'LuaObjectWrapper']

ls = LuaStack()


class Reference:
    def __init__(self, ref):
        self.ref = int(ref)

    def __enter__(self):
        ls.push_ref(self.ref)

    def __exit__(self, exc_type, exc_value, traceback):
        ls.pop(1)


def push_pyval_to_stack(val):
    """Converts a Python value to a Lua value and pushes it to the Lua stack.

    Supported types:

    ==============================  ========================================================
            Python type                                      Lua type
    ==============================  ========================================================
    ``None``                        ``nil``
    Any number                      number
    :class:`LuaObject`              Whatever ``LuaObject.ref`` is pointing to
    :class:`str`, :class:`bytes`    string
    :class:`bool`                   bool
    :class:`LuaObjectWrapper`       Whatever ``LuaObjectWrapper.lua_obj.ref is pointing to
    """
    if val is None:
        ls.push_nil()
    if isinstance(val, Number):
        ls.push_number(val)
    elif isinstance(val, LuaObject):
        ls.push_ref(val.ref)
    elif isinstance(val, str):
        ls.push_string(val.encode())
    elif isinstance(val, bytes):
        ls.push_string(val)
    elif isinstance(val, bool):
        ls.push_bool(val)
    elif isinstance(val, LuaObjectWrapper):
        ls.push_ref(val.lua_obj.ref)
    else:
        raise TypeError(f'unsupported value type: {type(val)}')


class LuaObject:
    def __init__(self):
        """Creates a :class:`LuaObject` which points to the topmost stack value and pops it."""
        self.ref = ls.create_ref()
        self._context = Reference(self.ref)

    def __del__(self):
        ls.free_ref(self.ref)

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

    def __bytes__(self):
        if self.type == ValueType.NIL:
            return 'None'

        with self._context:
            val = ls.get_string(-1)
            if val is None:
                raise ValueError("can't convert this value to str/bytes")
            return val

    def __str__(self):
        return str(bytes(self))

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
        if self.type == ValueType.NIL:
            raise ValueError("can't index nil")

        with self._context:
            push_pyval_to_stack(key)
            push_pyval_to_stack(value)
            ls.set_table(-3)

    def __getitem__(self, key):
        if self.type == ValueType.NIL:
            raise ValueError("can't index nil")

        with self._context:
            push_pyval_to_stack(key)
            ls.get_table(-2)
            return LuaObject()

    def __call__(self, *args):
        if self.type == ValueType.NIL:
            raise ValueError("can't call nil")

        ls.push_ref(self.ref)
        for val in args:
            push_pyval_to_stack(val)
        ls.call(len(args), -1)
        returns = []
        while ls.top() > 1:
            returns.insert(0, LuaObject())
        if len(returns) == 1:
            return returns[0]
        elif len(returns) > 1:
            return tuple(returns)

    def __repr__(self):
        return f'<LuaObject (type={str(self.type_name)!s})>'


# Lua global table
if IN_GMOD:
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
    if not isinstance(code, str):
        raise TypeError('code must be str, not ' + type(code).__name__)

    ls.push_special(Special.GLOBAL)

    ls.get_field(-1, b'RunString')
    ls.push_string(code.encode())  # Arg 1: code
    ls.push_string(b'GPython lua.exec')  # Arg 2: identifier
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
    if not isinstance(expr, str):
        raise TypeError('expr must be str, not ' + type(expr).__name__)

    ls.push_special(Special.GLOBAL)

    ls.get_field(-1, b'RunString')
    ls.push_string(f'_gpy_temp = {expr}'.encode())  # Assign expression to a temporary variable "_gpy_temp"
    ls.push_string(b'GPython lua.eval')
    ls.push_bool(True)

    ls.call(3, 0)

    # Grabbing the result from _gpy_temp
    ls.get_field(-1, b'_gpy_temp')
    obj = LuaObject()

    # Cleaning up: setting _gpy_temp to nil
    ls.push_nil()
    ls.set_field(-2, b'_gpy_temp')

    ls.pop(1)  # GLOBAL
    return obj


def table(iterable):
    """Creates and returns a :class:`LuaObject` of a new Lua table from ``iterable``."""
    ls.clear()  # Everything might go wrong if the stack is not empty

    ls.create_table()
    ls.push_special(Special.GLOBAL)
    ls.get_field(-1, b'table')
    for v in iterable:
        ls.get_field(-1, b'insert')
        ls.push(1)  # Pushing that new table again
        try:
            push_pyval_to_stack(v)
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
