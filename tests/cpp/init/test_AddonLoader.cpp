#include <gtest/gtest.h>

#include "init/AddonLoader.hpp"
#include "init/InitException.hpp"
#include "interop/python/PythonException.hpp"
#include "mocks/PythonMock.hpp"

using testing::StrEq;
using testing::Throw;

namespace pygmod::testing
{
    TEST(AddonLoader, delegates_to_python_loader)
    {
        PythonMock python;
        init::AddonLoader loader(python);
        EXPECT_CALL(python, run_string(StrEq("from pygmod import _loader; _loader.main()")));

        loader.load();
    }

    TEST(AddonLoader, handles_loading_failure)
    {
        PythonMock python;
        init::AddonLoader loader(python);
        EXPECT_CALL(python, run_string(StrEq("from pygmod import _loader; _loader.main()")))
            .WillOnce(Throw(interop::python::PythonException("gah")));

        EXPECT_THROW(loader.load(), init::InitException);
    }
}
