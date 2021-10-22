cmake_minimum_required(VERSION 3.10)
project(RunTests CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED true)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

set(INSTALL_GTEST false)
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest
    GIT_SHALLOW true
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

FetchContent_Declare(
    gmod_module_base
    GIT_REPOSITORY https://github.com/Facepunch/gmod-module-base
    GIT_TAG origin/development
    GIT_SHALLOW true
)
FetchContent_MakeAvailable(gmod_module_base)

enable_testing()

set(TEST_DIR .)
set(SRC_DIR ../../src/cpp)
add_executable(
    run_gtests

    ${TEST_DIR}/gtest_main.cpp
    ${TEST_DIR}/init/test_AddonLoader.cpp
    ${TEST_DIR}/interop/converters/test_LuaToPythonValueConverter.cpp
    ${TEST_DIR}/interop/lua/test_Lua.cpp
    ${TEST_DIR}/interop/lua/test_LuaValue.cpp

    ${SRC_DIR}/init/AddonLoader.cpp
    ${SRC_DIR}/interop/lua/Lua.cpp
    ${SRC_DIR}/interop/lua/LuaValue.cpp
)
target_include_directories(
    run_gtests PRIVATE
    ${SRC_DIR}
    ${TEST_DIR}
    ${gmod_module_base_SOURCE_DIR}/include
)
target_link_libraries(run_gtests gtest_main gmock_main ${PYTHON_LIBRARIES})
set_target_properties(
    run_gtests PROPERTIES
    COMPILE_DEFINITIONS GMOD_ALLOW_DEPRECATED
)
include(GoogleTest)
gtest_discover_tests(run_gtests)