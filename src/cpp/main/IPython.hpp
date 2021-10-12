#pragma once

namespace pygmod::init
{
	class IPython
	{
	public:
		virtual PyObject *py_long_from_long(long) = 0;
		virtual void parse_arg_tuple(PyObject* arg_tuple, const char* fmt, ...) = 0;
		virtual PyObject *py_string_from_c_string(const char*) = 0;
		virtual PyObject *import_module(const char*) = 0;
		virtual PyObject* get_attr(PyObject* obj, const char* attr) = 0;
		virtual void raise_exception(PyObject* exception_class, const char* message) = 0;
		virtual PyObject* create_module(PyModuleDef&) = 0;
		virtual void register_builtin_module(const char* module_name, PyObject* (*initfunc)()) = 0;
	};
}