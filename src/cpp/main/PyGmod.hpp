#pragma once

#include <GarrysMod/Lua/Interface.h>
#include "FileSystem.hpp"
#include "PythonPathProvider.hpp"
#include "Python.hpp"
#include "Lua.hpp"
#include "Logger.hpp"

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
		Logger logger;
	};
}