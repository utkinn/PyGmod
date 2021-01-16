# To compile PyGmod for Windows, stable 32-bit Garry's Mod branch, run in Developer Command Prompt for VS:
# Debug build:
#   cmake -A Win32 -DCMAKE_BUILD_TYPE=Debug . && msbuild -m PyGmod.sln
# Release build:
#   cmake -A Win32 . && msbuild -m PyGmod.sln -p:Configuration=Release
#
# To compile PyGmod for Linux, stable 32-bit Garry's Mod branch, run in terminal:
# cmake . && make

cmake_minimum_required(VERSION 3.13)

project(PyGmod)

if(NOT DEFINED CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

if(NOT DEFINED PYTHON_VERSION)
    set(PYTHON_VERSION 3.8)
endif()

string(REPLACE "." "" PYTHON_VERSION_NO_DOT ${PYTHON_VERSION})

add_subdirectory(cpp)

if(${CMAKE_BUILD_TYPE} EQUAL Debug)
    set(installer_generator_debug_args -d)
endif()
add_custom_command(OUTPUT installer-build/pygmod.pyz
    COMMAND buildscripts/generate-installer.py ${installer_generator_debug_args} ${PYTHON_VERSION_NO_DOT}
)
add_custom_target(installer ALL
    DEPENDS installer-build/pygmod.pyz
    COMMENT "Packing PyGmod installer"
)
add_dependencies(installer python-stdlib-dir)