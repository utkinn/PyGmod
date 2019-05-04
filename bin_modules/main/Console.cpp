#include "Console.hpp"

using std::to_string;

void Console::println(const char* message) {
    lua->PushSpecial(SPECIAL_GLOB);  // Pushing global table to stack

    lua->GetField(-1, "print");  // Getting "print" field of the global table
    lua->PushString(message);  // Pushing the message
    lua->Call(1, 0);  // Calling "print" with 1 argument and 0 return values and popping the function and the arguments from the stack

    lua->Pop();  // Popping the global table from the stack
}

void Console::println(const char* message, Color& color) {
    lua->PushSpecial(SPECIAL_GLOB);  // Pushing global table to stack

    lua->GetField(-1, "MsgC");  // Getting "MsgC" field of the global table

    // Creating Color structure
    lua->GetField(-2, "Color");
    // Stack here: _G, MsgC, Color
    lua->PushNumber(color.r);
    lua->PushNumber(color.g);
    lua->PushNumber(color.b);
    // Stack here: _G, MsgC, Color, r, g, b
    lua->Call(3, 1);
    // Stack here: _G, MsgC, Color structure(r, g, b)

    lua->PushString(message);  // Pushing the message
    lua->PushString("\n");  // Adding a newline
    lua->Call(3, 0);  // Calling "MsgC" with 3 arguments (color, message, newline) and 0 return values and popping the function and the arguments from the stack

    lua->Pop();  // Popping the global table from the stack
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

void Console::println(string message, Color& color) {
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

void Console::println(int message, Color& color) {
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
