#include "PyGmod.hpp"

#include <memory>

#include "extensions/LuaStackPythonModule.hpp"
#include "extensions/PyGmodLuaModule.hpp"

using std::make_shared;
using std::shared_ptr;

namespace pygmod::init
{
    PyGmod::PyGmod(GarrysMod::Lua::ILuaBase *lua_base)
        : addon_loader(AddonLoader(python)),
          lua_to_python_value_converter(interop::converters::LuaToPythonValueConverter(lua_base)),
          python_to_lua_value_converter(interop::converters::PythonToLuaValueConverter(
              lua_base, shared_ptr<interop::python::PythonFunctionRegistry>(&py_func_registry))),
          python(interop::python::Python(path_provider.get_home(), path_provider.get_path())),
          path_provider(interop::python::PythonPathProvider(fs)),
          py_func_registry(interop::python::PythonFunctionRegistry()), fs(util::FileSystem()),
          logger(util::Logger(lua_base))
    {
        logger.println(util::LogLevel::INFO, "Binary module loaded");

        const shared_ptr<interop::python::IPython> python_ptr(&python);
        const shared_ptr<interop::converters::LuaToPythonValueConverter> lua_to_py_conv_ptr(
            &lua_to_python_value_converter);
        const shared_ptr<interop::converters::PythonToLuaValueConverter> py_to_lua_conv_ptr(
            &python_to_lua_value_converter);

        extensions::python::set_python_instance(python_ptr);
        extensions::python::set_lua_base_instance(lua_base);
        extensions::python::set_lua_to_python_value_converter_instance(lua_to_py_conv_ptr);
        extensions::python::set_python_to_lua_value_converter_instance(py_to_lua_conv_ptr);
        extensions::python::init();
        python.init();
        logger.println(util::LogLevel::INFO, "Python initialized");

        extensions::lua::set_python_instance(python_ptr);
        extensions::lua::set_lua_instance(lua_base);
        extensions::lua::set_python_to_lua_value_converter_instance(py_to_lua_conv_ptr);
        extensions::lua::set_lua_to_python_value_converter_instance(lua_to_py_conv_ptr);
        extensions::lua::set_python_function_registry_instance(
            shared_ptr<interop::python::PythonFunctionRegistry>(&py_func_registry));
        extensions::lua::init();
        logger.println(util::LogLevel::INFO, "Lua extension initialized");

        addon_loader.load();
    }

    PyGmod::~PyGmod()
    {
        logger.println(util::LogLevel::INFO, "Binary module shutting down");
    }
}