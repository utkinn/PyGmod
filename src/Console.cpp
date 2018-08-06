#include "Console.hpp"

void Console::println(string message) {
	lua->PushSpecial(SPECIAL_GLOB);  // Pushing global table to stack

	lua->GetField(-1, "print");  // Getting "print" field of the global table
	lua->PushString(message.c_str());  // Pushing the message
	lua->Call(1, 0);  // Calling "print" with 1 argument and 0 return values and popping the function and the arguments from the stack

	lua->Pop();  // Popping the global table from the stack
}

void Console::log(string message) {
	println("[GPython] " + message);
}

void Console::error(string message) {
	log("[GPython] ERROR: " + message);
}

void Console::warn(string message) {
	log("[GPython] WARN: " + message);
}