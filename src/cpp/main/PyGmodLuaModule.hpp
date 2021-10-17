#pragma once

#include <memory>

#include "IPython.hpp"
#include "IPythonToLuaValueConverter.hpp"
#include "ILuaToPythonValueConverter.hpp"
#include "IPythonFunctionRegistry.hpp"
#include <GarrysMod/Lua/Interface.h>

namespace pygmod::lua_extension
{
    void set_python_instance(const std::shared_ptr<init::IPython> &);
    void set_lua_instance(GarrysMod::Lua::ILuaBase *const);
    void set_python_to_lua_value_converter_instance(const std::shared_ptr<converters::IPythonToLuaValueConverter>&);
    void set_lua_to_python_value_converter_instance(const std::shared_ptr<converters::ILuaToPythonValueConverter>&);
    void set_python_function_registry_instance(const std::shared_ptr<interop::IPythonFunctionRegistry>&);
    void init();
}