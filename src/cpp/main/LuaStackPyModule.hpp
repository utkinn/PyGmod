#pragma once

#include <memory>

#include <GarrysMod/Lua/Interface.h>
#include <Python.h>
#include "ILua.hpp"
#include "IPython.hpp"

namespace pygmod::py_extension
{
	void set_lua_base_instance(GarrysMod::Lua::ILuaBase*);
	void set_python_instance(const std::shared_ptr<init::IPython>&);
	void init();
}