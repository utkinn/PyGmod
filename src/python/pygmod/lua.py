"""
Access to the Lua environment. Can be used for getting and setting arbitrary variables,
calling Lua functions and manipulating tables and objects.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from functools import wraps, partial

import _luastack

__all__ = ["LuaError", "exec_lua", "eval_lua", "G", "Table"]


def auto_pop(func):
    """
    Decorator which automatically pops all Lua stack values
    which were pushed during the wrapped function execution.
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        # Number of values in the stack before calling the function
        values_before = _luastack.top()
        try:
            rtn = func(*args, **kwargs)
        finally:
            # Number of values in the stack after calling the function
            values_after = _luastack.top()
            # How much values we have to pop
            values_to_pop = values_after - values_before
            _luastack.pop(values_to_pop)
        return rtn

    return decorated


class LuaError(Exception):
    """Raised when a Lua error occurs while running some Lua code in Python."""


def exec_lua(lua_code):
    """Runs a string of Lua code."""
    error = G.RunString(lua_code, '<pygmod lua_exec()>', False)
    if error is not None:
        raise LuaError(error)


def eval_lua(lua_code):
    """Evaluates a Lua expression and returns the result."""
    exec_lua('_pygmod_eval_result = ' + lua_code)
    return G["_pygmod_eval_result"]


class BaseGetNamespace(ABC):
    """
    Abstract namespace class which supports reading abstract methods by
    accessing attributes and items
    (with ``__getitem__()`` and ``__getattr__()``).

    >>> class A(BaseGetNamespace):
    ...     def __init__(self):
    ...         self.dict = {'a': 1, 'b': 2, 'c': 3}
    ...     def _get(self, item):
    ...         return self.dict[item]
    ...
    >>> a = A()
    >>> a['b']
    2
    >>> a.c
    3
    >>> a['a'] is a.a
    True

    .. note::

        Members whose names start with ``_``
        should be accessed with the subscription syntax::

            namespace['_foo']
    """

    @abstractmethod
    def _get(self, key):
        """Gets the value by key ``key``."""

    def __getitem__(self, index):
        return self._get(index)

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return super().__getattribute__(attr)
        return self._get(attr)


class LuaNamespace(BaseGetNamespace):
    """
    Base class for Lua object classes
    with member manipulation features, such as getting and setting.

    .. note::

        Members whose names start with ``_``
        should be accessed with the subscription syntax::

            Globals()['_foo']
    """

    @abstractmethod
    def _push_namespace_object(self):
        """Should push a Lua object which members will be manipulated."""

    # Value getting

    @auto_pop
    def _get(self, key):
        self._push_namespace_object()
        _luastack.push_python_obj(key)
        _luastack.get_table(-2)
        return _luastack.get_stack_val_as_python_obj()

    # Value setting

    @auto_pop
    def _set(self, key, value):
        """Assigns the value ``value`` to the key ``key`` for the underlying table or userdata."""
        self._push_namespace_object()
        _luastack.push_python_obj(key)
        _luastack.push_python_obj(value)
        _luastack.set_table(-3)

    def __setitem__(self, index, value):
        self._set(index, value)

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            super().__setattr__(attr, value)
            return

        self._set(attr, value)

    # Value deleting

    @auto_pop
    def _del(self, key):
        """Same as ``LuaNamespace._set(key, None)``."""
        self._push_namespace_object()
        _luastack.push_python_obj(key)
        _luastack.push_nil()
        _luastack.set_table(-3)

    def __delitem__(self, key):
        self._del(key)

    def __delattr__(self, attr):
        if attr.startswith('_'):
            super().__delattr__(attr)
        else:
            self._del(attr)


class Globals(LuaNamespace):
    """Lua global namespace. Same as ``_G`` in Lua.

    .. note::

        Members whose names start with ``_``
        should be accessed with the subscription syntax::

            # Won't work
            G._foo
            # Will work
            G['_foo']
    """

    # pylint: disable=too-few-public-methods

    def _push_namespace_object(self):
        _luastack.push_globals()


G = Globals()


class LuaObject:
    """Base class for all Lua object classes."""

    # pylint: disable=too-few-public-methods

    def __init__(self, ref):
        self._ref = ref

    def __del__(self):
        _luastack.reference_free(self._ref)


class CallableLuaObject(LuaObject):
    """
    Class for callable Lua objects, such as functions and tables with
    ``__call`` metamethod.
    """

    # pylint: disable=too-few-public-methods

    @auto_pop
    def __call__(self, *args):
        # Saving the quantity of stack values before calling the function
        vals_in_stack_before_call = _luastack.top()

        # Pushing the function
        _luastack.reference_push(self._ref)
        # Pushing the arguments
        for arg in args:
            _luastack.push_python_obj(arg)
        # Calling the function
        _luastack.call(len(args), -1)

        # How much values did the function return
        values_returned = _luastack.top() - vals_in_stack_before_call
        if values_returned == 0:  # Function returned nothing; returning None
            return None
        if values_returned == 1:  # One value - just returning it
            return _luastack.get_stack_val_as_python_obj()
        # Many values - putting them all in a tuple and returning it
        return tuple(_luastack.get_stack_val_as_python_obj(i)
                     for i in
                     range(vals_in_stack_before_call + 1, _luastack.top() + 1))


