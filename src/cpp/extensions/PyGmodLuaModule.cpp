#include "PyGmodLuaModule.hpp"

#include "init/InitException.hpp"

using std::shared_ptr;

namespace pygmod::extensions::lua
{
#define LUA_FUNC(name) int name(lua_State *state)

    shared_ptr<interop::python::IPython> python_instance;
    GarrysMod::Lua::ILuaBase *lua_instance;
    shared_ptr<interop::converters::IPythonToLuaValueConverter> py_to_lua_conv_instance;
    shared_ptr<interop::converters::ILuaToPythonValueConverter> lua_to_py_conv_instance;
    shared_ptr<interop::python::IPythonFunctionRegistry> py_func_registry;

    LUA_FUNC(py_exec)
    {
        const char *code = lua_instance->CheckString();
        python_instance->run_string(code);
        lua_instance->Pop();
        return 0;
    }

    // Imports a Python module.
    LUA_FUNC(py_import)
    {
        const auto module_name = lua_instance->CheckString();
        const auto module = python_instance->import_module(module_name);
        py_to_lua_conv_instance->convert(module);
        return 1;
    }

    LUA_FUNC(pass_call_to_py_func)
    {
        int arg_count = lua_instance->Top() - 1; // How much args have we got for our Python function?
        auto func_id = static_cast<interop::python::PyFuncId>(lua_instance->CheckNumber(1));
        auto args = python_instance->create_tuple(arg_count);

        for (int i = 0; i < arg_count; i++)
        {
            PyTuple_SET_ITEM(args, i,
                             lua_to_py_conv_instance->convert(i + 2)); // args for our function start at stack index 2
        }

        auto result = PyObject_Call((*py_func_registry)[func_id], args, NULL);
        if (!result)
        {
            PyErr_Print();
            lua_instance->ThrowError("exception in Python function");
        }
        py_to_lua_conv_instance->convert(result);
        return 1;
    }

#undef LUA_FUNC

    void set_python_instance(const shared_ptr<interop::python::IPython> &python)
    {
        python_instance = python;
    }

    void set_lua_instance(GarrysMod::Lua::ILuaBase *const lua)
    {
        lua_instance = lua;
    }

    void set_python_to_lua_value_converter_instance(const shared_ptr<interop::converters::IPythonToLuaValueConverter> &conv)
    {
        py_to_lua_conv_instance = conv;
    }

    void set_lua_to_python_value_converter_instance(const shared_ptr<interop::converters::ILuaToPythonValueConverter> &conv)
    {
        lua_to_py_conv_instance = conv;
    }

    void set_python_function_registry_instance(const std::shared_ptr<interop::python::IPythonFunctionRegistry> &reg)
    {
        py_func_registry = reg;
    }

    void init()
    {
        if (!python_instance)
        {
            throw init::InitException("python_instance was not set");
        }

        if (!lua_instance)
        {
            throw init::InitException("lua_instance was not set");
        }

        if (!lua_to_py_conv_instance)
        {
            throw init::InitException("lua_to_py_conv_instance was not set");
        }

        if (!py_to_lua_conv_instance)
        {
            throw init::InitException("py_to_lua_conv_instance was not set");
        }

        if (!py_func_registry)
        {
            throw init::InitException("py_func_registry was not set");
        }

        lua_instance->PushSpecial(GarrysMod::Lua::SPECIAL_GLOB);
        lua_instance->CreateTable(); // To be "py" table

        lua_instance->PushCFunction(py_exec);
        lua_instance->SetField(-2, "Exec");

        lua_instance->PushCFunction(py_import);
        lua_instance->SetField(-2, "Import");

        lua_instance->PushCFunction(pass_call_to_py_func);
        lua_instance->SetField(-2, "_passCallToPyFunc");

        // Adding "py" table to the global namespace
        lua_instance->SetField(-2, "py");
        lua_instance->Pop();
    }
}
