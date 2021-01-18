#include "stack_utils.hpp"
#include <string>

void convertPyToLua(ILuaBase *lua, PyObject *obj) {
	if (obj == Py_None) {
		lua->PushNil();
	}

	else if (PyBool_Check(obj)) {
		lua->PushBool(PyObject_IsTrue(obj));
	}

	else if (PyNumber_Check(obj)) {
		PyObject *numberAsPyFloat = PyNumber_Float(obj);
		lua->PushNumber(PyFloat_AsDouble(numberAsPyFloat));
		Py_DECREF(numberAsPyFloat);
	}

	else if (PyBytes_Check(obj)) {
		lua->PushString(PyBytes_AsString(obj));
	}

	else if (PyUnicode_Check(obj)) {
		lua->PushString(PyUnicode_AsUTF8(obj));
	}

	// obj is a pygmod.lua.LuaObject instance.
	// Pushing the Lua value that this LuaObject represents.
	else if (PyObject_HasAttrString(obj, "_ref")) {
		PyObject *refPyInt = PyObject_GetAttrString(obj, "_ref");
		int refCInt = PyLong_AsLong(refPyInt);
		lua->ReferencePush(refCInt);
		Py_DECREF(refPyInt);
	}

	// Other Python objects are represented by a custom metatable type
	// defined in luapyobject.cpp.
	else {
		// Py_INCREF is necessary because otherwise that Python object could be deallocated even though being stored in our userdata.
		// By increasing the reference count we tell Python that this object is still in use
		// and therefore shouldn't be destroyed by the garbage collector.
		Py_INCREF(obj);
		UserData *pyObjectUserdataContainer = reinterpret_cast<UserData *>(lua->NewUserdata(sizeof(UserData)));
		pyObjectUserdataContainer->data = reinterpret_cast<void *>(obj);
		if (PyCallable_Check(obj)) {
			pyObjectUserdataContainer->type = LUA_TYPE_PYCALLABLE;
			lua->CreateMetaTableType("PyCallable", LUA_TYPE_PYCALLABLE);
		} else {
			pyObjectUserdataContainer->type = LUA_TYPE_PYOBJECT;
			lua->CreateMetaTableType("PyObject", LUA_TYPE_PYOBJECT);
		}
		lua->SetMetaTable(-2);
	}
}

bool isNumberFractional(double n) {
    return n != (int) n;
}

PyObject *convertLuaToPy(ILuaBase *lua, int index) {
	int type = lua->GetType(index);

	// switch statement is not used because it doesn't support declaring new variables inside of it

	if (type == Type::Nil) {
		Py_RETURN_NONE;
	}

	if (type == Type::Bool) {
		return PyBool_FromLong(lua->GetBool(index));
	}

	if (type == Type::Number) {
	    if (isNumberFractional(lua->GetNumber(index)))
		    return PyFloat_FromDouble(lua->GetNumber(index));
		else
		    return PyLong_FromDouble(lua->GetNumber(index));
	}

	if (type == Type::String) {
		return PyUnicode_FromString(lua->GetString(index, NULL));
	}

	if (type == Type::Function) {
		PyObject *luaModule = PyImport_ImportModule("pygmod.lua");
		if (luaModule == NULL)
			return NULL;
		PyObject *luaFuncFromStackFunc = PyObject_GetAttrString(luaModule, "_lua_func_from_stack");
		PyObject *luaFuncObject = PyObject_CallFunction(luaFuncFromStackFunc, "i", index);
		Py_DECREF(luaFuncFromStackFunc);
		Py_DECREF(luaModule);
		return luaFuncObject;
	}

	if (type == LUA_TYPE_PYOBJECT || type == LUA_TYPE_PYCALLABLE) {
		UserData *ud = reinterpret_cast<UserData *>(lua->GetUserdata(index));
	    PyObject *obj = reinterpret_cast<PyObject *>(ud->data);
	    Py_INCREF(obj);
	    return obj;
	}

	// else

	luaModule = PyImport_ImportModule("pygmod.lua");
	if (luaModule == NULL)
		return NULL;
	PyObject *tableFromStackFunc = PyObject_GetAttrString(luaModule, "_table_from_stack");
	PyObject *tableObject = PyObject_CallFunction(tableFromStackFunc, "i", index);
	Py_DECREF(tableFromStackFunc);
	Py_DECREF(luaModule);
	return tableObject;
}
