# distutils: language = c++

# ctypedef int (*CFunc) (lua_State *L)

from libcpp cimport bool

cdef extern from "../../src/include/GarrysMod/Lua/LuaBase.h" namespace "GarrysMod::Lua":
    cdef cppclass ILuaBase:
        # Some methods are left commented because they are currently unused.

        int Top()
        void Push(int iStackPos)
        void Pop(int iAmt)
        void GetTable(int iStackPos)
        void GetField(int iStackPos, const char* strName)
        void SetField(int iStackPos, const char* strName)
        void CreateTable()
        void SetTable(int i)
        # void SetMetaTable(int i)
        # bool GetMetaTable(int i)
        void Call(int iArgs, int iResults)
        # int PCall(int iArgs, int iResults, int iErrorFunc)
        int Equal(int iA, int iB)
        int RawEqual(int iA, int iB)
        void Insert(int iStackPos)
        void Remove(int iStackPos)
        # int Next(int iStackPos)
        # void* NewUserdata(unsigned int iSize)
        void ThrowError(const char* strError)
        # void CheckType(int iStackPos, int iType)
        # void ArgError(int iArgNum, const char* strMessage)
        # void RawGet(int iStackPos)
        # void RawSet(int iStackPos)

        const char* GetString(int iStackPos, unsigned int* iOutLen)
        double GetNumber(int iStackPos)
        bool GetBool(int iStackPos)
        # CFunc GetCFunction(int iStackPos = -1)
        # void* GetUserdata(int iStackPos = -1)

        void PushNil()
        void PushString(const char* val, unsigned int iLen = 0)
        void PushNumber(double val)
        void PushBool(bool val)
        # void PushCFunction(CFunc val)
        # void PushCClosure(CFunc val, int iVars)
        # void PushUserdata(void*)

        # int ReferenceCreate()
        # void ReferenceFree(int i)
        # void ReferencePush(int i)

        void PushSpecial(int iType)

        bool IsType(int iStackPos, int iType)
        int GetType(int iStackPos)
        # const char* GetTypeName(int iType)
        #
        # void CreateMetaTableType(const char* strName, int iType)
        #
        # const char* CheckString(int iStackPos = -1)
        # double CheckNumber(int iStackPos = -1)
