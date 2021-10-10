#pragma once

#include <string>

#include "IPython.hpp"

namespace pygmod::init
{
	class Python : public IPython
	{
	public:
		Python(const std::wstring& home, const std::wstring& path);
		~Python();

		void init();
	};
}
