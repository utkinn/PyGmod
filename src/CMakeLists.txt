# To compile PyGmod for Windows, run in Developer Command Prompt for VS:
# Debug build for stable 32-bit Garry's Mod branch:
#   cmake -A Win32 -DCMAKE_BUILD_TYPE=Debug . && msbuild -m PyGmod.sln -p:Configuration=Debug
# Debug build for x86-64 Garry's Mod branch:
#   cmake -A x64 -DCMAKE_BUILD_TYPE=Debug . && msbuild -m PyGmod.sln -p:Configuration=Debug
# Release build for stable 32-bit Garry's Mod branch:
#   cmake -A Win32 . && msbuild -m PyGmod.sln -p:Configuration=Release
# Release build for x86-64 Garry's Mod branch:
#   cmake -A x64 . && msbuild -m PyGmod.sln -p:Configuration=Release
#
# To compile version of PyGmod for Linux, run in terminal:
# Debug build for stable 32-bit Garry's Mod branch:
#   cmake -DCMAKE_BUILD_TYPE=Debug . && make
# Debug build for x86-64 Garry's Mod branch:
#   cmake -DCMAKE_BUILD_TYPE=Debug -DBITS=64 . && make
# Release build for stable 32-bit Garry's Mod branch:
#   cmake . && make
# Release build for x86-64 Garry's Mod branch:
#   cmake -DBITS=64 . && make

cmake_minimum_required(VERSION 3.13)

project(PyGmod)

macro(unknown_os_error)
    message(FATAL_ERROR "Unknown OS. PyGmod is supported only on Windows and Linux.")
endmacro()

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

if(NOT PYTHON_VERSION)
    set(PYTHON_VERSION 3.10)
endif()

string(REPLACE "." "" PYTHON_VERSION_NO_DOT ${PYTHON_VERSION})

if(NOT BITS)
    if(CMAKE_GENERATOR_PLATFORM STREQUAL x64)
        set(BITS 64)
    else()
        set(BITS 32)
    endif()
endif()

add_subdirectory(cpp)

if(WIN32)
    set(installer_suffix win${BITS})
elseif(UNIX)
    set(installer_suffix linux${BITS})
else()
    unknown_os_error()
endif()

if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
    set(installer_generator_args -d)
endif()

if(BITS EQUAL 64)
    list(APPEND installer_generator_args -b 64)
endif()

if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
    string(APPEND installer_suffix -debug)
endif()

set(installer_file installer-build/pygmod-${installer_suffix}.pyz)
add_custom_command(OUTPUT ${installer_file}
    COMMAND buildscripts/generate-installer.py ${installer_generator_args} ${PYTHON_VERSION} ${installer_file}
)
add_custom_target(installer ALL
    DEPENDS ${installer_file}
    COMMENT "Packing PyGmod installer"
)
add_dependencies(installer main client server)
if(WIN32)
    add_dependencies(installer python-stdlib-dir)
endif()
