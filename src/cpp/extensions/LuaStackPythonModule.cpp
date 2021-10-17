#include "LuaStackPythonModule.hpp"

#include <functional>
#include <memory>
#include <stdexcept>

#include "init/InitException.hpp"

using std::shared_ptr;

namespace pygmod::extensions::python
{
	using GarrysMod::Lua::ILuaBase;
	using init::IPython;

	ILuaBase *lua_base_instance;
	shared_ptr<IPython> python_instance;
	shared_ptr<converters::ILuaToPythonValueConverter> lua_to_python_value_converter_instance;
	shared_ptr<converters::IPythonToLuaValueConverter> python_to_lua_value_converter_instance;

	void set_lua_base_instance(ILuaBase *lua_base)
	{
		lua_base_instance = lua_base;
	}

	void set_python_instance(const shared_ptr<IPython> &python)
	{
		python_instance = python;
	}

	void set_lua_to_python_value_converter_instance(const shared_ptr<converters::ILuaToPythonValueConverter> &conv)
	{
		lua_to_python_value_converter_instance = conv;
	}

	void set_python_to_lua_value_converter_instance(const shared_ptr<converters::IPythonToLuaValueConverter> &conv)
	{
		python_to_lua_value_converter_instance = conv;
	}

#define PY_FUNC(name) static PyObject *name(PyObject *module, PyObject *args)

	PY_FUNC(top)
	{
		return python_instance->py_long_from_long(lua_base_instance->Top());
	}

	PY_FUNC(pop)
	{
		int pop_amount = 1;
		python_instance->parse_arg_tuple(args, "|i", &pop_amount);
		lua_base_instance->Pop(pop_amount);

		Py_RETURN_NONE;
	}

	PY_FUNC(get_table)
	{
		int stack_index;
		python_instance->parse_arg_tuple(args, "i", &stack_index);
		lua_base_instance->GetTable(stack_index);

		Py_RETURN_NONE;
	}

	PY_FUNC(get_field)
	{
		int stack_index;
		python_instance->parse_arg_tuple(args, "i", &stack_index);
		lua_base_instance->GetTable(stack_index);

		Py_RETURN_NONE;
	}

	PY_FUNC(set_table)
	{
		int stack_index;
		python_instance->parse_arg_tuple(args, "i", &stack_index);
		lua_base_instance->SetTable(stack_index);

		Py_RETURN_NONE;
	}

	PY_FUNC(set_field)
	{
		int stack_index;
		const char *name;
		python_instance->parse_arg_tuple(args, "is", &stack_index, &name);
		lua_base_instance->SetField(stack_index, name);

		Py_RETURN_NONE;
	}

	PY_FUNC(push)
	{
		int stack_index;
		python_instance->parse_arg_tuple(args, "i", &stack_index);
		lua_base_instance->Push(stack_index);
		Py_RETURN_NONE;
	}

	PY_FUNC(push_globals)
	{
		lua_base_instance->PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
		Py_RETURN_NONE;
	}

	PY_FUNC(push_nil)
	{
		lua_base_instance->PushNil();
		Py_RETURN_NONE;
	}

	PY_FUNC(create_table)
	{
		lua_base_instance->CreateTable();
		Py_RETURN_NONE;
	}

	PY_FUNC(next)
	{
		int stack_index;
		python_instance->parse_arg_tuple(args, "i", &stack_index);

		return python_instance->py_long_from_long(lua_base_instance->Next(stack_index));
	}

	PY_FUNC(get_type)
	{
		int stack_index;
		python_instance->parse_arg_tuple(args, "i", &stack_index);

		return python_instance->py_string_from_c_string(lua_base_instance->GetTypeName(lua_base_instance->GetType(stack_index)));
	}

	PY_FUNC(call)
	{
		int n_args, n_results;
		python_instance->parse_arg_tuple(args, "ii", &n_args, &n_results);

		const auto error_result = lua_base_instance->PCall(n_args, n_results, 0);
		if (error_result == 0)
			Py_RETURN_NONE;

		// Handling a Lua error by raising lua.LuaError
		const auto lua_module = python_instance->import_module("pygmod.lua");
		PyObject *lua_error_exc = python_instance->get_attr(lua_module, "LuaError");
		python_instance->raise_exception(lua_error_exc, lua_base_instance->GetString());
		Py_DECREF(lua_error_exc);
		Py_DECREF(lua_module);
		lua_base_instance->Pop(); // Popping the error message
		return nullptr;
	}

