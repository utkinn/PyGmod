// Third stage of PyGmod init.
// This binary module initializes Python and creates subinterpreters for each realm.

#include <fstream>
#include <filesystem>

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

bool isFileExists(const char *path) {
	std::ifstream file(path);
	return file.good();
}

void setPythonHome(Console &cons) {
	std::filesystem::path pythonStdlibPath = std::filesystem::current_path() / "garrysmod" / "pygmod" / "stdlib";
	if (!std::filesystem::exists(pythonStdlibPath)) {
		cons.error("Python standard library directory (garrysmod/pygmod/stdlib) not found.");
		return;
	}

	std::wstring pathWString = pythonStdlibPath.wstring();
	const wchar_t* pathWChar = pathWString.c_str();
	Py_SetPythonHome(pathWChar);
}

// Adds the _luastack Python extension module to builtins and initializes it.
void addAndInitializeLuastackExtension(Console &cons) {
	if (PyImport_AppendInittab("_luastack", PyInit__luastack) == -1)
        cons.error("Failed to append _luastack to inittab.");
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

void initPython(Console &cons) {
	setPythonHome(cons);
	addAndInitializeLuastackExtension(cons);
	Py_Initialize();
}

int finalize(lua_State*);

// Registers a hook which calls finalize() on game shutdown, so we have a chance to properly
// finalize Python.
void registerShutdownHook(lua_State *state) {
    LUA->PushSpecial(SPECIAL_GLOB);
    LUA->GetField(-1, "hook");
    LUA->GetField(-1, "Add");
    LUA->PushString("ShutDown");
    LUA->PushString("PyGmod early shutdown routine");
    LUA->PushCFunction(finalize);
    LUA->Call(3, 0);
    LUA->Pop(2);  // "hook" table, _G
}

DLL_EXPORT int pygmod_run(lua_State *state) {
	Console cons(LUA);  // Creating a Console object for printing to the Garry's Mod console

	cons.log("Binary module loaded");

	Realm currentRealm = getCurrentRealm(state);

	if (serverInterp == nullptr && clientInterp == nullptr) {
	    initPython(cons);
	}
	if (currentRealm == SERVER) {
		serverInterp = PyThreadState_Get();  // Saving the server subinterpreter for later use
	} else {  // Client
	    // If we should have interpreters for both realms...
        if (serverInterp != nullptr) {
            // Creating a subinterpreter for client and immediately swapping to it
            clientInterp = Py_NewInterpreter();
            PyThreadState_Swap(clientInterp);
		} else {
		    clientInterp = PyThreadState_Get();
		}
	}

    // Adding PyGmod's modules directory to sys.path
	PyRun_SimpleString("import sys, os.path; sys.path.append(os.path.abspath(os.path.join('garrysmod', 'pygmod')))");

	cons.log("Python initialized!");

	initLuastack(LUA);

	if (PyErr_Occurred()) {
		cons.error("Setup failed");
		PyErr_Print();
		return 0;
	}

	extendLua(LUA);
	cons.log("Lua2Python Lua extensions loaded");

    registerShutdownHook(state);
    cons.log("Shutdown hook registered");

	redirectIOToLogFile();

	PyRun_SimpleString("from pygmod import _loader; _loader.main()");  // See python/loader.py

	if (PyErr_Occurred()) {
		cons.error("Something went wrong");
		PyErr_Print();
		return 0;
	}

	return 0;
}

int finalize(lua_State *state) {
	Console cons(LUA);  // Creating a Console object for printing to the Garry's Mod console
	cons.log("Binary module shutting down.");

    // Is only one interpreter left?
	bool lastInterpreter = serverInterp == nullptr || clientInterp == nullptr;
	// If so, just finalize Python
	if (lastInterpreter) {
		PyThreadState *thatLastInterpreter = serverInterp == nullptr ? clientInterp : serverInterp;
		PyThreadState_Swap(thatLastInterpreter);
	    Py_FinalizeEx();
	} else {  // Otherwise, end that interpreter, and we know for sure that it's the client's interpreter
	    PyThreadState_Swap(clientInterp);
        Py_EndInterpreter(clientInterp);
		clientInterp = nullptr;
	}

	cons.log("Python finalized!");

    return 0;
}
