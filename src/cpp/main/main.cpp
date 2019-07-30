// Third stage of PyGmod init.
// This binary module initializes Python and creates subinterpreters for each realm.

#include <fstream>

#include <GarrysMod/Lua/Interface.h>

#include "Console.hpp"
#include "py_extensions/luapyobject.hpp"
#include "py_extensions/_luastack.hpp"
#include "lua2py_interop.hpp"
#include "realms.hpp"
#include "interpreter_states.hpp"

using namespace GarrysMod::Lua;
using std::to_string;

// Declaration of interpreter states in "interpreter_states.hpp"
PyThreadState *clientInterp = nullptr, *serverInterp = nullptr;

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

void initPython() {
	addAndInitializeLuastackExtension();
	Py_Initialize();
}

DLL_EXPORT int pygmod_run(lua_State *state) {
	Console cons(LUA);  // Creating a Console object for printing to the Garry's Mod console

	cons.log("Binary module loaded");

	Realm currentRealm = getCurrentRealm(state);

	if (currentRealm == SERVER) {
		initPython();
		serverInterp = PyThreadState_Get();  // Saving the server subinterpreter for later use
	} else {  // Client
		// In the singleplayer mode, Python is initialized by the server-side code above.
		// However, if we're connecting to a server, server-side code won't be executed,
		// so we have to initialize Python here.
		if (serverInterp == nullptr) {
			initPython();
			// Server subinterpreter will be unused, but saving it anyway to prevent a crash during disconnecting
			serverInterp = PyThreadState_Get();  
		}
		clientInterp = Py_NewInterpreter();  // Creating a subinterpreter for client and immediately swapping to it
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

	Realm currentRealm = getCurrentRealm(state);
	if (currentRealm == CLIENT && clientInterp != nullptr) {
		Py_EndInterpreter(clientInterp);
		clientInterp = nullptr;
		PyThreadState_Swap(serverInterp);
	} else {
		Py_FinalizeEx();
	}

	cons.log("Python finalized!");

	return 0;
}
