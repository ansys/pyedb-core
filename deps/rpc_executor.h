// -----------------------------------------------------------------
// Contents: Header-only loader and executor for the EDB_RPC_Services
//   shared library.
//   - Initialize: locates the shared library next to this extension
//     module, adds the Ansys EM install directory to the dynamic-library
//     search path so that transitive dependencies are resolved, and
//     stores the returned IEDB_RPC_Services interface pointer in a global.
//   - ExecuteRpc: thin wrapper around IEDB_RPC_Services::ExecuteRpc.
//
// Preprocessor macro set by CMakeLists.txt:
//   RPC_EXECUTOR_PLATFORM_WINDOWS  - defined only when building with
//       the MSVC toolchain on Windows.  All Windows-specific code is
//       guarded by #ifdef RPC_EXECUTOR_PLATFORM_WINDOWS; the else
//       branches use POSIX APIs (dlfcn.h) available on Linux and macOS.
// -----------------------------------------------------------------
#pragma once

#include <string>
#include <stdexcept>
#include <tuple>
#include <cstring>

#ifdef RPC_EXECUTOR_PLATFORM_WINDOWS
#  include <windows.h>
#else
#  include <dlfcn.h>    // dlopen, dlsym, dlclose, dladdr
#  include <cstdlib>   // getenv, setenv, unsetenv
#endif

#include "IEDB_RPC_Services.h"

namespace RPCExecutor
{
    // Process-wide state - inline variables require C++17.
    inline IEDB_RPC_Services* g_plugin  = nullptr;
#ifdef RPC_EXECUTOR_PLATFORM_WINDOWS
    inline HMODULE            g_hModule = nullptr;
#else
    inline void*              g_hModule = nullptr;
#endif

