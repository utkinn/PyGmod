cmake_minimum_required(VERSION 3.10)
project(RunTests CXX)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

set(SRC_DIR ./tests/)
set(SOURCES ${SRC_DIR}/gtest_main.cc
    ${SRC_DIR}/python_extensions/test_luapyobject.cc
    ${SRC_DIR}/python_extensions/test_luastack.cc
    ${SRC_DIR}/python_extensions/test_stack_utils.cc
    ./python_extensions/luapyobject.hpp
    ./python_extensions/_luastack.hpp
    ./python_extensions/stack_utils.hpp
)

add_executable(run_gtests ${SOURCES})
target_include_directories(run_gtests PRIVATE ./python_extensions)
target_link_libraries(run_gtests ${GTEST_LIBRARIES} pthread ${PYTHON_LIBRARIES})
