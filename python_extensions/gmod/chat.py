"""This module provides tools for manipulating the chat."""

from . import color, lua, net


@net.client
def print(*values, sep=' '):
    """Prints the values to the chat.

    Values may contain :class:`gmod.color.Color` objects to change the color of the following text. You can change the
    color multiple times.

    Newline is added after the message, and there is no way to change that.
    """
    args_no_sep = [v if isinstance(v, color.Color) else str(v) for v in values]

    args_with_sep = []
    for a in args_no_sep:
        if not isinstance(a, color.Color):
            args_with_sep += [a, sep]

    lua.G['chat']['AddText'](*args_with_sep)
