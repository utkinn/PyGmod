cmake_minimum_required(VERSION 3.10)

project(PyGmod CXX)

set(BUILD_SHARED_LIBS ON)
set(CMAKE_BUILD_TYPE RelWithDebInfo)

### 32 OR 64 BITS ###
if(NOT DEFINED BITS)
    set(BITS 32)
    message("Using default BITS value: 32.")
    message("Use \"cmake -DBITS=64 .\" to compile for x86-64 branch of Garry's Mod.")
endif()
if(NOT BITS MATCHES "32|64")
    message(FATAL_ERROR "Invalid BITS value: \"${BITS}\". Please use one of \"32\" or \"64\".")
endif()

if(WIN32)
    if(BITS EQUAL 32)
        message("Building for win32 (stable Garry's Mod branch, 32-bit)")
        set(CMAKE_GENERATOR_PLATFORM Win32)
    else()
        message("Building for x64 (x86-64 Garry's Mod branch, 64-bit)")
        set(CMAKE_GENERATOR_PLATFORM x64)
    endif()
endif()

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

# Setting up Python
find_package(Python REQUIRED COMPONENTS Development)
add_compile_definitions(GMMODULE)

### SHARED MODULE ###

set(MAIN_DLL_SRC_DIR main)
file(GLOB_RECURSE MAIN_DLL_SOURCES ${MAIN_DLL_SRC_DIR}/*.cpp ${MAIN_DLL_SRC_DIR}/*.hpp)
add_library(main ${MAIN_DLL_SOURCES})
add_dependencies(main gmod-module-base)
set_target_properties(main PROPERTIES
    COMPILE_DEFINITIONS PY_SSIZE_T_CLEAN
    OUTPUT_NAME pygmod
)
target_include_directories(main PRIVATE ${Python_INCLUDE_DIRS})
target_link_libraries(main ${Python_LIBRARIES})

### CLIENT AND SERVER MODULES ###

macro(realm_module realm gm_prefix)
    file(GLOB DLL_SOURCES ${realm}/*.cpp ${realm}/*.hpp)
    add_library(${realm} ${DLL_SOURCES})
    add_dependencies(${realm} gmod-module-base)
    if(UNIX)
        if (BITS EQUAL 64)
            set(output_name gm${gm_prefix}_pygmod_linux64)
            set(cflags "")
        else()
            set(output_name gm${gm_prefix}_pygmod_linux)
            set(cflags "-m32")
        endif()
        set_target_properties(${realm} PROPERTIES OUTPUT_NAME ${output_name} PREFIX "" SUFFIX ".dll" COMPILE_OPTIONS ${cflags})
    else()
        set_target_properties(${realm} PROPERTIES OUTPUT_NAME gm${gm_prefix}_pygmod_win32)
    endif()
    target_link_libraries(${realm} main)
endmacro()

realm_module(client cl)
realm_module(server sv)
