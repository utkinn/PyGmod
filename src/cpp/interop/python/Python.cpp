#include "Python.hpp"

#include <cstdarg>
#include <string>

#include "PythonException.hpp"
#include <Python.h>

using std::string;

namespace pygmod::interop::python
{
    Python::Python(const std::wstring &home, const std::wstring &path)
    {
        Py_SetPythonHome(home.c_str());
        Py_SetPath(path.c_str());
    }

    Python::~Python()
    {
        Py_FinalizeEx();
    }

    void Python::init()
    {
        Py_Initialize();
    }

    PyObject *Python::py_long_from_long(long l)
    {
        return PyLong_FromLong(l);
    }

    void Python::parse_arg_tuple(PyObject *arg_tuple, const char *fmt, ...)
    {
        va_list args;
        va_start(args, fmt);
        try
        {
            return parse_arg_tuple_va(arg_tuple, fmt, args);
        }
        catch (...)
        {
            va_end(args);
            throw;
        }
        va_end(args);
    }

    void Python::parse_arg_tuple_va(PyObject *arg_tuple, const char *fmt, va_list args)
    {
        const auto ret = PyArg_VaParse(arg_tuple, fmt, args);

        if (!ret)
        {
            throw PythonException("failed to parse argument tuple tuple");
        }
    }

    PyObject *Python::py_string_from_c_string(const string &s)
    {
        return PyUnicode_FromString(s.c_str());
    }

    PyObject *Python::import_module(const string &module_name)
    {
        const auto module_obj = PyImport_ImportModule(module_name.c_str());
        if (!module_obj)
        {
            string msg = "failed to import the ";
            msg += module_name;
            msg += " module";
            throw PythonException(msg.c_str());
        }
        return module_obj;
    }

    PyObject *Python::get_attr(PyObject *obj, const string &attr)
    {
        return PyObject_GetAttrString(obj, attr.c_str());
    }

    void Python::raise_exception(PyObject *exception_class, const string &message)
    {
        PyErr_SetString(exception_class, message.c_str());
    }

    PyObject *Python::create_module(PyModuleDef &module_def)
    {
        return PyModule_Create(&module_def);
    }

    PyObject *Python::create_tuple(Py_ssize_t size)
    {
        return PyTuple_New(size);
    }

    void Python::register_builtin_module(const string &module_name, PyObject *(*initfunc)())
    {
        const auto result = PyImport_AppendInittab(module_name.c_str(), initfunc);
        if (result == -1)
        {
            throw PythonException("failed to register builtin module");
        }
    }

    void Python::run_string(const string &code)
    {
        PyRun_SimpleString(code.c_str());

        PyObject *exc_type, *exc_value, *exc_traceback;
        PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);

        if (exc_value)
        {
            const auto exc_as_py_string = PyObject_Str(exc_value);
            const auto exc_as_c_string = PyUnicode_AsUTF8(exc_as_py_string);
            Py_XDECREF(exc_as_py_string);
            Py_XDECREF(exc_type);
            Py_XDECREF(exc_value);
            Py_XDECREF(exc_traceback);
            throw PythonException(exc_as_c_string);
        }
    }
}