	PY_FUNC(reference_create)
	{
		return python_instance->py_long_from_long(lua_base_instance->ReferenceCreate());
	}

	PY_FUNC(reference_push)
	{
		int ref;
		python_instance->parse_arg_tuple(args, "i", &ref);

		lua_base_instance->ReferencePush(ref);

		Py_RETURN_NONE;
	}

	PY_FUNC(reference_free)
	{
		int ref;
		python_instance->parse_arg_tuple(args, "i", &ref);

		lua_base_instance->ReferenceFree(ref);

		Py_RETURN_NONE;
	}

	PY_FUNC(convert_lua_to_py)
	{
		int stack_index = -1;

		python_instance->parse_arg_tuple(args, "i", &stack_index);

		return lua_to_python_value_converter_instance->convert(stack_index);
	}

	PY_FUNC(convert_py_to_lua)
	{
		PyObject *obj;

		python_instance->parse_arg_tuple(args, "O", &obj);

		Py_INCREF(obj);
		python_to_lua_value_converter_instance->convert(obj);
		Py_DECREF(obj);
		Py_RETURN_NONE;
	}

#undef PY_FUNC

	static PyMethodDef method_def[] = {
		{"top", top, METH_NOARGS,
		 "top() -> int\n" PyDoc_STR("Returns the index of the top element in the stack."
									"Because indices start at 1, this result is equal to the number of elements in the stack (and so 0 means an empty stack).")},
		{"pop", pop, METH_VARARGS,
		 PyDoc_STR("pop(amount: int = 1) -> None\n"
				   "Pops 'amount' elements from the stack.")},
		{"get_table", get_table, METH_VARARGS,
		 PyDoc_STR("get_table(stack_index: int) -> None\n"
				   "Pushes onto the stack the value t[k], where t is the value at the given valid index and k is the value at the top of the stack.\n\n"
				   "This function pops the key from the stack (putting the resulting value in its place). As in Lua, this function may trigger a metamethod for the \"index\" event.")},
		{"get_field", get_field, METH_VARARGS,
		 PyDoc_STR("get_field(stack_index: int, name: str) -> None\n"
				   "Pushes onto the stack the value t[name], where t is the value at the given valid stack index. "
				   "As in Lua, this function may trigger a metamethod for the \"index\" event.")},
		{"set_table", set_table, METH_VARARGS,
		 PyDoc_STR("set_table(stack_index: int) -> None\n"
				   "Does the equivalent to t[k] = v, where t is the value at the given valid index, v is the value at the top of the stack, and k is the value just below the top.\n\n"
				   "This function pops both the key and the value from the stack. As in Lua, this function may trigger a metamethod for the \"newindex\" event.")},
		{"set_field", set_field, METH_VARARGS,
		 PyDoc_STR("set_field(stack_index: int, name: str) -> None\n"
				   "Does the equivalent to t[k] = v, where t is the value at the given valid index and v is the value at the top of the stack.\n\n"
				   "This function pops the value from the stack. As in Lua, this function may trigger a metamethod for the \"newindex\" event.")},
		{"push", push, METH_VARARGS,
		 PyDoc_STR("push(stack_index: int) -> None\n"
				   "Pushes a copy of the element at the given valid index onto the stack.")},
		{"push_globals", push_globals, METH_NOARGS,
		 PyDoc_STR("push_globals() -> None\n"
				   "Pushes the globals table (aka _G) to the stack.")},
		{"push_nil", push_nil, METH_NOARGS,
		 PyDoc_STR("push_nil() -> None\n"
				   "Pushes 'nil' to the stack.")},
		{"create_table", create_table, METH_NOARGS,
		 PyDoc_STR("create_table() -> None\n"
				   "Creates a new table on the top of the stack.")},
		{"next", next, METH_VARARGS,
		 PyDoc_STR("next(stack_index: int) -> int\n"
				   "Pops a key from the stack, and pushes a key-value pair from the table at the given index "
				   "(the \"next\" pair after the given key). If there are no more elements in the table, then next() returns 0 (and pushes nothing).")},
		{"get_type", get_type, METH_VARARGS,
		 PyDoc_STR("get_type(stack_index: int) -> str\n"
				   "Returns the name of the type of the Lua value at the given stack index.")},

		{"call", call, METH_VARARGS,
		 PyDoc_STR("call(args: int, results: int) -> None\n"
				   "Calls a function.\n\n"
				   "To call a function you must use the following protocol: first, the function to be called is pushed onto the stack; "
				   "then, the arguments to the function are pushed in direct order; that is, the first argument is pushed first. "
				   "Finally you call '_luastack.call'; 'args' is the number of arguments that you pushed onto the stack.\n\n"
				   "All arguments and the function value are popped from the stack when the function is called. "
				   "The function results are pushed onto the stack when the function returns. The number of results is adjusted to 'results', unless 'results' is -1. "
				   "In this case, all results from the function are pushed. The function results are pushed onto the stack in direct order "
				   "(the first result is pushed first), so that after the call the last result is on the top of the stack.")},

		{"reference_create", reference_create, METH_NOARGS,
		 PyDoc_STR("reference_create() -> int\n"
				   "Creates a new reference to an object on the top of the stack and pops that object.\n"
				   "Returns the reference.")},
		{"reference_push", reference_push, METH_VARARGS,
		 PyDoc_STR("reference_push(ref: int) -> None\n"
				   "Pushes the object which the reference ref points to, to the top of the stack.")},
		{"reference_free", reference_free, METH_VARARGS,
		 PyDoc_STR("reference_free(ref: int) -> None\n"
				   "Frees the reference ref.")},

		{"convert_lua_to_py", convert_lua_to_py, METH_VARARGS,
		 PyDoc_STR("convert_lua_to_py(stack_index: int = -1) -> object\n"
				   "Converts a Lua value on the given index of the stack to a Python value and returns it.\n"
				   "Raises NotImplementedError if Lua to Python conversion for this value type is not supported yet.")},
		{"convert_py_to_lua", convert_py_to_lua, METH_VARARGS,
		 PyDoc_STR("convert_py_to_lua(o) -> None\n"
				   "Converts a Python object to a Lua object and pushes it to the stack.")},

		{NULL, NULL, 0, NULL}};

