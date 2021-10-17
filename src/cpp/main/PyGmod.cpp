#include "PyGmod.hpp"

#include <memory>

#include "LuaStackPyModule.hpp"

using std::shared_ptr;
using std::make_shared;

namespace pygmod::init
{
	PyGmod::PyGmod(GarrysMod::Lua::ILuaBase* lua_base)
		: fs(FileSystem()),
		path_provider(PythonPathProvider(fs)),
		python(Python(path_provider.get_home(), path_provider.get_path())),
		py_func_registry(interop::PythonFunctionRegistry()),
		lua_to_python_value_converter(converters::LuaToPythonValueConverter(lua_base)),
		python_to_lua_value_converter(converters::PythonToLuaValueConverter(lua_base, shared_ptr<interop::PythonFunctionRegistry>(&py_func_registry))),
		logger(Logger(lua_base)),
		addon_loader(AddonLoader(python))
	{
		logger.println(LogLevel::INFO, "Binary module loaded");

		py_extension::set_lua_base_instance(lua_base);
		py_extension::set_python_instance(shared_ptr<IPython>(&python));
		py_extension::set_lua_to_python_value_converter_instance(shared_ptr<converters::LuaToPythonValueConverter>(&lua_to_python_value_converter));
		py_extension::set_python_to_lua_value_converter_instance(shared_ptr<converters::PythonToLuaValueConverter>(&python_to_lua_value_converter));
		py_extension::init();
		python.init();
		logger.println("Python initialized");

		addon_loader.load();
	}

	PyGmod::~PyGmod()
	{
		logger.println(LogLevel::INFO, "Binary module shutting down");
	}
}