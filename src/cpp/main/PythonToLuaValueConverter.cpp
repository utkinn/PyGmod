#include "PythonToLuaValueConverter.hpp"

#include <string>

#include "LuaCustomTypes.hpp"

using GarrysMod::Lua::ILuaBase;

namespace pygmod::converters
{
    void PythonToLuaValueConverter::convert(PyObject *obj)
    {
        if (obj == Py_None)
        {
            lua->PushNil();
        }
        else if (PyBool_Check(obj))
        {
            lua->PushBool(PyObject_IsTrue(obj));
        }

        else if (PyNumber_Check(obj))
        {
            PyObject *numberAsPyFloat = PyNumber_Float(obj);
            lua->PushNumber(PyFloat_AsDouble(numberAsPyFloat));
            Py_DECREF(numberAsPyFloat);
        }

        else if (PyBytes_Check(obj))
        {
            lua->PushString(PyBytes_AsString(obj));
        }

        else if (PyUnicode_Check(obj))
        {
            lua->PushString(PyUnicode_AsUTF8(obj));
        }

        else if (PyFunction_Check(obj))
        {
            auto funcIdString = std::to_string(py_func_registry->add(obj));

            lua->PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
            lua->GetField(-1, "RunString");
            lua->PushString(
                (std::string("_pygmod_func = function(...) return py._passCallToPyFunc(") + funcIdString + ", ...) end")
                    .c_str());
            lua->Call(1, 0);
            lua->GetField(-1, "_pygmod_func");
            lua->PushNil();
            lua->SetField(-3, "_pygmod_func");
            lua->Remove(-2); // Removing _G
        }
        else if (PyObject_HasAttrString(obj, "_ref"))
        {
            // obj is a pygmod.lua.LuaObject instance.
            // Pushing the Lua value that this LuaObject represents.
            PyObject *refPyInt = PyObject_GetAttrString(obj, "_ref");
            int refCInt = PyLong_AsLong(refPyInt);
            lua->ReferencePush(refCInt);
            Py_DECREF(refPyInt);
        }
        else
        {
            // Other Python objects are represented by a custom metatable type
            // defined in luapyobject.cpp.

            // Py_INCREF is necessary because otherwise that Python object could be deallocated even though being stored
            // in our userdata. By increasing the reference count we tell Python that this object is still in use and
            // therefore shouldn't be destroyed by the garbage collector.
            Py_INCREF(obj);
            const auto py_object_userdata_container =
                static_cast<ILuaBase::UserData *>(lua->NewUserdata(sizeof(ILuaBase::UserData)));
            py_object_userdata_container->data = reinterpret_cast<void *>(obj);
            if (PyCallable_Check(obj))
            {
                py_object_userdata_container->type = interop::lua::LUA_TYPE_PYCALLABLE;
                lua->CreateMetaTableType("PyCallable", interop::lua::LUA_TYPE_PYCALLABLE);
            }
            else
            {
                py_object_userdata_container->type = interop::lua::LUA_TYPE_PYOBJECT;
                lua->CreateMetaTableType("PyObject", interop::lua::LUA_TYPE_PYOBJECT);
            }
            lua->SetMetaTable(-2);
        }
    }
}
