cmake_minimum_required(VERSION 3.15)

# ---------------------------------------------------------------------------
# Optional: install a pre-built extension instead of compiling from source.
# Set the PREBUILT_PYD environment variable (or pass -DPREBUILT_PYD=<path>)
# to the absolute path of a previously compiled hello_world .pyd/.so file.
# bootstrap.ps1 / bootstrap.sh set this automatically when a cached build
# is available.  Using LANGUAGES NONE avoids compiler detection on cache hits.
# ---------------------------------------------------------------------------
if(NOT DEFINED PREBUILT_PYD)
    set(PREBUILT_PYD "$ENV{PREBUILT_PYD}")
endif()
# Normalise to forward slashes so CMake does not misinterpret Windows
# backslashes as escape sequences (e.g. \a, \n) in the install() call.
if(PREBUILT_PYD)
    file(TO_CMAKE_PATH "${PREBUILT_PYD}" PREBUILT_PYD)
endif()

if(PREBUILT_PYD)
    # Cache hit: install the pre-built extension without any compilation.
    project(hello_world LANGUAGES NONE)
    message(STATUS "Cache hit: installing pre-built extension ${PREBUILT_PYD}")
    install(FILES "${PREBUILT_PYD}" DESTINATION ansys/edb/core/)

else()
    # Build the pybind11 extension from source.  Works on Windows, Linux,
    # and macOS without any platform-specific configuration.
    project(hello_world LANGUAGES CXX)
    find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
    find_package(pybind11 CONFIG REQUIRED)

    pybind11_add_module(hello_world deps/hello_world_bindings.cpp)
    target_compile_features(hello_world PRIVATE cxx_std_17)

    install(TARGETS hello_world DESTINATION ansys/edb/core/)

endif()
