#pragma once

#include <vector>

#include "IPythonFunctionRegistry.hpp"

namespace pygmod::interop
{
    class PythonFunctionRegistry : public IPythonFunctionRegistry
    {
    public:
        PyFuncId add(PyObject *) override;
        void remove(PyFuncId) override;
        PyObject *operator[](PyFuncId) override;

    private:
        std::vector<PyObject *> func_table;

        PyFuncId next_id = 0;
    };
}
