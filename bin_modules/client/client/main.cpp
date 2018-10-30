#define GMMODULE
#define DLL_IMPORT extern "C" __declspec(dllimport)

#include "Interface.h"

DLL_IMPORT int pygmod_run(lua_State *state, bool client);
DLL_IMPORT int pygmod_finalize(lua_State* state);

GMOD_MODULE_OPEN() {
    return pygmod_run(state, true);
}

GMOD_MODULE_CLOSE() {
    return pygmod_finalize(state);
}
