#pragma once

#include <GarrysMod/Lua/Interface.h>
#include "FileSystem.hpp"
#include "PythonPathProvider.hpp"
#include "Python.hpp"
#include "Lua.hpp"
#include "Logger.hpp"
#include "PythonToLuaValueConverter.hpp"
#include "LuaToPythonValueConverter.hpp"

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
		converters::PythonToLuaValueConverter python_to_lua_value_converter;
		converters::LuaToPythonValueConverter lua_to_python_value_converter;
		Logger logger;
	};
}