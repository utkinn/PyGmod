#include "Console.hpp"

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
	char buffer[512] = "ERROR: ";
	strcat_s(buffer, 512, message);
	log(buffer);
}

void Console::warn(const char* message) {
	char buffer[512] = "WARN: ";
	strcat_s(buffer, 512, message);
	log(buffer);
}

void Console::println(string message) {
	println(message.c_str());
}

void Console::log(string message) {
	println("[GPython] " + message);
}

void Console::error(string message) {
	log("ERROR: " + message);
}

void Console::warn(string message) {
	log("WARN: " + message);
}

void Console::println(int message) {
	char buffer[10];
	itoa(message, buffer, 10);
	println(buffer);
}

void Console::log(int message) {
	println("[GPython] " + message);
}

void Console::error(int message) {
	log("ERROR: " + message);
}

void Console::warn(int message) {
	log("WARN: " + message);
}
