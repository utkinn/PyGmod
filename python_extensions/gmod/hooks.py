"""
This module contains tools for creating and running so called *hooks*.

Hooks are the callbacks for game events. When an event occurs, all callbacks hooked to it are ran by Garry's Mod.

Some hooks have arguments, for example, the sender and the message content of "New message in chat" event.
In this case, the arguments are passed to callbacks.

You can register hooks with :func:`hook` decorator.
"""

from collections import defaultdict
from sys import stderr
import traceback

from . import lua, realms

__all__ = ['hook']

# Callback registry.
# Keys are the event names, values are the lists of callbacks.
callbacks = defaultdict(lambda: [])


def event_occurred(event):
    """Runs callbacks for event ``event``. ``n_args`` is the quantity of the hook arguments."""
    data = lua.G['_py_hook_data']
    n = int(lua.G['_py_n_data'])
    pydata = [data[i] for i in range(1, n + 1)]

    for callback in callbacks[event]:
        try:
            callback(*pydata)
        except:
            print(f'Exception in hook "{callback.__module__}.{callback.__name__}":', file=stderr)
            traceback.print_exc()


def hook(event: str):
    """Decorator which hooks the decorated function to event ``event``.

    You can find the list of available events at http://wiki.garrysmod.com/page/Category:GM_Hooks and
    http://wiki.garrysmod.com/page/Category:SANDBOX_Hooks.

    .. note::

        Hooks with ``GM`` prefix are available for any gamemode, whereas ``SANDBOX`` hooks are available only for
        the Sandbox gamemode.

    .. note::

        You should omit ``GM:`` and ``SANDBOX:`` when specifying the event name.

    ::

        # Registering the world initialization hook
        # hello_world will be called when the world initializes
        @hook('Initialize')
        def hello_world():
            print('Hello world!')

        # Removing the hook, so this function won't be called on event occurrences anymore.
        hello_world.remove()

    Some hooks have arguments which are passed to the hooked function.
    For example, event ``PlayerSay`` has 3 arguments:
    the message sender, the message text and whether it was sent to the team chat.

    ::

        @hook('PlayerSay')
        def log_chat_to_file(sender, text, team_chat):
            prefix = '(TEAM)' if bool(team_chat) else ''
            file.write(Player(sender).nick + prefix + ': ' + str(text))

    .. note::

        Arguments are actually :class:`gmod.lua.LuaObject`\\ s, so you have to explicitly convert them to right types.
    """
    if not isinstance(event, str):
        raise TypeError('event must be str')

    def decorator(func):
        if lua.G['py']['_watched_events'].type_name == b'nil':
            lua.G['py']['_watched_events'] = lua.table(())

        lua.G['py']['_watched_events'][event] = True
        callbacks[event].append(func)

        def remove(self):
            callbacks[event].remove(func)

            if not callbacks[event]:
                lua.G['py']['_watched_events'][event] = False

            del self.remove

        func.remove = remove
        return func

    return decorator
