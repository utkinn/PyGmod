"""
This module provides tools for distinguishing the current code execution environment - so called **realms**.

There is two realms that are available for executing any user code, whether it be Lua or Python code
- **server** and **client**.

The **Client** state is basically the game client. It handles things such as visual rendering.

The **Server** state handles things on the server; it's the only state used on Dedicated Servers. This handles things
like telling entities what to do, controlling weapons/players and all game logic
(what happens when and how in gamemodes).

You can use :data:`CLIENT` and :data:`SERVER` constants to check the current realm.
"""

import luastack
from .lua import G

# Don't define this if we're generating docs
if luastack.IN_GMOD:
    # client/server bool constants, same as in GLua
    CLIENT = bool(G['CLIENT'])
    SERVER = not CLIENT

    # String version of the current realm
    REALM = 'client' if CLIENT else 'server'
else:
    # Dummy definitions to keep imports working
    CLIENT, SERVER, REALM = None, None, None

# def _realm_call_restriction_decorator(func, realm):
#     """Abstract realm function usage restriction decorator.
#
#     :param str realm: The required realm.
#     """
#
#     def decorated(*args, **kwargs):
#         if REALM != realm:
#             raise RealmError("'" + func.__name__ + f"' is intended to be used in {realm} realm only")
#         func(*args, **kwargs)
#
#     return decorated
#
#
# def client_only(func):
#     """Decorator which allows calling of the decorated function on *client* side only.
#
#     Raises :exc:`RealmError` if the decorated function is called in the *server* realm.
#     """
#     return _realm_call_restriction_decorator(func, 'client')
#
#
# def server_only(func):
#     """Decorator which allows calling of the decorated function on *server* side only.
#
#     Raises :exc:`RealmError` if the decorated function is called in the *client* realm.
#     """
#     return _realm_call_restriction_decorator(func, 'server')
