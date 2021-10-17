#include "LuaToPythonValueConverter.hpp"

#include <cmath>

#include <GarrysMod/Lua/Types.h>
#include "LuaCustomTypes.hpp"

namespace pygmod::converters
{
	static bool is_number_fractional(const double n)
	{
		return std::trunc(n) == n;
	}

	using namespace GarrysMod::Lua;

	PyObject* LuaToPythonValueConverter::convert(int stack_index) {
		switch (lua->GetType(stack_index))
		{
		case Type::Nil:
			Py_RETURN_NONE;

		case Type::Bool:
			return PyBool_FromLong(lua->GetBool(stack_index));

		case Type::Number:
			if (is_number_fractional(lua->GetNumber(stack_index)))
			{
				return PyFloat_FromDouble(lua->GetNumber(stack_index));
			}
			return PyLong_FromDouble(lua->GetNumber(stack_index));

		case Type::String:
			return PyUnicode_FromString(lua->GetString(stack_index, nullptr));

		case Type::Function:
		{
			const auto lua_module = PyImport_ImportModule("pygmod.lua");
			if (lua_module == nullptr)
				return nullptr;
			const auto lua_func_from_stack_func = PyObject_GetAttrString(lua_module, "_lua_func_from_stack");
			const auto lua_func_object = PyObject_CallFunction(lua_func_from_stack_func, "i", stack_index);
			Py_DECREF(lua_func_from_stack_func);
			Py_DECREF(lua_module);
			return lua_func_object;
		}

		case interop::lua::LUA_TYPE_PYOBJECT:
		case interop::lua::LUA_TYPE_PYCALLABLE:
		{
			const auto ud = static_cast<UserData*>(lua->GetUserdata(stack_index));
			const auto obj = static_cast<PyObject*>(ud->data);
			Py_INCREF(obj);
			return obj;
		}

		default:
		{
			const auto lua_module = PyImport_ImportModule("pygmod.lua");
			if (lua_module == nullptr)
				return nullptr;
			const auto table_from_stack_func = PyObject_GetAttrString(lua_module, "_table_from_stack");
			const auto table_object = PyObject_CallFunction(table_from_stack_func, "i", stack_index);
			Py_DECREF(table_from_stack_func);
			Py_DECREF(lua_module);
			return table_object;
		}
		}
	}
}