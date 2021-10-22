#include "Lua.hpp"

#include "LuaValue.hpp"

namespace pygmod::interop::lua
{
    std::unique_ptr<ILuaValue> Lua::globals()
    {
        lua->PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
        const auto ref = lua->ReferenceCreate();
        lua->Pop();
        return lua_value_factory.create_from_ref(ref);
    }
}