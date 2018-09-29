#include "addon_launcher.hpp"

using std::string;
using namespace std;
namespace fs = filesystem;

// fs::path of directory where Python addons reside.
const auto PYTHON_ADDONS_PATH = fs::path("garrysmod\\addons");

// PYTHON_ADDONS_PATH as string.
const auto PYTHON_ADDONS_PATH_STR = PYTHON_ADDONS_PATH.string();

// Absolute PYTHON_ADDONS_PATH as string.
const auto PYTHON_ADDONS_PATH_ABSOLUTE_STR = fs::absolute(PYTHON_ADDONS_PATH).string();

// Appends the given path to sys.path.
void appendPath(const char* pathString) {
    PyObject *path = PySys_GetObject("path");
    Py_INCREF(path);
    PyObject *pathPyString = PyUnicode_FromString(pathString);

    PyList_Append(path, pathPyString);

    Py_DECREF(pathPyString);
    Py_DECREF(path);
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

// Returns true if there is "garrysmod\addons" directory, returns false and prints a warning otherwise.
bool checkAddonsDirectoryPresence(Console& cons) {
    const bool exists = fs::is_directory(PYTHON_ADDONS_PATH);

    if (!exists)
        cons.warn(PYTHON_ADDONS_PATH_STR + " (" + PYTHON_ADDONS_PATH_ABSOLUTE_STR + ") directory does not exist");

    return exists;
}

// Returns true if there is __init__.py in any (addonDir)\python\__*_autorun__ directory, returns false otherwise.
bool checkInitScriptPresence(fs::path addonDir) {
    const fs::path addonCodePath = addonDir / fs::path("python");
    const bool isGPythonAddon = fs::is_regular_file(addonCodePath / fs::path("__shared_autorun__\\__init__.py")) 
                                || fs::is_regular_file(addonCodePath / fs::path("__client_autorun__\\__init__.py"))
                                || fs::is_regular_file(addonCodePath / fs::path("__server_autorun__\\__init__.py"));

    return isGPythonAddon;
}

// Prints a traceback surrounded by bars.
void printTraceback(Console& cons) {
    const string bar = "________________________________________________________________________________________________________________________\n";
    Color c{ 255, 0, 0 };

    cons.println(bar, c);
    PyErr_Print();
    cons.println(bar, c);
}

// Imports a single package "(addonDir).python.(pkgName)".
void importPkg(Console& cons, fs::path &addonDir, string pkgName) {
    PyObject *pkg = PyImport_ImportModule((getLastPathComponent(addonDir) + ".python." + pkgName).c_str());
    if (pkg != nullptr)  // exception not occurred
        Py_DECREF(pkg);  // Freeing reference
    else {
        cons.warn("package " + pkgName + " at " + addonDir.string() + " not found.");
        PyErr_Clear();
    }
}

// Imports an addon from given addon directory.
void importAddon(Console& cons, fs::path addonDir, bool client) {
    // Selecting a realm-dependent package
    string realmAutorunPackage = client ? "__client_autorun__" : "__server_autorun__";

    // Importing shared code package
    importPkg(cons, addonDir, "__shared_autorun__");
    // Importing realm-dependent package
    importPkg(cons, addonDir, realmAutorunPackage);

    if (PyErr_Occurred()) {
        cons.error("During execution of " + addonDir.string());
        return;
    }
}

void launchAddons(Console& cons, bool client) {
	cons.log("Started addon loading process");

	// Checking if Python addons directory exists at all.
	// Issuing a warning and finishing loading if it doesn't exist.
	if (!checkAddonsDirectoryPresence(cons))
		return;

    appendPath(fs::absolute(PYTHON_ADDONS_PATH).string().c_str());  // Appending "garrysmod\addons" to sys.path, so we can import addons from its subdirectiories

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

        if (!checkInitScriptPresence(dirPath))
            continue;

		cons.log("Found addon: " + dirPathString + ", loading...");
        
        // Appending the (addon)\python\ dir to sys.path, so packages and modules in this dir can be imported by scripts in __*_autorun__
        appendPath((dirPath / fs::path("python")).string().c_str());
        importAddon(cons, dirPath, client);
        PyRun_SimpleString("del sys.path[-1]");  // Removing that path to avoid collision between addons

		cons.log("Loaded " + dirPathString);
	}

	cons.log("Addon loading process finished");
}
