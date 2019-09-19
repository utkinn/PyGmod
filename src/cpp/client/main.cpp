// Second stage of PyGmod init.
// This binary module runs pygmod_run() from pygmod.dll.

// Macro for exposing GMOD_MODULE_OPEN() and GMOD_MODULE_CLOSE() to Garry's Mod
#define DLL_IMPORT extern "C" __declspec(dllimport)

#include <GarrysMod/Lua/Interface.h>

DLL_IMPORT int pygmod_run(lua_State *state);

GMOD_MODULE_OPEN() {
    return pygmod_run(state);  // See src\cpp\main\main.cpp
}

GMOD_MODULE_CLOSE() {
    return 0;
}
