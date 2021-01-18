#include <string>
#include <Python.h>
#include "luapyobject.hpp"
#include "valueconv.hpp"
#include "realms.hpp"

#define LUA_FUNC(name) static int name(lua_State *state)

LUA_FUNC(luapycallable_call) {
	prepareInterpreterForCurrentRealm(state);

	// Getting the function PyObject
	UserData *ud = reinterpret_cast<UserData *>(LUA->GetUserdata(1));
	PyObject *func = reinterpret_cast<PyObject *>(ud->data);

	if (!PyCallable_Check(func)) {
		LUA->ArgError(1, "this Python object is not callable");
		return 0;
	}

	int nArgs = LUA->Top() - 1;  // -1 because the userdata itself is also pushed as the first argument. The rest are the call arguments.
	PyObject *argsTuple = PyTuple_New(nArgs);  // Creating a tuple for arguments
	for (int i = 2; i <= LUA->Top(); i++) {  // Filling the tuple with arguments
		PyTuple_SetItem(argsTuple, i - 2, convertLuaToPy(LUA, i));
	}
	PyObject *result = PyObject_CallObject(func, argsTuple);  // Calling the function
	if (result == NULL) {  // If result == NULL, func has thrown an exception
		PyErr_Print();
		Py_DECREF(argsTuple);
		LUA->ThrowError("Exception in Python function");
		return 0;
	}
	convertPyToLua(LUA, result);  // Pushing the result to the stack

	Py_DECREF(argsTuple);
	Py_DECREF(result);
	return 1;
}

LUA_FUNC(luapyobject_index) {
    prepareInterpreterForCurrentRealm(state);

    PyObject *self = convertLuaToPy(LUA, 1);
    PyObject *attr = convertLuaToPy(LUA, 2);

    PyObject *val = PyObject_GetAttr(self, attr);
    if (val == NULL) {
        PyObject *valReprPy = PyObject_Repr(val);
        std::string valRepr = PyUnicode_AsUTF8(valReprPy);
        PyErr_Print();
        Py_DECREF(valReprPy);
        Py_DECREF(attr);
        Py_DECREF(self);
        LUA->ThrowError(("__getattribute__ failed, probably there is no such item: " + valRepr).c_str());
        return 0;
    }

    convertPyToLua(LUA, val);

    Py_DECREF(val);
    Py_DECREF(attr);
    Py_DECREF(self);

    return 1;
}

LUA_FUNC(luapyobject_newindex) {
    prepareInterpreterForCurrentRealm(state);

    PyObject *self = convertLuaToPy(LUA, 1);
    PyObject *attr = convertLuaToPy(LUA, 2);
    PyObject *val = convertLuaToPy(LUA, 3);

    PyObject_SetItem(self, attr, val);

    Py_DECREF(val);
    Py_DECREF(attr);
    Py_DECREF(self);

    return 1;
}

LUA_FUNC(luapyobject_tostring) {
    prepareInterpreterForCurrentRealm(state);

    PyObject *self = convertLuaToPy(LUA, 1);
    PyObject *selfAsPyStr = PyObject_Str(self);
    if (selfAsPyStr == NULL) {
        PyErr_Print();
        Py_DECREF(self);
        LUA->ThrowError("__tostring failed");
        return 0;
    }

    convertPyToLua(LUA, selfAsPyStr);

    Py_DECREF(selfAsPyStr);
    Py_DECREF(self);
    return 1;
}

LUA_FUNC(luapyobject_unaryMinus) {
    prepareInterpreterForCurrentRealm(state);

    PyObject *self = convertLuaToPy(LUA, 1);

    PyObject *negative = PyNumber_Negative(self);
    if (negative == NULL) {
        PyErr_Print();
        Py_DECREF(self);
        LUA->ThrowError("__neg__ failed or not supported by this object");
        return 0;
    }

    convertPyToLua(LUA, negative);

    Py_DECREF(negative);
    Py_DECREF(self);
    return 1;
}

