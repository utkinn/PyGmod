#pragma once
#include <GarrysMod/Lua/Interface.h>
#include <Python.h>

using namespace GarrysMod::Lua;

// Defining a custom Lua value type for Python objects in Lua
#define LUA_TYPE_PYOBJECT (Type::COUNT + 11)
#define LUA_TYPE_PYCALLABLE (Type::COUNT + 12)

// Converts a Python object to a Lua object and pushes it to the stack.
void pushPythonObj(ILuaBase *lua, PyObject *obj);

// Gets a Lua object from the given stack index,
// converts it to a Python object and returns it.
PyObject *getStackValAsPythonObj(ILuaBase *lua, int index = -1);
