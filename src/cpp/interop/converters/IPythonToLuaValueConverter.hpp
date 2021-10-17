#pragma once

#include <Python.h>

namespace pygmod::interop::converters
{
	class IPythonToLuaValueConverter
	{
	public:
		virtual void convert(PyObject*) = 0;
	};
}