#include "lua2py_interop.hpp"
#include "py_extensions/_luastack.hpp"
#include "realms.hpp"

#define LUA_FUNC(name) int name(lua_State *state)

// Eexcutes a string of Python code.
LUA_FUNC(py_Exec) {
    switchToCurrentRealm(state);

    const char *code = LUA->CheckString();
    PyRun_SimpleString(code);
	LUA->Pop();
    return 0;
}

}

void extendLua(ILuaBase *lua) {
    lua->PushSpecial(SPECIAL_GLOB);
    lua->CreateTable();  // To be "py" table

    lua->PushCFunction(py_Exec);
    lua->SetField(-2, "Exec");


    // Adding "py" table to the global namespace
    lua->SetField(-2, "py");
    lua->Pop();
}
