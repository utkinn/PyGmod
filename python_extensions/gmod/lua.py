"""
This module provides tools for Garry's Mod Lua interoperability, for example getting, setting values, indexing tables
and calling functions.
"""

from luastack import *


__all__ = ['G', 'lua_exec', 'lua_eval']


class Reference:
    def __init__(self, ref):
        self._ref = ref

    def __enter__(self):
        push_ref(self._ref)

    def __exit__(self, exc_type, exc_value, traceback):
        pop(1)


class LuaObject:
    def __init__(self):
        self._ref = create_ref()
        self._context = Reference(self._ref)

    def __del__(self):
        free_ref(self._ref)

    @property
    def type(self):
        with self._context:
            return get_type(-1)

    @property
    def type_name(self):
        with self._context:
            return get_type_name(get_type(-1))

    def __str__(self):
        with self._context:
            return get_string(-1)

    def __int__(self):
        with self._context:
            return int(get_number(-1))

    def __float__(self):
        with self._context:
            return float(get_number(-1))

    def __bool__(self):
        with self._context:
            return get_bool(-1)

    def _push_key_or_value(self, key_or_value):
        if key_or_value is None:
            push_nil()
        if isinstance(key_or_value, int) or isinstance(key_or_value, float):
            push_number(key_or_value)
        elif isinstance(key_or_value, LuaObject):
            push_ref(key_or_value._ref)
        elif isinstance(key_or_value, str):
            push_string(key_or_value.encode())
        elif isinstance(key_or_value, bytes):
            push_string(key_or_value)
        elif isinstance(key_or_value, bool):
            push_bool(key_or_value)
        else:
            raise TypeError(f'unsupported key/value type: {type(key_or_value)}')

    def __setitem__(self, key, value):
        with self._context:
            self._push_key_or_value(key)
            self._push_key_or_value(value)
            set_table(-3)

    def __getitem__(self, key):
        with self._context:
            self._push_key_or_value(key)
            get_table(-2)
            return LuaObject()

    def __call__(self, *args):
        push_ref(self._ref)
        for val in args:
            self._push_key_or_value(val)
        call(len(args), -1)
        returns = []
        while top():
            returns.insert(0, LuaObject())
        if len(returns) == 1:
            return returns[0]
        elif len(returns) > 1:
            return tuple(returns)


push_special(Special.GLOBAL)
G = LuaObject()


def lua_exec(code):
    """Executes the given Lua code block. Returns nothing.

    ::

        code = 'MsgN("test")'
        lua_exec(code)  # 'test' will be printed to the console
    """
    push_special(Special.GLOBAL)

    get_field(-1, 'RunString')
    push_string(code.encode())  # Arg 1: code
    push_string('GPython lua_exec')  # Arg 2: identifier
    push_bool(True)  # Arg 3: throw error if error occurred during code exec

    call(3, 0) # Call RunString and pop it from the stack

    pop(1)  # GLOBAL


def lua_eval(expr):
    """Evaluates a single Lua expression. Returns :class:`LuaObject` with evaluation result.

    ::

        expr = 'game.SinglePlayer()'  # Returns "true" if the current session is a single player game
        single_player_luaobj = lua_eval(expr)
        # Remember that we need to convert the evaluation result to bool explicitly
        single_player = bool(single_player_luaobj)

        # Now we can use it
        if single_player:
            ...
    """
    push_special(Special.GLOBAL)

    get_field(-1, 'RunString')
    push_string(f'_gpy_temp = {expr}'.encode())  # Assign expression to temporary var _gpy_temp
    push_string('GPython lua_eval')
    push_bool(True)

    call(3, 0)

    # Grabbing the result from _gpy_temp
    get_field(-1, '_gpy_temp')
    obj = LuaObject()

    # Cleaning up: setting _gpy_temp to nil
    push_nil()
    set_field(-2, '_gpy_temp')

    pop(1)  # GLOBAL
    return obj
