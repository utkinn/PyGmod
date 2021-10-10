#pragma once

#include <Python.h>

namespace pygmod::converters
{
	class IPythonToLuaValueConverter
	{
	public:
		virtual void convert(PyObject*) = 0;
	};
}