#pragma once

#include <memory>

#include <GarrysMod/Lua/Interface.h>
#include "ILua.hpp"

namespace pygmod::init
{
	class Lua : public ILua
	{
	public:
		Lua(GarrysMod::Lua::ILuaBase& lua_base) : lua_base(lua_base) {}

		std::unique_ptr<ILuaObject> globals() override;
		std::unique_ptr<ILuaObject> create_string(const std::string&) override;

	private:
		GarrysMod::Lua::ILuaBase& lua_base;
	};
}