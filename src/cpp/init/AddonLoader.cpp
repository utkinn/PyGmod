#include "AddonLoader.hpp"

namespace pygmod::init
{
    void AddonLoader::load()
    {
        python.run_string("from pygmod import _loader; _loader.main()");
    }
}