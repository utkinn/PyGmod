from .. import lua, realms


class Panel:
    _lua_class = 'DPanel'

    def __init__(self):
        if realms.SERVER:
            raise realms.RealmError('derma is available on client only')
        self._lua = lua.G['vgui']['Create'](self._lua_class)

    @property
    def w(self):
        return int(self._lua['GetSize'](self._lua)[1])

    @w.setter
    def w(self, val):
        if not isinstance(val, int):
            raise ValueError('w must be int')
        self._lua['SetSize'](self._lua, val, self.h)

    @property
    def h(self):
        return int(self._lua['GetSize'](self._lua)[2])

    @h.setter
    def h(self, val):
        if not isinstance(val, int):
            raise ValueError('w must be int')
        self._lua['SetSize'](self._lua, self.w, val)

    @property
    def size(self):
        return self.w, self.h

    @size.setter
    def size(self, val):
        w, h = val
        if any(not isinstance(o, int) for o in (w, h)):
            raise TypeError('size iterable members must be int')
        self._lua['SetSize'](self._lua, w, h)

    @property
    def x(self):
        return int(self._lua['GetPos'](self._lua)[1])

    @x.setter
    def x(self, val):
        if not isinstance(val, int):
            raise ValueError('x must be int')
        self._lua['SetPos'](self._lua, val, self.y)

    @property
    def y(self):
        return int(self._lua['GetPos'](self._lua)[2])

    @y.setter
    def y(self, val):
        if not isinstance(val, int):
            raise ValueError('y must be int')
        self._lua['SetPos'](self._lua, self.y, val)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, val):
        x, y = val
        if any(not isinstance(o, int) for o in (x, y)):
            raise TypeError('pos iterable members must be int')
        self._lua['SetPos'](self._lua, x, y)

    @property
    def bounds(self):
        return self.x, self.y, self.w, self.h

    @bounds.setter
    def bounds(self, val):
        x, y, w, h = val
        if any(not isinstance(o, int) for o in (x, y, w, h)):
            raise TypeError('bounds iterable members must be int')
        self._lua['SetBounds'](self._lua, x, y, w, h)
