#include "PythonFunctionRegistry.hpp"

namespace pygmod::interop
{
    PyFuncId PythonFunctionRegistry::add(PyObject *func)
    {
        Py_INCREF(func);
        func_table.push_back(func);
        return next_id++;
    }

    void PythonFunctionRegistry::remove(PyFuncId id)
    {
        Py_DECREF(func_table[id]);
        func_table[id] = nullptr;
    }

    PyObject *PythonFunctionRegistry::operator[](PyFuncId id)
    {
        return func_table[id];
    }
}
