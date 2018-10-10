# distutils: language = c++

"""Functions for manipulating the Lua stack. The lowest level of Garry's Mod Lua interoperability.

Lua uses a virtual stack to pass values to and from C.
Each element in this stack represents a Lua value (``nil``, number, string, etc.).

For convenience, most query operations in the API do not follow a strict stack discipline.
Instead, they can refer to any element in the stack by using an index:

- A positive index represents an absolute stack position (starting at **1**)
- A negative index represents an offset relative to the top of the stack.

More specifically, if the stack has **n** elements, then index **1** represents the first element
(that is, the element that was pushed onto the stack first) and index **n** represents the last element;
index **-1** also represents the last element (that is, the element at the top)
and index **-n** represents the first element.
We say that an index is valid if it lies between **1** and the stack top (that is, if **1 ≤ abs(index) ≤ top**).
"""

from libcpp cimport bool
from LuaBase cimport ILuaBase


cpdef enum Special:
    GLOBAL, ENVIRONMENT, REGISTRY


cpdef enum ValueType:
    NIL,
    BOOL,
    LIGHTUSERDATA,
    NUMBER,
    STRING,
    TABLE,
    FUNCTION,
    USERDATA,
    THREAD,

    # UserData
    ENTITY,
    VECTOR,
    ANGLE,
    PHYSOBJ,
    SAVE,
    RESTORE,
    DAMAGEINFO,
    EFFECTDATA,
    MOVEDATA,
    RECIPIENTFILTER,
    USERCMD,
    SCRIPTEDVEHICLE,

    # Client Only
    MATERIAL,
    PANEL,
    PARTICLE,
    PARTICLEEMITTER,
    TEXTURE,
    USERMSG,

    CONVAR,
    IMESH,
    MATRIX,
    SOUND,
    PIXELVISHANDLE,
    DLIGHT,
    VIDEO,
    FILE


type_names = [
    "nil",
    "bool",
    "lightuserdata",
    "number",
    "string",
    "table",
    "function",
    "userdata",
    "thread",
    "entity",
    "vector",
    "angle",
    "physobj",
    "save",
    "restore",
    "damageinfo",
    "effectdata",
    "movedata",
    "recipientfilter",
    "usercmd",
    "vehicle",
    "material",
    "panel",
    "particle",
    "particleemitter",
    "texture",
    "usermsg",
    "convar",
    "mesh",
    "matrix",
    "sound",
    "pixelvishandle",
    "dlight",
    "video",
    "file"
]


# ILuaBase pointer.
# Being set in setup().
cdef ILuaBase* lua = NULL

# Guard variable for safe documentation generation.
# Stack functions are no-ops if this equals False.
IN_GMOD = False


cdef public setup(ILuaBase* base):
    """This function is called in ``giveILuaBasePtrToLuastack()`` in ``main.cpp`` of the C++ module."""
    global lua
    global IN_GMOD
    lua = base
    IN_GMOD = True


def _stack(func):
    """Decorator for stack manipulation functions.

    Makes the decorated function to be a static method and act only if :const:`IN_GMOD` is ``True``.
    """

    def decorated(*args, **kwargs):
        if IN_GMOD:
            return func(*args, **kwargs)

    return staticmethod(decorated)


