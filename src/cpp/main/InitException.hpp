#pragma once

#include <exception>
#include <string>

namespace pygmod::init
{
	class InitException : std::exception
	{
	public:
		InitException(const char* message) : std::exception(message) {}
	};
}