#pragma once

#include <string>

#include "IFileSystem.hpp"

namespace pygmod::init
{
	class PythonPathProvider
	{
	public:
		PythonPathProvider(IFileSystem& fs) : fs(fs) {}

		std::wstring get_home() const;
		std::wstring get_path() const;

	private:
		IFileSystem& fs;

		std::filesystem::path get_home_path_object() const;
	};
}