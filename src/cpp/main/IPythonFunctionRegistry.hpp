#pragma once

#include <Python.h>

namespace pygmod::interop
{
    using PyFuncId = unsigned int;

    class IPythonFunctionRegistry
    {
    public:
        virtual PyFuncId add(PyObject *) = 0;
        virtual void remove(PyFuncId) = 0;
        virtual PyObject *operator[](PyFuncId) = 0;
    };
}
