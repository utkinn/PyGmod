#pragma once

#include <GarrysMod/Lua/Interface.h>
#include "LuaException.hpp"

namespace pygmod::interop::lua
{
    class ILuaValue
    {
    public:
        virtual int type() const = 0;
        virtual bool get_bool() const = 0;
    };
}