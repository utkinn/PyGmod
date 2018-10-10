class TableMock:
    """Mock for Lua tables including :const:`gmod.lua.G`."""

    def __init__(self, table=None, *args, **kw):
        super().__init__(*args, **kw)
        self.table = {} if table is None else table

    def _get(self, key):
        return self.table[key]

    def _set(self, key, value):
        self.table[key] = value

    def __getitem__(self, key):
        return self._get(key)

    def __getattr__(self, key):
        return self._get(key)

    def __setitem__(self, key, value):
        self._set(key, value)

    def __setattr__(self, key, value):
        if key == 'table':
            super().__setattr__(key, value)
            return

        self._set(key, value)

    def __repr__(self):
        return f'TableMock({repr(self.table)})'
