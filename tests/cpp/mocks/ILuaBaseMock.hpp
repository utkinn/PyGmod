#include <GarrysMod/Lua/Interface.h>
#include <gmock/gmock.h>

using namespace GarrysMod::Lua;

namespace pygmod::testing
{
    class ILuaBaseMock : public ILuaBase
    {
    public:
        MOCK_METHOD(int, Top, (), (override));
        MOCK_METHOD(void, Push, (int iStackPos), (override));
        MOCK_METHOD(void, Pop, (int iAmt));
        void Pop()
        {
            Pop(1);
        }
        MOCK_METHOD(void, GetTable, (int iStackPos), (override));
        MOCK_METHOD(void, GetField, (int iStackPos, const char *strName), (override));
        MOCK_METHOD(void, SetField, (int iStackPos, const char *strName), (override));
        MOCK_METHOD(void, CreateTable, (), (override));
        MOCK_METHOD(void, SetTable, (int iStackPos), (override));
        MOCK_METHOD(void, SetMetaTable, (int iStackPos), (override));
        MOCK_METHOD(bool, GetMetaTable, (int i), (override));
        MOCK_METHOD(void, Call, (int iArgs, int iResults), (override));
        MOCK_METHOD(int, PCall, (int iArgs, int iResults, int iErrorFunc), (override));
        MOCK_METHOD(int, Equal, (int iA, int iB), (override));
        MOCK_METHOD(int, RawEqual, (int iA, int iB), (override));
        MOCK_METHOD(void, Insert, (int iStackPos), (override));
        MOCK_METHOD(void, Remove, (int iStackPos), (override));
        MOCK_METHOD(int, Next, (int iStackPos), (override));
        MOCK_METHOD(void *, NewUserdata, (unsigned int iSize), (override));
        MOCK_METHOD(void, ThrowError, (const char *strError), (override));
        MOCK_METHOD(void, CheckType, (int iStackPos, int iType), (override));
        MOCK_METHOD(void, ArgError, (int iArgNum, const char *strMessage), (override));
        MOCK_METHOD(void, RawGet, (int iStackPos), (override));
        MOCK_METHOD(void, RawSet, (int iStackPos), (override));
        MOCK_METHOD(const char *, GetString, (int iStackPos, unsigned int *iOutLen));
        const char *GetString(int iStackPos)
        {
            return GetString(iStackPos, NULL);
        }
        const char *GetString()
        {
            return GetString(-1, NULL);
        }
        MOCK_METHOD(double, GetNumber, (int iStackPos));
        double GetNumber()
        {
            return GetNumber(-1);
        }
        MOCK_METHOD(bool, GetBool, (int iStackPos));
        bool GetBool()
        {
            return GetBool(-1);
        }
        MOCK_METHOD(CFunc, GetCFunction, (int iStackPos));
        CFunc GetCFunction()
        {
            return GetCFunction(-1);
        }
        MOCK_METHOD(void *, GetUserdata, (int iStackPos));
        void *GetUserdata()
        {
            return GetUserdata(-1);
        }
        MOCK_METHOD(void, PushNil, (), (override));
        MOCK_METHOD(void, PushString, (const char *val, unsigned int iLen));
        void PushString(const char *val)
        {
            return PushString(val, 0);
        }
        MOCK_METHOD(void, PushNumber, (double val), (override));
        MOCK_METHOD(void, PushBool, (bool val), (override));
        MOCK_METHOD(void, PushCFunction, (CFunc val), (override));
        MOCK_METHOD(void, PushCClosure, (CFunc val, int iVars), (override));
        MOCK_METHOD(void, PushUserdata, (void *), (override));
        MOCK_METHOD(int, ReferenceCreate, (), (override));
        MOCK_METHOD(void, ReferenceFree, (int i), (override));
        MOCK_METHOD(void, ReferencePush, (int i), (override));
        MOCK_METHOD(void, PushSpecial, (int iType), (override));
        MOCK_METHOD(bool, IsType, (int iStackPos, int iType), (override));
        MOCK_METHOD(int, GetType, (int iStackPos), (override));
        MOCK_METHOD(const char *, GetTypeName, (int iType), (override));
        MOCK_METHOD(void, CreateMetaTableType, (const char *strName, int iType), (override));
        MOCK_METHOD(const char *, CheckString, (int iStackPos));
        const char *CheckString()
        {
            return CheckString(-1);
        }
        MOCK_METHOD(double, CheckNumber, (int iStackPos));
        double CheckNumber()
        {
            return CheckNumber(-1);
        }
        MOCK_METHOD(int, ObjLen, (int iStackPos));
        int ObjLen()
        {
            return ObjLen(-1);
        }
        MOCK_METHOD(const QAngle &, GetAngle, (int iStackPos));
        const QAngle &GetAngle()
        {
            return GetAngle(-1);
        }
        MOCK_METHOD(const Vector &, GetVector, (int iStackPos));
        const Vector &GetVector()
        {
            return GetVector(-1);
        }
        MOCK_METHOD(void, PushAngle, (const QAngle &val), (override));
        MOCK_METHOD(void, PushVector, (const Vector &val), (override));
        MOCK_METHOD(void, SetState, (lua_State * L), (override));
        MOCK_METHOD(int, CreateMetaTable, (const char *strName), (override));
        MOCK_METHOD(bool, PushMetaTable, (int iType), (override));
        MOCK_METHOD(void, PushUserType, (void *data, int iType), (override));
        MOCK_METHOD(void, SetUserType, (int iStackPos, void *data), (override));
    };
}