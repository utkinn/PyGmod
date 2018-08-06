cdef struct lua_State:
    unsigned char _ignore_this_common_lua_header_[69]
    ILuaBase* luabase
