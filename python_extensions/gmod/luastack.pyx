# distutils: language = c++

"""Functions for manipulating the Lua stack. The lowest level of Garry's Mod Lua interoperability."""

from libcpp cimport bool
from .LuaBase cimport ILuaBase


cpdef enum Special:
    GLOBAL, ENVIRONMENT, REGISTRY


# ILuaBase pointer.
# Being set in ``setup()``.
cdef ILuaBase* lua = NULL


cdef public setup(ILuaBase* base):
    """This function is called in ``giveILuaBasePtrToLuastack()`` in ``main.cpp`` of the C++ module."""
    global lua
    lua = base


def push_special(int type):
    lua.PushSpecial(type)


def push_nil():
    """Pushes ``nil`` to the top of the stack."""
    lua.PushNil()


def push_string(const char* val):
    """Pushes the specified ``bytes`` to the top of the stack."""
    lua.PushString(val)


def push_number(double num):
    """Pushes the specified ``int``/``float`` to the top of the stack."""
    lua.PushNumber(num)


def push_bool(bool val):
    """Pushes the specified boolean to the top of the stack."""
    lua.PushBool(val)


def pop(int amt=1):
    """Removes ``amt`` values from the top of the stack."""
    lua.Pop(amt)


def get_table(int stack_pos):
    lua.GetTable(stack_pos)


def get_field(int stack_pos, const char* name):
    """Gets the value for key ``name`` of a table at index ``stack_pos``
       of the stack and puts that value to the top of the stack.

    Negative values can be used for indexing the stack from top.
    """
    lua.GetField(stack_pos, name)


def set_field(int stack_pos, const char* name):
    """Sets the topmost item in the stack as the value
       for key ``name`` of a table at index ``stack_pos`` of the stack.

    Negative values can be used for indexing the stack from top.
    """
    lua.SetField(stack_pos, name)


def call(int args, int results):
    """Calls the topmost function in the stack using ``args`` items after the function as arguments
       and puts ``results`` items to the top of the stack."""
    lua.Call(args, results)


def get_string(int stack_pos=-1):
    """Returns the ``bytes`` value of a string item at ``stack_pos`` index of the stack.

    Negative values can be used for indexing the stack from top.
    """
    return lua.GetString(stack_pos, <unsigned int*> 0)


def get_number(int stack_pos=-1):
    """Returns the ``float`` value of a number item at ``stack_pos`` index of the stack.

    Negative values can be used for indexing the stack from top.
    """
    return lua.GetNumber(stack_pos)


def get_bool(int stack_pos=-1):
    """Returns the boolean value of a boolean item at ``stack_pos`` index of the stack.

    Negative values can be used for indexing the stack from top.
    """
    return lua.GetBool(stack_pos)
