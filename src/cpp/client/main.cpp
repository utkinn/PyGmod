// Second stage of PyGmod init.
// This binary module runs pygmod_run() from pygmod.dll.

#include <GarrysMod/Lua/Interface.h>

extern "C" int pygmod_run(lua_State *state);

GMOD_MODULE_OPEN() {
    return pygmod_run(state);  // See src/cpp/main/main.cpp
}

GMOD_MODULE_CLOSE() {
    return 0;
}
