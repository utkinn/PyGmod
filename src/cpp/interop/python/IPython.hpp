#pragma once

#include <cstdarg>
#include <string>

#include <Python.h>

namespace pygmod::interop::python
{
    class IPython
    {
    public:
        virtual PyObject *py_long_from_long(long) = 0;
        virtual void parse_arg_tuple(PyObject *arg_tuple, const char *fmt, ...) = 0;
        virtual void parse_arg_tuple_va(PyObject *arg_tuple, const char *fmt, va_list) = 0;
        virtual PyObject *py_string_from_c_string(const std::string &) = 0;
        virtual PyObject *import_module(const std::string &) = 0;
        virtual PyObject *get_attr(PyObject *obj, const std::string &attr) = 0;
        virtual void raise_exception(PyObject *exception_class, const std::string &message) = 0;
        virtual PyObject *create_module(PyModuleDef &) = 0;
        virtual PyObject *create_tuple(Py_ssize_t) = 0;
        virtual void register_builtin_module(const std::string &module_name, PyObject *(*initfunc)()) = 0;
        virtual void run_string(const std::string &) = 0;
    };
}