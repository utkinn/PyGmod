#include "Logger.hpp"

#include <stdexcept>

using std::string;

namespace pygmod::init
{
	static string log_level_to_label(const LogLevel level)
	{
		switch (level)
		{
		case LogLevel::ERROR: return "ERROR";
		case LogLevel::WARNING: return "WARNING";
		case LogLevel::INFO: return "INFO";
		case LogLevel::DEBUG: return "DEBUG";
		}

		throw std::invalid_argument(string("invalid log level: ") + std::to_string(static_cast<int>(level)));
	}

	void Logger::print(const std::string& message)
	{
		const auto globals = lua.globals();
		const auto msg = (*globals)["Msg"];
		const auto lua_string = lua.create_string(message);
		(*msg)(1, &lua_string);
	}

	void Logger::print(const LogLevel level, const std::string& message)
	{
		print(log_level_to_label(level));
		print(": ");
		print(message);
	}
}