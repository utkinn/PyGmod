#pragma once

#include <GarrysMod/Lua/Interface.h>
#include "IPythonToLuaValueConverter.hpp"

namespace pygmod::converters
{
	class PythonToLuaValueConverter : public IPythonToLuaValueConverter
	{
	public:
		PythonToLuaValueConverter(GarrysMod::Lua::ILuaBase* lua) : lua(lua) {}

		void convert(PyObject*) override;

	private:
		GarrysMod::Lua::ILuaBase* lua;
	};
}