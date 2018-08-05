#pragma once

#include "GarrysMod/Lua/Interface.h"
#include <string>

using namespace GarrysMod::Lua;
using std::string;

class Console {
public:
	Console(ILuaBase *lua) : lua(lua) {};

	// Prints message to the console.
	void println(string message);

	// Prints "[GPython] " + message to the console.
	void log(string message);

private:
	ILuaBase *lua;
};
