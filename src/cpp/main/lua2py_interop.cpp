#include <string>
#include "lua2py_interop.hpp"
#include "valueconv.hpp"
#include "realms.hpp"
#include "py_function_registry.hpp"

#define LUA_FUNC(name) int name(lua_State *state)

// Eexcutes a string of Python code.
LUA_FUNC(py_Exec) {
    prepareInterpreterForCurrentRealm(state);

    const char *code = LUA->CheckString();
    PyRun_SimpleString(code);
	LUA->Pop();
    return 0;
}

// Imports a Python module.
LUA_FUNC(py_Import) {
    prepareInterpreterForCurrentRealm(state);
    const char *moduleName = LUA->CheckString();
    PyObject *module = PyImport_ImportModule(moduleName);
    if (module == NULL) {
        PyErr_Print();
        LUA->ThrowError((std::string("could not import Python module ") + moduleName).c_str());
        return 0;
    }
    convertPyToLua(LUA, module);
    return 1;
}

LUA_FUNC(passCallToPyFunc) {
    int argCount = LUA->Top() - 1;  // How much args have we got for our Python function?
    auto funcId = LUA->CheckNumber(1);
    auto args = PyTuple_New(argCount);

    for (int i = 0; i < argCount; i++) {
        PyTuple_SET_ITEM(args, i, convertLuaToPy(LUA, i + 2));  // args for our function start at stack index 2
    }

    auto result = PyObject_Call(pyFunctionRegistry[funcId], args, NULL);
    if (!result) {
        PyErr_Print();
        LUA->ThrowError("exception in Python function");
    }
    convertPyToLua(LUA, result);
    return 1;
}

void extendLua(ILuaBase *lua) {
    lua->PushSpecial(SPECIAL_GLOB);
    lua->CreateTable();  // To be "py" table

    lua->PushCFunction(py_Exec);
    lua->SetField(-2, "Exec");

    lua->PushCFunction(py_Import);
    lua->SetField(-2, "Import");

    lua->PushCFunction(passCallToPyFunc);
    lua->SetField(-2, "_passCallToPyFunc");

    // Adding "py" table to the global namespace
    lua->SetField(-2, "py");
    lua->Pop();
}
