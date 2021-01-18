// Provides functionality for converting Python values to Lua values and vice versa.

#pragma once

#include <GarrysMod/Lua/Interface.h>
#include <Python.h>

using namespace GarrysMod::Lua;

// A custom Lua value type for Python objects in Lua
#define LUA_TYPE_PYOBJECT (Type::COUNT + 11)
#define LUA_TYPE_PYCALLABLE (Type::COUNT + 12)

// Converts a Python object to a Lua object and pushes it to the stack.
void convertPyToLua(ILuaBase *lua, PyObject *obj);

// Gets a Lua object from the given stack index,
// converts it to a Python object and returns it.
// Returns a new reference (reference counter will be already increased).
PyObject *convertLuaToPy(ILuaBase *lua, int index = -1);
