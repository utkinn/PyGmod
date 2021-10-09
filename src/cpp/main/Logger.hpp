#pragma once

#include "ILogger.hpp"
#include "ILua.hpp"

namespace pygmod::init
{
	class Logger : public ILogger
	{
	public:
		Logger(ILua& lua) : lua(lua) {}

		void print(const std::string&) override;
		void print(const LogLevel, const std::string&) override;

	private:
		ILua& lua;
	};
}