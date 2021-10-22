#pragma once

#include <memory>

#include "ILuaValue.hpp"

namespace pygmod::interop::lua
{
    class ILua
    {
    public:
        virtual std::unique_ptr<ILuaValue> globals() = 0;
    };
}