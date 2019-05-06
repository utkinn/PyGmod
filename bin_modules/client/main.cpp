// Second stage of PyGmod init.
// This binary module runs two functions from pygmod.dll:
// - pygmod_run() on game startup
// - pygmod_finalize() on game end

// Macro for exposing GMOD_MODULE_OPEN() and GMOD_MODULE_CLOSE() to Garry's Mod
#define DLL_IMPORT extern "C" __declspec(dllimport)

#include <GarrysMod/Lua/Interface.h>

DLL_IMPORT int pygmod_run(lua_State *state, bool client);
DLL_IMPORT int pygmod_finalize(lua_State *state);

GMOD_MODULE_OPEN() {
    return pygmod_run(state, true);  // See bin_modules\main\main.cpp
}

GMOD_MODULE_CLOSE() {
    return pygmod_finalize(state);
}
