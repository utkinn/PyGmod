#pragma once

#include <exception>
#include <string>

namespace pygmod::init
{
    class InitException : public std::exception
    {
    public:
        InitException(const char *message) : message(message)
        {
        }

        const char *what() const noexcept override
        {
            return message;
        }

    private:
        const char *message;
    };
}