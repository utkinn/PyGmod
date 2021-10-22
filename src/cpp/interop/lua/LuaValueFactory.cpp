#include "LuaValueFactory.hpp"

#include <string>

#include "LuaValue.hpp"

namespace pygmod::interop::lua
{
    std::unique_ptr<ILuaValue> LuaValueFactory::create_from_ref(int ref)
    {
        return std::make_unique<LuaValue>(lua, ref);
    }
}