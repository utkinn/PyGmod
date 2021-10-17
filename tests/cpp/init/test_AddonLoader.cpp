#include <gtest/gtest.h>

#include "init/AddonLoader.hpp"
#include "mocks/PythonMock.hpp"

using testing::StrEq;

namespace pygmod::testing
{
    TEST(AddonLoader, delegates_to_python_loader)
    {
        PythonMock python;
        init::AddonLoader loader(python);
        EXPECT_CALL(python, run_string(StrEq("from pygmod import _loader; _loader.main()")));

        loader.load();
    }
}
