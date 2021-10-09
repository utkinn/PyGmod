#pragma once

#include <memory>

namespace pygmod::init
{
	class ILuaObject
	{
	public:
		virtual std::unique_ptr<ILuaObject> operator[](const char*) = 0;
		virtual void operator()(int, ...) = 0;
		virtual int ref() = 0;
	};
}