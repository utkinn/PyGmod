# To compile PyGmod for Windows, run in Developer Command Prompt for VS:
# Debug build for stable 32-bit Garry's Mod branch:
#   cmake -A Win32 -B build -DCMAKE_BUILD_TYPE=Debug . && cmake --build build --config Debug
# Debug build for x86-64 Garry's Mod branch:
#   cmake -A x64 -B build -DCMAKE_BUILD_TYPE=Debug . && cmake --build build --config Debug
# Release build for stable 32-bit Garry's Mod branch:
#   cmake -A Win32 -B build . && cmake --build build --config Release
# Release build for x86-64 Garry's Mod branch:
#   cmake -A x64 -B build . && cmake --build build --config Release
#
# To compile version of PyGmod for Linux, run in terminal:
# Debug build for stable 32-bit Garry's Mod branch:
#   cmake -B build -DCMAKE_BUILD_TYPE=Debug . && cmake --build build
# Debug build for x86-64 Garry's Mod branch:
#   cmake -B build -DCMAKE_BUILD_TYPE=Debug -DBITS=64 . && cmake --build build
# Release build for stable 32-bit Garry's Mod branch:
#   cmake -B build . && cmake --build build
# Release build for x86-64 Garry's Mod branch:
#   cmake -B build -DBITS=64 . && cmake --build build

cmake_minimum_required(VERSION 3.13)

project(PyGmod)

macro(unknown_os_error)
    message(FATAL_ERROR "Unknown OS. PyGmod is supported only on Windows and Linux.")
endmacro()

set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type (Release/Debug/RelWithDebugInfo)")
set(PYTHON_VERSION 3.10 CACHE STRING "Embedded Python version (3.10)")
string(REPLACE "." "" PYTHON_VERSION_NO_DOT ${PYTHON_VERSION})
if(NOT BITS)
    if(CMAKE_GENERATOR_PLATFORM STREQUAL x64)
        set(BITS 64 CACHE STRING "PyGmod binary module bitness (32/64)")
    else()
        set(BITS 32 CACHE STRING "PyGmod binary module bitness (32/64)")
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

set(installer_generator_args -b ${BITS})

if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
    list(APPEND installer_generator_args -d)
endif()

if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
    list(APPEND installer_suffix -debug)
endif()

set(installer_file ${CMAKE_CURRENT_BINARY_DIR}/installer/pygmod-${installer_suffix}.pyz)
add_custom_command(OUTPUT ${installer_file}
    COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/buildscripts/installer_generator.py ${installer_generator_args} ${PYTHON_VERSION} ${CMAKE_CURRENT_BINARY_DIR} ${installer_file}
)
add_custom_target(installer ALL
    DEPENDS ${installer_file}
    COMMENT "Packing PyGmod installer"
)
add_dependencies(installer main)
