"""
This module provides the access to Lua environment. You can use it for getting and setting arbitrary variables,
calling available Garry's Mod Lua functions and manipulating and creating tables and objects.
"""

from abc import ABC, abstractmethod
from numbers import Number
from collections.abc import Iterable

# noinspection PyUnresolvedReferences
from luastack import LuaStack, Special, IN_GMOD, ValueType

__all__ = ['G', 'exec', 'eval', 'table', 'LuaObject', 'LuaObjectWrapper', 'pairs', 'luafunction']

ls = LuaStack()


class Reference:
    """Context manager that pushes a reference on enter and pops it on exit."""

    def __init__(self, ref):
        self.ref = int(ref)

    def __enter__(self):
        ls.push_ref(self.ref)

    def __exit__(self, exc_type, exc_value, traceback):
        ls.pop(1)


def can_push(o):
    """Returns ``True`` if ``o`` can be pushed to the Lua stack."""
    return o is None or isinstance(o, (Number, LuaObject, str, bytes, bool, LuaObjectWrapper, Iterable))


def check_pushable(o):
    """Raises :class:`TypeError` if ``o`` isn't pushable to the Lua stack."""
    if not can_push(o):
        raise TypeError(f'unsupported value type: type - {type(o).__name__!r}, value - {o!r}')


def push_pyval_to_stack(val):
    """Converts a Python value to a Lua value and pushes it to the Lua stack.

    Supported types:

    ==============================  ========================================================
            Python type                                      Lua type
    ==============================  ========================================================
    ``None``                        ``nil``
    Any number                      number
    :class:`LuaObject`              Whatever ``LuaObject._ref_`` is pointing to
    :class:`str`, :class:`bytes`    string
    :class:`bool`                   bool
    :class:`LuaObjectWrapper`       Whatever ``LuaObjectWrapper.lua_obj._ref_ is pointing to
    :class:`Iterable`               Table
    """
    check_pushable(val)

    if val is None:
        ls.push_nil()
    if isinstance(val, Number):
        ls.push_number(val)
    elif isinstance(val, LuaObject):
        ls.push_ref(val._ref_)
    elif isinstance(val, str):
        ls.push_string(val.encode())
    elif isinstance(val, bytes):
        ls.push_string(val)
    elif isinstance(val, bool):
        ls.push_bool(val)
    elif isinstance(val, LuaObjectWrapper):
        ls.push_ref(val.lua_obj._ref_)
    elif isinstance(val, Iterable):
        # noinspection PyTypeChecker
        push_pyval_to_stack(table(val))


class SelfCallingNamespace:
    """Namespace which gives :class:`SelfCallingFunction`\\ s when indexed.

    >>> ply = Player(1)
    >>> ply._
    <SelfCallingNamespace (target=<LuaObject (type=entity)>)>
    >>> ply._.Nick
    <SelfCallingFunction 'Nick' (target=<LuaObject (type=entity)>)>
    """

    def __init__(self, lo):
        self._luaobj = lo

    def _get(self, item):
        return SelfCallingFunction(self._luaobj, self._luaobj._get(item), item)

    def __getitem__(self, item):
        return self._get(item)

    def __getattr__(self, item):
        return self._get(item)

    def __repr__(self):
        return f'<SelfCallingNamespace (target={self._luaobj!r})>'


class SelfCallingFunction:
    """Wrapper of Lua function which calls it with self (same purpose as colon in Lua has).

    >>> ply = Player(1)
    >>> ply._.Nick()  # Same as "ply:Nick()" in Lua
    """

    def __init__(self, obj, func, funcname):
        self._obj = obj
        self._func = func
        self._funcname = funcname

    def __call__(self, *args, _autoconvert_=True, **kwargs):
        return self._func(self._obj, *args, _autoconvert_)

    def __repr__(self):
        return f'<SelfCallingFunction {self._funcname!r} (target={self._obj!r}, func={self._func!r})>'


