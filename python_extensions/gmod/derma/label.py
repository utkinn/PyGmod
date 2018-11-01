from .panel import Panel


class Label(Panel):
    _lua_class = 'DLabel'

    def __init__(self, parent, text='Label'):
        super().__init__(parent)
        self.text = text
        self.wrap = True

    def paint(self):
        pass

    @property
    def text(self):
        return str(self._lua['GetText'](self._lua))

    @text.setter
    def text(self, val):
        if not isinstance(val, str):
            raise TypeError('text must be str')
        self._lua['SetText'](self._lua, val)

    @property
    def wrap(self):
        return bool(self._lua['GetWrap'](self._lua))

    @wrap.setter
    def wrap(self, val):
        if not isinstance(val, bool):
            raise TypeError('val must be bool')
        self._lua['SetWrap'](self._lua, val)
