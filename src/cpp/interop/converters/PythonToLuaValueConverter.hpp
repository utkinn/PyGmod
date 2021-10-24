#pragma once

#include <memory>
#include <utility>

#include "interop/python/IPythonFunctionRegistry.hpp"
#include "IPythonToLuaValueConverter.hpp"
#include <GarrysMod/Lua/Interface.h>

namespace pygmod::interop::converters
{
    class PythonToLuaValueConverter : public IPythonToLuaValueConverter
    {
    public:
        PythonToLuaValueConverter(GarrysMod::Lua::ILuaBase *lua,
                                  std::shared_ptr<interop::python::IPythonFunctionRegistry> py_func_registry)
            : lua(lua), py_func_registry(py_func_registry)
        {
        }

        void convert(PyObject *) override;

    private:
        GarrysMod::Lua::ILuaBase *lua;
        std::shared_ptr<interop::python::IPythonFunctionRegistry> &py_func_registry;
    };
}