cmake_minimum_required(VERSION 3.10)
project(RunTests CXX)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

set(INSTALL_GTEST false)
include(FetchContent)
FetchContent_Declare(
    gtest
    GIT_REPOSITORY https://github.com/google/googletest
    GIT_SHALLOW true
)
FetchContent_MakeAvailable(gtest)

set(TEST_DIR .)
set(SRC_DIR ../../src/cpp/main)
set(SOURCES
    ${TEST_DIR}/gtest_main.cpp
    ${TEST_DIR}/test_AddonLoader.cpp

    ${SRC_DIR}/AddonLoader.cpp
)

add_executable(run_gtests ${SOURCES})
target_include_directories(run_gtests PRIVATE ${SRC_DIR}/main ${SRC_DIR})
target_link_libraries(run_gtests gtest gtest_main gmock gmock_main ${PYTHON_LIBRARIES})
