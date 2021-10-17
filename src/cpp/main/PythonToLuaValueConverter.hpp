#pragma once

#include <memory>
#include <utility>

#include "IPythonFunctionRegistry.hpp"
#include "IPythonToLuaValueConverter.hpp"
#include <GarrysMod/Lua/Interface.h>

namespace pygmod::converters
{
    class PythonToLuaValueConverter : public IPythonToLuaValueConverter
    {
    public:
        PythonToLuaValueConverter(GarrysMod::Lua::ILuaBase *lua,
                                  std::shared_ptr<interop::IPythonFunctionRegistry> py_func_registry)
            : lua(lua), py_func_registry(py_func_registry)
        {
        }

        void convert(PyObject *) override;

    private:
        GarrysMod::Lua::ILuaBase *lua;
        std::shared_ptr<interop::IPythonFunctionRegistry> &py_func_registry;
    };
}