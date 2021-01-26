// Provides PyFunctionRegistry class for storing Python functions which were sent to Lua, for example, hook and timer callbacks.
#pragma once

#include <vector>
#include <Python.h>

typedef unsigned int PyFuncId;

class PyFunctionRegistry {
    // Here we store Python functions that were sent to Lua.
    std::vector<PyObject *> funcTable;

    PyFuncId nextId = 0;

public:
    PyFuncId add(PyObject *);
    void remove(PyFuncId);
    PyObject *operator[](PyFuncId);

};

extern PyFunctionRegistry pyFunctionRegistry;
