def check(o, t):
    """Raises :class:`TypeError` if the type of ``o`` is not ``t``."""
    if not isinstance(o, t):
        raise TypeError(f'invalid argument type: expected {t.__name__!r}, got {type(o).__name__!r} (value: {o!r})')


def check_iter(i, t):
    """Raises :class:`TypeError` if any object in iterable ``i`` don't have type ``t``."""
    for o in i:
        check(o, t)


def check_batch(assertion_dict):
    """
    Assumes that the ``assertion_dict`` keys have types of their corresponding values. Raises ``TypeError`` otherwise.

    >>> assertion = {1: int, 'abc': str}
    >>> check_batch(assertion)  # No errors
    >>> assertion = {2: str}
    >>> check_batch(assertion)
    Traceback (most recent call last):
      ...
    TypeError: invalid argument type: expected 'str', got 'int' (value: 2)
    """
    for o, t in assertion_dict.values():
        check(o, t)
