#pragma once

#include <memory>

#include "ILuaValueFactory.hpp"
#include <GarrysMod/Lua/Interface.h>

namespace pygmod::interop::lua
{
    class LuaValueFactory : public ILuaValueFactory
    {
    public:
        LuaValueFactory(GarrysMod::Lua::ILuaBase *lua) : lua(lua)
        {
        }

        std::unique_ptr<ILuaValue> create_from_ref(int ref) override;

    private:
        GarrysMod::Lua::ILuaBase *lua;
    };
}