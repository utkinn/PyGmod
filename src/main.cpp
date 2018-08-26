#include <Python.h>
#include "GarrysMod/Lua/Interface.h"

#include "Console.hpp"
#include "addon_launcher.hpp"
#include "../../python_extensions/luastack.h"

using namespace GarrysMod::Lua;
using std::to_string;

GMOD_MODULE_OPEN() {
	Console cons(LUA);

	cons.log("Binary module loaded");

	PyImport_AppendInittab("luastack", PyInit_luastack);
	Py_Initialize();
	cons.log("Python initialized!");

	PyImport_ImportModule("luastack");
	setup(LUA);



	//PyRun_SimpleString(("import sys; sys.lua_interface_addr = " + to_string((int) LUA)).c_str());
	//cons.log("Set sys.lua_interface_addr to " + to_string((int) LUA));
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
