Getting Started
===============

What is PyGmod?
---------------

**PyGmod** is an experimental project which allows to create addons for sandbox game **Garry's Mod** with Python.

PyGmod is currently in the Alpha development stage. Many features are planned, but not implemented yet.

.. danger::
    Do not use addons from untrusted sources, because there is no security features currently implemented.

What advantages does PyGmod have?
---------------------------------

At the moment, there is only one available programming language for Garry's Mod addon creation: Lua.

Lua is exclusively simple to learn and use due to its minimalistic design. Minimalistic language design means a small
standard library and few syntactic features. Sometimes you need something more powerful than Lua, and Python
is quite a good choice.

Python's power and its simple and neat syntax allows to create better addons in terms of quality and richness.

How PyGmod addons look like?
----------------------------

PyGmod addons look pretty much the same like traditional Lua addons. The difference is the presence of ``python`` folder
in addon root directory. This folder contains Python code. You can code addons completely with Python without any Lua
code, or you can code them with both Python and Lua.

How to use it?
--------------

If you are a regular Garry's Mod player or addon developer, you have to
`install the latest Python version <https://www.python.org/downloads/>`_, then
`download the latest release <https://github.com/javabird25/PyGmod/releases/latest>`_, open the ZIP archive and
follow the instructions in ``install.txt``.

If you are a player that want to try out addons that require PyGmod, copy your addons to ``addons`` folder in your
Garry's Mod folder and you're set.

For addon developers: take a look at :doc:`Getting Started for Addon Developers <for_addon_developers/getting_started>`.

If you are a PyGmod internal developer, you should check out
:doc:`Getting Started for PyGmod developers <for_pygmod_developers/getting_started>`.
