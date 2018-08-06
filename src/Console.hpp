#pragma once

#include "GarrysMod/Lua/Interface.h"
#include <string>

using namespace GarrysMod::Lua;
using std::string;

// Provides access for Garry's Mod developer console logging.
class Console {
public:
	Console(ILuaBase *lua) : lua(lua) {};

	// Prints message to the console.
	void println(string message);

	// Prints "[GPython] " + message to the console.
	void log(string message);

	// Prints "[GPython] ERROR: " + message to the console.
	void error(string message);

	// Prints "[GPython] WARN: " + message to the console.
	void warn(string message);

private:
	ILuaBase *lua;
};
