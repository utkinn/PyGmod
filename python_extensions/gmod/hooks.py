"""
This module contains tools for creating and running so called *hooks*.

Hooks are the callbacks for game events. When an event occurs, all callbacks hooked to it are ran by Garry's Mod.

Some hooks have arguments, for example, the sender and the message content of "New message in chat" event.
In this case, the arguments are passed to callbacks.

You can register hooks with :func:`hook` decorator.
"""

from . import lua

__all__ = ['hook']

# Callback registry.
# Keys are the event names, values are the lists of callbacks.
callbacks = {}


def register_callback(event, callback):
    """
    Adds a callback to the callback registry.
    Returns index of the callback.
    """
    callback_list = callbacks.get(event, [])
    new_index = len(callbacks)
    callback_list.append(callback)
    callbacks[event] = callback_list
    return new_index


def event_occurred(event, n_args):
    """Runs callbacks for event ``event``. ``n_args`` is the quantity of the hook arguments."""
    args_luaobj = lua.G['py']['_hook_cb_args']
    args = [args_luaobj[i] for i in range(1, n_args + 1)]
    for callback in callbacks[event]:
        callback(*args)


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

    def decorator(func):
        index = register_callback(event, func)

        lua_callback = f'''function(...)
            py._hook_cb_args = {{}}  -- Curly brackets are escaped in f-strings by repeating them two times
            for _, v in pairs(...) do
                table.insert(py._hook_cb_args, v)
            end
            py.Exec("import gmod.hooks; gmod.hooks.event_occurred({repr(event)}, "..#py._hook_cb_args..")")
        end
        '''

        # This hook's ID
        id_ = f'gpy_hook_{event}{index}'
        lua.G['hook']['add'](event, lua.lua_eval(lua_callback), id_)

        def remove(self):
            lua.G['hook']['Remove'](event, id_)
            del self.remove

        func.remove = remove
        return func

    return decorator
