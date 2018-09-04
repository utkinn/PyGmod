#define GMMODULE
#define DLL_IMPORT extern "C" __declspec(dllimport)

#include "Interface.h"

DLL_IMPORT int gpython_run(lua_State *state, bool client);
DLL_IMPORT int gpython_finalize(lua_State* state);

GMOD_MODULE_OPEN() {
    return gpython_run(state, true);
}

GMOD_MODULE_CLOSE() {
    return gpython_finalize(state);
}
