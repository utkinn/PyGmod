#include <Python.h>
#include "luapyobject.hpp"
#include "stack_utils.hpp"

#define LUA_FUNC(name) static int name(lua_State *state)

LUA_FUNC(luapyobject_call) {
	// Getting the function PyObject
	UserData *ud = reinterpret_cast<UserData *>(LUA->GetUserdata(1));
	PyObject *func = reinterpret_cast<PyObject *>(ud->data);

	if (!PyCallable_Check(func)) {
		LUA->ArgError(1, "this Python object is not callable");
		LUA->Pop(LUA->Top());
		return 0;
	}

	PyRun_SimpleString("import _luastack; _luastack.stack_dump()");

	int nArgs = LUA->Top() - 1;  // -1 because the userdata itself is also pushed as the first argument. The rest are the call arguments.
	PyObject *argsTuple = PyTuple_New(nArgs);  // Creating a tuple for arguments
	for (int i = 2; i <= 2 + nArgs; i++) {  // Filling the tuple with arguments
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

// Creates a metatable for representing Python objects in Lua.
void createLuaPyObjectMetatable(ILuaBase *lua) {
	lua->CreateMetaTableType("PyObject", LUA_TYPE_PYOBJECT);

	lua->PushCFunction(luapyobject_call);
	lua->SetField(-2, "__call");

	lua->Pop();
}