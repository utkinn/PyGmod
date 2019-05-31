import logging

import pytest

import _luastack
from pygmod import lua

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(autouse=True)
def luastack():
    yield
    _luastack.stack = [_luastack.StackPad()]


def test_auto_pop_from_empty_stack():
    @lua.auto_pop
    def func():
        _luastack.push_nil()
        _luastack.push_nil()

    func()
    assert _luastack.top() == 0


def test_auto_pop_from_non_empty_stack():
    _luastack.push_nil()
    _luastack.push_nil()

    @lua.auto_pop
    def func():
        _luastack.push_nil()
        _luastack.push_nil()

    func()
    assert _luastack.top() == 2


def test_exec_no_error(mocker):
    mocker.patch("pygmod.lua.G")
    lua.G.RunString.return_value = None
    lua.exec_lua("")  # Shouldn't raise LuaError


def test_exec_error(mocker):
    mocker.patch("pygmod.lua.G")
    lua.G.RunString.return_value = "you should not see a LuaError"
    with pytest.raises(lua.LuaError):
        lua.exec_lua("")


@pytest.fixture
def base_get_namespace_instance():
    class A(lua.BaseGetNamespace):
        def __init__(self):
            self.dict = {'a': 1, 'b': 2, 'c': 3}

        def _get(self, item):
            return self.dict[item]

    return A()


def test_base_get_namespace_getitem(base_get_namespace_instance):
    assert base_get_namespace_instance["b"] == 2


def test_base_get_namespace_getitem_missing(base_get_namespace_instance):
    with pytest.raises(KeyError):
        base_get_namespace_instance["no"]


def test_base_get_namespace_getattr(base_get_namespace_instance):
    assert base_get_namespace_instance.b == 2


def test_base_get_namespace_getattr_missing(base_get_namespace_instance):
    with pytest.raises(KeyError):
        base_get_namespace_instance["no"]


def test_base_get_namespace_getattr_underscore(base_get_namespace_instance):
    with pytest.raises(AttributeError):
        base_get_namespace_instance._no


@pytest.fixture
def lua_namespace_instance(mocker):
    class A(lua.LuaNamespace):
        def __init__(self):
            self._set = mocker.Mock()
            self._del = mocker.Mock()
            self._to_delete = 1

        def _push_namespace_object(self):
            _luastack.push_nil()

    return A()


def test_lua_namespace_setattr(lua_namespace_instance):
    lua_namespace_instance.abc = 1
    lua_namespace_instance._set.assert_called_with("abc", 1)
    assert not hasattr(lua_namespace_instance, "_abc")


def test_lua_namespace_setattr_underscore(lua_namespace_instance):
    lua_namespace_instance._abc = 1
    lua_namespace_instance._set.assert_not_called()
    assert getattr(lua_namespace_instance, "_abc") == 1


def test_lua_namespace_delattr(lua_namespace_instance):
    del lua_namespace_instance.abc
    lua_namespace_instance._del.assert_called_with("abc")


def test_lua_namespace_delattr_underscore(lua_namespace_instance):
    del lua_namespace_instance._to_delete
    assert not hasattr(lua_namespace_instance, "_to_delete")


def test_callable_constructor(mocker):
    mock = mocker.Mock()
    _luastack.stack.append(mock)
    func = lua._lua_func_from_stack_top()
    assert mock == _luastack.references[func._LuaObject__ref]


def test_callable_returns_none(mocker):
    def call(*_):
        _luastack.pop(3 + 1)  # Arguments 1, 2, 3 + the function itself

    mocker.patch("_luastack.call", side_effect=call)

    mock = mocker.Mock()
    _luastack.stack.append(mock)
    func = lua._lua_func_from_stack_top()
    returned_value = func(1, 2, 3)
    assert returned_value is None


def test_callable_returns_one_val(mocker):
    def call(*_):
        _luastack.pop(3 + 1)  # Arguments 1, 2, 3 + the function itself
        _luastack.stack.append("returned value")

    mocker.patch("_luastack.call", side_effect=call)

    mock = mocker.Mock()
    _luastack.stack.append(mock)
    func = lua._lua_func_from_stack_top()
    returned_value = func(1, 2, 3)
    assert returned_value == "returned value"


def test_callable_returns_many_vals(mocker):
    def call(*_):
        _luastack.pop(3 + 1)  # Arguments 1, 2, 3 + the function itself
        _luastack.stack.append("returned value 1")
        _luastack.stack.append("returned value 2")

    mocker.patch("_luastack.call", side_effect=call)

    mock = mocker.Mock()
    _luastack.stack.append(mock)
    func = lua._lua_func_from_stack_top()
    returned_value = func(1, 2, 3)
    assert returned_value == ("returned value 1", "returned value 2")


def test_method_call_namespace(mocker):
    mock = mocker.Mock()
    table = {"method": mock}

    class A(lua.MethodCallNamespace):
        # noinspection PyMissingConstructor
        def __init__(self):
            self._tbl = table

    a = A()
    a.method(1, 2, 3)
    mock.assert_called_with(table, 1, 2, 3)
    a["method"]()
    mock.assert_called_with(table)

# TODO: Table tests: iterator classes


def test_table_from_dict():
    d = {"a": 1, "_b": 2, "c": {"d": 0, "e": [1, 2, 3]}}
    tbl = lua.Table(d)
    assert _luastack.references[tbl._LuaObject__ref] == d
