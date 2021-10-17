#pragma once

#include "ILuaToPythonValueConverter.hpp"
#include <GarrysMod/Lua/Interface.h>
#include <Python.h>

namespace pygmod::interop::converters
{
    class LuaToPythonValueConverter : public ILuaToPythonValueConverter
    {
    public:
        LuaToPythonValueConverter(GarrysMod::Lua::ILuaBase *lua) : lua(lua)
        {
        }

        PyObject *convert(int stack_index) override;

    private:
        GarrysMod::Lua::ILuaBase *lua;
    };
}