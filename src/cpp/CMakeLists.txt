cmake_minimum_required(VERSION 3.10)

project(PyGmod CXX)

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

# Setting up Python
find_package(Python REQUIRED COMPONENTS Development)
add_compile_definitions(GMMODULE)

set(MAIN_DLL_SRC_DIR main)
file(GLOB_RECURSE MAIN_DLL_SOURCES ${MAIN_DLL_SRC_DIR}/*.cpp ${MAIN_DLL_SRC_DIR}/*.hpp)
add_library(main ${MAIN_DLL_SOURCES})
set_target_properties(main PROPERTIES
    COMPILE_DEFINITIONS PY_SSIZE_T_CLEAN
    OUTPUT_NAME pygmod
)
target_include_directories(main PRIVATE ${Python_INCLUDE_DIRS})
target_link_libraries(main ${Python_LIBRARIES})

set(CLIENT_DLL_SRC_DIR client)
file(GLOB CLIENT_DLL_SOURCES ${CLIENT_DLL_SRC_DIR}/*.cpp ${CLIENT_DLL_SRC_DIR}/*.hpp)
add_library(client ${CLIENT_DLL_SOURCES})
set_target_properties(client PROPERTIES OUTPUT_NAME gmcl_pygmod_win32)
target_link_libraries(client main)

set(SERVER_DLL_SRC_DIR server)
file(GLOB SERVER_DLL_SOURCES ${SERVER_DLL_SRC_DIR}/*.cpp ${SERVER_DLL_SRC_DIR}/*.hpp)
add_library(server ${SERVER_DLL_SOURCES})
set_target_properties(server PROPERTIES OUTPUT_NAME gmsv_pygmod_win32)
target_link_libraries(server main)
