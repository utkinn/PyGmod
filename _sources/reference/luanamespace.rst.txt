``luanamespace`` - all Lua definitions
======================================

Contains all names that are listed in `Garry's Mod Wiki <https://wiki.garrysmod.com>`_, that is, variables,
functions, libraries, classes, etc, so you don't have to prepend ``lua.G`` before Lua names.

Best way to use it is import everything from it::

    from gmod.luanamespace import *

And now you can write code that looks pretty much like Lua::

    from gmod.lua import *
    from gmod.luanamespace import *

    def init():
        print('Hello world')

    hook.Add('Initialized', 'init', luafunction(init))

    def log_chat_to_console(sender, text, team_chat):
        print(sender._.Nick(), 'says:', text)

    hook.Add('PlayerSay', 'logChatToConsole', luafunction(init))

.. note:: Keep in mind that Python standard library has many of them already implemented.
    Prefer using Python alternatives whenever possible.

.. note:: Enumerations are not available from this module. Use :data:`gmod.lua.G` to get them.

.. note:: Creating variables in Python won't make them available in Lua. Use :data:`gmod.lua.G` to set values in Lua.

Exceptions
----------

Some names are not accessible from this module for various reasons. You can still access them using :data:`gmod.lua.G`.
Trying to access them anyway will raise :class:`NameError`, since they are not created in the module at all.

Globals
^^^^^^^

+-------------------------------+---------------------------+
|             Name              |     Exclusion reason      |
+===============================+===========================+
| ``assert``                    | Python Keyword/name       |
| ``next``                      | conflict                  |
| ``print``                     |                           |
| ``type``                      |                           |
+-------------------------------+---------------------------+
| ``AddBackgroundImage``        | Menu-only function        |
| ``CanAddServerToFavorite``    |                           |
| ``CancelLoading``             |                           |
| ``ChangeBackground``          |                           |
| ``ClearBackgroundImages``     |                           |
| ``ConsoleAutoComplete``       |                           |
| ``DrawBackground``            |                           |
| ``GameDetails``               |                           |
| ``GetDefaultLoadingHTML``     |                           |
| ``GetDemoFileDetails``        |                           |
| ``GetDownloadables``          |                           |
| ``GetLoadPanel``              |                           |
| ``GetLoadStatus``             |                           |
| ``GetMapList``                |                           |
| ``GetOverlayPanel``           |                           |
| ``GetSaveFileDetails``        |                           |
| ``IsInGame``                  |                           |
| ``JoinServer``                |                           |
| ``LanguageChanged``           |                           |
| ``LoadLastMap``               |                           |
| ``NumDownloadables``          |                           |
| ``OpenFolder``                |                           |
| ``RecordDemoFrame``           |                           |
| ``RunGameUICommand``          |                           |
| ``SaveLastMap``               |                           |
| ``ToggleFavourite``           |                           |
| ``TranslateDownloadableName`` |                           |
| ``UpdateLoadPanel``           |                           |
+-------------------------------+---------------------------+
| ``gcinfo``                    | Deprecated                |
| ``GetConVarNumber``           |                           |
| ``GetConVarString``           |                           |
| ``IncludeCS``                 |                           |
| ``RunStringEx``               |                           |
| ``SScale``                    |                           |
| ``ValidPanel``                |                           |
+-------------------------------+---------------------------+
| ``AddConsoleCommand``         | Internal                  |
| ``OnModelLoaded``             |                           |
| ``WorkshopFileBase``          |                           |
| ``GetConVar_Internal``        |                           |
+-------------------------------+---------------------------+

Libraries
^^^^^^^^^

+-------------------------------+---------------------------+
|             Name              |     Exclusion reason      |
+===============================+===========================+
| ``input``                     | Python Keyword/name       |
| ``list``                      | conflict                  |
| ``math``                      |                           |
| ``os``                        |                           |
+-------------------------------+---------------------------+
| ``umsg``                      | Deprecated                |
| ``usermessage``               |                           |
+-------------------------------+---------------------------+
