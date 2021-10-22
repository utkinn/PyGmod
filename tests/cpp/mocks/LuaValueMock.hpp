#pragma once

#include <gmock/gmock.h>

#include "interop/lua/ILuaValue.hpp"

namespace pygmod::testing
{
    class LuaValueMock : public interop::lua::ILuaValue
    {
    public:
        MOCK_METHOD(int, type, (), (const));
        MOCK_METHOD(bool, get_bool, (), (const));
    };
}