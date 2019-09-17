"""
Contains all variables, functions, libraries, classes, etc.
that are listed in Garry's Mod Wiki (https://wiki.garrysmod.com).
"""

from pygmod import lua


def __getattr__(name):
    return lua.G[name]
