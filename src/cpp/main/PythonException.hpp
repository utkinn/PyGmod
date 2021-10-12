#pragma once

#include <exception>

namespace pygmod::init
{
    class PythonException : public std::exception
    {
    public:
        PythonException(const char *message) : std::exception(message) {}
    };
}
