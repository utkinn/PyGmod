#include "PythonPathProvider.hpp"

#include <filesystem>

#include "InitException.hpp"

using std::wstring;
using std::filesystem::path;

#ifdef _WIN32
const wstring OS_PATH_SEPARATOR = L";";
#else
const wstring OS_PATH_SEPARATOR = L":";
#endif

namespace pygmod::init
{
	wstring PythonPathProvider::get_home() const
	{
		const auto home = get_home_path_object();
		if (!fs.exists(home))
		{
			throw InitException("Python standard library directory (garrysmod/pygmod/stdlib) not found.");
		}

		return home.wstring();
	}

	wstring PythonPathProvider::get_path() const
	{
		const auto home = get_home_path_object();

		// PYTHONPATH = PYTHONHOME (*.py modules)
		//				+ PYTHONHOME/lib-dynload (binary modules)
		//				+ PYTHONHOME/site-packages (pip packages)
		//				+ ./garrysmod/pygmod (PyGmod modules)

		const auto lib_dynload_path = home / "lib-dynload";
		const auto site_packages_path = home / "site-packages";
		return home.wstring() + OS_PATH_SEPARATOR
			+ lib_dynload_path.wstring() + OS_PATH_SEPARATOR
			+ site_packages_path.wstring() + OS_PATH_SEPARATOR
			+ (fs.get_current_path() / "garrysmod" / "pygmod").wstring();
	}

	path PythonPathProvider::get_home_path_object() const
	{
		return fs.get_current_path() / "garrysmod" / "pygmod" / "stdlib";
	}

}
