#pragma once

#include <fstream>
#include <filesystem>

#include <Python.h>

#include "Console.hpp"

// Runs __init__.py scripts of all Python addons from PYTHON_ADDONS_PATH directory.
void launchAddons(Console& cons, bool client);
