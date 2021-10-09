// Third stage of PyGmod init.
// This binary module initializes Python and creates subinterpreters for each realm.

#include <fstream>
#include <filesystem>
#ifdef __linux__
	#include <dlfcn.h>  // For dlopen workaround
#endif

#include <GarrysMod/Lua/Interface.h>

#include "Console.hpp"
#include "_luastack.hpp"
#include "luapyobject.hpp"
#include "lua2py_interop.hpp"
#include "realms.hpp"
#include "interpreter_states.hpp"

#define STRINGIFY(x) #x
#define TO_STRING(x) STRINGIFY(x)

using namespace GarrysMod::Lua;
using std::to_string;

// Declaration of interpreter states in "interpreter_states.hpp"
PyThreadState *clientInterp = nullptr, *serverInterp = nullptr;

bool isFileExists(const char *path) {
	std::ifstream file(path);
	return file.good();
}

class SetupFailureException : public std::exception {
	const char *message;

public:
	SetupFailureException(const char *message) : message(message) {}
	SetupFailureException(string message) : message(message.c_str()) {}

	const char *what() {
		return this->message;
	}
};

void setPythonHomeAndPath(Console &cons) {
	std::filesystem::path pythonHome = std::filesystem::current_path() / "garrysmod" / "pygmod" / "stdlib";
	if (!std::filesystem::exists(pythonHome))
		throw SetupFailureException("Python standard library directory (garrysmod/pygmod/stdlib) not found.");

	std::wstring homeWString = pythonHome.wstring();
	const wchar_t* homeWChar = homeWString.c_str();
	Py_SetPythonHome(homeWChar);

	// Choosing an OS-specific symbol to separate paths in PYTHONPATH
	#ifdef _WIN32
		const std::wstring os_pathsep = L";";
	#else
		const std::wstring os_pathsep = L":";
	#endif

	// PYTHONPATH = PYTHONHOME (*.py modules)
	//				+ PYTHONHOME/lib-dynload (binary modules)
	//				+ PYTHONHOME/site-packages (pip packages)
	//				+ ./garrysmod/pygmod (PyGmod modules)

	std::filesystem::path libDynloadPath = pythonHome / "lib-dynload";
	std::filesystem::path sitePackagesPath = pythonHome / "site-packages";
	std::wstring pathWString = homeWString + os_pathsep
								+ libDynloadPath.wstring() + os_pathsep
								+ sitePackagesPath.wstring() + os_pathsep
								+ (std::filesystem::current_path() / "garrysmod" / "pygmod").wstring();
	const wchar_t* pathWChar = pathWString.c_str();
	Py_SetPath(pathWChar);
}

// Preloads libpygmod.so to help Python binary modules find Py_* symbols on Linux.
// It's required because for some bizarre reason binary modules don't have
// libpython3.X.so as their dynamic link dependency.
void doDlopenWorkaround() {
	#ifdef __linux__
		const char *soName = "libpython" TO_STRING(PYTHON_VERSION) ".so.1.0";
		if(!dlopen(soName, RTLD_LAZY | RTLD_GLOBAL))
			throw SetupFailureException((string("Couldn't load ") + soName + ", which must be at GarrysMod/bin."));
	#endif
}

// Schedules the initialization of _luastack module.
void appendLuastackToInittab() {
	if (PyImport_AppendInittab("_luastack", PyInit__luastack) == -1)
		throw SetupFailureException("PyImport_AppendInittab(\"_luastack\") failed");
}

// Initializes the _luastack module by calling its init() function.
void initLuastack(Console &cons, ILuaBase *ptr) {
	createLuaPyObjectMetatable(ptr);

	PyObject *luastackModule = PyImport_ImportModule("_luastack");  // import _luastack
	if (!luastackModule) {
		PyErr_Print();
		throw SetupFailureException("Couldn't import or find _luastack module.");
	}
	PyObject *initFunc = PyObject_GetAttrString(luastackModule, "init");  // initFunc = _luastack.init
	Py_DECREF(PyObject_CallFunction(initFunc, "n", reinterpret_cast<Py_ssize_t>(ptr)));  // initFunc(ILuaBase memory address)
	Py_DECREF(initFunc);
	Py_DECREF(luastackModule);
}

