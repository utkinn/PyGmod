#include <fstream>

#include <Python.h>
#include "GarrysMod/Lua/Interface.h"

#include "Console.hpp"
#include "../../python_extensions/luastack.h"
#include "lua2py_interop.hpp"

using namespace GarrysMod::Lua;
using std::to_string;

// Adds "luastack" and "streams" modules to builtins and initializes them.
void addAndInitializePyGmodBuiltins() {
    PyImport_AppendInittab("luastack", PyInit_luastack);
}

// Sets the "lua" variable in the "luastack" module to the pointer to ILuaBase.
void giveILuaBasePtrToLuastack(ILuaBase* ptr) {
    PyImport_ImportModule("luastack");
    setup(ptr);  // Declaration and definition of this function is in "luastack.pyx"
    PyRun_SimpleString("import luastack; luastack.IN_GMOD = True");
}

// Redirects the Python stdout and stderr to "pygmod.log" for debugging errors which prevent Garry's Mod IO from working.
void redirectIO_toLogFile() {
    PyRun_SimpleString("import sys; sys.stdout = sys.stderr = open('pygmod.log', 'w+')");
}

bool isFileExists(const char *path) {
    std::ifstream file(path);
    return file.good();
}

DLL_EXPORT int pygmod_run(lua_State *state, bool client) {
    Console cons(LUA);

    cons.log("Binary module loaded");

    if (!client) {
        addAndInitializePyGmodBuiltins();
        Py_Initialize();
        serverInterp = PyThreadState_Get();
    } else {
        clientInterp = Py_NewInterpreter();
        PyThreadState_Swap(clientInterp);
    }

    PyRun_SimpleString("import sys, os.path; sys.path.append(os.path.abspath('garrysmod\\\\pygmod'))");

    cons.log("Python initialized!");

    giveILuaBasePtrToLuastack(LUA);

    if (PyErr_Occurred()) {
        cons.error("Setup failed");
        return 0;
    }

    extendLua(LUA);
    cons.log("Lua2Python Lua extensions loaded");

    if (isFileExists("out_to_log.pygmod")) {
        redirectIO_toLogFile();  // In case of the broken loader
        cons.log("The output was redirected to the file 'pygmod.log' in the Garry's Mod root directory.");
    }

    PyRun_SimpleString("import loader; loader.main()");

    if (PyErr_Occurred()) {
        cons.error("Something went wrong");
        return 0;
    }

    if (client)
        clientLua = LUA;
    else
        serverLua = LUA;

    return 0;
}

DLL_EXPORT int pygmod_finalize(lua_State *state) {
    Console cons(LUA);

    cons.log("Binary module shutting down.");

    Py_FinalizeEx();
    cons.log("Python finalized!");

    return 0;
}
