"""
Mock module for _luastack C++ extension.
Behaves like true _luastack module, but operates an imaginary Lua stack
represented by a list.
"""


class StackPad:
    """Stub for padding the stack to make indexing start at 1."""

    def __repr__(self):
        return "<StackPad>"


stack = [StackPad()]  # Imaginary Lua stack
references = {}  # Lua reference registry


def top():
    return len(stack) - 1


def pop(n=1):
    for _ in range(n):
        stack.pop()


def push(n):
    stack.append(stack[n])


def push_nil():
    stack.append(None)


def push_globals():
    create_table()


def convert_py_to_lua(o):
    stack.append(o)


def convert_lua_to_py(i=-1):
    return stack[i]


def get_field(i, name):
    assert isinstance(i, int)
    assert isinstance(name, str)

    print("get_field", i, name, "\nBefore operation")
    stack_dump()

    val = stack[i][name]
    stack.append(val)

    print("After operation")
    stack_dump()
    print()


def set_field(i, name):
    assert isinstance(i, int)
    assert isinstance(name, str)

    print("set_field", i, name, "\nBefore operation")
    stack_dump()

    stack[i][name] = stack[-1]
    stack.pop()

    print("After operation")
    stack_dump()
    print()


def get_table(i):
    assert isinstance(i, int)

    print("get_table", i, "\nBefore operation")
    stack_dump()

    key = stack[-1]
    value = stack[i][key]
    stack[-1] = value  # Replacing key with value

    print("After operation")
    stack_dump()
    print()


def set_table(i):
    assert isinstance(i, int)

    print("set_table", i, "\nBefore operation")
    stack_dump()

    key, value = stack[-2], stack[-1]
    stack[i][key] = value
    del stack[-1]  # Deleting value
    del stack[-1]  # Deleting key

    print("After operation")
    stack_dump()
    print()


def call(n_args, n_returns):
    """Stub. Always replaced with a mock by mocker.patch()."""
    raise NotImplementedError("call() should always be mocked")


python_next = next


def next(table_index):
    pop()
    try:
        key, value = python_next(table_index)
        stack.append(key)
        stack.append(value)
        return 1
    except StopIteration:
        return 0


def reference_create():
    referent = stack.pop()
    references[id(referent)] = referent
    return id(referent)


def reference_push(ref):
    stack.append(references[ref])


def reference_free(ref):
    del references[ref]


def create_table():
    stack.append({})


def stack_dump():
    print("Stack:", stack)