// Redirects the Python stdout and stderr to "pygmod.log" for debugging errors which prevent Garry's Mod IO from working.
void redirectIOToLogFile() {
	PyRun_SimpleString("import sys; sys.stdout = sys.stderr = sys.__stdout__ = sys.__stderr__ = open('pygmod.log', 'w+')");
}

void initPython(Console &cons) {
	setPythonHomeAndPath(cons);
	doDlopenWorkaround();
	appendLuastackToInittab();
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

// PyGmod main init routine which may throw SetupFailureException.
// This exception is handled at pygmod_run, the function just below.
void pygmodRunThrowing(Console& cons, lua_State *state) {
	cons.log("Binary module loaded");

	Realm currentRealm = getCurrentRealm(state);

	if (serverInterp == nullptr && clientInterp == nullptr) {
	    initPython(cons);
	}
	if (currentRealm == SERVER) {
		serverInterp = PyThreadState_Get();  // Saving the server subinterpreter for later use
		cons.log("Client:");
		cons.log(to_string(reinterpret_cast<unsigned long long>(clientInterp)));
		cons.log("Server:");
		cons.log(to_string(reinterpret_cast<unsigned long long>(serverInterp)));
	} else {  // Client
	    // If we should have interpreters for both realms...
        if (serverInterp != nullptr) {
            // Creating a subinterpreter for client and immediately swapping to it
            clientInterp = Py_NewInterpreter();
			cons.log("Client:");
		cons.log(to_string(reinterpret_cast<unsigned long long>(clientInterp)));
		cons.log("Server:");
		cons.log(to_string(reinterpret_cast<unsigned long long>(serverInterp)));
            PyThreadState_Swap(clientInterp);
		} else {
		    clientInterp = PyThreadState_Get();
		}
	}

	cons.log("Python initialized!");

	redirectIOToLogFile();

	initLuastack(cons, LUA);

	if (PyErr_Occurred()) {
		PyErr_Print();
		throw SetupFailureException("Internal Python error occurred");
	}

	extendLua(LUA);
	cons.log("Lua2Python Lua extensions loaded");

    registerShutdownHook(state);
    cons.log("Shutdown hook registered");

	PyRun_SimpleString("from pygmod import _loader; _loader.main()");  // See python/loader.py

	if (PyErr_Occurred()) {
		PyErr_Print();
		throw SetupFailureException("Exception occurred after an attempt to call _loader.main()");
	}
}

// Main init routine.
DLL_EXPORT int pygmod_run(lua_State *state) {
	Console cons(LUA);  // Creating a Console object for printing to the Garry's Mod console

	try {
		pygmodRunThrowing(cons, state);
	} catch (SetupFailureException e) {
		cons.error(e.what());
	}

	return 0;
}

int finalize(lua_State *state) {  // TODO: rewrite
	Console cons(LUA);  // Creating a Console object for printing to the Garry's Mod console
	cons.log("Binary module shutting down.");

	Realm currentRealm = getCurrentRealm(state);

	auto currentInterp = currentRealm == CLIENT ? clientInterp : serverInterp;
	PyThreadState_Swap(currentInterp);

	if (currentRealm == CLIENT && serverInterp == nullptr || currentRealm == SERVER && clientInterp == nullptr)
		Py_FinalizeEx();
	else
		Py_EndInterpreter(currentInterp);

	if (currentRealm == CLIENT)
		clientInterp = nullptr;
	else
		serverInterp = nullptr;

	cons.log("Python finalized!");

    return 0;
}

// ----- Old code above -----

#include "PyGmod.hpp"

pygmod::init::PyGmod* pygmod_instance;

GMOD_MODULE_OPEN()
{
	pygmod_instance = new pygmod::init::PyGmod;
	return 0;
}

GMOD_MODULE_CLOSE()
{
	delete pygmod_instance;
	pygmod_instance = nullptr;
	return 0;
}