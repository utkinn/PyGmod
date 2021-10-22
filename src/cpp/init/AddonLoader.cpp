#include "AddonLoader.hpp"

#include <exception>

#include "InitException.hpp"
#include "interop/python/PythonException.hpp"

namespace pygmod::init
{
    void AddonLoader::load()
    {
        try
        {
            python.run_string("from pygmod import _loader; _loader.main()");
        }
        catch (const interop::python::PythonException &)
        {
            std::throw_with_nested(InitException("failed to load addons due to a Python exception"));
        }
    }
}