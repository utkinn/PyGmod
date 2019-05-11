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
    return G._pygmod_eval_result


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
    def _get(self, name):
        pass

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
        pass

    # Value getting

    @auto_pop
    def _get(self, name):
        self._push_namespace_object()
        _luastack.get_field(-1, name)
        return _luastack.get_stack_val_as_python_obj()

    # Value setting

    @auto_pop
    def _set(self, name, value):
        self._push_namespace_object()
        _luastack.push_python_obj(value)
        _luastack.set_field(-2, name)

    def __setitem__(self, index, value):
        self._set(index, value)

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            super().__setattr__(attr, value)
            return

        self._set(attr, value)

    # Value deleting

    @auto_pop
    def _del(self, name):
        self._push_namespace_object()
        _luastack.push_nil()
        _luastack.set_field(-2, name)

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

    def _push_namespace_object(self):
        _luastack.push_globals()


G = Globals()


class LuaObject:
    """Base class for all Lua object classes."""

    def __init__(self, ref):
        self.__ref = ref

    def __del__(self):
        _luastack.reference_free(self.__ref)


class Callable(LuaObject):
    """
    Base class for callable Lua objects, such as functions and tables with
    ``__call`` metamethod.
    """

    @auto_pop
    def __call__(self, *args):
        # Saving the quantity of stack values before calling the function
        vals_in_stack_before_call = _luastack.top()

        # Pushing the function
        _luastack.reference_push(self._LuaObject__ref)
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
        else:  # Many values - putting them all in a tuple and returning it
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

    def __init__(self, tbl):
        self._tbl = tbl

    def _get(self, name):
        return partial(self._tbl[name], self._tbl)


class Table(Callable, LuaNamespace):
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
            _luastack.create_table()
            LuaObject.__init__(self, _luastack.reference_create())
        elif isinstance(ref_or_iterable, int):  # Wrapping a Lua table
            LuaObject.__init__(self, ref_or_iterable)
        elif isinstance(ref_or_iterable, Mapping):  # Converting a dict
            self.__init__()
            for k, v in ref_or_iterable.items():
                self[k] = v
        elif isinstance(ref_or_iterable, Iterable):  # Converting an iterable
            self.__init__()
            for v in ref_or_iterable:
                # noinspection PyMethodFirstArgAssignment
                self += v
        else:
            raise ValueError(f'unknown constructor argument type: '
                             '{type(ref_or_iterable).__name__}')

        self._ = MethodCallNamespace(self)

    def _push_namespace_object(self):
        _luastack.reference_push(self._LuaObject__ref)

    # def __iadd__(self, value):  # TODO
    #     ...

    def __call__(self, *args):
        if G.getmetatable(self)["__call"] is None:
            raise ValueError("this table's metatable "
                             "does not have __call method")

        super().__call__(*args)

    # Iteration

    def __iter__(self):
        return TableKeyIterator(self)

    def keys(self):
        """Returns a key iterator for this table. Same as ``iter(table)``."""
        return iter(self)

    def values(self):
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
    @auto_pop
    def __next__(self):
        super().__next__()
        return self._previous_key


class TableValueIterator(TableBaseIterator):
    @auto_pop
    def __next__(self):
        super().__next__()
        return _luastack.get_stack_val_as_python_obj()


class TableItemIterator(TableBaseIterator):
    @auto_pop
    def __next__(self):
        super().__next__()
        return self._previous_key, _luastack.get_stack_val_as_python_obj()


def _table_from_stack_top():
    ref = _luastack.reference_create()
    table = Table(ref)
    # This function is called from _luastack.get_stack_val_as_python_obj().
    # _luastack.get_stack_val_as_python_obj() shouldn't modify the stack,
    # but _luastack.reference_create() pops the referenced object.
    # We have to manually push that object back.
    _luastack.reference_push(ref)
    return table


def _lua_func_from_stack_top():
    ref = _luastack.reference_create()
    func = Callable(ref)
    # This function is called from _luastack.get_stack_val_as_python_obj().
    # _luastack.get_stack_val_as_python_obj() shouldn't modify the stack,
    # but _luastack.reference_create() pops the referenced object.
    # We have to manually push that object back.
    _luastack.reference_push(ref)
    return func
