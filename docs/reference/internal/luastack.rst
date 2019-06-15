``_luastack`` - Lua Stack manipulation
======================================

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

.. module:: _luastack
    :synopsis: Lua stack manipulation

.. function:: init(lua_base_ptr: int) -> None

    Sets the internal Lua state pointer.

Stack manipulation
------------------

.. function:: top()

    Returns the index of the top element in the stack.

    Because indices start at **1**,
    this result is equal to the number of elements in the stack (and so **0** means an empty stack).

.. function:: create_table() -> None

    Creates a new empty table and pushes it onto the stack.

.. function:: push_globals() -> None

    Pushes the globals table (aka _G) to the stack.

.. function:: push_nil() -> None

    Pushes a ``nil`` value onto the stack.

.. function:: pop(amt=1) -> None

    Pops ``amt`` elements from the stack.

.. function:: get_field(stack_index: int, name: str) -> None

    Pushes onto the stack the value ``t[name]``, where ``t`` is the value at the given valid index ``stack_index``.

.. function:: set_field(stack_index: int, name: str) -> None

    Does the equivalent to ``t[k] = v``,
    where ``t`` is the value at the given valid index ``stack_index``
    and ``v`` is the value at the top of the stack.

    This function pops the value from the stack.

.. function:: call(args: int, results: int) -> None

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

.. function:: reference_create() -> int

    Creates a new reference to an object on the top of the stack and pops that object.
    Returns the reference.

.. function:: reference_push(ref: int) -> None

    Pushes the object which the reference ``ref`` points to, to the top of the stack.

.. function:: reference_free(ref: int) -> None

    Frees the reference ``ref``.

.. function:: get_type(stack_pos: int) -> str

    Returns the name of the type of the Lua value at the given stack index.

.. function:: get_stack_val_as_python_obj(stack_index=-1) -> object

    Converts a Lua value on the given index of the stack to a Python value and returns it.
