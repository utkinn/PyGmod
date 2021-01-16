# To compile PyGmod for Windows, stable 32-bit Garry's Mod branch, run in Developer Command Prompt for VS:
# Debug build:
#   cmake -A Win32 -DCMAKE_BUILD_TYPE=Debug . && msbuild -m PyGmod.sln -p:Configuration=Debug
# Release build:
#   cmake -A Win32 . && msbuild -m PyGmod.sln -p:Configuration=Release
#
# To compile PyGmod for Linux, stable 32-bit Garry's Mod branch, run in terminal:
#   cmake . && make

cmake_minimum_required(VERSION 3.13)

project(PyGmod)

macro(unknown_os_error)
    message(FATAL_ERROR "Unknown OS. PyGmod is supported only on Windows and Linux.")
endmacro()

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

if(NOT PYTHON_VERSION)
    set(PYTHON_VERSION 3.8)
endif()

string(REPLACE "." "" PYTHON_VERSION_NO_DOT ${PYTHON_VERSION})

add_subdirectory(cpp)

if(WIN32)
    set(installer_suffix win32)
elseif(UNIX)
    set(installer_suffix linux32)
else()
    unknown_os_error()
endif()

if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
    set(installer_generator_args -d)
endif()

if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
    string(APPEND installer_suffix -debug)
endif()

set(installer_file installer-build/pygmod-${installer_suffix}.pyz)
add_custom_command(OUTPUT ${installer_file}
    COMMAND buildscripts/generate-installer.py ${installer_generator_args} ${PYTHON_VERSION_NO_DOT} ${installer_file}
)
add_custom_target(installer ALL
    DEPENDS ${installer_file}
    COMMENT "Packing PyGmod installer"
)
add_dependencies(installer main client server)
if(WIN32)
    add_dependencies(installer python-stdlib-dir)
endif()