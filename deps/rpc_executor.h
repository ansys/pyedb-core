// -----------------------------------------------------------------
// Contents: Header-only loader and executor for the EDB_RPC_Services
//   shared library.
//   - Initialize: loads EDB_RPC_Services directly from the path given
//     by ansysEmInstallDirectory (the library is NOT bundled inside the
//     Python package), adds that directory to the dynamic-library search
//     path so that transitive dependencies are resolved, and stores the
//     returned IEDB_RPC_Services interface pointer in a global.
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
    //       directory (e.g. 64Release / 64Debug) that contains
    //       EDB_RPC_Services.dll (Windows) or libEDB_RPC_Services.so
    //       (Linux) and their transitive dependencies.
    //
    //   The shared library is loaded directly from this directory; it is
    //   NOT bundled inside the Python package.
    //
    //   Windows: the directory is also added to the DLL search path via
    //       SetDllDirectoryA so that transitive dependencies are resolved
    //       by the Windows loader.
    //   Linux:   the directory is prepended to LD_LIBRARY_PATH before
    //       dlopen so that transitive .so dependencies are resolved.
    //
    //   Returns true on success, false on any failure.
    // ------------------------------------------------------------------
    inline bool Initialize(const std::string& ansysEmInstallDirectory)
    {
        // Already initialized — no-op.
        if (g_plugin)
            return true;

#ifdef RPC_EXECUTOR_PLATFORM_WINDOWS
        // ------------------------------------------------------------------
        // Windows implementation
        // ------------------------------------------------------------------

        // Add the install directory to the DLL search path so that
        // transitive dependencies of EDB_RPC_Services.dll are found.
        char previousDir[MAX_PATH] = {};
        GetDllDirectoryA(MAX_PATH, previousDir);
        if (!SetDllDirectoryA(ansysEmInstallDirectory.c_str()))
            return false;

        // Load EDB_RPC_Services.dll directly from the install directory.
        const std::string libPath = ansysEmInstallDirectory + "\\EDB_RPC_Services.dll";
        HMODULE hMod = LoadLibraryA(libPath.c_str());
        if (!hMod)
        {
            SetDllDirectoryA(*previousDir ? previousDir : nullptr);
            return false;
        }

        using GetIEDB_RPC_ServicesFn = IEDB_RPC_Services* (*)();
        auto getPlugin = reinterpret_cast<GetIEDB_RPC_ServicesFn>(
            GetProcAddress(hMod, "GetIEDB_RPC_Services"));
        if (!getPlugin) { FreeLibrary(hMod); SetDllDirectoryA(*previousDir ? previousDir : nullptr); return false; }

        IEDB_RPC_Services* plugin = getPlugin();
        if (!plugin) { FreeLibrary(hMod); SetDllDirectoryA(*previousDir ? previousDir : nullptr); return false; }

        if (plugin->Initialize() != 0) { FreeLibrary(hMod); SetDllDirectoryA(*previousDir ? previousDir : nullptr); return false; }

        // Success — restore DLL search directory now that all transitive
        // loads triggered by Initialize() are complete.
        SetDllDirectoryA(*previousDir ? previousDir : nullptr);
        if (g_hModule) FreeLibrary(g_hModule);
        g_hModule = hMod;
        g_plugin  = plugin;
        return true;

#else
        // ------------------------------------------------------------------
        // Linux / POSIX implementation
        // ------------------------------------------------------------------

        // Prepend the install directory to LD_LIBRARY_PATH so that the
        // dynamic linker can find transitive .so dependencies when dlopen
        // is called.  Save and restore the previous value on every path.
        //
        // The value is copied into a std::string immediately; the raw
        // pointer returned by getenv() must not be used after setenv()
        // because setenv() may reallocate the environment block.
        const char* prevRaw = getenv("LD_LIBRARY_PATH");
        const std::string savedLdPath = prevRaw ? prevRaw : "";

        std::string newLdPath = ansysEmInstallDirectory;
        if (!savedLdPath.empty()) { newLdPath += ':'; newLdPath += savedLdPath; }
        setenv("LD_LIBRARY_PATH", newLdPath.c_str(), 1);

        auto restoreLdPath = [&]()
        {
            if (!savedLdPath.empty())
                setenv("LD_LIBRARY_PATH", savedLdPath.c_str(), 1);
            else
                unsetenv("LD_LIBRARY_PATH");
        };

        // Load libEDB_RPC_Services.so directly from the install directory.
        // RTLD_GLOBAL makes its symbols visible so transitive deps resolve.
        const std::string libPath = ansysEmInstallDirectory + "/libEDB_RPC_Services.so";
        void* hMod = dlopen(libPath.c_str(), RTLD_NOW | RTLD_GLOBAL);
        if (!hMod) { restoreLdPath(); return false; }

        using GetIEDB_RPC_ServicesFn = IEDB_RPC_Services* (*)();
        auto getPlugin = reinterpret_cast<GetIEDB_RPC_ServicesFn>(
            dlsym(hMod, "GetIEDB_RPC_Services"));
        if (!getPlugin) { dlclose(hMod); restoreLdPath(); return false; }

        IEDB_RPC_Services* plugin = getPlugin();
        if (!plugin) { dlclose(hMod); restoreLdPath(); return false; }

        if (plugin->Initialize() != 0) { dlclose(hMod); restoreLdPath(); return false; }

        restoreLdPath();
        if (g_hModule) dlclose(g_hModule);
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
