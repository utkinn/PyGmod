#pragma once

#include <string>

#include "util/IFileSystem.hpp"

namespace pygmod::interop::python
{
    class PythonPathProvider
    {
    public:
        PythonPathProvider(util::IFileSystem &fs) : fs(fs)
        {
        }

        std::wstring get_home() const;
        std::wstring get_path() const;

    private:
        util::IFileSystem &fs;

        std::filesystem::path get_home_path_object() const;
    };
}