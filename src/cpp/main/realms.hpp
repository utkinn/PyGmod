#pragma once

#include <GarrysMod/Lua/Interface.h>

enum Realm {
	CLIENT,
	SERVER
};

// Retrieves the current realm.
Realm getCurrentRealm(lua_State* state);
bool switchToCurrentRealm(lua_State *state);
