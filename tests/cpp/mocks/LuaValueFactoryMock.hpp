#pragma once

#include "interop/lua/ILuaValue.hpp"
#include "interop/lua/ILuaValueFactory.hpp"
#include <gmock/gmock.h>

namespace pygmod::testing
{
    class LuaValueFactoryMock : public interop::lua::ILuaValueFactory
    {
    public:
        MOCK_METHOD(std::unique_ptr<interop::lua::ILuaValue>, create_from_ref, (int ref), (override));
    };
}