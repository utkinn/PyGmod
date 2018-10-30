#pragma once

#include "GarrysMod/Lua/Interface.h"
#include <string>

using namespace GarrysMod::Lua;
using std::string;

struct Color {
    int r, g, b;
};

// Provides printing and logging functionality to Garry's Mod console.
class Console {
public:
    Console(ILuaBase *lua) : lua(lua) {};

    // string overloads

    // Prints message to the console.
    void println(string message);

    // Prints message to the console with a color.
    void println(string message, Color& color);

    // Prints "[PyGmod] " + message to the console.
    void log(string message);

    // Prints "[PyGmod] ERROR: " + message to the console.
    void error(string message);

    // Prints "[PyGmod] WARN: " + message to the console.
    void warn(string message);

    // const char* overloads

    // Prints message to the console.
    void println(const char* message);

    // Prints message to the console with a color.
    void println(const char* message, Color& color);

    // Prints "[PyGmod] " + message to the console.
    void log(const char* message);

    // Prints "[PyGmod] ERROR: " + message to the console.
    void error(const char* message);

    // Prints "[PyGmod] WARNING: " + message to the console.
    void warn(const char* message);

    // int overloads

    // Prints message to the console.
    void println(int message);

    // Prints message to the console with a color.
    void println(int message, Color& color);

    // Prints "[PyGmod] " + message to the console.
    void log(int message);

    // Prints "[PyGmod] ERROR: " + message to the console.
    void error(int message);

    // Prints "[PyGmod] WARNING: " + message to the console.
    void warn(int message);

private:
    ILuaBase *lua;
};
