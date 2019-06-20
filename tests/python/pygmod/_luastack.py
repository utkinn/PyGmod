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


def push_nil():
    stack.append(None)


def push_python_obj(o):
    stack.append(o)


def get_stack_val_as_python_obj(i=-1):
    return stack[i]


def set_field(i, name):
    stack[i][name] = stack[-1]
    stack.pop()


def call():
    """Stub. Always replaced with a mock by mocker.patch()."""
    raise NotImplementedError("call() should always be mocked")


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
