#include "PyGmod.hpp"

namespace pygmod::init
{
	PyGmod::PyGmod(GarrysMod::Lua::ILuaBase& lua_base)
		: fs(FileSystem()),
		path_provider(PythonPathProvider(fs)),
		python(Python(path_provider.get_home(), path_provider.get_path())),
		lua(Lua(lua_base)),
		logger(Logger(lua))
	{
		logger.println(LogLevel::INFO, "Binary module loaded");
	}
}