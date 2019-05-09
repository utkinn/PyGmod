cmake_minimum_required(VERSION 3.10)
project(RunTests CXX)

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

set(TEST_DIR .)
set(SRC_DIR ../../src/cpp)
set(SOURCES ${TEST_DIR}/gtest_main.cc
    ${TEST_DIR}/client/test_main.cc
    ${TEST_DIR}/main/test_console.cc
    ${TEST_DIR}/main/test_main.cc
    ${TEST_DIR}/main/test_lua2py_interop.cc
    ${TEST_DIR}/py_extensions/test_luapyobject.cc
    ${TEST_DIR}/py_extensions/test_luastack.cc
    ${TEST_DIR}/py_extensions/test_stack_utils.cc
    ${TEST_DIR}/server/test_main.cc

    ${SRC_DIR}/main/Console.hpp
    ${SRC_DIR}/main/lua2py_interop.hpp
    ${SRC_DIR}/py_extensions/luapyobject.hpp
    ${SRC_DIR}/py_extensions/_luastack.hpp
    ${SRC_DIR}/py_extensions/stack_utils.hpp
)

add_executable(run_gtests ${SOURCES})
target_include_directories(run_gtests PRIVATE ${SRC_DIR}/main ${SRC_DIR}/py_extensions)
target_link_libraries(run_gtests ${GTEST_LIBRARIES} pthread ${PYTHON_LIBRARIES})
