#include "Python.hpp"

#include <Python.h>

namespace pygmod::init
{
	Python::Python(const std::wstring& home, const std::wstring& path)
	{
		Py_SetPythonHome(home.c_str());
		Py_SetPath(path.c_str());
	}
}
