#include <string>
#include "_luastack.hpp"
#include <GarrysMod/Lua/Interface.h>
#include "stack_utils.hpp"

using namespace GarrysMod::Lua;

// Macro for retrieving ILuaBase from the module state
#define MS_LUA (*reinterpret_cast<ILuaBase**>(PyModule_GetState(module)))
#define Py_MODULE_FUNC(name) static PyObject *name(PyObject *module, PyObject *args)

// Function definitions

Py_MODULE_FUNC(init) {
	int iLuaBasePtr;
	if (!PyArg_ParseTuple(args, "i", &iLuaBasePtr))
		return NULL;

    // Putting the pointer to ILuaBase to the module state
	*reinterpret_cast<ILuaBase **>(PyModule_GetState(module)) = reinterpret_cast<ILuaBase *>(iLuaBasePtr);
	Py_RETURN_NONE;
}
Py_MODULE_FUNC(top) {
	return PyLong_FromLong(MS_LUA->Top());
}
Py_MODULE_FUNC(pop) {
	int popAmount = 1;

	if (!PyArg_ParseTuple(args, "|i", &popAmount))
		return NULL;

	MS_LUA->Pop(popAmount);

	Py_RETURN_NONE;
}
Py_MODULE_FUNC(getField) {
	int stackIndex;
	const char *name;

	if (!PyArg_ParseTuple(args, "is", &stackIndex, &name))
		return NULL;

	MS_LUA->GetField(stackIndex, name);

	Py_RETURN_NONE;
}
Py_MODULE_FUNC(setField) {
	int stackIndex;
	const char *name;

	if (!PyArg_ParseTuple(args, "is", &stackIndex, &name))
		return NULL;

	MS_LUA->SetField(stackIndex, name);

	Py_RETURN_NONE;
}
Py_MODULE_FUNC(pushGlobals) {
	MS_LUA->PushSpecial(SPECIAL_GLOB);
	Py_RETURN_NONE;
}
Py_MODULE_FUNC(pushNil) {
	MS_LUA->PushNil();
	Py_RETURN_NONE;
}
Py_MODULE_FUNC(createTable) {
	MS_LUA->CreateTable();
	Py_RETURN_NONE;
}
Py_MODULE_FUNC(next) {
	int stackIndex;

	if (!PyArg_ParseTuple(args, "i", &stackIndex))
		return NULL;

	return PyLong_FromLong(MS_LUA->Next(stackIndex));
}
Py_MODULE_FUNC(getType) {
	int stackIndex;

	if (!PyArg_ParseTuple(args, "i", &stackIndex))
		return NULL;

	return PyUnicode_FromString(MS_LUA->GetTypeName(MS_LUA->GetType(stackIndex)));
}

Py_MODULE_FUNC(call) {
	int nArgs, nResults;

	if (!PyArg_ParseTuple(args, "ii", &nArgs, &nResults))
		return NULL;

	int errorResult = MS_LUA->PCall(nArgs, nResults, 0);
	if (errorResult == 0)
		Py_RETURN_NONE;
	else {
	    // Handling a Lua error by raising lua.LuaError
		PyObject *luaModule = PyImport_ImportModule("pygmod.lua");
		PyObject *luaErrorExc = PyObject_GetAttrString(luaModule, "LuaError");
		PyErr_SetString(luaErrorExc, MS_LUA->GetString());
		Py_DECREF(luaErrorExc);
		Py_DECREF(luaModule);
		MS_LUA->Pop();  // Popping the error message
		return NULL;
	}
}

Py_MODULE_FUNC(referenceCreate) {
	return PyLong_FromLong(MS_LUA->ReferenceCreate());
}
Py_MODULE_FUNC(referencePush) {
	int ref;

	if (!PyArg_ParseTuple(args, "i", &ref))
		return NULL;

	MS_LUA->ReferencePush(ref);

	Py_RETURN_NONE;
}
Py_MODULE_FUNC(referenceFree) {
	int ref;

	if (!PyArg_ParseTuple(args, "i", &ref))
		return NULL;

	MS_LUA->ReferenceFree(ref);

	Py_RETURN_NONE;
}

