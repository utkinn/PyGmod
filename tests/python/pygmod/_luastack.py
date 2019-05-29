"""
Mock module for _luastack C++ extension.
Behaves like true _luastack module, but operates an imaginary Lua stack
represented by a list.
"""

from collections import namedtuple

Reference = namedtuple("Reference", "id")

_stack = []  # Imaginary Lua stack


def reset_stack():
    _stack.clear()


def top():
    return len(_stack)


def pop(n=1):
    for _ in range(n):
        del _stack[-1]


def push_nil():
    _stack.append(None)


def call():
    """Stub. Always replaced with a mock by mocker.patch()."""
    raise NotImplementedError("call() should always be mocked")


def reference_push(ref):
    _stack.append(Reference(ref))
