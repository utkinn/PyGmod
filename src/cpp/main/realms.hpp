#pragma once

#include <GarrysMod/Lua/Interface.h>

enum Realm {
	CLIENT,
	SERVER
};

// Retrieves the current realm.
Realm getCurrentRealm(lua_State* state);

// Prepares the Python interpreter for the current realm by
// swapping to the corresponding PyThreadState.
// Returns true if the interpreter was actually switch
// or false if the destination interpreter doesn't exist
// (for example on a dedicated server).
bool prepareInterpreterForCurrentRealm(lua_State *state);
