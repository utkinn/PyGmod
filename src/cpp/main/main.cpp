// Third stage of PyGmod init.
// This binary module initializes Python and creates subinterpreters for each realm.

#include <fstream>

#include <GarrysMod/Lua/Interface.h>

#include "Console.hpp"
#include "py_extensions/luapyobject.hpp"
#include "py_extensions/_luastack.hpp"
#include "lua2py_interop.hpp"

using namespace GarrysMod::Lua;
using std::to_string;

// Adds the _luastack Python extension module to builtins and initializes it.
void addAndInitializeLuastackExtension() {
	PyImport_AppendInittab("_luastack", PyInit__luastack);
}

// Initializes the _luastack module by calling its init() function.
void initLuastack(ILuaBase *ptr) {
	createLuaPyObjectMetatable(ptr);

	PyObject *luastackModule = PyImport_ImportModule("_luastack");  // import _luastack
	PyObject *initFunc = PyObject_GetAttrString(luastackModule, "init");  // initFunc = _luastack.init
	Py_DECREF(PyObject_CallFunction(initFunc, "l", reinterpret_cast<long>(ptr)));  // initFunc(ILuaBase memory address)
	Py_DECREF(initFunc);
	Py_DECREF(luastackModule);
}

// Redirects the Python stdout and stderr to "pygmod.log" for debugging errors which prevent Garry's Mod IO from working.
void redirectIOToLogFile() {
	PyRun_SimpleString("import sys; sys.stdout = sys.stderr = sys.__stdout__ = sys.__stderr__ = open('pygmod.log', 'w+')");
}

bool isFileExists(const char *path) {
	std::ifstream file(path);
	return file.good();
}

DLL_EXPORT int pygmod_run(lua_State *state, bool client) {
	Console cons(LUA);  // Creating a Console object for printing to the Garry's Mod console

	cons.log("Binary module loaded");

	if (!client) {
		addAndInitializeLuastackExtension();
		Py_Initialize();
		serverInterp = PyThreadState_Get();  // Saving the server subinterpreter for later use
	} else {
	    // Creating a subinterpreter for client and immediately swapping to it
		clientInterp = Py_NewInterpreter();
		PyThreadState_Swap(clientInterp);
	}

	PyRun_SimpleString("import sys, os.path; sys.path.append(os.path.abspath('garrysmod\\\\pygmod'))");

	cons.log("Python initialized!");

	initLuastack(LUA);

	if (PyErr_Occurred()) {
		cons.error("Setup failed");
		return 0;
	}

	extendLua(LUA);
	cons.log("Lua2Python Lua extensions loaded");

	redirectIOToLogFile();

	PyRun_SimpleString("from pygmod import _loader; _loader.main()");  // See python\loader.py

	if (PyErr_Occurred()) {
		cons.error("Something went wrong");
		PyErr_Print();
		return 0;
	}

	return 0;
}

DLL_EXPORT int pygmod_finalize(lua_State *state) {
	Console cons(LUA);  // Creating a Console object for printing to the Garry's Mod console

	cons.log("Binary module shutting down.");

	Py_FinalizeEx();
	cons.log("Python finalized!");

	return 0;
}
