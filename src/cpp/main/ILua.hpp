#pragma once

#include <memory>
#include <string>

#include "ILuaObject.hpp"

namespace pygmod::init
{
	class ILua
	{
	public:
		virtual std::unique_ptr<ILuaObject> globals() = 0;
		virtual std::unique_ptr<ILuaObject> create_string(const std::string&) = 0;
	};
}