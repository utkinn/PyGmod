#pragma once

#include <string>

#include "LogLevel.hpp"

namespace pygmod::util
{
    class ILogger
    {
    public:
        virtual void print(const std::string &) = 0;
        virtual void print(LogLevel, const std::string &) = 0;

        void println(const std::string &message)
        {
            print(message + "\n");
        }

        void println(const LogLevel level, const std::string &message)
        {
            print(level, message + "\n");
        }
    };
}