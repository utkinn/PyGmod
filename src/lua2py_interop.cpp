#include "lua2py_interop.hpp"
#include <Python.h>

#define LUA_FUNC(name) int name(lua_State *state)

// Eexcutes a string of Python code.
LUA_FUNC(py_exec) {
    const char *code = LUA->CheckString();

    PyRun_SimpleString(code);

    return 0;
}

void extendLua(ILuaBase *lua) {
    lua->PushSpecial(SPECIAL_GLOB);
    lua->CreateTable();  // To be "py" table

    lua->PushCFunction(py_exec);
    lua->SetField(-2, "exec");

    // Adding "py" table to the global namespace
    lua->SetField(-2, "py");
    lua->Pop();
}
