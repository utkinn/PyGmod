from . import lua, net


@net.client
def getsize():
    return int(lua.G['ScrW']()), int(lua.G['ScrH']())
