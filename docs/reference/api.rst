``pygmod.gmodapi`` - all Garry's Mod Lua definitions
====================================================

.. module:: pygmod.gmodapi
    :synopsis: all Garry's Mod Lua definitions

Contains all variables, functions, libraries, classes, etc. that are listed in
`Garry's Mod Wiki <https://wiki.garrysmod.com>`_.

The simplest way to use this module is to import everything from it::

    from pygmod.gmodapi import *

And now you can write code that looks similar to Lua::

    from pygmod.gmodapi import *

    def init():
        print('Hello world')

    hook.Add('Initialized', 'init', init)

    def log_chat_to_console(sender, text, team_chat):
        print(sender._.Nick(), 'says:', text)

    hook.Add('PlayerSay', 'logChatToConsole', init)

.. note:: Enums can not be accessed with this module. Use :data:`pygmod.lua.G` instead.

.. note:: Creating variables in Python won't make them visible in Lua. Use :data:`pygmod.lua.G` to set values in Lua.

Excluded definitions
-----------------------

Some definitions are not accessible from this module for various reasons. You can still access them with :data:`pygmod.lua.G`.

Globals
^^^^^^^

+-------------------------------+---------------------------+
|             Name              |     Exclusion reason      |
+===============================+===========================+
| ``assert``                    | Python                    |
| ``next``                      | keyword/builtin/module    |
| ``print``                     | conflict                  |
| ``type``                      |                           |
+-------------------------------+---------------------------+
| ``AddBackgroundImage``        | Menu-only function        |
| ``CanAddServerToFavorite``    | Neither Python nor Lua    |
| ``CancelLoading``             | addons are able to        |
| ``ChangeBackground``          | access the Menu realm     |
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
| ``input``                     | Python                    |
| ``list``                      | keyword/builtin/module    |
| ``math``                      | conflict                  |
| ``os``                        |                           |
+-------------------------------+---------------------------+
| ``umsg``                      | Deprecated                |
| ``usermessage``               |                           |
+-------------------------------+---------------------------+
