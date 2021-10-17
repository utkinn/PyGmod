#pragma once

#include <Python.h>

namespace pygmod::interop::converters
{
	class ILuaToPythonValueConverter
	{
	public:
		virtual PyObject* convert(int stack_index) = 0;
	};
}