Py_MODULE_FUNC(getStackValAsPythonObj) {
	int stackIndex = -1;

	if (!PyArg_ParseTuple(args, "|i", &stackIndex))
		return NULL;

	return getStackValAsPythonObj(MS_LUA, stackIndex);
}
Py_MODULE_FUNC(pushPythonObj) {
	PyObject *obj;

	if (!PyArg_ParseTuple(args, "O", &obj))
		return NULL;

	Py_INCREF(obj);
	pushPythonObj(MS_LUA, obj);
	Py_DECREF(obj);
	Py_RETURN_NONE;
}

Py_MODULE_FUNC(stackDump) {
	PyRun_SimpleString("import logging\n" \
		               "logger = logging.getLogger('pygmod._luastack.stack_dump')\n" \
		               "logger.debug('--- LUA STACK DUMP ---')\n" \
		               "logger.debug('----------------------', stack_info=True)");
	for (int i = 1; i <= MS_LUA->Top(); i++) {
		int valType = MS_LUA->GetType(i);
		const char *valTypeName = MS_LUA->GetTypeName(valType);
		std::string repr;
		switch (valType) {
		case Type::NIL:
			repr = "nil";
			break;
		case Type::NUMBER:
			repr = std::to_string(MS_LUA->GetNumber(i));
			break;
		case Type::STRING:
			repr = MS_LUA->GetString(i);
			break;
		}
		std::string code = "import logging; logging.getLogger('pygmod._luastack.stack_dump').debug('%i: %s (%s)', " + std::to_string(i) + ", '" + valTypeName + "', '" + repr + "')";
		PyRun_SimpleString(code.c_str());
	}
	PyRun_SimpleString("import logging; logging.getLogger('pygmod._luastack.stack_dump').debug('----------------------')");

	Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
	{"init", init, METH_VARARGS,
	 PyDoc_STR("init(lua_base_ptr: int) -> None\n" \
	 "Initializes the module. Sets the internal ILuaBase pointer to lua_base_ptr.")},

	{"top", top, METH_NOARGS,
	 "top() -> int\n" \
	 PyDoc_STR("Returns the index of the top element in the stack." \
	 "Because indices start at 1, this result is equal to the number of elements in the stack (and so 0 means an empty stack).")},
	{"pop", pop, METH_VARARGS,
	 PyDoc_STR("pop(amount: int = 1) -> None\n" \
	 "Pops 'amount' elements from the stack.")},
	{"get_field", getField, METH_VARARGS,
	 PyDoc_STR("get_field(stack_index: int, name: str) -> None\n" \
	 "Pushes onto the stack the value t[name], where t is the value at the given valid stack index. " \
	 "As in Lua, this function may trigger a metamethod for the \"index\" event.")},
	{"set_field", setField, METH_VARARGS,
	 PyDoc_STR("set_field(stack_index: int, name: str) -> None\n" \
	 "Does the equivalent to t[k] = v, where t is the value at the given valid index and v is the value at the top of the stack.\n\n" \
	 "This function pops the value from the stack. As in Lua, this function may trigger a metamethod for the \"newindex\" event.")},
	{"push_globals", pushGlobals, METH_NOARGS,
	 PyDoc_STR("push_globals() -> None\n" \
	 "Pushes the globals table (aka _G) to the stack.")},
	{"push_nil", pushNil, METH_NOARGS,
	 PyDoc_STR("push_nil() -> None\n" \
	 "Pushes 'nil' to the stack.")},
	{"create_table", createTable, METH_NOARGS,
	 PyDoc_STR("create_table() -> None\n" \
	 "Creates a new table on the top of the stack.")},
	{"next", next, METH_VARARGS,
	 PyDoc_STR("next(stack_index: int) -> int\n" \
	 "Pops a key from the stack, and pushes a key-value pair from the table at the given index " \
     "(the \"next\" pair after the given key). If there are no more elements in the table, then lua_next returns 0 (and pushes nothing).")},
	{"get_type", getType, METH_VARARGS,
	 PyDoc_STR("get_type(stack_index: int) -> str\n" \
	 "Returns the name of the type of the Lua value at the given stack index.")},

	{"call", call, METH_VARARGS,
	 PyDoc_STR("call(args: int, results: int) -> None\n" \
	 "Calls a function.\n\n" \
	 "To call a function you must use the following protocol: first, the function to be called is pushed onto the stack; " \
	 "then, the arguments to the function are pushed in direct order; that is, the first argument is pushed first. " \
	 "Finally you call '_luastack.call'; 'args' is the number of arguments that you pushed onto the stack.\n\n" \
	 "All arguments and the function value are popped from the stack when the function is called. " \
	 "The function results are pushed onto the stack when the function returns. The number of results is adjusted to 'results', unless 'results' is -1. " \
	 "In this case, all results from the function are pushed. The function results are pushed onto the stack in direct order " \
	 "(the first result is pushed first), so that after the call the last result is on the top of the stack.")},

	{"reference_create", referenceCreate, METH_NOARGS,
	 PyDoc_STR("reference_create() -> int\n" \
	 "Creates a new reference to an object on the top of the stack and pops that object.\n" \
	 "Returns the reference.")},
	{"reference_push", referencePush, METH_VARARGS,
	 PyDoc_STR("reference_push(ref: int) -> None\n" \
	 "Pushes the object which the reference ref points to, to the top of the stack.")},
	{"reference_free", referenceFree, METH_VARARGS,
	 PyDoc_STR("reference_free(ref: int) -> None\n" \
	 "Frees the reference ref.")},

	{"get_stack_val_as_python_obj", getStackValAsPythonObj, METH_VARARGS,
	 PyDoc_STR("get_stack_val_as_python_obj(stack_index: int = -1) -> object\n" \
	 "Converts a Lua value on the given index of the stack to a Python value and returns it.\n" \
     "Raises NotImplementedError if Lua to Python conversion for this value type is not supported yet.")},
	{"push_python_obj", pushPythonObj, METH_VARARGS,
	 PyDoc_STR("push_python_obj(o) -> None\n" \
	 "Converts a Python object to a Lua object and pushes it to the stack.")},

	{"stack_dump", stackDump, METH_NOARGS,
	 PyDoc_STR("stack_dump() -> None\n" \
	 "Performs a Lua stack dump. Logs the type and the string representation of every stack object.")},

	{NULL, NULL, 0, NULL}
};

static PyModuleDef luastackModule = {
	PyModuleDef_HEAD_INIT,
	"_luastack",
	PyDoc_STR("Functions for manipulating the Lua stack. The lowest level of Garry's Mod Lua interoperability.\n\n" \

              "Lua uses a virtual stack to pass values to and from C.\n" \
              "Each element in this stack represents a Lua value(nil, number, string, etc.).\n\n" \

              "For convenience, most query operations in the API do not follow a strict stack discipline.\n" \
              "Instead, they can refer to any element in the stack by using an index:\n\n" \

              "- A positive index represents an absolute stack position (starting at 1)\n" \
              "- A negative index represents an offset relative to the top of the stack.\n\n" \

              "More specifically, if the stack has **n** elements, then index 1 represents the first element\n" \
              "(that is, the element that was pushed onto the stack first) and index n represents the last element;\n" \
              "index -1 also represents the last element (that is, the element at the top)\n" \
              "and index -n represents the first element.\n" \
              "We say that an index is valid if it lies between 1 and the stack top (that is, if 1 ≤ abs(index) ≤ top)."),
	sizeof(ILuaBase *),
	methods
};

PyMODINIT_FUNC PyInit__luastack() {
	return PyModule_Create(&luastackModule);
}
