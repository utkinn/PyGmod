#include "realms.hpp"
#include "interpreter_states.hpp"

Realm getCurrentRealm(lua_State* state) {
	LUA->PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
	LUA->GetField(-1, "CLIENT");
	bool client = LUA->GetBool();
	LUA->Pop(2);
	return client ? CLIENT : SERVER;
}

void switchToCurrentRealm(lua_State *state) {
    Realm currentRealm = getCurrentRealm(state);
    PyThreadState *targetState = currentRealm == CLIENT ? clientInterp : serverInterp;
    if (targetState != nullptr)
        PyThreadState_Swap(targetState);
}