    // ------------------------------------------------------------------
    // Initialize
    //   ansysEmInstallDirectory - absolute path to the Ansys EM install
    //       directory (e.g. 64Release / 64Debug).
    //
    //   Windows: added to the DLL search path via SetDllDirectoryA so
    //       that the transitive dependencies of EDB_RPC_Services.dll are
    //       resolved by the Windows loader.
    //   Linux:   prepended to LD_LIBRARY_PATH before calling dlopen so
    //       that the transitive dependencies of libEDB_RPC_Services.so
    //       are resolved by the dynamic linker.
    //
    //   The shared library (EDB_RPC_Services.dll on Windows,
    //   libEDB_RPC_Services.so on Linux) is loaded from the same
    //   directory as this extension module.
    //
    //   Returns true on success, false on any failure.
    // ------------------------------------------------------------------
    inline bool Initialize(const std::string& ansysEmInstallDirectory)
    {
#ifdef RPC_EXECUTOR_PLATFORM_WINDOWS
        // ------------------------------------------------------------------
        // Windows implementation
        // ------------------------------------------------------------------

        // Save the current custom DLL search directory so it can be
        // restored on every exit path.
        char previousDir[MAX_PATH] = {};
        GetDllDirectoryA(MAX_PATH, previousDir);

        // Add the Ansys EM install directory so that EDB_RPC_Services.dll's
        // transitive dependencies are found by the Windows loader.
        if (!SetDllDirectoryA(ansysEmInstallDirectory.c_str()))
            return false;

        // Determine the directory containing this .pyd by querying the
        // module handle of a function inside this translation unit.
        HMODULE hSelf = nullptr;
        if (!GetModuleHandleExA(
                GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                reinterpret_cast<LPCSTR>(&Initialize),
                &hSelf))
        {
            SetDllDirectoryA(*previousDir ? previousDir : nullptr);
            return false;
        }

        char pydPath[MAX_PATH] = {};
        if (!GetModuleFileNameA(hSelf, pydPath, MAX_PATH))
        {
            SetDllDirectoryA(*previousDir ? previousDir : nullptr);
            return false;
        }

        // Strip the filename to obtain just the directory.
        char* lastSep = strrchr(pydPath, '\\');
        if (lastSep)
            *(lastSep + 1) = '\0';

        std::string libPath = std::string(pydPath) + "EDB_RPC_Services.dll";

        HMODULE hMod = LoadLibraryA(libPath.c_str());
        if (!hMod)
        {
            SetDllDirectoryA(*previousDir ? previousDir : nullptr);
            return false;
        }

        using GetIEDB_RPC_ServicesFn = IEDB_RPC_Services* (*)();
        auto getPlugin = reinterpret_cast<GetIEDB_RPC_ServicesFn>(
            GetProcAddress(hMod, "GetIEDB_RPC_Services"));
        if (!getPlugin)
        {
            FreeLibrary(hMod);
            SetDllDirectoryA(*previousDir ? previousDir : nullptr);
            return false;
        }

        IEDB_RPC_Services* plugin = getPlugin();
        if (!plugin)
        {
            FreeLibrary(hMod);
            SetDllDirectoryA(*previousDir ? previousDir : nullptr);
            return false;
        }

        if (plugin->Initialize() != 0)
        {
            FreeLibrary(hMod);
            SetDllDirectoryA(*previousDir ? previousDir : nullptr);
            return false;
        }

        // Success - restore DLL search directory and commit state.
        SetDllDirectoryA(*previousDir ? previousDir : nullptr);
        if (g_hModule)
            FreeLibrary(g_hModule);
        g_hModule = hMod;
        g_plugin  = plugin;
        return true;

#else
        // ------------------------------------------------------------------
        // Linux / POSIX implementation
        // ------------------------------------------------------------------

        // Prepend ansysEmInstallDirectory to LD_LIBRARY_PATH so that the
        // dynamic linker can find transitive .so dependencies of
        // libEDB_RPC_Services.so when dlopen is called.  Save and restore
        // the previous value on every exit path.
        //
        // The value is copied into a std::string immediately; the raw
        // pointer returned by getenv() must not be used after setenv()
        // because setenv() may reallocate the environment block.
        const char* prevRaw = getenv("LD_LIBRARY_PATH");
        const std::string savedLdPath = prevRaw ? prevRaw : "";

        std::string newLdPath = ansysEmInstallDirectory;
        if (!savedLdPath.empty())
        {
            newLdPath += ':';
            newLdPath += savedLdPath;
        }
        setenv("LD_LIBRARY_PATH", newLdPath.c_str(), 1);

        // Restores LD_LIBRARY_PATH to its value before this call.
        auto restoreLdPath = [&]()
        {
            if (!savedLdPath.empty())
                setenv("LD_LIBRARY_PATH", savedLdPath.c_str(), 1);
            else
                unsetenv("LD_LIBRARY_PATH");
        };

        // Use dladdr() to discover the path of this .so, then strip the
        // filename to obtain the containing directory (equivalent to
        // GetModuleHandleEx + GetModuleFileName on Windows).
        Dl_info dlInfo = {};
        if (dladdr(reinterpret_cast<void*>(&Initialize), &dlInfo) == 0
            || !dlInfo.dli_fname)
        {
            restoreLdPath();
            return false;
        }

        const std::string soPath(dlInfo.dli_fname);
        const std::size_t lastSlash = soPath.rfind('/');
        const std::string dir = (lastSlash != std::string::npos)
            ? soPath.substr(0, lastSlash + 1)
            : "./";

        const std::string libPath = dir + "libEDB_RPC_Services.so";

        // RTLD_GLOBAL makes the loaded library's symbols globally visible
        // so that its own transitive dependencies can resolve against them.
        void* hMod = dlopen(libPath.c_str(), RTLD_NOW | RTLD_GLOBAL);
        if (!hMod)
        {
            restoreLdPath();
            return false;
        }

        using GetIEDB_RPC_ServicesFn = IEDB_RPC_Services* (*)();
        auto getPlugin = reinterpret_cast<GetIEDB_RPC_ServicesFn>(
            dlsym(hMod, "GetIEDB_RPC_Services"));
        if (!getPlugin)
        {
            dlclose(hMod);
            restoreLdPath();
            return false;
        }

        IEDB_RPC_Services* plugin = getPlugin();
        if (!plugin)
        {
            dlclose(hMod);
            restoreLdPath();
            return false;
        }

        if (plugin->Initialize() != 0)
        {
            dlclose(hMod);
            restoreLdPath();
            return false;
        }

        // Success - restore LD_LIBRARY_PATH and commit state.
        restoreLdPath();
        if (g_hModule)
            dlclose(g_hModule);
        g_hModule = hMod;
        g_plugin  = plugin;
        return true;
#endif
    }

    // ------------------------------------------------------------------
    // ExecuteRpc
    //   Forwards the call directly to IEDB_RPC_Services::ExecuteRpc on the
    //   interface pointer obtained by Initialize().
    //
    //   Returns a tuple of (success, serializedResponse, errorMessage).
    //   Throws std::runtime_error if Initialize() has not been called
    //   successfully.
    // ------------------------------------------------------------------
    inline std::tuple<bool, std::string, std::string>
    ExecuteRpc(const std::string& serviceName,
               const std::string& rpcName,
               const std::string& serializedRequest)
    {
        if (!g_plugin)
        {
            throw std::runtime_error(
                "RPCExecutor: plugin not initialized. Call Initialize() first.");
        }

        std::string serializedResponse;
        std::string errorMessage;
        bool ok = g_plugin->ExecuteRpc(
            serviceName, rpcName, serializedRequest,
            serializedResponse, errorMessage);
        return {ok, serializedResponse, errorMessage};
    }

} // namespace RPCExecutor
