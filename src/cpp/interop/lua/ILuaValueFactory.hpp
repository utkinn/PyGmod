#pragma once

#include <memory>

#include "ILuaValue.hpp"

namespace pygmod::interop::lua
{
    class ILuaValueFactory
    {
    public:
        virtual std::unique_ptr<ILuaValue> create_from_ref(int ref) = 0;
    };
}