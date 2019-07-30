#pragma once

#include <GarrysMod/Lua/Interface.h>

enum Realm {
	CLIENT,
	SERVER
};

// Retrieves the current realm.
Realm getCurrentRealm(lua_State* state);
void switchToCurrentRealm(lua_State *state);
