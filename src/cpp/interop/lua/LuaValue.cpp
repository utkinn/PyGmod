#include "LuaValue.hpp"

#include <GarrysMod/Lua/Interface.h>
#include "LuaException.hpp"

using namespace GarrysMod::Lua;

namespace pygmod::interop::lua
{
    LuaValue::~LuaValue()
    {
        lua->ReferenceFree(ref);
    }

    int LuaValue::type() const
    {
        lua->ReferencePush(ref);
        const auto type = lua->GetType(-1);
        lua->Pop();
        return type;
    }

    bool LuaValue::get_bool() const
    {
        require_type(Type::Bool);
        lua->ReferencePush(ref);
        const auto result = lua->GetBool();
        lua->Pop();
        return result;
    }

    void LuaValue::require_type(int expected_type) const
    {
        const auto real_type = type();
        if (real_type != expected_type)
        {
            std::string msg = "value has to be of expected type ";
            msg += lua->GetTypeName(expected_type);
            msg += ", actually is ";
            msg += lua->GetTypeName(real_type);
            throw LuaException(msg.c_str());
        }
    }
}