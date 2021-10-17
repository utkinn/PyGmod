#pragma once

#include <memory>

#include <GarrysMod/Lua/Interface.h>
#include "FileSystem.hpp"
#include "PythonPathProvider.hpp"
#include "Python.hpp"
#include "Logger.hpp"
#include "PythonFunctionRegistry.hpp"
#include "PythonToLuaValueConverter.hpp"
#include "LuaToPythonValueConverter.hpp"
#include "AddonLoader.hpp"

namespace pygmod::init
{
	class PyGmod
	{
	public:
		PyGmod(GarrysMod::Lua::ILuaBase*);
		~PyGmod();

	private:
		FileSystem fs;
		const PythonPathProvider path_provider;
		Python python;
		interop::PythonFunctionRegistry py_func_registry;
		converters::PythonToLuaValueConverter python_to_lua_value_converter;
		converters::LuaToPythonValueConverter lua_to_python_value_converter;
		Logger logger;
		AddonLoader addon_loader;
	};
}