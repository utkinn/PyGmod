#include "PyGmod.hpp"

#include <memory>

#include "LuaStackPyModule.hpp"

namespace pygmod::init
{
	PyGmod::PyGmod(GarrysMod::Lua::ILuaBase* lua_base)
		: fs(FileSystem()),
		path_provider(PythonPathProvider(fs)),
		python(Python(path_provider.get_home(), path_provider.get_path())),
		logger(Logger(lua_base))
	{
		logger.println(LogLevel::INFO, "Binary module loaded");

		py_extension::set_lua_base_instance(lua_base);
		py_extension::set_python_instance(std::shared_ptr<IPython>(&python));
		py_extension::init();
		python.init();
		logger.println("Python initialized");
	}

	PyGmod::~PyGmod()
	{
		logger.println(LogLevel::INFO, "Binary module shutting down");
	}
}