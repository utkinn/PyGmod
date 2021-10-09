#include "PythonFactory.hpp"

#include "IPython.hpp"
#include "Python.hpp"

namespace pygmod::init
{
	IPython PythonFactory::create_python(const std::wstring& home, const std::wstring& path)
	{
		return Python(home, path);
	}
}