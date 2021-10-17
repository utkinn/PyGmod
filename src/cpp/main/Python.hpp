#pragma once

#include <string>

#include "IPython.hpp"

namespace pygmod::init
{
    class Python : public IPython
    {
    public:
        Python(const std::wstring &home, const std::wstring &path);
        ~Python();

        void init();

        PyObject *py_long_from_long(long) override;
        void parse_arg_tuple(PyObject *arg_tuple, const char *fmt, ...) override;
        PyObject *py_string_from_c_string(const char *) override;
        PyObject *import_module(const char *) override;
        PyObject *get_attr(PyObject *obj, const char *attr) override;
        void raise_exception(PyObject *exception_class, const char *message) override;
        PyObject *create_module(PyModuleDef &) override;
        PyObject *create_tuple(Py_ssize_t) override;
        void register_builtin_module(const char *module_name, PyObject *(*initfunc)()) override;
        void run_string(const char *) override;
    };
}
