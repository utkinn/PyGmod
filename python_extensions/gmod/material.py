from . import lua, typecheck

# Material parameters
NOCULL = 'nocull'
ALPHATEST = 'alphatest'
MIPS = 'mips'
NOCLAMP = 'noclamp'
SMOOTH = 'smooth'


class Material(lua.LuaObjectWrapper):
    def __init__(self, name_or_path, *parameters):
        typecheck.check(name_or_path, str)
        typecheck.check_iter(parameters, str)

        self._name_or_path = name_or_path
        self._parameters = parameters

    @property
    def lua_obj(self):
        lua_mat = lua.G.Material(self._name_or_path, ' '.join(self._parameters))[0]
        return lua_mat