	static PyModuleDef module_def = {
		PyModuleDef_HEAD_INIT,
		"_luastack",
		PyDoc_STR("Functions for manipulating the Lua stack. The lowest level of Garry's Mod Lua interoperability.\n\n"

				  "Lua uses a virtual stack to pass values to and from C.\n"
				  "Each element in this stack represents a Lua value(nil, number, string, etc.).\n\n"

				  "For convenience, most query operations in the API do not follow a strict stack discipline.\n"
				  "Instead, they can refer to any element in the stack by using an index:\n\n"

				  "- A positive index represents an absolute stack position (starting at 1)\n"
				  "- A negative index represents an offset relative to the top of the stack.\n\n"

				  "More specifically, if the stack has **n** elements, then index 1 represents the first element\n"
				  "(that is, the element that was pushed onto the stack first) and index n represents the last element;\n"
				  "index -1 also represents the last element (that is, the element at the top)\n"
				  "and index -n represents the first element.\n"
				  "We say that an index is valid if it lies between 1 and the stack top (that is, if 1 <= abs(index) <= top)."),
		0,
		method_def};

	PyMODINIT_FUNC PyInit__luastack()
	{
		return python_instance->create_module(module_def);
	}

	void init()
	{
		if (!lua_base_instance)
		{
			throw std::logic_error("lua_base_instance was not set by calling set_lua_base_instance");
		}

		if (!python_instance)
		{
			throw std::logic_error("python_instance was not set by calling set_lua_instance");
		}

		if (!lua_to_python_value_converter_instance)
		{
			throw std::logic_error("lua_to_python_value_converter_instance was not set by calling set_lua_to_python_value_converter_instance");
		}

		if (!python_to_lua_value_converter_instance)
		{
			throw std::logic_error("python_to_lua_value_converter_instance was not set by calling set_python_to_lua_value_converter_instance");
		}

		try
		{
			python_instance->register_builtin_module("_luastack", PyInit__luastack);
		}
		catch(const std::exception&)
		{
			std::throw_with_nested(init::InitException("PyImport_AppendInittab(\"_luastack\") failed"));
		}
	}
}
