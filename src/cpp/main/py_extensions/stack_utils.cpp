#include "stack_utils.hpp"
#include <string>

void pushPythonObj(ILuaBase *lua, PyObject *obj) {
	if (obj == Py_None)
		lua->PushNil();
	else if (PyBool_Check(obj))
		lua->PushBool(PyObject_IsTrue(obj));
	else if (PyNumber_Check(obj)) {
		PyObject *numberAsPyFloat = PyNumber_Float(obj);
		lua->PushNumber(PyFloat_AsDouble(numberAsPyFloat));
		Py_DECREF(numberAsPyFloat);
	}
	else if (PyBytes_Check(obj))
		lua->PushString(PyBytes_AsString(obj));
	else if (PyUnicode_Check(obj))
		lua->PushString(PyUnicode_AsUTF8(obj));
	else if (PyObject_HasAttrString(obj, "_LuaObject__ref")) {  // A reference wrapper: pushing the referenced object
		PyObject *refPyInt = PyObject_GetAttrString(obj, "_LuaObject__ref");
		int refCInt = PyLong_AsLong(refPyInt);
		lua->ReferencePush(refCInt);
		Py_DECREF(refPyInt);
	}
	else {  // Pushing a userdata with PyObject
		Py_INCREF(obj);  // This is necessary because otherwise that Python object could be deallocated even though being stored in our userdata.
						 // By increasing the reference count we tell Python that this object is still in use
		                 // and therefore shouldn't be destroyed by the garbage collector.
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

PyObject *getStackValAsPythonObj(ILuaBase *lua, int index) {
	int type = lua->GetType(index);
	PyObject *luaModule, *tableObject, *luaFuncObject, *tableFromStackFunc, *luaFuncFromStackFunc;

	switch (type) {
	case Type::NIL:
		Py_RETURN_NONE;
	case Type::BOOL:
		return PyBool_FromLong(lua->GetBool(index));
	case Type::NUMBER:
	    if (isNumberFractional(lua->GetNumber(index)))
		    return PyFloat_FromDouble(lua->GetNumber(index));
		else
		    return PyLong_FromDouble(lua->GetNumber(index));
	case Type::STRING:
		return PyUnicode_FromString(lua->GetString(index, NULL));
	case Type::FUNCTION:
		luaModule = PyImport_ImportModule("pygmod.lua");
		if (luaModule == NULL)
			return NULL;
		luaFuncFromStackFunc = PyObject_GetAttrString(luaModule, "_lua_func_from_stack");
		luaFuncObject = PyObject_CallFunction(luaFuncFromStackFunc, "i", index);
		Py_DECREF(luaFuncFromStackFunc);
		Py_DECREF(luaModule);
		return luaFuncObject;
	case Type::TABLE:
	default:
		luaModule = PyImport_ImportModule("pygmod.lua");
		if (luaModule == NULL)
			return NULL;
		tableFromStackFunc = PyObject_GetAttrString(luaModule, "_table_from_stack");
		tableObject = PyObject_CallFunction(tableFromStackFunc, "i", index);
		Py_DECREF(tableFromStackFunc);
		Py_DECREF(luaModule);
		return tableObject;
		//const char *typeName = lua->GetTypeName(type);
		//std::string errorMessage = std::string("Lua type ") + typeName + " is not accessible from Python yet";
		//PyErr_SetString(PyExc_NotImplementedError, errorMessage.c_str());
		//return NULL;

	// TODO: Make separate classes for userdata types
	}
}
