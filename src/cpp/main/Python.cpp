#include "Python.hpp"

#include <cstdarg>

#include <Python.h>
#include "PythonException.hpp"

namespace pygmod::init
{
	Python::Python(const std::wstring& home, const std::wstring& path)
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

	PyObject* Python::py_long_from_long(long l)
	{
		return PyLong_FromLong(l);
	}

	void Python::parse_arg_tuple(PyObject *arg_tuple, const char *fmt, ...)
	{
		va_list args;
		va_start(args, fmt);
		const auto ret = PyArg_VaParse(arg_tuple, fmt, args);
		va_end(args);

		if (!ret)
		{
			throw PythonException("failed to parse argument tuple tuple");
		}
	}

	PyObject* Python::py_string_from_c_string(const char* s)
	{
		return PyUnicode_FromString(s);
	}

	PyObject* Python::get_attr(PyObject* obj, const char* attr)
	{
		return PyObject_GetAttrString(obj, attr);
	}

	void Python::raise_exception(PyObject* exception_class, const char* message)
	{
		PyErr_SetString(exception_class, message);
	}

	PyObject* Python::create_module(PyModuleDef& module_def)
	{
		return PyModule_Create(&module_def);
	}

	void Python::register_builtin_module(const char* module_name, PyObject* (*initfunc)())
	{
		const auto result = PyImport_AppendInittab(module_name, initfunc);
		if (result == -1)
		{
			throw PythonException("failed to register builtin module");
		}
	}
}
