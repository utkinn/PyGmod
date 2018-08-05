#include "Console.hpp"

void Console::println(string message) {
	lua->PushSpecial(SPECIAL_GLOB);

	lua->GetField(-1, "print");
	lua->PushString(message.c_str());
	lua->Call(1, 0);

	lua->Pop();
}

void Console::log(string message) {
	println("[GPython] " + message);
}
