#include "lua2py_interop.hpp"
#include "../../python_extensions/luastack.h"

#define LUA_FUNC(name) int name(lua_State *state)

// Realm subinterpreters which are created by pygmod_run()
PyThreadState *clientInterp, *serverInterp;
ILuaBase *clientLua, *serverLua;

// Eexcutes a string of Python code.
LUA_FUNC(py_Exec) {
    const char *code = LUA->CheckString();
    PyRun_SimpleString(code);

    return 0;
}

void swap(PyThreadState *state, ILuaBase *lua) {
    if (is_setup_complete()) {
        PyThreadState_Swap(state);
        setup(lua);
    }
}

LUA_FUNC(py_SwitchToClient) {
    swap(clientInterp, clientLua);
    return 0;
}

// Swaps the current subinterpreter to server.
LUA_FUNC(py_SwitchToServer) {
    swap(serverInterp, serverLua);
    return 0;
}

void extendLua(ILuaBase *lua) {
    lua->PushSpecial(SPECIAL_GLOB);
    lua->CreateTable();  // To be "py" table

    lua->PushCFunction(py_Exec);
    lua->SetField(-2, "Exec");

    lua->PushCFunction(py_SwitchToClient);
    lua->SetField(-2, "_SwitchToClient");

    lua->PushCFunction(py_SwitchToServer);
    lua->SetField(-2, "_SwitchToServer");

    // Adding "py" table to the global namespace
    lua->SetField(-2, "py");
    lua->Pop();
}
