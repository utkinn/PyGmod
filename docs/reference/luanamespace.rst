``luanamespace`` - all Lua definitions
======================================

Contains all names that are listed in `Garry's Mod Wiki <https://wiki.garrysmod.com>`_, that is, variables,
functions, libraries, classes, etc, so you don't have to prepend ``lua.G`` before Lua names.

.. note:: Keep in mind that Python standard library has many of them already implemented.
    Prefer using Python alternatives whenever possible.

.. note:: Enumerations are not available from this module. Use :data:`gmod.lua.G` to get them.

Exceptions
----------

Some names are not accessible from this module for various reasons. You can still access them using :data:`gmod.lua.G`.

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
