#pragma once

#include <string>
#include <memory>

#include <GarrysMod/Lua/Interface.h>
#include "ILuaObject.hpp"

namespace pygmod::init
{
	class LuaObject : public ILuaObject
	{
	public:
		LuaObject(GarrysMod::Lua::ILuaBase& lua_base, int ref) : lua_base(lua_base), _ref(ref) {}
		~LuaObject();

		std::unique_ptr<ILuaObject> operator[](const char*) override;
		void operator()(int, ...) override;
		int ref() override;

	private:
		GarrysMod::Lua::ILuaBase& lua_base;
		int _ref;
	};
}