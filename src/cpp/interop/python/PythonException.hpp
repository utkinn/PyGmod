#pragma once

#include <exception>

namespace pygmod::interop::python
{
    class PythonException : public std::exception
    {
    public:
        PythonException(const char *message) : std::exception(message)
        {
        }
    };
}
