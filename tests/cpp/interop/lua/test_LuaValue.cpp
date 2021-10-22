#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include "interop/lua/LuaException.hpp"
#include "interop/lua/LuaValue.hpp"
#include "mocks/ILuaBaseMock.hpp"
#include <GarrysMod/Lua/Interface.h>

using pygmod::interop::lua::LuaValue;
using namespace GarrysMod::Lua;
using testing::Return;

namespace pygmod::testing
{
    class LuaValueTest : public ::testing::Test
    {
    protected:
        const int ref = 123;
        ILuaBaseMock lua_base;
        LuaValue lua_value = LuaValue(&lua_base, ref);
    };

    TEST_F(LuaValueTest, get_type)
    {
        const auto expected_type = Type::Number;
        EXPECT_CALL(lua_base, ReferencePush(ref));
        EXPECT_CALL(lua_base, ReferenceFree(ref));
        EXPECT_CALL(lua_base, GetType(-1)).WillOnce(Return(expected_type));
        EXPECT_CALL(lua_base, Pop(1));

        const auto actual_type = lua_value.type();

        EXPECT_EQ(expected_type, actual_type);
    }

    TEST_F(LuaValueTest, get_bool)
    {
        EXPECT_CALL(lua_base, ReferencePush(ref)).Times(2);
        EXPECT_CALL(lua_base, ReferenceFree(ref));
        EXPECT_CALL(lua_base, GetType(-1)).WillOnce(Return(Type::Bool));
        EXPECT_CALL(lua_base, Pop(1)).Times(2);
        EXPECT_CALL(lua_base, GetBool(-1)).WillOnce(Return(true));

        const auto value = lua_value.get_bool();

        EXPECT_EQ(value, true);
    }

    TEST_F(LuaValueTest, get_mismatching_type)
    {
        EXPECT_CALL(lua_base, ReferencePush(ref));
        EXPECT_CALL(lua_base, ReferenceFree(ref));
        EXPECT_CALL(lua_base, GetType(-1)).WillOnce(Return(Type::Angle));
        EXPECT_CALL(lua_base, GetTypeName(Type::Bool)).WillOnce(Return("bool"));
        EXPECT_CALL(lua_base, GetTypeName(Type::Angle)).WillOnce(Return("angle"));
        EXPECT_CALL(lua_base, Pop(1));

        EXPECT_THROW(lua_value.get_bool(), interop::lua::LuaException);
    }
}