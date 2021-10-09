#pragma once

#include <string>

namespace pygmod::init
{
	class IPythonFactory
	{
	public:
		virtual IPython create_python(const std::wstring& home, const std::wstring& path) = 0;
	};
}