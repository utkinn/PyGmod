from enum import Enum, auto
from unittest.mock import Mock


class Special(Enum):
    GLOBAL = auto()
    ENVIRONMENT = auto()
    REGISTRY = auto()


class ValueType(Enum):
    NIL = auto()
    BOOL = auto()
    LIGHTUSERDATA = auto()
    NUMBER = auto()
    STRING = auto()
    TABLE = auto()
    FUNCTION = auto()
    USERDATA = auto()
    THREAD = auto()

    # UserData
    ENTITY = auto()
    VECTOR = auto()
    ANGLE = auto()
    PHYSOBJ = auto()
    SAVE = auto()
    RESTORE = auto()
    DAMAGEINFO = auto()
    EFFECTDATA = auto()
    MOVEDATA = auto()
    RECIPIENTFILTER = auto()
    USERCMD = auto()
    SCRIPTEDVEHICLE = auto()

    # Client Only
    MATERIAL = auto()
    PANEL = auto()
    PARTICLE = auto()
    PARTICLEEMITTER = auto()
    TEXTURE = auto()
    USERMSG = auto()

    CONVAR = auto()
    IMESH = auto()
    MATRIX = auto()
    SOUND = auto()
    PIXELVISHANDLE = auto()
    DLIGHT = auto()
    VIDEO = auto()
    FILE = auto()


IN_GMOD = True

LuaStack = Mock(name='LuaStack')

LuaStack.return_value.create_ref.return_value = 1
