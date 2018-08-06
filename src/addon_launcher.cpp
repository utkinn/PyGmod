#include "addon_launcher.hpp"

using std::string;
using namespace std;
namespace fs = filesystem;

const auto PYTHON_ADDONS_PATH = fs::path("garrysmod\\addons_python");
const auto PYTHON_ADDONS_PATH_STR = PYTHON_ADDONS_PATH.string();
const auto PYTHON_ADDONS_PATH_ABSOLUTE_STR = fs::absolute(PYTHON_ADDONS_PATH).string();

void launchAddons(Console& cons) {
	cons.log("Started addon loading process");

	if (!fs::is_directory(PYTHON_ADDONS_PATH)) {
		cons.log("WARN: " + PYTHON_ADDONS_PATH_STR + " (" + PYTHON_ADDONS_PATH_ABSOLUTE_STR + ") directory does not exist");
		return;
	}

	fs::directory_iterator iter;
	try {
		iter = fs::directory_iterator(PYTHON_ADDONS_PATH);
	} catch (fs::filesystem_error) {
		cons.log("ERROR: Can't create directory_iterator for path " + PYTHON_ADDONS_PATH.string() + " (" + fs::absolute(PYTHON_ADDONS_PATH).string() + ")");
		return;
	}

	for (auto& dir : iter) {
		const fs::path initPath(dir.path() / fs::path("python\\__init__.py"));
		if (!fs::is_regular_file(initPath)) continue;
		
		const string initPathStr = initPath.string();

		cons.log("Found addon init script: " + initPathStr);
		cons.log("Loading " + initPathStr);

		const char* cPath = initPathStr.c_str();
		FILE *file = _Py_fopen(cPath, "r");
		PyRun_SimpleFile(file, cPath);

		cons.log("Loaded " + initPathStr);
	}

	cons.log("Addon loading process finished");
}
