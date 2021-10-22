#pragma once

#include "ILua.hpp"
#include "ILuaValueFactory.hpp"
#include <GarrysMod/Lua/Interface.h>

namespace pygmod::interop::lua
{
    class Lua : public ILua
    {
    public:
        Lua(GarrysMod::Lua::ILuaBase *lua, ILuaValueFactory &lua_value_factory)
            : lua(lua), lua_value_factory(lua_value_factory)
        {
        }
        std::unique_ptr<ILuaValue> globals() override;

    private:
        GarrysMod::Lua::ILuaBase *lua;
        ILuaValueFactory &lua_value_factory;
    };
}