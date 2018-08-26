# distutils: language = c++

from libcpp cimport bool
from LuaBase cimport ILuaBase

cpdef enum Special:
    GLOBAL, ENVIRONMENT, REGISTRY

cdef ILuaBase* lua = NULL

def push_special(int type):
    lua.PushSpecial(type)

def push_nil():
    lua.PushNil()

def push_string(const char* val):
    lua.PushString(val)

def push_number(double num):
    lua.PushNumber(num)

def push_bool(bool val):
    lua.PushBool(val)

def pop(int amt=1):
    lua.Pop(amt)

def get_table(int stack_pos):
    lua.GetTable(stack_pos)

def get_field(int stack_pos, const char* name):
    lua.GetField(stack_pos, name)

def set_field(int stack_pos, const char* name):
    lua.SetField(stack_pos, name)

def call(int args, int results):
    lua.Call(args, results)

def get_string(int stack_pos=-1):
    return lua.GetString(stack_pos, <unsigned int*> 0)

def get_number(int stack_pos=-1):
    return lua.GetNumber(stack_pos)

def get_bool(int stack_pos=-1):
    return lua.GetBool(stack_pos)

cdef public setup(ILuaBase* base):
    global lua
    lua = base
