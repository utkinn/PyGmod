#pragma once

#include <GarrysMod/Lua/Interface.h>
#include "ILogger.hpp"

namespace pygmod::init
{
	class Logger : public ILogger
	{
	public:
		Logger(GarrysMod::Lua::ILuaBase* lua) : lua(lua) {}

		void print(const std::string&) override;
		void print(const LogLevel, const std::string&) override;

	private:
		GarrysMod::Lua::ILuaBase* lua;
	};
}