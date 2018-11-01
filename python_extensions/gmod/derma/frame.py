from .. import draw
from .panel import Panel


class Frame(Panel):
    _lua_class = 'DFrame'

    def __init__(self, parent):
        super().__init__(parent)
        self.draggable = True

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

    def paint(self):
        draw.rounded_box(0, 0, self.w, self.h, (0, 0, 0, 230), 8)

    @property
    def draggable(self):
        return bool(self._lua['GetDraggable'](self._lua))

    @draggable.setter
    def draggable(self, val):
        if not isinstance(val, bool):
            raise TypeError('draggable must be bool')
        self._lua['SetDraggable'](self._lua, val)

    @property
    def resizable(self):
        return bool(self._lua['GetSizable'](self._lua))

    @resizable.setter
    def resizable(self, val):
        if not isinstance(val, bool):
            raise TypeError('resizable must be bool')
        self._lua['SetSizable'](self._lua, val)
