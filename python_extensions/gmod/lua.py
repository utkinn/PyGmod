from .luastack import *


__all__ = ['G']


class Reference:
    def __init__(self, ref):
        self._ref = ref

    def __enter__(self):
        push_ref(self._ref)

    def __exit__(self):
        pop(1)


class LuaObject:
    def __init__(self):
        self._ref = create_ref()
        self._context = _Reference(self._ref)

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

    def _push_kv(self, kv, s):
        if value is None:
            push_nil()
        if isinstance(key, int) or isinstance(key, float):
            push_number(key)
        elif isinstance(value, LuaObject):
            push_ref(value._ref)
        elif isinstance(value, str):
            push_string(value.encode())
        elif isinstance(value, bytes):
            push_string(value)
        elif isinstance(value, bool):
            push_bool(value)
        else:
            raise KeyError(f'unsupported {s} type: {type(key)}')

    def _push_key(self, key):
        self._push_kv(key, 'key')

    def _push_value(self, value):
        self._push_kv(value, 'value')

    def __setitem__(self, key, value):
        with self._context:
            self._push_key(key)
            self._push_value(value)
            set_table(-3)

    def __getitem__(self, key):
        with self._context:
            self._push_key(key)
            get_table(-2)
            return LuaObject()


push_special(Special.GLOBAL)
G = LuaObject()
