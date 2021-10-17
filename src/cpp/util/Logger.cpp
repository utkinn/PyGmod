#include "Logger.hpp"

#include <stdexcept>

using std::string;

namespace pygmod::util
{
    static string log_level_to_label(const LogLevel level)
    {
        switch (level)
        {
        case LogLevel::ERROR:
            return "ERROR";
        case LogLevel::WARNING:
            return "WARNING";
        case LogLevel::INFO:
            return "INFO";
        case LogLevel::DEBUG:
            return "DEBUG";
        }

        throw std::invalid_argument(string("invalid log level: ") + std::to_string(static_cast<int>(level)));
    }

    void Logger::print(const std::string &message)
    {
        lua->PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
        lua->GetField(-1, "Msg");
        lua->PushString(message.c_str());
        lua->Call(1, 0);
        lua->Pop();
    }

    void Logger::print(const LogLevel level, const std::string &message)
    {
        print(log_level_to_label(level));
        print(": ");
        print(message);
    }
}