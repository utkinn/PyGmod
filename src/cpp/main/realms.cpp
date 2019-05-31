#include "realms.hpp"

Realm getCurrentRealm(lua_State* state) {
	LUA->PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
	LUA->GetField(-1, "CLIENT");
	bool client = LUA->GetBool();
	LUA->Pop(2);
	return client ? CLIENT : SERVER;
}