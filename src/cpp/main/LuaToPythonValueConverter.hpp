#pragma once

#include <GarrysMod/Lua/Interface.h>
#include <Python.h>
#include "ILuaToPythonValueConverter.hpp"

namespace pygmod::converters
{
	class LuaToPythonValueConverter : public ILuaToPythonValueConverter
	{
	public:
		LuaToPythonValueConverter(GarrysMod::Lua::ILuaBase* lua) : lua(lua) {}

		PyObject* convert(int stack_index) override;

	private:
		GarrysMod::Lua::ILuaBase* lua;
	};
}