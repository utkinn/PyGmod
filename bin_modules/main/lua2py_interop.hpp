// Lua functions for interacting with Python

#pragma once

#include <GarrysMod/Lua/Interface.h>
#include <Python.h>

using namespace GarrysMod::Lua;

extern PyThreadState *clientInterp, *serverInterp;

void extendLua(ILuaBase *lua);