class LuaObject:
    def __init__(self):
        """Creates a :class:`LuaObject` which points to the topmost stack value and pops it."""
        self._ref_ = ls.create_ref()
        self._context_ = Reference(self._ref_)

    def __del__(self):
        ls.free_ref(self._ref_)

    @property
    def _type_(self):
        """Returns the :class:`luastack.ValueType` of the held value."""
        with self._context_:
            return ls.get_type(-1)

    @property
    def _type_name_(self):
        """Returns the :class:`str` type representation of the held value."""
        with self._context_:
            return ls.get_type_name(ls.get_type(-1)).decode()

    @property
    def _(self):
        return SelfCallingNamespace(self)

    def _autoconvert_to_py(self):
        """Tries to convert itself to an appropriate Python type. Returns self if conversion is not possible."""

        # Convertable Lua types and corresponding conversion functions
        types_and_converters = {
            ValueType.NIL: lambda _: None,
            ValueType.BOOL: bool,
            ValueType.NUMBER: float,
            ValueType.STRING: str
        }

        if self._type_ in types_and_converters:
            # Convert self using the conversion func which corresponds to the Lua type of self.
            return types_and_converters[self._type_](self)
        else:
            return self

    # noinspection PyUnusedLocal
    def _table_to_str(self):
        keys_and_vals = {}

        next_ = G.pairs(self)[0]  # Retrieving the pairs iterator function

        t = self  # Table that we iterate
        k = None  # Current key
        v = None  # Current value

        pair = next_(t, None)  # Getting the first pair

        while pair:  # next() returns nil when there is no pairs left
            k, v = pair  # Unpacking the pair
            keys_and_vals[k] = v

            pair = next_(t, k)  # Getting the next pair

        return repr(keys_and_vals)

    def _convert_to_byte_or_str(self):
        if self._type_ == ValueType.NIL:
            return 'None'
        elif self._type_ == ValueType.STRING:
            with self._context_:
                val = ls.get_string(-1)
                if val is None:
                    raise ValueError("can't convert this value to str/bytes")
                return val
        elif self._type_ == ValueType.TABLE:
            return self._table_to_str()
        else:
            with self._context_:
                return G.tostring(self)[1]

    def __str__(self):
        val = self._convert_to_byte_or_str()
        if isinstance(val, str):
            return val
        else:  # val is bytes object
            return val.decode()

    def __bytes__(self):
        val = self._convert_to_byte_or_str()
        if isinstance(val, bytes):
            return val
        else:  # val is str object
            return val.encode()

    def __int__(self):
        with self._context_:
            return int(ls.get_number(-1))

    def __float__(self):
        with self._context_:
            return float(ls.get_number(-1))

    def __bool__(self):
        with self._context_:
            return ls.get_bool(-1)

    def _get(self, key):
        if self._type_ == ValueType.NIL:
            raise ValueError("can't index nil")

        with self._context_:
            push_pyval_to_stack(key)
            ls.get_table(-2)
            return LuaObject()

    def __getitem__(self, key):
        return self._get(key)

    def __getattr__(self, item):
        return self._get(item)

    def _set(self, key, value):
        if self._type_ == ValueType.NIL:
            raise ValueError("can't index nil")

        with self._context_:
            push_pyval_to_stack(key)
            push_pyval_to_stack(value)
            ls.set_table(-3)

    def __setitem__(self, key, value):
        self._set(key, value)

    def __setattr__(self, key, value):
        if key.startswith('_') and key.endswith('_'):
            super().__setattr__(key, value)
        else:
            self._set(key, value)

    def __call__(self, *args, _autoconvert_=True):
        if self._type_ == ValueType.NIL:
            raise ValueError("can't call nil")

        for o in args:
            check_pushable(o)

        ls.push_ref(self._ref_)
        for val in args:
            push_pyval_to_stack(val)
        ls.call(len(args), -1)

        returns = []
        while ls.top() > 1:
            returns.insert(0, LuaObject())

        if len(returns) == 1:
            if _autoconvert_:
                return returns[0]._autoconvert_to_py()
            else:
                return returns[0]
        elif len(returns) > 1:
            if _autoconvert_:
                return tuple((o._autoconvert_to_py() for o in returns))
            else:
                return tuple(returns)

    def __repr__(self):
        return f'<LuaObject: {self!s}>'


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


