#pragma once

#include <memory>

#include "interop/converters/ILuaToPythonValueConverter.hpp"
#include "interop/converters/IPythonToLuaValueConverter.hpp"
#include "interop/python/IPython.hpp"
#include "interop/python/IPythonFunctionRegistry.hpp"
#include <GarrysMod/Lua/Interface.h>

namespace pygmod::extensions::lua
{
    void set_python_instance(const std::shared_ptr<interop::python::IPython> &);
    void set_lua_instance(GarrysMod::Lua::ILuaBase *const);
    void set_python_to_lua_value_converter_instance(const std::shared_ptr<interop::converters::IPythonToLuaValueConverter> &);
    void set_lua_to_python_value_converter_instance(const std::shared_ptr<interop::converters::ILuaToPythonValueConverter> &);
    void set_python_function_registry_instance(const std::shared_ptr<interop::python::IPythonFunctionRegistry> &);
    void init();
}