#include <string>
#include "Console.hpp"
#include "stack_dump.hpp"

using namespace GarrysMod::Lua;

void stackDump(ILuaBase *lua) {
    Console cons(lua);
    const char *bar = "---------------------------";

    cons.log(bar);
    cons.log("LUA STACK DUMP");

	for (int i = 1; i <= lua->Top(); i++) {
		int valType = lua->GetType(i);
		const char *valTypeName = lua->GetTypeName(valType);
		std::string repr;
		switch (valType) {
		case Type::Nil:
			repr = "nil";
			break;
		case Type::Number:
			repr = std::to_string(lua->GetNumber(i));
			break;
		case Type::String:
			repr = lua->GetString(i);
			break;
		}
        cons.log(std::to_string(i) + ": " + valTypeName + " (" + repr + ")");
	}

	cons.log(bar);
}
