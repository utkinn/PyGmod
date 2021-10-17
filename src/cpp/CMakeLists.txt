cmake_minimum_required(VERSION 3.13)

project(BinaryModulesAndPythonStdlib CXX)

set(BUILD_SHARED_LIBS ON)

# Setting up Garry's Mod module headers
include(ExternalProject)
ExternalProject_Add(gmod-module-base
    GIT_REPOSITORY https://github.com/Facepunch/gmod-module-base
    GIT_TAG origin/development
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
)
ExternalProject_Get_Property(gmod-module-base SOURCE_DIR)
include_directories(${SOURCE_DIR}/include)

# Download Python source
if(WIN32)
    set(python_build_flags --no-tkinter)
    if(${CMAKE_BUILD_TYPE} STREQUAL Debug)
        list(APPEND python_build_flags -d)
    endif()
    if(BITS EQUAL 64)
        list(APPEND python_build_flags -p x64)
    endif()
    ExternalProject_Add(cpython
        URL https://github.com/python/cpython/archive/${PYTHON_VERSION}.zip
        CONFIGURE_COMMAND ""
        BUILD_COMMAND "${PROJECT_SOURCE_DIR}\\cpython-prefix\\src\\cpython\\PCbuild\\build.bat" ${python_build_flags}
        INSTALL_COMMAND ""
    )
elseif(UNIX)
    set(python_install_prefix ${PROJECT_SOURCE_DIR}/cpython-out)
    if(BITS EQUAL 32)
        set(python_toolchain_flags CFLAGS=-m32 LDFLAGS=-m32)
    endif()
    if(${CMAKE_BUILD_TYPE} STREQUAL Release)
        set(python_configure_flags --enable-optimizations)
    endif()
    ExternalProject_Add(cpython
        URL https://github.com/python/cpython/archive/${PYTHON_VERSION}.zip
        CONFIGURE_COMMAND ${python_toolchain_flags} "${PROJECT_SOURCE_DIR}/cpython-prefix/src/cpython/configure" --config-cache "--prefix=${PROJECT_SOURCE_DIR}/cpython-out" --enable-shared ${python_configure_flags}
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

add_compile_definitions(GMMODULE GMOD_ALLOW_DEPRECATED)

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
    set_target_properties(main PROPERTIES
        COMPILE_DEFINITIONS "PY_SSIZE_T_CLEAN;PYTHON_VERSION=${PYTHON_VERSION}"
        OUTPUT_NAME pygmod
        CXX_STANDARD 20
        CXX_STANDARD_REQUIRED ON
    )
    if(BITS EQUAL 32)
        set_target_properties(main PROPERTIES
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
