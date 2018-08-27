#include <Python.h>
#include "GarrysMod/Lua/Interface.h"

#include "Console.hpp"
#include "addon_launcher.hpp"
#include "../../python_extensions/luastack.h"
#include "../../python_extensions/gmodstreams.h"

using namespace GarrysMod::Lua;
using std::to_string;

GMOD_MODULE_OPEN() {
	Console cons(LUA);

	cons.log("Binary module loaded");

	PyImport_AppendInittab("luastack", PyInit_luastack);
	PyImport_AppendInittab("gmodstreams", PyInit_gmodstreams);
	Py_Initialize();
	cons.log("Python initialized!");

    //PyRun_SimpleString("import sys;sys.stdout=sys.stderr=open('gpy.log', 'a+');print(1)");

	PyImport_ImportModule("luastack");
    setup(LUA);
	PyImport_ImportModule("gmodstreams");
    set_stream();
    if (PyErr_Occurred()) {
        cons.error("Setup fail");
        return -1;
    }

    PyObject *mainModule = PyImport_AddModule("__main__");
    Py_INCREF(mainModule);
    PyObject *globals = PyObject_GetAttrString(mainModule, "__dict__");
    Py_INCREF(globals);

	//PyRun_SimpleString(("import sys; sys.lua_interface_addr = " + to_string((int) LUA)).c_str());
	//cons.log("Set sys.lua_interface_addr to " + to_string((int) LUA));
	launchAddons(cons, globals);

    Py_DECREF(globals);
    Py_DECREF(mainModule);

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
