cmake_minimum_required(VERSION 3.15)

# ---------------------------------------------------------------------------
# Optional: install a pre-built extension instead of compiling from source.
# Set the PREBUILT_PYD environment variable (or pass -DPREBUILT_PYD=<path>)
# to the absolute path of a previously compiled rpc_executor .pyd file.
# bootstrap.ps1 sets this automatically when a cached build is available.
# Using LANGUAGES NONE avoids compiler detection entirely on cache hits.
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
    # bootstrap.ps1 / bootstrap.sh cache hit: install the cached extension
    # directly without compiling.  LANGUAGES NONE skips compiler detection.
    project(rpc_executor LANGUAGES NONE)
    message(STATUS "Cache hit: installing pre-built extension ${PREBUILT_PYD}")
    install(FILES "${PREBUILT_PYD}" DESTINATION ansys/edb/core/)
    # Bundle the platform shared library alongside the extension module.
    if(WIN32)
        install(FILES deps/EDB_RPC_Services.dll DESTINATION ansys/edb/core/)
    elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/deps/libEDB_RPC_Services.so")
        install(FILES deps/libEDB_RPC_Services.so DESTINATION ansys/edb/core/)
    endif()

elseif(WIN32)
    # Windows: compile the pybind11 extension with the MSVC toolchain and
    # define RPC_EXECUTOR_PLATFORM_WINDOWS so that rpc_executor.h selects
    # the Windows code paths (HMODULE, LoadLibraryA, SetDllDirectoryA, etc.).
    project(rpc_executor LANGUAGES CXX)
    find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
    find_package(pybind11 CONFIG REQUIRED)

    pybind11_add_module(rpc_executor deps/rpc_executor_bindings.cpp)
    target_include_directories(rpc_executor PRIVATE deps/)
    target_compile_features(rpc_executor PRIVATE cxx_std_17)
    target_compile_definitions(rpc_executor PRIVATE RPC_EXECUTOR_PLATFORM_WINDOWS)

    install(TARGETS rpc_executor DESTINATION ansys/edb/core/)
    # Bundle EDB_RPC_Services.dll alongside the .pyd.
    # rpc_executor.h locates it via GetModuleFileName at runtime.
    install(FILES deps/EDB_RPC_Services.dll DESTINATION ansys/edb/core/)

else()
    # Linux / macOS: compile with the system C++ toolchain.
    # RPC_EXECUTOR_PLATFORM_WINDOWS is intentionally NOT defined, so
    # rpc_executor.h uses the POSIX code paths (dlopen, dladdr, etc.).
    project(rpc_executor LANGUAGES CXX)
    find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
    find_package(pybind11 CONFIG REQUIRED)

    pybind11_add_module(rpc_executor deps/rpc_executor_bindings.cpp)
    target_include_directories(rpc_executor PRIVATE deps/)
    target_compile_features(rpc_executor PRIVATE cxx_std_17)
    # CMAKE_DL_LIBS is '-ldl' on Linux (needed for dlopen/dladdr/dlsym)
    # and empty on platforms where those symbols are built in (e.g. macOS).
    target_link_libraries(rpc_executor PRIVATE ${CMAKE_DL_LIBS})

    install(TARGETS rpc_executor DESTINATION ansys/edb/core/)
    # Bundle libEDB_RPC_Services.so if present in deps/.
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/deps/libEDB_RPC_Services.so")
        install(FILES deps/libEDB_RPC_Services.so DESTINATION ansys/edb/core/)
    endif()

endif()
