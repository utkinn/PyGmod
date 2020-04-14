#include <string>
#include "lua2py_interop.hpp"
#include "py_extensions/_luastack.hpp"
#include "py_extensions/stack_utils.hpp"
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

LUA_FUNC(py_Import) {
    switchToCurrentRealm(state);
    const char *moduleName = LUA->CheckString();
    PyObject *module = PyImport_ImportModule(moduleName);
    if (module == NULL) {
        PyErr_Print();
        LUA->ThrowError((std::string("could not import Python module ") + moduleName).c_str());
        return 0;
    }
    pushPythonObj(LUA, module);
    return 1;
}

void extendLua(ILuaBase *lua) {
    lua->PushSpecial(SPECIAL_GLOB);
    lua->CreateTable();  // To be "py" table

    lua->PushCFunction(py_Exec);
    lua->SetField(-2, "Exec");

    lua->PushCFunction(py_Import);
    lua->SetField(-2, "Import");

    // Adding "py" table to the global namespace
    lua->SetField(-2, "py");
    lua->Pop();
}