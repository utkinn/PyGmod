#pragma once

#include <cstdarg>
#include <string>

#include "IPython.hpp"
#include <gmock/gmock.h>

namespace pygmod::testing
{
    class PythonMock : public init::IPython
    {
    public:
        MOCK_METHOD(PyObject *, py_long_from_long, (long), (override));
        MOCK_METHOD(void, parse_arg_tuple_va, (PyObject * arg_tuple, const std::string &fmt, va_list), (override));

        void parse_arg_tuple(PyObject *arg_tuple, const std::string &fmt, ...) override
        {
            va_list args;
            va_start(args, fmt);

            try
            {
                parse_arg_tuple_va(arg_tuple, fmt, args);
            }
            catch (...)
            {
                va_end(args);
                throw;
            }

            va_end(args);
        }

        MOCK_METHOD(PyObject *, py_string_from_c_string, (const std::string &), (override));
        MOCK_METHOD(PyObject *, import_module, (const std::string &), (override));
        MOCK_METHOD(PyObject *, get_attr, (PyObject * obj, const std::string &attr), (override));
        MOCK_METHOD(void, raise_exception, (PyObject * exception_class, const std::string &message), (override));
        MOCK_METHOD(PyObject *, create_module, (PyModuleDef &), (override));
        MOCK_METHOD(PyObject *, create_tuple, (Py_ssize_t), (override));
        MOCK_METHOD(void, register_builtin_module, (const std::string &module_name, PyObject *(*initfunc)()), (override));
        MOCK_METHOD(void, run_string, (const std::string &), (override));
    };
}
