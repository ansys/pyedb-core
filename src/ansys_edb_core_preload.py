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

Install directory resolution order:
  1. ANSYS_EDB_CORE_INSTALL_DIR — explicit override, highest priority.
  2. ANSYSEM_ROOT<XYZ> (e.g. ANSYSEM_ROOT261) — the variable with the largest
     numeric suffix is used when ANSYS_EDB_CORE_INSTALL_DIR is absent.
  3. If neither is set, a warning is printed and the system libstdc++ is used.

This is a no-op when:
  - Running on Windows or macOS (no action needed).
  - No Ansys install directory can be resolved (see above).
  - The AnsysEM libstdc++.so.6 is not present at the resolved path.
  - libstdc++.so.6 is already loaded (guards against double-execution).
"""
import ctypes
import os
import re
import sys

_YELLOW = "\033[93m"
_RESET = "\033[0m"
_PREFIX = "ansys-edb-core:"


def _warn(msg):
    print(f"{_YELLOW}{_PREFIX} {msg}{_RESET}", file=sys.stderr)


def _resolve_install_dir():
    """Return the AnsysEM install directory to use, or an empty string."""
    explicit = os.environ.get("ANSYS_EDB_CORE_INSTALL_DIR", "")
    if explicit:
        return explicit

    # Scan for ANSYSEM_ROOT<digits> variables and pick the one with the
    # largest numeric suffix.
    best_version = -1
    best_dir = ""
    for key, value in os.environ.items():
        m = re.fullmatch(r"ANSYSEM_ROOT(\d+)", key)
        if m:
            version = int(m.group(1))
            if version > best_version:
                best_version = version
                best_dir = value
    return best_dir


if sys.platform != "win32":
    _ansysem_dir = _resolve_install_dir()

    if not _ansysem_dir:
        _warn(
            "No AnsysEM install directory found. The system libstdc++.so.6 will "
            "be used, which may be incompatible with libEDB_RPC_Services.so. "
            "Set ANSYS_EDB_CORE_INSTALL_DIR or ANSYSEM_ROOT<XYZ> to the AnsysEM "
            " install directory (e.g. /path/to/AnsysEM) to ensure the correct library is loaded."
        )
    else:
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
                    _warn(f"Pre-loaded AnsysEM libstdc++.so.6 from '{_ansysem_dir}'.")
                except OSError:
                    pass