class LuaStack:
    @_stack
    def top():
        """Returns the index of the top element in the stack.

        Because indices start at 1,
        this result is equal to the number of elements in the stack (and so 0 means an empty stack).
        """
        return lua.Top()


    @_stack
    def equal(int a, int b):
        """
        Returns ``True`` if the two values in acceptable indices ``a`` and ``b`` are equal,
        following the semantics of the Lua ``==`` operator (that is, may call metamethods).
        Otherwise returns ``False``. Also returns ``False`` if any of the indices is non valid.
        """
        return <bool> lua.Equal(a, b)


    @_stack
    def raw_equal(int a, int b):
        """
        Returns ``True`` if the two values in acceptable indices
        ``a`` and ``b`` are primitively equal (that is, without calling metamethods).
        Otherwise returns ``False``. Also returns ``False`` if any of the indices are non valid.
        """
        return <bool> lua.RawEqual(a, b)


    @_stack
    def insert(int destination_index):
        """Moves the top element into the given valid index, shifting up the elements above this index to open space."""
        lua.Insert(destination_index)


    @_stack
    def throw_error(const char* message):
        """Raises an error with the given :class:`bytes` message.

        It also adds at the beginning of the message the file name and the line number where the error occurred,
        if this information is available.
        """
        lua.ThrowError(message)


    @_stack
    def create_table():
        """Creates a new empty table and pushes it onto the stack."""
        lua.CreateTable()


    @_stack
    def push(int stack_pos):
        lua.Push(stack_pos)


    @_stack
    def push_special(int type):
        lua.PushSpecial(type)


    @_stack
    def push_nil():
        """Pushes a ``nil`` value onto the stack."""
        lua.PushNil()


    @_stack
    def push_number(double num):
        """Pushes a number with value ``num`` onto the stack."""
        lua.PushNumber(num)


    @_stack
    def push_string(const char* val):
        """Pushes a ``bytes`` onto the stack."""
        lua.PushString(val)


    @_stack
    def push_bool(bool val):
        """Pushes a boolean value ``val`` onto the stack."""
        lua.PushBool(val)


    @_stack
    def pop(int amt=1):
        """Pops ``amt`` elements from the stack."""
        lua.Pop(amt)


    @_stack
    def clear():
        """Clears the stack."""
        LuaStack.pop(LuaStack.top())


    @_stack
    def get_table(int stack_pos):
        """
        Pushes onto the stack the value ``t[k]``, where ``t`` is the value at the given valid index ``stack_pos``
        and ``k`` is the value at the top of the stack.

        This function pops the key from the stack (putting the resulting value in its place).
        """
        lua.GetTable(stack_pos)


    @_stack
    def get_field(int stack_pos, const char* name):
        """Pushes onto the stack the value ``t[name]``, where ``t`` is the value at the given valid index ``stack_pos``."""
        lua.GetField(stack_pos, name)


    @_stack
    def set_table(int stack_pos):
        """
        Does the equivalent to ``t[k] = v``,
        where ``t`` is the value at the given valid index ``stack_pos``,
        ``v`` is the value at the top of the stack, and ``k`` is the value just below the top.

        This function pops both the key and the value from the stack.
        """
        lua.SetTable(stack_pos)


    @_stack
    def set_field(int stack_pos, const char* name):
        """
        Does the equivalent to ``t[k] = v``,
        where ``t`` is the value at the given valid index ``stack_pos``
        and ``v`` is the value at the top of the stack.

        This function pops the value from the stack.
        """
        lua.SetField(stack_pos, name)


    @_stack
    def call(int args, int results):
        """Calls a function.

        To call a function you must use the following protocol:

        1. The function to be called is pushed onto the stack
        2. The arguments to the function are pushed in direct order; that is, the first argument is pushed first.
        3. You call this function; ``args`` is the number of arguments that you pushed onto the stack.

        All arguments and the function value are popped from the stack when the function is called.
        The function results are pushed onto the stack when the function returns.
        The number of results is adjusted to ``results``.
        The function results are pushed onto the stack in direct order (the first result is pushed first),
        so that after the call the last result is on the top of the stack.

        The following example shows how the host program can do the equivalent to this Lua code::

          a = f("how", t.x, 14)

        Here it is in GPython::

          push_special(Special.GLOBAL)
          get_field(1, "f")  # function to be called
          push_string("how")  # 1st argument
          get_field(1, "t")  # table to be indexed
          get_field(-1, "x")  # push result of t.x (2nd arg)
          remove(-2)  # remove 't' from the stack
          push_number(14)  # 3rd argument
          call(3, 1)  # call 'f' with 3 arguments and 1 result
          set_field(1, "a")  # set global 'a'

        Note that the code above is "balanced": at its end, the stack is back to its original configuration.
        This is considered good programming practice.
        """
        lua.Call(args, results)


    @_stack
    def get_string(int stack_pos=-1):
        """Returns the ``bytes`` value of a string item at ``stack_pos`` index of the stack.

        Negative values can be used for indexing the stack from top.
        """
        return lua.GetString(stack_pos, <unsigned int*> 0)


    @_stack
    def get_number(int stack_pos=-1):
        """Returns the ``float`` value of a number item at ``stack_pos`` index of the stack.

        Negative values can be used for indexing the stack from top.
        """
        return lua.GetNumber(stack_pos)


    @_stack
    def get_bool(int stack_pos=-1):
        """Returns the boolean value of a boolean item at ``stack_pos`` index of the stack.

        Negative values can be used for indexing the stack from top.
        """
        return lua.GetBool(stack_pos)


    @_stack
    def create_ref():
        """Saves the value at the top of the stack to a reference, pops it and returns the reference."""
        return lua.ReferenceCreate()


    @_stack
    def free_ref(int ref):
        """Frees the reference."""
        lua.ReferenceFree(ref)


    @_stack
    def push_ref(int ref):
        """Pushes the value saved in the reference."""
        lua.ReferencePush(ref)


    @_stack
    def get_type(int stack_pos):
        return lua.GetType(stack_pos)


    @_stack
    def get_type_name(ValueType type):
        return lua.GetTypeName(type)


    @_stack
    def is_type(int stack_pos, ValueType type):
        return lua.IsType(stack_pos, type)