class MethodCallNamespace(BaseGetNamespace):
    """
    Helper object for making method calls.
    Acts as a colon operator in Lua.

    >>> ply = Globals().Player(1)
    >>> ply._.Health()
    100
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, tbl):
        self._tbl = tbl

    def _get(self, key):
        return partial(self._tbl[key], self._tbl)


class Table(CallableLuaObject, LuaNamespace):
    """Class for representing Lua tables.

    :class:`Table` has a multifunctional constructor::

        # Creating an empty table
        t = Table()

        # Converting a dict to a table
        d = {'a': 1, 'b': 2}
        t = Table(d)

        # Converting an iterable to a table
        i = [1, 2, 3]
        t = Table(i)

    .. note::

        Members whose names start with ``_``
        should be accessed with the subscription syntax::

            # Won't work
            Table({"_foo": 1})._foo
            # Will work
            Table({"_foo": 1})['_foo']
    """

    def __init__(self, ref_or_iterable=None):
        if ref_or_iterable is None:  # Creating a new table
            self._init_empty_table()
        elif isinstance(ref_or_iterable, int):  # Wrapping a Lua table
            CallableLuaObject.__init__(self, ref_or_iterable)
        elif isinstance(ref_or_iterable, Mapping):  # Converting a dict
            self._init_empty_table()
            for key, value in ref_or_iterable.items():
                self[key] = value
        elif isinstance(ref_or_iterable, Iterable):  # Converting an iterable
            self._init_empty_table()
            for value in ref_or_iterable:
                # noinspection PyMethodFirstArgAssignment
                self += value
        else:
            raise ValueError(f'unknown constructor argument type: '
                             '{type(ref_or_iterable).__name__}')

        self._ = MethodCallNamespace(self)

    def _init_empty_table(self):
        """Creates an empty table in the Lua stack and wraps it in this :class:`Table` instance."""
        _luastack.create_table()
        super().__init__(_luastack.reference_create())

    def _push_namespace_object(self):
        _luastack.reference_push(self._ref)

    def __iadd__(self, value):
        G.table.insert(self, value)
        return self

    def __call__(self, *args):
        if G.getmetatable(self)["__call"] is None:
            raise ValueError("this table's metatable "
                             "does not have __call method")

        super().__call__(*args)

    def __len__(self):
        # ILuaBase doesn't feature a C++ way to retrieve the length of a table,
        # so we have to be creative.
        return eval_lua("function(tbl) return #tbl end")(self)

    # Iteration

    def __iter__(self):
        return TableKeyIterator(self)

    def keys(self):
        """Returns a key iterator for this table. Same as ``iter(table)``."""
        return iter(self)

    def values(self):
        """Returns a value iterator for this table."""
        return TableValueIterator(self)

    def items(self):
        """
        Returns an item iterator for this table.
        Item is a key-value pair.
        """
        return TableItemIterator(self)

    def __dict__(self):
        """
        Returns this table as a :class:`dict`.
        Equivalent to ``dict(table.items())``.
        """
        return dict(self.items())


class TableBaseIterator(ABC):
    """Base class for table iterators."""

    # pylint: disable=too-few-public-methods

    def __init__(self, table):
        self._table = table
        self._previous_key = None

    @abstractmethod
    def __next__(self):
        _luastack.push_python_obj(self._table)
        _luastack.push_python_obj(self._previous_key)

        iteration_is_not_over = _luastack.next(-2)
        # _luastack.next() == 0 means the iteration end
        if not iteration_is_not_over:
            raise StopIteration

        self._previous_key = _luastack.get_stack_val_as_python_obj(-2)

        # Returning something in overridden methods...


class TableKeyIterator(TableBaseIterator):
    """Iterator of table keys."""

    # pylint: disable=too-few-public-methods

    @auto_pop
    def __next__(self):
        super().__next__()
        return self._previous_key


class TableValueIterator(TableBaseIterator):
    """Iterator of table values."""

    # pylint: disable=too-few-public-methods

    @auto_pop
    def __next__(self):
        super().__next__()
        return _luastack.get_stack_val_as_python_obj()


class TableItemIterator(TableBaseIterator):
    """Iterator of table key-value pairs."""

    # pylint: disable=too-few-public-methods

    @auto_pop
    def __next__(self):
        super().__next__()
        return self._previous_key, _luastack.get_stack_val_as_python_obj()


def _table_from_stack(stack_index):
    """Wraps a table at the Lua stack index ``stack_index`` in a :class:`Table` instance."""
    _luastack.push(stack_index)
    ref = _luastack.reference_create()
    table = Table(ref)
    return table


def _lua_func_from_stack(stack_index):
    """
    Wraps a function at the Lua stack index ``stack_index``
    in a :class:`CallableLuaObject` instance.
    """
    _luastack.push(stack_index)
    ref = _luastack.reference_create()
    func = CallableLuaObject(ref)
    return func
