#include "FileSystem.hpp"

using std::filesystem::path;

namespace pygmod::init
{
	path FileSystem::get_current_path()
	{
		return std::filesystem::current_path();
	}

	bool FileSystem::exists(const path& path) const
	{
		return std::filesystem::exists(path);
	}
}