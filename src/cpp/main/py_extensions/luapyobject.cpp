#include <Python.h>
#include "luapyobject.hpp"
#include "stack_utils.hpp"
#include "../realms.hpp"

#define LUA_FUNC(name) static int name(lua_State *state)

// Switches the Python interpreter to the current realm.
void switchToCurrentRealm(lua_State *state) {
    LUA->PushSpecial(SPECIAL_GLOB);
    LUA->GetField(-1, "py");

    Realm currentRealm = getCurrentRealm(state);
    LUA->GetField(-1, currentRealm == CLIENT ? "_SwitchToClient" : "_SwitchToServer");
    LUA->Call(0, 0);
    LUA->Pop(2);
}

LUA_FUNC(luapyobject_call) {
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

LUA_FUNC(luapyobject_gc) {
	// Here we decrease the reference count, as we previously increased it in pushPythonObj()
	UserData *ud = reinterpret_cast<UserData *>(LUA->GetUserdata(1));
	PyObject *obj = reinterpret_cast<PyObject *>(ud->data);
	Py_DECREF(obj);
	return 0;
}

// Creates a metatable for representing Python objects in Lua.
void createLuaPyObjectMetatable(ILuaBase *lua) {
	lua->CreateMetaTableType("PyObject", LUA_TYPE_PYOBJECT);

	lua->PushCFunction(luapyobject_call);
	lua->SetField(-2, "__call");

	lua->PushCFunction(luapyobject_gc);
	lua->SetField(-2, "__gc");

	lua->Pop();
}
