#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <memory>
#include <utility>

#include "interop/lua/Lua.hpp"
#include "mocks/ILuaBaseMock.hpp"
#include "mocks/LuaValueFactoryMock.hpp"
#include "mocks/LuaValueMock.hpp"
#include <GarrysMod/Lua/Interface.h>

using pygmod::interop::lua::Lua;
using testing::Invoke;
using testing::Return;

namespace pygmod::testing
{
    TEST(Lua, returns_globals)
    {
        ILuaBaseMock lua_base;
        EXPECT_CALL(lua_base, PushSpecial(GarrysMod::Lua::SPECIAL_GLOB));
        EXPECT_CALL(lua_base, Pop(1));
        const auto ref = 123;
        EXPECT_CALL(lua_base, ReferenceCreate()).WillOnce(Return(ref));
        auto lua_value = new LuaValueMock;
        LuaValueFactoryMock lua_value_factory;
        EXPECT_CALL(lua_value_factory, create_from_ref(ref)).WillOnce(Invoke([&] {
            return std::unique_ptr<LuaValueMock>(lua_value);
        }));
        Lua lua(&lua_base, lua_value_factory);

        const auto globals = lua.globals();

        EXPECT_EQ(globals.get(), lua_value);
    }
}