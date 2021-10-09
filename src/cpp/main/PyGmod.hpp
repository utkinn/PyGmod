#pragma once

namespace pygmod::init
{
	class PyGmod
	{
	public:
		PyGmod() : fs(FileSystem()), path_provider(PythonPathProvider(fs)), python(Python(path_provider.get_home(), path_provider.get_path())) {};
		~PyGmod() {};

	private:
		FileSystem fs;
		const PythonPathProvider path_provider;
		Python python;
	};
}