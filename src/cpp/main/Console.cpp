#include "Console.hpp"

static const Color RED = {255, 0, 0};

using std::to_string;

void Console::println(const char* message) {
    lua->PushSpecial(SPECIAL_GLOB);  // Pushing "_G" to the stack, +1 = 1

    lua->GetField(-1, "print");  // Getting the "print" function from "_G", +1 = 2
    lua->PushString(message);  // Pushing the message, +1 = 3
    // Calling "print" with 1 argument and 0 return values
    // and popping the function and the arguments from the stack,
    // -1 function and -1 argument = 1
    lua->Call(1, 0);

    lua->Pop();  // Popping "_G" off the stack, -1 = 0
}

// Helper for println(const char*, Color) which creates a
// Lua Color structure from our C++ Color structure
// and leaves it at the top of the Lua stack.
// This function expects _G to be at the top of the stack.
void Console::_pushColor(Color &color) {
    // Getting the "Color" function, +1 = 2
    lua->GetField(-2, "Color");
    // Stack contents here: _G, Color() (2)
    lua->PushNumber(color.r);
    lua->PushNumber(color.g);
    lua->PushNumber(color.b);
    // Stack contents here: _G, Color(), r, g, b (5)
    lua->Call(3, 1);  // -3 args, -1 function, +1 return value = 2
    // Stack contents here: _G, Color(r, g, b)
}

void Console::println(const char* message, Color color) {
    lua->PushSpecial(SPECIAL_GLOB);  // Pushing "_G" to the stack, +1 = 1

    lua->GetField(-1, "MsgC");  // Getting "MsgC" function from "_G", +1 = 2

    _pushColor(color);

    lua->PushString(message);  // Pushing the message
    lua->PushString("\n");  // Adding a newline
    // Calling "MsgC" with 3 arguments (color, message, newline)
    // and 0 return values and popping the function and the arguments from the stack
    lua->Call(3, 0);

    lua->Pop();  // Popping "_G" off the stack, -1 = 0
}

void Console::log(const char* message) {
    println(("[PyGmod|pygmod.dll|LOG] " + string(message)).c_str());
}

void Console::error(const char* message) {
    println(("[PyGmod|pygmod.dll|ERROR] " + string(message)).c_str(), Color{ 255, 0, 0 });
}

void Console::warn(const char* message) {
    println(("[PyGmod|pygmod.dll|WARNING] " + string(message)).c_str(), Color{ 255, 255, 0 });
}

void Console::println(string message) {
    println(message.c_str());
}

void Console::println(string message, Color color) {
    println(message.c_str(), color);
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

void Console::println(int message, Color color) {
    println(to_string(message), color);
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
