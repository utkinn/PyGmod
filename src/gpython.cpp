#include <Python.h>
#include "GarrysMod/Lua/Interface.h"

#include "Console.hpp"
#include "addon_launcher.hpp"
#include "../../python_extensions/gmod/luastack.h"
#include "lua2py_interop.hpp"

using namespace GarrysMod::Lua;
using std::to_string;

// Adds "luastack" and "streams" modules to builtins and initializes them.
void addAndInitializeGPythonBuiltins() {
    PyImport_AppendInittab("luastack", PyInit_luastack);
}

// Sets the "lua" variable in the "luastack" module to the pointer to ILuaBase.
void giveILuaBasePtrToLuastack(ILuaBase* ptr) {
    PyImport_ImportModule("luastack");
    setup(ptr);  // Declaration and definition of this function is in "luastack.pyx"
}

// Redirects the Python stdout and stderr to Garry's Mod console.
void redirectIO_toGmod() {
    PyRun_SimpleString("import gmod.streams, sys; sys.stdout = gmod.streams.GmodConsoleOut(); sys.stderr = gmod.streams.GmodConsoleErr()");
}

// Redirects the Python stdout and stderr to "gpy.log" for debugging errors which prevent Garry's Mod IO from working.
void redirectIO_toLogFile() {
    PyRun_SimpleString("import sys; sys.stdout = sys.stderr = open('gpy.log', 'w+')");
}

DLL_EXPORT int gpython_run(lua_State *state, bool client) {
	Console cons(LUA);

	cons.log("Binary module loaded");

    addAndInitializeGPythonBuiltins();

    if (!client) {
	    Py_Initialize();
        PyRun_SimpleString("import sys, os.path; sys.path.append(os.path.abspath('garrysmod\\\\gpython'))");
    } else {
        PyThreadState *clientInterp = Py_NewInterpreter();
        PyThreadState_Swap(clientInterp);
    }
    
	cons.log("Python initialized!");

    giveILuaBasePtrToLuastack(LUA);
    
    //redirectIO_toLogFile();
    redirectIO_toGmod();

    if (PyErr_Occurred()) {
        cons.error("Setup failed");
        return -1;
    }

    extendLua(LUA);
    cons.log("Lua2Python Lua extensions loaded");

	launchAddons(cons);

    if (PyErr_Occurred()) {
        cons.error("Something went wrong");
        return -2;
    }

	return 0;
}

DLL_EXPORT int gpython_finalize(lua_State *state) {
	Console cons(LUA);

	cons.log("Binary module shutting down.");

	Py_FinalizeEx();
	cons.log("Python finalized!");

	return 0;
}