def eval(expr, *, autoconvert=True):
    """Evaluates a single Lua expression. Returns a :class:`LuaObject` with an evaluation result.
    If ``autoconvert`` is ``True``, tries to convert primitive Lua types to Python analogues.

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

    if autoconvert:
        return obj._autoconvert_to_py()
    else:
        return obj


def iter_to_dict(iterable):
    """Converts an iterable to a Lua Table-like dictionary.

    >>> iter_to_dict({'a': 1})
    {'a': 1}
    >>> iter_to_dict([1, 2, 'a'])
    {1: 1, 2: 2, 3: 'a'}
    """
    if isinstance(iterable, dict):
        return iterable
    else:
        as_tuple = tuple(iterable)
        return {i + 1: as_tuple[i] for i in range(0, len(as_tuple))}


def table(iterable: Iterable = None):
    """Creates and returns a :class:`LuaObject` of a new Lua table from ``iterable`` (empty by default).

    ::

        tbl = lua.table((1, 2, 3))
        lua.G.PrintTable(tbl)
        # 1 = 1
        # 2 = 2
        # 3 = 3

        tbl = lua.table({'a': 1, 2: 'b', 1: {1, 2, 3}})
        lua.G.PrintTable(tbl)
        # 1:
        #   1 = 1
        #   2 = 2
        #   3 = 3
        # 2 = b
        # a = 1
    """

    if not isinstance(iterable, Iterable):
        raise TypeError(f'iterable must be actually iterable, not {type(iterable).__name__!r}')

    if iterable is None:
        iterable = {}
    else:
        iterable = iter_to_dict(iterable)

    tbl = eval('{}')
    for k, v in iterable.items():
        tbl[k] = v
    return tbl


def pairs(tbl):
    """Works the same as ``pairs()`` in Lua.

    >>> tbl = table(('a', 'b', 'c'))
    >>> for k, v in pairs(tbl):
    ...     print(k, '-', v)
    ...
    1 - a
    2 - b
    3 - c
    """
    if isinstance(tbl, LuaObject):
        if tbl._type_ != ValueType.TABLE:
            raise ValueError(f'this LuaObject is not a table, but {tbl._type_name_}, repr: {tbl!r}')

        def pairs_generator():
            next_ = G.pairs(tbl)[0]  # Retrieving the pairs iterator function

            t = tbl  # Table that we iterate
            k = None  # Current key

            pair = next_(t, None)  # Getting the first pair

            while pair:  # next() returns nil when there is no pairs left
                yield pair
                pair = next_(t, k)  # Getting the next pair

        return pairs_generator

    elif isinstance(tbl, Iterable):
        return iter_to_dict(tbl).items()
    else:
        raise TypeError(f'unsupported type: {type(tbl).__name__!r}')


lua_functions = {}


def luafunction(pyfunction):
    """Creates a Lua function out of a Python function.

    >>> @luafunction
    ... def noclip_log(ply, noclip):
    ...     print(ply._.Nick(), 'changed noclip state to', noclip)
    ...
    >>> hook.Add('PlayerNoClip', 'noclip_log', noclip_log)
    """

    func_id = pyfunction.__module__ + '.' + pyfunction.__name__

    # Backing function which calls pyfunction and receives the return values.
    passer = eval(f'''
    function(...)
        py._func_in = {{...}}
        py._func_in_n = #py._func_in
        
        if CLIENT then
            py._SwitchToClient()
        else
            py._SwitchToServer()
        end
        
        py.Exec("from gmod import lua; lua.pass_call({func_id!r})")
        
        return py._func_rtn
    end
    ''')

    lua_functions[func_id] = pyfunction

    return passer


def pass_call(func_id):
    """Called in Lua by a backing function when it called. "Passes" the call, args, and gives the return values back."""
    pyfunc = lua_functions[func_id]

    args_table = G.py._func_in
    n_args = int(G.py._func_in_n)

    args = [args_table[i] for i in range(1, n_args + 1)]

    G.py._func_rtn = pyfunc(*args)


class LuaObjectWrapper(ABC):
    """Abstract class for Lua class wrappers, such as :class:`gmod.entity.Entity`.
    Subclasses of ``LuaObjectWrapper`` can be used in :class:`LuaObject` calls and :const:`G` indexing operations.

    Subclasses must implement a ``lua_obj`` property that should return the wrapped :class:`LuaObject`.
    """

    @property
    @abstractmethod
    def lua_obj(self):
        pass
