#include <Python.h>
#include "GarrysMod/Lua/Interface.h"

#include "Console.hpp"
#include "addon_launcher.hpp"

using namespace GarrysMod::Lua;

GMOD_MODULE_OPEN() {
	Console cons(LUA);

	cons.log("Binary module loaded");

	Py_Initialize();
	cons.log("Python initialized!");

	launchAddons(cons);

	return 0;
}

GMOD_MODULE_CLOSE() {
	Console cons(LUA);

	cons.log("Binary module shutting down.");

	Py_FinalizeEx();
	cons.log("Python finalized!");

	return 0;
}