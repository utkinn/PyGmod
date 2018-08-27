#include "addon_launcher.hpp"

using std::string;
using namespace std;
namespace fs = filesystem;

// fs::path of directory where Python addons reside.
const auto PYTHON_ADDONS_PATH = fs::path("garrysmod\\addons_python");

// PYTHON_ADDONS_PATH as string.
const auto PYTHON_ADDONS_PATH_STR = PYTHON_ADDONS_PATH.string();

// Absolute PYTHON_ADDONS_PATH as string.
const auto PYTHON_ADDONS_PATH_ABSOLUTE_STR = fs::absolute(PYTHON_ADDONS_PATH).string();

void launchAddons(Console& cons, PyObject *globals) {
	//PyRun_SimpleString((string("import sys,pprint;sys.path.append('") + fs::path("garrysmod\\lua\\bin").string() + string("')")).c_str());
	PyRun_SimpleString((string("import sys,pprint;sys.path.append('garrysmod\\\\lua\\\\bin')")).c_str());  // Temporary stub
    if (PyErr_Occurred()) {
        cons.error("Can't append path");
        return;
    }

	cons.log("Started addon loading process");

	// Checking if Python addons directory exists at all.
	// Issuing a warning and finishing loading if it doesn't exist.
	if (!fs::is_directory(PYTHON_ADDONS_PATH)) {
		cons.log("WARN: " + PYTHON_ADDONS_PATH_STR + " (" + PYTHON_ADDONS_PATH_ABSOLUTE_STR + ") directory does not exist");
		return;
	}

	fs::directory_iterator iter;
	try {
		// Trying to create Python addon folder iterator
		iter = fs::directory_iterator(PYTHON_ADDONS_PATH);
	} catch (fs::filesystem_error) {
		cons.log("ERROR: Can't create directory_iterator for path " + PYTHON_ADDONS_PATH.string() + " (" + fs::absolute(PYTHON_ADDONS_PATH).string() + ")");
		return;
	}

	// Iterating through the Python addon folder
	for (auto& dir : iter) {
		const fs::path initPath(dir.path() / fs::path("python\\__init__.py"));  // Path of the assumed addon init script
		if (!fs::is_regular_file(initPath)) continue;  // Skipping the current directory if there is no init script
		
		const string initPathStr = initPath.string();  // Init script path as string
		cons.log("Found addon init script: " + initPathStr);
		cons.log("Loading " + initPathStr);

		const char* cPath = initPathStr.c_str();  // Init script path as C-style string
		//FILE *file = _Py_fopen(cPath, "r");  // Opening the script file
		//PyRun_SimpleFileEx(file, cPath, 1);  // Running the script. "1" is for closing the script after its execution.
        //PyObject *locals = PyDict_New();
        //PyRun_FileEx(file, cPath, Py_file_input, globals, locals, 1);
        //Py_DECREF(locals);
        PyRun_SimpleString("sys.path.append('garrysmod\\\\addons_python');pprint.pprint(sys.path);import GPythonTest.python;del sys.path[-1]");  // Temporary stub
        if (PyErr_Occurred()) {
            cons.error("During execution");
            return;
        }

		cons.log("Loaded " + initPathStr);
	}

	cons.log("Addon loading process finished");
}
