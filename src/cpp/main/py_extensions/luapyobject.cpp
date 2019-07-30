#include <string>
#include <Python.h>
#include "luapyobject.hpp"
#include "stack_utils.hpp"
#include "../realms.hpp"

#define LUA_FUNC(name) static int name(lua_State *state)

LUA_FUNC(luapycallable_call) {
	switchToCurrentRealm(state);

	// Getting the function PyObject
	UserData *ud = reinterpret_cast<UserData *>(LUA->GetUserdata(1));
	PyObject *func = reinterpret_cast<PyObject *>(ud->data);

	if (!PyCallable_Check(func)) {
		LUA->ArgError(1, "this Python object is not callable");
		LUA->Pop(LUA->Top());
		return 0;
	}

	int nArgs = LUA->Top() - 1;  // -1 because the userdata itself is also pushed as the first argument. The rest are the call arguments.
	PyObject *argsTuple = PyTuple_New(nArgs);  // Creating a tuple for arguments
	for (int i = 2; i <= LUA->Top(); i++) {  // Filling the tuple with arguments
		PyTuple_SetItem(argsTuple, i - 2, getStackValAsPythonObj(LUA, i));
	}
	PyObject *result = PyObject_CallObject(func, argsTuple);  // Calling the function
	if (result == NULL) {  // If result == NULL, func has thrown an exception
		PyErr_Print();
		Py_DECREF(argsTuple);
		LUA->ThrowError("Exception in Python function");
		return 0;
	}
	pushPythonObj(LUA, result);  // Pushing the result to the stack

	Py_DECREF(argsTuple);
	Py_DECREF(result);
	return 1;
}

LUA_FUNC(luapyobject_index) {
    switchToCurrentRealm(state);

    PyObject *self = getStackValAsPythonObj(LUA, 1);
    PyObject *attr = getStackValAsPythonObj(LUA, 2);

    PyObject *val = PyObject_GetAttr(self, attr);
    if (val == NULL) {
        PyObject *valReprPy = PyObject_Repr(val);
        std::string valRepr = PyUnicode_AsUTF8(valReprPy);
        PyErr_Print();
        LUA->ThrowError(("__getattribute__ failed, probably there is no such item: " + valRepr).c_str());
        Py_DECREF(valReprPy);
        Py_DECREF(attr);
        Py_DECREF(self);
        return 0;
    }

    pushPythonObj(LUA, val);

    Py_DECREF(val);
    Py_DECREF(attr);
    Py_DECREF(self);

    return 1;
}

LUA_FUNC(luapyobject_newindex) {
    switchToCurrentRealm(state);

    PyObject *self = getStackValAsPythonObj(LUA, 1);
    PyObject *attr = getStackValAsPythonObj(LUA, 2);
    PyObject *val = getStackValAsPythonObj(LUA, 3);

    PyObject_SetItem(self, attr, val);

    Py_DECREF(val);
    Py_DECREF(attr);
    Py_DECREF(self);

    return 1;
}

LUA_FUNC(luapyobject_tostring) {
    switchToCurrentRealm(state);

    PyObject *self = getStackValAsPythonObj(LUA, 1);
    PyObject *selfAsPyStr = PyObject_Str(self);
    if (selfAsPyStr == NULL) {
        PyErr_Print();
        LUA->ThrowError("__tostring failed");
        Py_DECREF(self);
        return 0;
    }

    pushPythonObj(LUA, selfAsPyStr);

    Py_DECREF(selfAsPyStr);
    Py_DECREF(self);
    return 1;
}

LUA_FUNC(luapyobject_unaryMinus) {
    switchToCurrentRealm(state);

    PyObject *self = getStackValAsPythonObj(LUA, 1);

    PyObject *negative = PyNumber_Negative(self);
    if (negative == NULL) {
        PyErr_Print();
        LUA->ThrowError("__neg__ failed or not supported by this object");
        Py_DECREF(self);
        return 0;
    }

    pushPythonObj(LUA, negative);

    Py_DECREF(negative);
    Py_DECREF(self);
    return 1;
}

#define LUAPYOBJECT_BINARY_OP(LUA_OP_NAME, MAGIC_METHOD_NAME, PYTHON_API_OP_FUNC) \
    LUA_FUNC(luapyobject_ ## LUA_OP_NAME) { \
        switchToCurrentRealm(state); \
        \
        PyObject *self = getStackValAsPythonObj(LUA, 1); \
        PyObject *other = getStackValAsPythonObj(LUA, 2); \
        \
        PyObject *result = PYTHON_API_OP_FUNC(self, other); \
        if (result == NULL) { \
            PyErr_Print(); \
            LUA->ThrowError(MAGIC_METHOD_NAME " failed or not supported by this object"); \
            Py_DECREF(self); \
            Py_DECREF(other); \
            return 0; \
        } \
        \
        pushPythonObj(LUA, result); \
        \
        Py_DECREF(self); \
        Py_DECREF(other); \
        Py_DECREF(result); \
        return 1; \
    }

