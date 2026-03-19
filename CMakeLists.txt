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

# ---------------------------------------------------------------------------
# The .pth hook that pre-loads the AnsysEM libstdc++.so.6 before any other
# C extension can claim the system version.  Both files are installed to the
# platlib root (site-packages) so that Python's site.py picks up the .pth
# file on every interpreter startup.
# ---------------------------------------------------------------------------
set(PRELOAD_PY  "${CMAKE_CURRENT_SOURCE_DIR}/src/ansys_edb_core_preload.py")
set(PRELOAD_PTH "${CMAKE_CURRENT_SOURCE_DIR}/src/ansys_edb_core_preload.pth")

if(PREBUILT_PYD)
    # bootstrap.ps1 / bootstrap.sh cache hit: install the cached extension
    # directly without compiling.  LANGUAGES NONE skips compiler detection.
    project(rpc_executor LANGUAGES NONE)
    message(STATUS "Cache hit: installing pre-built extension ${PREBUILT_PYD}")
    install(FILES "${PREBUILT_PYD}" DESTINATION ansys/edb/core/)
    install(FILES "${PRELOAD_PY}" "${PRELOAD_PTH}" DESTINATION ".")

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
    install(FILES "${PRELOAD_PY}" "${PRELOAD_PTH}" DESTINATION ".")

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
    # Force the new (post-GCC-5) C++11 std::string ABI so that std::string
    # objects cross the rpc_executor / libEDB_RPC_Services.so boundary with
    # the same 32-byte layout.  libEDB_RPC_Services.so is built with GCC 12
    # and uses the __cxx11 ABI; without this flag an older system GCC or a
    # Python interpreter built with _GLIBCXX_USE_CXX11_ABI=0 would produce
    # mismatched 8-byte (old-ABI) strings, corrupting the stack on return.
    target_compile_definitions(rpc_executor PRIVATE _GLIBCXX_USE_CXX11_ABI=1)
    # CMAKE_DL_LIBS is '-ldl' on Linux (needed for dlopen/dlsym) and
    # empty on platforms where those symbols are built in (e.g. macOS).
    target_link_libraries(rpc_executor PRIVATE ${CMAKE_DL_LIBS})

    install(TARGETS rpc_executor DESTINATION ansys/edb/core/)
    install(FILES "${PRELOAD_PY}" "${PRELOAD_PTH}" DESTINATION ".")

endif()
