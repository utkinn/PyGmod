from .. import draw
from .panel import Panel


# noinspection PyMissingConstructor
class Frame(Panel):
    _lua_class = 'DFrame'

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
