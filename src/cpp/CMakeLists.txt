cmake_minimum_required(VERSION 3.13)

project(BinaryModulesAndPythonStdlib CXX)

include(FetchContent)
include(ExternalProject)

set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type")

if(NOT PYTHON_VERSION)
    message(FATAL_ERROR "PYTHON_VERSION is required. Try using src/CMakeLists.txt for building instead.")
endif()

# Setting up Garry's Mod module headers
FetchContent_Declare(
    gmod_module_base
    GIT_REPOSITORY https://github.com/Facepunch/gmod-module-base
    GIT_TAG origin/development
    GIT_SHALLOW true
)
FetchContent_MakeAvailable(gmod_module_base)
set_target_properties(HelloWorld MetaTable PROPERTIES EXCLUDE_FROM_ALL true)

# Download Python source
if(WIN32)
    set(python_build_flags --no-tkinter)

    if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
        list(APPEND python_build_flags -d)
    endif()

    if(BITS EQUAL 64)
        list(APPEND python_build_flags -p x64)
    endif()
    
    ExternalProject_Add(
        cpython
        URL https://github.com/python/cpython/archive/${PYTHON_VERSION}.zip
        PREFIX ${CMAKE_CURRENT_BINARY_DIR}/cpython
        DOWNLOAD_DIR cpython/download
        SOURCE_DIR cpython/source
        CONFIGURE_COMMAND ""
        BUILD_COMMAND "${CMAKE_CURRENT_BINARY_DIR}\\cpython\\source\\PCbuild\\build.bat" ${python_build_flags}
        INSTALL_COMMAND ""
    )
elseif(UNIX)
    set(python_install_prefix ${CMAKE_CURRENT_BINARY_DIR}/cpython/out)
    if(BITS EQUAL 32)
        set(python_toolchain_flags CFLAGS=-m32 LDFLAGS=-m32)
    endif()
    if(${CMAKE_BUILD_TYPE} STREQUAL Release)
        set(python_configure_flags --enable-optimizations)
    endif()
    ExternalProject_Add(
        cpython
        URL https://github.com/python/cpython/archive/${PYTHON_VERSION}.zip
        PREFIX ${CMAKE_CURRENT_BINARY_DIR}/cpython
        DOWNLOAD_DIR cpython/download
        SOURCE_DIR cpython/source
        CONFIGURE_COMMAND ${python_toolchain_flags} "${CMAKE_CURRENT_BINARY_DIR}/cpython/source/configure" --config-cache "--prefix=${CMAKE_CURRENT_BINARY_DIR}/cpython/out" --enable-shared ${python_configure_flags}
        BUILD_COMMAND make -j
        INSTALL_COMMAND make -j install
    )
else()
    unknown_os_error()
endif()

ExternalProject_Get_Property(cpython SOURCE_DIR)
set(PYTHON_SOURCE_DIR ${SOURCE_DIR})
ExternalProject_Get_Property(cpython BINARY_DIR)
set(PYTHON_BUILD_DIR ${BINARY_DIR})

# Python headers
if(WIN32)
    include_directories(${PYTHON_SOURCE_DIR}/Include ${PYTHON_SOURCE_DIR}/PC)
elseif(UNIX)
    include_directories(${python_install_prefix}/include/python${PYTHON_VERSION})
else()
    unknown_os_error()
endif()

add_compile_definitions()

add_library(
    main SHARED

    extensions/LuaStackPythonModule.cpp
    extensions/PyGmodLuaModule.cpp

    init/AddonLoader.cpp
    init/PyGmod.cpp

    interop/converters/LuaToPythonValueConverter.cpp
    interop/converters/PythonToLuaValueConverter.cpp

    interop/lua/Lua.cpp
    interop/lua/LuaValue.cpp
    interop/lua/LuaValueFactory.cpp

    interop/python/Python.cpp
    interop/python/PythonFunctionRegistry.cpp
    interop/python/PythonPathProvider.cpp

    util/FileSystem.cpp
    util/Logger.cpp

    main.cpp
)
add_dependencies(main cpython)
target_include_directories(main PRIVATE . ${gmod_module_base_SOURCE_DIR}/include)
target_link_directories(main PRIVATE ${PYTHON_SOURCE_DIR}/PCbuild/win32 ${PYTHON_SOURCE_DIR}/PCbuild/amd64)
set_target_properties(
    main PROPERTIES
    COMPILE_DEFINITIONS "PY_SSIZE_T_CLEAN;GMOD_ALLOW_DEPRECATED"
    OUTPUT_NAME pygmod
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED true
)
if (WIN32)
    if(BITS EQUAL 32)
        set(pcbuild_dir win32)
    else()
        set(pcbuild_dir amd64)
    endif()
    if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
        target_link_libraries(main
            ${PYTHON_SOURCE_DIR}/PCbuild/${pcbuild_dir}/python${PYTHON_VERSION_NO_DOT}_d.lib
        )
    else()
        target_link_libraries(main
            ${PYTHON_SOURCE_DIR}/PCbuild/${pcbuild_dir}/python${PYTHON_VERSION_NO_DOT}.lib
        )
    endif()
elseif(UNIX)
    if(BITS EQUAL 32)
        set_target_properties(
            main PROPERTIES
            COMPILE_OPTIONS -m32
            LINK_OPTIONS -m32
        )
    endif()
    target_link_libraries(main
        ${PYTHON_BUILD_DIR}/libpython${PYTHON_VERSION}.so.1.0
        libutil.a  # Requires libc6-dev:i386 on Debian, lib32-glibc on Arch Linux
    )
else()
    unknown_os_error()
endif()