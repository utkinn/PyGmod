#pragma once

#include <memory>

#include "AddonLoader.hpp"
#include "interop/converters/LuaToPythonValueConverter.hpp"
#include "interop/converters/PythonToLuaValueConverter.hpp"
#include "interop/python/Python.hpp"
#include "interop/python/PythonFunctionRegistry.hpp"
#include "interop/python/PythonPathProvider.hpp"
#include "util/FileSystem.hpp"
#include "util/Logger.hpp"
#include <GarrysMod/Lua/Interface.h>

namespace pygmod::init
{
    class PyGmod
    {
    public:
        PyGmod(GarrysMod::Lua::ILuaBase *);
        ~PyGmod();

    private:
        AddonLoader addon_loader;
        interop::converters::LuaToPythonValueConverter lua_to_python_value_converter;
        interop::converters::PythonToLuaValueConverter python_to_lua_value_converter;
        interop::python::Python python;
        interop::python::PythonFunctionRegistry py_func_registry;
        interop::python::PythonPathProvider path_provider;
        util::FileSystem fs;
        util::Logger logger;
    };
}