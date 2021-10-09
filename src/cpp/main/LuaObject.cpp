#include "LuaObject.hpp"

#include <cstdarg>

namespace pygmod::init
{
	LuaObject::~LuaObject()
	{
		lua_base.ReferenceFree(_ref);
	}

	std::unique_ptr<ILuaObject> LuaObject::operator[](const char* key)
	{
		lua_base.ReferencePush(ref());
		lua_base.GetField(-1, key);
		const auto field_ref = lua_base.ReferenceCreate();
		lua_base.Pop();
		return std::make_unique<LuaObject>(lua_base, field_ref);
	}

	void LuaObject::operator()(int n_args, ...)
	{
		lua_base.ReferencePush(ref());

		va_list arg_list;
		va_start(arg_list, n_args);
		for (int i = 0; i < n_args; i++)
		{
			auto& arg = va_arg(arg_list, ILuaObject*);
			lua_base.ReferencePush(arg->ref());
		}
		va_end(arg_list);

		lua_base.Call(n_args, 0);
	}

	int LuaObject::ref()
	{
		return _ref;
	}
}