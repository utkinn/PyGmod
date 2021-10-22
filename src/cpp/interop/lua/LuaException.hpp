#pragma once

#include <exception>
#include <string>

namespace pygmod::interop::lua
{
    class LuaException : public std::exception
    {
    public:
        LuaException(const char *msg) : msg(msg)
        {
        }

        const char *what() const noexcept override
        {
            return msg;
        }

    private:
        const char *msg;
    };
}