LUAPYOBJECT_BINARY_OP(add, "__add__", PyNumber_Add)
LUAPYOBJECT_BINARY_OP(sub, "__sub__", PyNumber_Subtract)
LUAPYOBJECT_BINARY_OP(mul, "__mul__", PyNumber_Multiply)
LUAPYOBJECT_BINARY_OP(div, "__truediv__", PyNumber_TrueDivide)
LUAPYOBJECT_BINARY_OP(mod, "__mod__", PyNumber_Remainder)
LUA_FUNC(luapyobject_pow) {
    switchToCurrentRealm(state);

    PyObject *self = getStackValAsPythonObj(LUA, 1);
    PyObject *other = getStackValAsPythonObj(LUA, 2);

    PyObject *result = PyNumber_Power(self, other, Py_None);
    if (result == NULL) {
        PyErr_Print();
        LUA->ThrowError("__pow__ failed or not supported by this object");
        Py_DECREF(self);
        Py_DECREF(other);
        return 0;
    }

    pushPythonObj(LUA, result);

    Py_DECREF(self);
    Py_DECREF(other);
    Py_DECREF(result);
    return 1;
}

#define LUAPYOBJECT_COMPARISON_OP(LUA_OP_NAME, MAGIC_METHOD_NAME, COMPARISON_TYPE) \
    LUA_FUNC(luapyobject_ ## LUA_OP_NAME) { \
        switchToCurrentRealm(state); \
        \
        PyObject *self = getStackValAsPythonObj(LUA, 1); \
        PyObject *other = getStackValAsPythonObj(LUA, 2); \
        \
        PyObject *result = PyObject_RichCompare(self, other, COMPARISON_TYPE); \
        if (result == NULL) { \
            PyErr_Print(); \
            LUA->ThrowError(MAGIC_METHOD_NAME " failed or not supported by this object"); \
            Py_DECREF(self); \
            Py_DECREF(other); \
            return 0; \
        } \
        \
        pushPythonObj(LUA, result); \
        \
        Py_DECREF(self); \
        Py_DECREF(other); \
        Py_DECREF(result); \
        return 1; \
    }

LUAPYOBJECT_COMPARISON_OP(eq, "__eq__", Py_EQ)
LUAPYOBJECT_COMPARISON_OP(lt, "__lt__", Py_LT)
LUAPYOBJECT_COMPARISON_OP(le, "__le__", Py_LE)
LUAPYOBJECT_COMPARISON_OP(gt, "__gt__", Py_GT)
LUAPYOBJECT_COMPARISON_OP(ge, "__ge__", Py_GE)

LUA_FUNC(luapyobject_gc) {
    switchToCurrentRealm(state);

	// Here we decrease the reference count, as we previously increased it in pushPythonObj()
	UserData *ud = reinterpret_cast<UserData *>(LUA->GetUserdata(1));
	PyObject *obj = reinterpret_cast<PyObject *>(ud->data);
	Py_DECREF(obj);
	return 0;
}

// Sets a concrete metatable function for the topmost Lua stack table.
void setLuaPyObjectMetaFunction(ILuaBase *lua, CFunc func, const char *fieldName) {
    lua->PushCFunction(func);
	lua->SetField(-2, fieldName);
}

// Creates LuaPyObject metamethods for the topmost Lua stack table.
void setLuaPyObjectMetatables(ILuaBase *lua) {
	setLuaPyObjectMetaFunction(lua, luapyobject_gc, "__gc");
	setLuaPyObjectMetaFunction(lua, luapyobject_index, "__index");
	setLuaPyObjectMetaFunction(lua, luapyobject_newindex, "__newindex");
	setLuaPyObjectMetaFunction(lua, luapyobject_tostring, "__tostring");
	setLuaPyObjectMetaFunction(lua, luapyobject_unaryMinus, "__unm");
	setLuaPyObjectMetaFunction(lua, luapyobject_add, "__add");
	setLuaPyObjectMetaFunction(lua, luapyobject_sub, "__sub");
	setLuaPyObjectMetaFunction(lua, luapyobject_mul, "__mul");
	setLuaPyObjectMetaFunction(lua, luapyobject_div, "__div");
	setLuaPyObjectMetaFunction(lua, luapyobject_mod, "__mod");
	setLuaPyObjectMetaFunction(lua, luapyobject_pow, "__pow");
	// TODO: concat
	setLuaPyObjectMetaFunction(lua, luapyobject_eq, "__eq");
	setLuaPyObjectMetaFunction(lua, luapyobject_lt, "__lt");
	setLuaPyObjectMetaFunction(lua, luapyobject_le, "__le");
	setLuaPyObjectMetaFunction(lua, luapyobject_gt, "__gt");
	setLuaPyObjectMetaFunction(lua, luapyobject_ge, "__ge");
}

// Creates a metatable for representing Python objects and functions in Lua.
void createLuaPyObjectMetatable(ILuaBase *lua) {
	lua->CreateMetaTableType("PyObject", LUA_TYPE_PYOBJECT);
    setLuaPyObjectMetatables(lua);
	lua->Pop();

	lua->CreateMetaTableType("PyCallable", LUA_TYPE_PYCALLABLE);
    setLuaPyObjectMetatables(lua);

	lua->PushCFunction(luapycallable_call);
	lua->SetField(-2, "__call");

	lua->PushString("function");
	lua->SetField(-2, "__type");

	lua->Pop();
}
