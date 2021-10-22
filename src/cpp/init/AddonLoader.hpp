#pragma once

#include <memory>

#include "IAddonLoader.hpp"
#include "interop/python/IPython.hpp"

namespace pygmod::init
{
    class AddonLoader : public IAddonLoader
    {
    public:
        AddonLoader(interop::python::IPython &python) : python(python)
        {
        }
        void load() override;

    private:
        interop::python::IPython &python;
    };
}