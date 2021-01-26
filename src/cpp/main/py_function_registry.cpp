#include "py_function_registry.hpp"

PyFunctionRegistry pyFunctionRegistry;

PyFuncId PyFunctionRegistry::add(PyObject *func) {
    Py_INCREF(func);
    funcTable.push_back(func);
    return nextId++;
}

void PyFunctionRegistry::remove(PyFuncId id) {
    Py_DECREF(funcTable[id]);
    funcTable[id] = nullptr;
}

PyObject *PyFunctionRegistry::operator[](PyFuncId id) {
    return funcTable[id];
}
