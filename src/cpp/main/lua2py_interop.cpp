#include "lua2py_interop.hpp"
#include "py_extensions/_luastack.hpp"

#define LUA_FUNC(name) int name(lua_State *state)

// Realm subinterpreters which are created by pygmod_run()
PyThreadState *clientInterp = nullptr, *serverInterp = nullptr;

// Eexcutes a string of Python code.
LUA_FUNC(py_Exec) {
    const char *code = LUA->CheckString();
    PyRun_SimpleString(code);
	LUA->Pop();
    return 0;
}

// Swaps the current subinterpreter to client.
LUA_FUNC(py_SwitchToClient) {
	if (clientInterp != nullptr)
		PyThreadState_Swap(clientInterp);
	else
		LUA->ThrowError("client Python state is not available");
    return 0;
}

// Swaps the current subinterpreter to server.
LUA_FUNC(py_SwitchToServer) {
	if (serverInterp != nullptr)
		PyThreadState_Swap(serverInterp);
	else
		LUA->ThrowError("server Python state is not available");
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
