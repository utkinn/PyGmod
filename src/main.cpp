#include <Python.h>
#include "GarrysMod/Lua/Interface.h"

#include "Console.hpp"
#include "addon_launcher.hpp"
#include "../../python_extensions/luastack.h"
#include "../../python_extensions/gmodstreams.h"

using namespace GarrysMod::Lua;
using std::to_string;

// Adds "luastack" and "gmodstreams" modules to builtins and initializes them.
void addAndInitializeGPythonBuiltins() {
    PyImport_AppendInittab("luastack", PyInit_luastack);
	PyImport_AppendInittab("gmodstreams", PyInit_gmodstreams);
}

// Sets the "lua" variable in the "luastack" module to the pointer to ILuaBase.
void giveILuaBasePtrToLuastack(ILuaBase* ptr) {
    PyImport_ImportModule("luastack");
    setup(ptr);  // Declaration and definition of this function is in "luastack.pyx"
}

// Redirects the Python stdout and stderr to Garry's Mod console.
void redirectIO_toGmod() {
    PyImport_ImportModule("gmodstreams");
    // set_stream() uses "luastack" module and don't need ILuaBase pointer to be passed here.
    // Declaration and defintion of this function is in "gmodstreams.pyx".
    set_stream();
}

// Redirects the Python stdout and stderr to "gpy.log" for debugging errors which prevent Garry's Mod IO from working.
void redirectIO_toLogFile() {
    PyRun_SimpleString("import sys; sys.stdout = sys.stderr = open('gpy.log', 'w+')");
}

GMOD_MODULE_OPEN() {
	Console cons(LUA);

	cons.log("Binary module loaded");

    addAndInitializeGPythonBuiltins();

	Py_Initialize();
	cons.log("Python initialized!");

    giveILuaBasePtrToLuastack(LUA);
    
    redirectIO_toGmod();
    //redirectIO_toLogFile();

    if (PyErr_Occurred()) {
        cons.error("Setup failed");
        return -1;
    }

	launchAddons(cons);

    if (PyErr_Occurred()) {
        cons.error("Something went wrong");
        return -2;
    }

	return 0;
}

GMOD_MODULE_CLOSE() {
	Console cons(LUA);

	cons.log("Binary module shutting down.");

	Py_FinalizeEx();
	cons.log("Python finalized!");

	return 0;
}
