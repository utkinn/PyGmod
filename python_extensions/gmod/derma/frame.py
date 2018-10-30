from .. import lua, realms
from .panel import Panel


# noinspection PyMissingConstructor
class Frame(Panel):
    def __init__(self):
        if realms.SERVER:
            raise realms.RealmError('derma is available on client only')
        self._lua = lua.G['vgui']['Create']('DFrame')

    @property
    def title(self):
        return str(self._lua['GetTitle'](self._lua))

    @title.setter
    def title(self, val):
        if not isinstance(val, str):
            raise ValueError('title must be str')
        self._lua['SetTitle'](self._lua, val)

    def popup(self):
        self._lua['MakePopup'](self._lua)
