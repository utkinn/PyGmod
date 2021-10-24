#pragma once

#include <memory>

#include <GarrysMod/Lua/Interface.h>
#include <Python.h>
#include "interop/python/IPython.hpp"
#include "interop/converters/ILuaToPythonValueConverter.hpp"
#include "interop/converters/IPythonToLuaValueConverter.hpp"

namespace pygmod::extensions::python
{
	void set_lua_base_instance(GarrysMod::Lua::ILuaBase*);
	void set_python_instance(const std::shared_ptr<interop::python::IPython>&);
	void set_lua_to_python_value_converter_instance(const std::shared_ptr<interop::converters::ILuaToPythonValueConverter>&);
	void set_python_to_lua_value_converter_instance(const std::shared_ptr<interop::converters::IPythonToLuaValueConverter>&);
	void init();
}