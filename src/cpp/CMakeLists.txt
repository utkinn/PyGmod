cmake_minimum_required(VERSION 3.10)

project(PyGmod CXX)

set(BUILD_SHARED_LIBS ON)
set(CMAKE_BUILD_TYPE RelWithDebInfo)

# Determine 32 vs 64 bit
set(bitness 32)
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
  set(bitness 64)
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
    if (UNIX)
        if (bitness EQUAL 64)
            set(output_name gm${gm_prefix}_pygmod_linux64)
        else()
            set(output_name gm${gm_prefix}_pygmod_linux)
        endif()
        set_target_properties(${realm} PROPERTIES OUTPUT_NAME ${output_name} PREFIX "" SUFFIX ".dll")
    else()
        set_target_properties(${realm} PROPERTIES OUTPUT_NAME gm${gm_prefix}_pygmod_win32)
    endif()
    target_link_libraries(${realm} main)
endmacro()

realm_module(client cl)
realm_module(server sv)
