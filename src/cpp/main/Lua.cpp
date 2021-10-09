#include "Lua.hpp"

#include "LuaObject.hpp"

namespace pygmod::init
{
	std::unique_ptr<ILuaObject> Lua::globals()
	{
		lua_base.PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
		return std::make_unique<LuaObject>(lua_base, lua_base.ReferenceCreate());
	}

	std::unique_ptr<ILuaObject> Lua::create_string(const std::string& str)
	{
		lua_base.PushString(str.c_str());
		return std::make_unique<LuaObject>(lua_base, lua_base.ReferenceCreate());
	}
}