# To compile PyGmod for Windows, stable 32-bit Garry's Mod branch, run in Developer Command Prompt for VS:
# cmake -A Win32 . && msbuild -m BinaryModulesAndPythonStdlib.sln
# To compile PyGmod for Linux, stable 32-bit Garry's Mod branch, run in terminal:
# cmake . && make

cmake_minimum_required(VERSION 3.13)

macro(unknown_os_error)
    message(FATAL_ERROR "Unknown OS. PyGmod is supported only on Windows and Linux.")
endmacro()

# Defining Python version

if(NOT DEFINED PYTHON_VERSION)
    set(PYTHON_VERSION 3.8)
endif()

string(REPLACE "." "" PYTHON_VERSION_NO_DOT ${PYTHON_VERSION})

project(BinaryModulesAndPythonStdlib CXX)

set(BUILD_SHARED_LIBS ON)
set(CMAKE_BUILD_TYPE RelWithDebInfo)

# Setting up Garry's Mod module headers
include(ExternalProject)
ExternalProject_Add(gmod-module-base
    GIT_REPOSITORY https://github.com/Facepunch/gmod-module-base
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
)
ExternalProject_Get_Property(gmod-module-base SOURCE_DIR)
include_directories(${SOURCE_DIR}/include)

# Download Python source
if(WIN32)
    ExternalProject_Add(cpython
        URL https://github.com/python/cpython/archive/${PYTHON_VERSION}.zip
        CONFIGURE_COMMAND ""
        BUILD_COMMAND "${PROJECT_SOURCE_DIR}\\cpython-prefix\\src\\cpython\\PCbuild\\build.bat" -d --no-tkinter
        INSTALL_COMMAND ""
    )
elseif(UNIX)
    set(python_install_prefix ${PROJECT_SOURCE_DIR}/cpython-out)
    ExternalProject_Add(cpython
        URL https://github.com/python/cpython/archive/${PYTHON_VERSION}.zip
        CONFIGURE_COMMAND CFLAGS=-m32 LDFLAGS=-m32 "${PROJECT_SOURCE_DIR}/cpython-prefix/src/cpython/configure" --config-cache "--prefix=${PROJECT_SOURCE_DIR}/cpython-out"
        BUILD_COMMAND make
        INSTALL_COMMAND make install
    )
else()
    unknown_os_error()
endif()
ExternalProject_Get_Property(cpython SOURCE_DIR)
set(PYTHON_SOURCE_DIR ${SOURCE_DIR})

# Python headers
if(WIN32)
    include_directories(${PYTHON_SOURCE_DIR}/Include ${PYTHON_SOURCE_DIR}/PC)
elseif(UNIX)
    include_directories(${python_install_prefix}/include/python${PYTHON_VERSION})
else()
    unknown_os_error()
endif()

add_compile_definitions(GMMODULE)

# Main module

file(GLOB_RECURSE MAIN_SOURCES main/*.cpp)
add_library(main ${MAIN_SOURCES})
add_dependencies(main gmod-module-base cpython)
if (WIN32)
    set_target_properties(main PROPERTIES
        COMPILE_DEFINITIONS PY_SSIZE_T_CLEAN
        OUTPUT_NAME pygmod
        CXX_STANDARD 20
        CXX_STANDARD_REQUIRED ON
    )
    target_link_libraries(main
        ${PYTHON_SOURCE_DIR}/PCbuild/win32/python${PYTHON_VERSION_NO_DOT}_d.lib
    )
elseif(UNIX)
    set_target_properties(main PROPERTIES
        COMPILE_DEFINITIONS PY_SSIZE_T_CLEAN
        OUTPUT_NAME pygmod
        CXX_STANDARD 20
        CXX_STANDARD_REQUIRED ON
        COMPILE_OPTIONS -m32
        LINK_OPTIONS -m32
    )
    target_link_libraries(main
        ${PYTHON_SOURCE_DIR}/PCbuild/win32/python${PYTHON_VERSION_NO_DOT}_d.lib
    )
else()
    unknown_os_error()
endif()

# Client and server modules

macro(realm_module realm gm_prefix)
    file(GLOB REALM_DLL_SOURCES ${realm}/*.cpp)
    add_library(${realm} ${REALM_DLL_SOURCES})
    add_dependencies(${realm} gmod-module-base)
    if (WIN32)
        set_target_properties(${realm} PROPERTIES
            OUTPUT_NAME gm${gm_prefix}_pygmod_win32
            PREFIX ""
            SUFFIX ".dll"
        )
    elseif(UNIX)
        set_target_properties(${realm} PROPERTIES
            OUTPUT_NAME gm${gm_prefix}_pygmod_linux
            PREFIX ""
            SUFFIX ".dll"
            COMPILE_OPTIONS -m32
            LINK_OPTIONS -m32
        )
    else()
        unknown_os_error()
    endif()
    target_link_libraries(${realm} main)
endmacro()

realm_module(client cl)
realm_module(server sv)

# Python standard library collection

if(WIN32)
    add_custom_command(OUTPUT stdlib.generated
        COMMAND ${CMAKE_COMMAND} "-DPYTHON_SOURCE_DIR=${PYTHON_SOURCE_DIR}" -P buildscripts/python-stdlib-dir.cmake
    )
    add_custom_target(python-stdlib-dir ALL
        DEPENDS stdlib.generated
        COMMENT "Python standard library directiory"
    )
    add_dependencies(python-stdlib-dir cpython)
endif()  # On Linux, cpython's make install collects stdlib into cpython-out/lib/python3.X by itself
