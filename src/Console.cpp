#include "Console.hpp"

using std::to_string;

void Console::println(const char* message) {
	lua->PushSpecial(SPECIAL_GLOB);  // Pushing global table to stack

	lua->GetField(-1, "print");  // Getting "print" field of the global table
	lua->PushString(message);  // Pushing the message
	lua->Call(1, 0);  // Calling "print" with 1 argument and 0 return values and popping the function and the arguments from the stack

	lua->Pop();  // Popping the global table from the stack
}

void Console::log(const char* message) {
	println(("[GPython] " + string(message)).c_str());
}

void Console::error(const char* message) {
	log(("ERROR: " + string(message)).c_str());
}

void Console::warn(const char* message) {
	log(("WARNING: " + string(message)).c_str());
}

void Console::println(string message) {
	println(message.c_str());
}

void Console::log(string message) {
	log(message.c_str());
}

void Console::error(string message) {
	error(message.c_str());
}

void Console::warn(string message) {
	warn(message.c_str());
}

void Console::println(int message) {
	println(to_string(message));
}

void Console::log(int message) {
	log(to_string(message));
}

void Console::error(int message) {
	error(to_string(message));
}

void Console::warn(int message) {
	warn(to_string(message));
}
