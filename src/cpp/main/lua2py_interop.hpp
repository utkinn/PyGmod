// Defines Lua extension functions for basic Python interoperability.

#pragma once

#include <GarrysMod/Lua/Interface.h>
#include <Python.h>

using namespace GarrysMod::Lua;

// Adds the aforementioned functions to the Lua global namespace.
void extendLua(ILuaBase *lua);
