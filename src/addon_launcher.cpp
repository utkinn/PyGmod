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

// Appends the given path to sys.path.
void appendPath(const char* pathString) {
    PyObject *sys = PyImport_ImportModule("sys");
    PyObject *path = PyObject_GetAttrString(sys, "path");
    PyObject *pathPyString = PyUnicode_FromString(pathString);

    PyList_Append(path, pathPyString);

    Py_DECREF(pathPyString);
    Py_DECREF(path);
    Py_DECREF(sys);
}

// Appends GPython modules directory (garrysmod\gpython\) to sys.path.
void appendModulesPath() {
    appendPath("garrysmod\\\\gpython");
}

// Deletes the last item from sys.path.
void deleteLastPath() {
    PyObject *sys = PyImport_ImportModule("sys");
    PyObject *path = PyObject_GetAttrString(sys, "path");

    PySequence_DelItem(path, -1);

    Py_DECREF(path);
    Py_DECREF(sys);
}

// Example: returns "addons" from path "garrysmod\addons".
string getLastPathComponent(fs::path path) {
    string pathString = path.string();
    size_t lastSlashIndex = pathString.find_last_of("\\");
    return pathString.substr(lastSlashIndex + 1, string::npos);
}

// Returns true if there is "garrysmod\addons_python" directory, returns false and prints a warning otherwise.
bool checkAddonsDirectoryPresence(Console& cons) {
    const bool exists = fs::is_directory(PYTHON_ADDONS_PATH);

    if (!exists)
        cons.warn(PYTHON_ADDONS_PATH_STR + " (" + PYTHON_ADDONS_PATH_ABSOLUTE_STR + ") directory does not exist");

    return exists;
}

// Returns true if there is __init__.py in (addonDir)\python directory, returns false and prints a warning otherwise.
bool checkInitScriptPresence(Console& cons, fs::path addonDir) {
    const fs::path initScriptPath = addonDir / fs::path("python\\__init__.py");  // Path of the assumed __init__.py
    const bool exists = fs::is_regular_file(initScriptPath);

    if (!exists)
        cons.warn("__init__.py not found in " + addonDir.string() + ", skipping.");

    return exists;
}

// Imports an addon from given addon directory.
void importAddon(Console& cons, fs::path addonDir) {
    Py_DECREF(PyImport_ImportModule((getLastPathComponent(addonDir) + ".python").c_str()));
    deleteLastPath();

    if (PyErr_Occurred()) {
        cons.error("During execution of " + addonDir.string());
        return;
    }
}

void launchAddons(Console& cons) {
    appendModulesPath();

	cons.log("Started addon loading process");

	// Checking if Python addons directory exists at all.
	// Issuing a warning and finishing loading if it doesn't exist.
	if (!checkAddonsDirectoryPresence(cons))
		return;

	fs::directory_iterator iter;
	try {
		// Trying to create Python addon folder iterator
		iter = fs::directory_iterator(PYTHON_ADDONS_PATH);
	} catch (fs::filesystem_error) {
		cons.error("Can't create directory_iterator for path " + PYTHON_ADDONS_PATH_STR + " (" + PYTHON_ADDONS_PATH_ABSOLUTE_STR + ")");
		return;
	}

	// Iterating through the Python addon folder
	for (auto& dir : iter) {
        const fs::path& dirPath = dir.path();  // Addon directory path
        const string dirPathString = dirPath.string(); // Addon directory path as string

        if (!checkInitScriptPresence(cons, dirPath))
            continue;

		cons.log("Found addon: " + dirPathString + ", loading...");

        appendPath(PYTHON_ADDONS_PATH_STR.c_str());  // Appending "garrysmod\addons_python" to sys.path, so we can import addons from its subdirectiories
        importAddon(cons, dirPath);

		cons.log("Loaded " + dirPathString);
	}

	cons.log("Addon loading process finished");
}