#define LUAPYOBJECT_BINARY_OP(LUA_OP_NAME, MAGIC_METHOD_NAME, PYTHON_API_OP_FUNC) \
    LUA_FUNC(luapyobject_ ## LUA_OP_NAME) { \
        prepareInterpreterForCurrentRealm(state); \
        \
        PyObject *self = convertLuaToPy(LUA, 1); \
        PyObject *other = convertLuaToPy(LUA, 2); \
        \
        PyObject *result = PYTHON_API_OP_FUNC(self, other); \
        if (result == NULL) { \
            PyErr_Print(); \
            Py_DECREF(self); \
            Py_DECREF(other); \
            LUA->ThrowError(MAGIC_METHOD_NAME " failed or not supported by this object"); \
            return 0; \
        } \
        \
        convertPyToLua(LUA, result); \
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
    prepareInterpreterForCurrentRealm(state);

    PyObject *self = convertLuaToPy(LUA, 1);
    PyObject *other = convertLuaToPy(LUA, 2);

    PyObject *result = PyNumber_Power(self, other, Py_None);
    if (result == NULL) {
        PyErr_Print();
        Py_DECREF(self);
        Py_DECREF(other);
        LUA->ThrowError("__pow__ failed or not supported by this object");
        return 0;
    }

    convertPyToLua(LUA, result);

    Py_DECREF(self);
    Py_DECREF(other);
    Py_DECREF(result);
    return 1;
}

#define LUAPYOBJECT_COMPARISON_OP(LUA_OP_NAME, MAGIC_METHOD_NAME, COMPARISON_TYPE) \
    LUA_FUNC(luapyobject_ ## LUA_OP_NAME) { \
        prepareInterpreterForCurrentRealm(state); \
        \
        PyObject *self = convertLuaToPy(LUA, 1); \
        PyObject *other = convertLuaToPy(LUA, 2); \
        \
        PyObject *result = PyObject_RichCompare(self, other, COMPARISON_TYPE); \
        if (result == NULL) { \
            PyErr_Print(); \
            Py_DECREF(self); \
            Py_DECREF(other); \
            LUA->ThrowError(MAGIC_METHOD_NAME " failed or not supported by this object"); \
            return 0; \
        } \
        \
        convertPyToLua(LUA, result); \
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
	if (!prepareInterpreterForCurrentRealm(state))
		return 0;

	// Here we decrease the reference count, as we previously increased it in convertPyToLua()
	UserData *ud = reinterpret_cast<UserData *>(LUA->GetUserdata(1));
	PyObject *obj = reinterpret_cast<PyObject *>(ud->data);
	Py_DECREF(obj);
	return 0;
}

// Adds a function to the luapyobject metatable.
void addFuncToMetatable(ILuaBase *lua, CFunc func, const char *fieldName) {
    lua->PushCFunction(func);
	lua->SetField(-2, fieldName);
}

// Creates LuaPyObject metamethods for the topmost Lua stack table.
void populateMetatable(ILuaBase *lua) {
	addFuncToMetatable(lua, luapyobject_gc, "__gc");
	addFuncToMetatable(lua, luapyobject_index, "__index");
	addFuncToMetatable(lua, luapyobject_newindex, "__newindex");
	addFuncToMetatable(lua, luapyobject_tostring, "__tostring");
	addFuncToMetatable(lua, luapyobject_unaryMinus, "__unm");
	addFuncToMetatable(lua, luapyobject_add, "__add");
	addFuncToMetatable(lua, luapyobject_sub, "__sub");
	addFuncToMetatable(lua, luapyobject_mul, "__mul");
	addFuncToMetatable(lua, luapyobject_div, "__div");
	addFuncToMetatable(lua, luapyobject_mod, "__mod");
	addFuncToMetatable(lua, luapyobject_pow, "__pow");
	// TODO: concat
	addFuncToMetatable(lua, luapyobject_eq, "__eq");
	addFuncToMetatable(lua, luapyobject_lt, "__lt");
	addFuncToMetatable(lua, luapyobject_le, "__le");
	addFuncToMetatable(lua, luapyobject_gt, "__gt");
	addFuncToMetatable(lua, luapyobject_ge, "__ge");
}

// Creates a metatable for representing Python objects and functions in Lua.
void createLuaPyObjectMetatable(ILuaBase *lua) {
	lua->CreateMetaTableType("PyObject", LUA_TYPE_PYOBJECT);
    populateMetatable(lua);
	lua->Pop();

	lua->CreateMetaTableType("PyCallable", LUA_TYPE_PYCALLABLE);
    populateMetatable(lua);

	lua->PushCFunction(luapycallable_call);
	lua->SetField(-2, "__call");

	lua->PushString("function");
	lua->SetField(-2, "__type");

	lua->Pop();
}
