#pragma once

#include <filesystem>

namespace pygmod::util
{
    class IFileSystem
    {
    public:
        virtual std::filesystem::path get_current_path() = 0;
        virtual bool exists(const std::filesystem::path &) const = 0;
    };
}