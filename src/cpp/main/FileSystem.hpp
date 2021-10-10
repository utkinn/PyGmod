#pragma once

#include <filesystem>

#include "IFileSystem.hpp"

namespace pygmod::init
{
	class FileSystem : public IFileSystem
	{
	public:
		std::filesystem::path get_current_path() override;
		bool exists(const std::filesystem::path&) const override;
	};
}