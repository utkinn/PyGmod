``luastack`` - Lua Stack manipulation
====================================

.. note::

	``luastack`` is not a part of the ``gmod`` package. So, instead of:

    ::

        from gmod.luastack import *

    or::

        from gmod import *
        # Trying to use luastack

    *you should use*\ :

    ::

        from luastack import *
        # Using luastack

This module contains functions for manipulating the Lua stack. The lowest level of Garry's Mod Lua interoperability.

Lua Stack description
---------------------

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

.. data:: IN_GMOD

    Boolean constant which is ``True`` if GPython system is running during a Garry's Mod session.
    This constant is used in GPython libraries for preventing some code from executing when generating documentation.

.. cpp:var:: ILuaBase *lua

    Pointer to Lua Stack C++ object. Not available to Python.

    Being set by :cpp:func:`setup`.

.. cpp:function:: void setup(ILuaBase *lua)

    Sets the global lua pointer and :py:data:`IN_GMOD`.

Stack manipulation
------------------

.. function:: top()

    Returns the index of the top element in the stack.

    Because indices start at **1**,
    this result is equal to the number of elements in the stack (and so **0** means an empty stack).

.. function:: equal(a: int, b: int) -> bool

    Returns ``True`` if the two values in acceptable indices ``a`` and ``b`` are equal,
    following the semantics of the Lua ``==`` operator (that is, may call metamethods).
    Otherwise returns ``False``. Also returns ``False`` if any of the indices is non valid.

.. function:: raw_equal(a: int, b: int) -> bool

    Returns ``True`` if the two values in acceptable indices
    ``a`` and ``b`` are primitively equal (that is, without calling metamethods).
    Otherwise returns ``False``. Also returns ``False`` if any of the indices are non valid.

.. function:: insert(destination_index: int)

    Moves the top element into the given valid index, shifting up the elements above this index to open space.

.. function:: throw_error(message: bytes)

    Raises a Lua error with the given :class:`bytes` message.

    It also adds at the beginning of the message the file name and the line number where the error occurred,
    if this information is available.

.. function:: create_table() -> None

    Creates a new empty table and pushes it onto the stack.

.. function:: push(stack_pos: int)
.. function:: push_special(type: int)

    Pushes a special value onto the stack. Use :class:`Special` enum.

.. function:: push_nil()

    Pushes a ``nil`` value onto the stack.

.. function:: push_number(num)

    Pushes a number ``num`` onto the stack.

.. function:: push_string(val: bytes)

    Pushes a :class:`bytes` object onto the stack.

    You can push :class:`str` like this::

        s = '...'
        push_string(s.encode())

.. function:: push_bool(val: bool)

    Pushes a boolean value ``val`` onto the stack.

.. function:: pop(amt: int = 1) -> None

    Pops ``amt`` elements from the stack.

.. function:: clear()

    Clears the stack (pops all values).

.. function:: get_table(stack_pos: int) -> None

    Pushes onto the stack the value ``t[k]``, where ``t`` is the value at the given valid index ``stack_pos``
    and ``k`` is the value at the top of the stack.

    This function pops the key from the stack (putting the resulting value in its place).

.. function:: get_field(stack_pos: int, name: bytes) -> None

    Pushes onto the stack the value ``t[name]``, where ``t`` is the value at the given valid index ``stack_pos``.

.. function:: set_table(stack_pos: int)

    Does the equivalent to ``t[k] = v``,
    where ``t`` is the value at the given valid index ``stack_pos``,
    ``v`` is the value at the top of the stack, and ``k`` is the value just below the top.

    This function pops both the key and the value from the stack.

.. function:: set_field(stack_pos: int, name: bytes)

    Does the equivalent to ``t[k] = v``,
    where ``t`` is the value at the given valid index ``stack_pos``
    and ``v`` is the value at the top of the stack.

    This function pops the value from the stack.

.. function:: call(args: int, results: int)

    Calls a function.

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

    Here it is with GPython's luastack::

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

.. function:: get_string(stack_pos: int = -1) -> bytes

    Returns the :class:`bytes` value of a string item at ``stack_pos`` index of the stack.

    Negative values can be used for indexing the stack from top.

.. function:: get_number(stack_pos: int = -1) -> float

    Returns the :class:`float` value of a number item at ``stack_pos`` index of the stack.

    Negative values can be used for indexing the stack from top.

.. function:: get_bool(stack_pos: int = -1) -> bool

    Returns the boolean value of a boolean item at ``stack_pos`` index of the stack.

    Negative values can be used for indexing the stack from top.

.. function:: create_ref() -> int

    Saves the value at the top of the stack to a reference, pops it and returns the reference ID.

.. function:: free_ref(ref: int)

    Frees the reference with ID ``ref``.

.. function:: push_ref(ref: int)

    Pushes the value saved in the reference with ID ``ref`` onto the stack.

.. function:: get_type(stack_pos: int) -> ValueType

    Returns :class:`ValueType`
    enum member which corresponds to the type of the value at index ``stack_pos`` of the stack.

.. function:: get_type_name(type: ValueType) -> str

    Returns a lowercase string representation of ``type`` type.

.. function:: is_type(stack_pos: int, type: ValueType) -> bool

    Returns ``True`` if the value's type at index ``stack_pos`` is the same as ``type`` argument.

Special values
--------------

.. class:: Special(enum.enum)

    Enum of special values. The only practically usable value is :attr:`Special.GLOBAL`.

    Special values can be pushed with :func:`push_special`.

    .. attribute:: GLOBAL

        Represents the global Lua namespace (``_G``).

    .. attribute:: ENVIRONMENT

        Represents the environment table.

    .. attribute:: REGISTRY

        Represents the registry table. More data can be found in
        `Official Lua documentation <https://www.lua.org/pil/27.3.1.html>`_.

Value types
-----------

.. class:: ValueType(enum.enum)

    Enum of Lua value types.

    ::

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
