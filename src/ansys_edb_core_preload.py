"""ansys_edb_core_preload.py — installed to site-packages via a .pth hook.

This module is executed automatically by Python's site.py at interpreter
startup (before any user code runs) via ansys_edb_core_preload.pth.

On Linux, libEDB_RPC_Services.so requires a newer libstdc++ than the one
shipped with RHEL 8 / CentOS 8 and other enterprise distributions.  The
dynamic linker will reuse whichever libstdc++.so.6 is resident in the
process when libEDB_RPC_Services.so is dlopen'd.  If the system version was
loaded first (e.g. via grpcio's cygrpc extension), the newer GLIBCXX symbols
that Ansys requires are missing and initialization fails.

The fix: load the AnsysEM-bundled libstdc++.so.6 *here*, with RTLD_GLOBAL, so
it is the first copy resident in the process.  All subsequent C extensions
that request libstdc++.so.6 (grpcio, etc.) will find it already loaded and
use the same, newer copy.

This is a no-op when:
  - Running on Windows or macOS (no action needed).
  - ANSYSEM_EDB_EXE_DIR is not set (Ansys install unknown; nothing to load).
  - The AnsysEM libstdc++.so.6 is not present at the expected path.
  - libstdc++.so.6 is already loaded (guards against double-execution).
"""
import ctypes
import os
import sys

if sys.platform != "win32":
    _ansysem_dir = os.environ.get("ANSYSEM_EDB_EXE_DIR", "")
    if _ansysem_dir:
        _libstdcpp = os.path.join(_ansysem_dir, "libstdc++.so.6")
        if os.path.isfile(_libstdcpp):
            # Check whether any libstdc++.so.6 is already mapped in this
            # process.  If it is, loading ours at this point would be too
            # late — the existing version is already locked in.
            _already_loaded = False
            try:
                with open("/proc/self/maps") as _maps:
                    for _line in _maps:
                        if "libstdc++" in _line:
                            _already_loaded = True
                            break
            except OSError:
                pass

            if not _already_loaded:
                try:
                    ctypes.CDLL(_libstdcpp, mode=ctypes.RTLD_GLOBAL)
                except OSError:
                    pass
