#include "ILuaValue.hpp"

#include <GarrysMod/Lua/Interface.h>

namespace pygmod::interop::lua
{
    class LuaValue : public ILuaValue
    {
    public:
        LuaValue(GarrysMod::Lua::ILuaBase *lua, int ref) : lua(lua), ref(ref)
        {
        }
        ~LuaValue();

        int type() const override;
        bool get_bool() const override;

    private:
        GarrysMod::Lua::ILuaBase *lua;
        int ref;

        void require_type(int) const;
    };
}