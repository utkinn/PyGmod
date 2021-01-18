// Defines Lua extension functions for basic Python interoperability.

#pragma once

#include <GarrysMod/Lua/Interface.h>
#include <Python.h>

using namespace GarrysMod::Lua;

// Adds py.Exec and py.Import to the Lua global namespace.
void extendLua(ILuaBase *lua);
