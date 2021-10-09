#pragma once

#include <string>

#include "IPython.hpp"
#include "IPythonFactory.hpp"

namespace pygmod::init
{
	class PythonFactory : public IPythonFactory
	{
	public:
		IPython create_python(const std::wstring& home, const std::wstring& path) override;
	};
}