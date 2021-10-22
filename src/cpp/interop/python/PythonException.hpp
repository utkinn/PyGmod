#pragma once

#include <exception>
#include <string>

namespace pygmod::interop::python
{
    class PythonException : public std::exception
    {
    public:
        PythonException(const char *message) : message(message)
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
