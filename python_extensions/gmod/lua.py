from .luastack import *


__all__ = ['G']


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

    def _push_kv(self, kv, s):
        if kv is None:
            push_nil()
        if isinstance(kv, int) or isinstance(kv, float):
            push_number(kv)
        elif isinstance(kv, LuaObject):
            push_ref(kv._ref)
        elif isinstance(kv, str):
            push_string(kv.encode())
        elif isinstance(kv, bytes):
            push_string(kv)
        elif isinstance(kv, bool):
            push_bool(kv)
        else:
            raise kvError(f'unsupported {s} type: {type(kv)}')

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

    def __call__(self, *args):
        push_ref(self._ref)
        for val in args:
            self._push_value(val)
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
