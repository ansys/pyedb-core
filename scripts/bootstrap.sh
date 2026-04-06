#!/usr/bin/env bash
# bootstrap.sh – Developer build helper for pyedb-core on Linux / macOS.
#
# Usage:
#   ./scripts/bootstrap.sh               # build sdist + wheel (Release)
#   ./scripts/bootstrap.sh debug         # build sdist + wheel (Debug)
#   ./scripts/bootstrap.sh --wheel       # build wheel only
#   ./scripts/bootstrap.sh --no-isolation
#
# Any arguments are forwarded verbatim to `python3 -m build`.
#
# The script caches the compiled rpc_executor extension module under
# .pyd-cache/<python-tag>/<source-hash>/ and reuses it on subsequent
# builds when the C++ sources in deps/ and CMakeLists.txt are unchanged.
# On a cache hit the C++ compiler is not required.
#
# Make this script executable once after cloning:
#   chmod +x scripts/bootstrap.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# ---------------------------------------------------------------------------
# Parse optional build type argument.
#
# Usage:
#   ./scripts/bootstrap.sh          -> Release build (default)
#   ./scripts/bootstrap.sh debug    -> Debug build
#
# The "debug" token is consumed here and not forwarded to `python3 -m build`.
# All other arguments are passed through verbatim.
# ---------------------------------------------------------------------------
BUILD_TYPE="Release"
PASSTHROUGH_ARGS=()
for arg in "$@"; do
    if [ "${arg,,}" = "debug" ]; then
        BUILD_TYPE="Debug"
    else
        PASSTHROUGH_ARGS+=("$arg")
    fi
done
set -- "${PASSTHROUGH_ARGS[@]+"${PASSTHROUGH_ARGS[@]}"}"

# ---------------------------------------------------------------------------
# Resolve the Python interpreter to use for the build.
#
# The system Python may lack development headers (python3-devel not installed).
# If uv is available in the venv, prefer the uv-managed Python which ships as
# a self-contained build and always includes full headers.  Fall back to the
# plain 'python3' command if uv is not present.
#
# IMPORTANT: when using the uv-managed Python we must pass --no-isolation to
# `python3 -m build`.  Without it, the build frontend creates a fresh isolated
# virtualenv that inherits the system Python and looks for Python development
# headers at the system path (/usr/include/python3.x/patchlevel.h).  Those
# headers come from an optional package (python3.x-dev / python3-devel) that
# is often not installed.  The uv-managed Python is fully self-contained and
# bundles its own headers, but cmake only finds them when invoked from *within*
# that interpreter — i.e. with --no-isolation so no new venv is created.
# ---------------------------------------------------------------------------
UV="$REPO_ROOT/.venv/bin/uv"
USING_UV_PYTHON=0
if [ -x "$UV" ]; then
    # Install a managed Python if one isn't already present, then resolve its path.
    "$UV" python install 3.11 --quiet 2>/dev/null || true
    _UV_PYTHON="$("$UV" python find --system 3.11 2>/dev/null || echo "")"
    if [ -n "$_UV_PYTHON" ] && [ -x "$_UV_PYTHON" ]; then
        PYTHON3="$_UV_PYTHON"
        USING_UV_PYTHON=1
    fi
fi
# Fallback: use whatever python3 is on PATH.
PYTHON3="${PYTHON3:-python3}"

# When using the system Python (not uv-managed), verify that the development
# headers are present.  They live in python3.x-dev (Debian/Ubuntu) or
# python3.x-devel (Fedora/RHEL) and are required by CMake's FindPython module.
if [ "$USING_UV_PYTHON" -eq 0 ]; then
    _PY_VERSION="$("$PYTHON3" -c 'import sys; print("{}.{}".format(*sys.version_info[:2]))')"
    _PY_HEADER_DIR="/usr/include/python${_PY_VERSION}"
    if [ ! -f "${_PY_HEADER_DIR}/patchlevel.h" ]; then
        echo ""
        echo "ERROR: Python development headers not found at ${_PY_HEADER_DIR}/patchlevel.h" >&2
        echo "" >&2
        echo "CMake requires the Python header files to compile the C++ extension." >&2
        echo "Install them with one of:" >&2
        echo "  Debian/Ubuntu:  sudo apt install python${_PY_VERSION}-dev" >&2
        echo "  Fedora/RHEL:    sudo dnf install python${_PY_VERSION}-devel" >&2
        echo "" >&2
        echo "Alternatively, install 'uv' (https://docs.astral.sh/uv/) inside" >&2
        echo "the .venv and re-run this script; it will download a self-contained" >&2
        echo "Python that bundles its own headers." >&2
        echo "" >&2
        exit 1
    fi
fi

# ---------------------------------------------------------------------------
# Helper: compute a 16-hex-char SHA-256 fingerprint of the C++ source tree
# (deps/*.cpp, deps/*.h, CMakeLists.txt).
# ---------------------------------------------------------------------------
get_source_hash() {
    "$PYTHON3" - "$REPO_ROOT" <<'EOF'
import hashlib, glob, os, sys
base = sys.argv[1]
files = sorted(
    glob.glob(os.path.join(base, 'deps', '*.cpp')) +
    glob.glob(os.path.join(base, 'deps', '*.h')) +
    [os.path.join(base, 'CMakeLists.txt')]
)
h = hashlib.sha256()
for f in files:
    with open(f, 'rb') as fp:
        h.update(fp.read())
print(h.hexdigest()[:16])
EOF
}

# ---------------------------------------------------------------------------
# Helper: extract rpc_executor*.so from the most recently built wheel in
# dist/ and save it to CACHE_DIR.
# ---------------------------------------------------------------------------
save_so_to_cache() {
    local cache_dir="$1"
    "$PYTHON3" - "$cache_dir" "$REPO_ROOT" <<'EOF'
import zipfile, glob, os, sys
cache_dir = sys.argv[1]
repo_root = sys.argv[2]
wheels = sorted(
    glob.glob(os.path.join(repo_root, 'dist', '*.whl')),
    key=os.path.getmtime
)
if not wheels:
    print('WARNING: no wheel found in dist/ - skipping cache.', file=sys.stderr)
    sys.exit(0)
with zipfile.ZipFile(wheels[-1]) as z:
    for name in z.namelist():
        basename = os.path.basename(name)
        if basename.startswith('rpc_executor') and basename.endswith('.so'):
            os.makedirs(cache_dir, exist_ok=True)
            dest = os.path.join(cache_dir, basename)
            with open(dest, 'wb') as f:
                f.write(z.read(name))
            print(f'Cached: {dest}')
            break
    else:
        print('WARNING: rpc_executor*.so not found in wheel - skipping cache.',
              file=sys.stderr)
EOF
}

# ---------------------------------------------------------------------------
# 1. Compute source fingerprint and check the cache.
# ---------------------------------------------------------------------------
SOURCE_HASH="$(get_source_hash)"
PYTHON_TAG="$("$PYTHON3" -c "import sys; print('cp{}{}'.format(*sys.version_info[:2]))")"
CACHE_DIR="$REPO_ROOT/.pyd-cache/$PYTHON_TAG/$BUILD_TYPE/$SOURCE_HASH"
CACHED_SO="$(find "$CACHE_DIR" -name 'rpc_executor*.so' 2>/dev/null | head -1 || true)"

if [ -n "$CACHED_SO" ]; then
    # -----------------------------------------------------------------------
    # Cache hit: set PREBUILT_PYD so CMakeLists.txt installs the cached file
    # directly (LANGUAGES NONE - no C++ compiler required for this build).
    # -----------------------------------------------------------------------
    echo ""
    echo "Cache hit [$SOURCE_HASH] ($BUILD_TYPE) - skipping C++ compilation."
    echo "Using: $CACHED_SO"
    echo ""
    # When using the uv-managed Python, pass its path to CMake via
    # cmake.define.Python_EXECUTABLE.  This makes FindPython use the bundled
    # headers that come with the managed Python instead of looking for the
    # (often absent) system python3.x-dev headers.  Isolation is kept ON so
    # that scikit-build-core / pybind11 are installed into the temp build env.
    EXTRA_CMAKE_ARGS=()
    [ "$USING_UV_PYTHON" -eq 1 ] && EXTRA_CMAKE_ARGS+=("--config-setting" "cmake.define.Python_EXECUTABLE=$PYTHON3")
    echo "Running: $PYTHON3 -m build --config-setting cmake.build-type=$BUILD_TYPE${EXTRA_CMAKE_ARGS:+ ${EXTRA_CMAKE_ARGS[*]}} $*"
    echo ""
    PREBUILT_PYD="$CACHED_SO" "$PYTHON3" -m build --config-setting "cmake.build-type=$BUILD_TYPE" "${EXTRA_CMAKE_ARGS[@]}" "$@"
else
    # -----------------------------------------------------------------------
    # Cache miss: full C++ compilation required.
    # -----------------------------------------------------------------------
    echo ""
    echo "Cache miss [$SOURCE_HASH] ($BUILD_TYPE) - full C++ compilation required."
    echo ""

    # Check for a C++ compiler.
    if ! command -v c++ &>/dev/null && \
       ! command -v g++ &>/dev/null && \
       ! command -v clang++ &>/dev/null; then
        echo "ERROR: No C++ compiler found." >&2
        echo "Install one with:" >&2
        echo "  Debian/Ubuntu:  sudo apt install build-essential" >&2
        echo "  Fedora/RHEL:    sudo dnf install gcc-c++" >&2
        echo "  macOS:          xcode-select --install" >&2
        exit 1
    fi

    # Same cmake.define.Python_EXECUTABLE trick as the cache-hit branch above.
    EXTRA_CMAKE_ARGS=()
    [ "$USING_UV_PYTHON" -eq 1 ] && EXTRA_CMAKE_ARGS+=("--config-setting" "cmake.define.Python_EXECUTABLE=$PYTHON3")
    echo "Running: $PYTHON3 -m build --config-setting cmake.build-type=$BUILD_TYPE${EXTRA_CMAKE_ARGS:+ ${EXTRA_CMAKE_ARGS[*]}} $*"
    echo ""
    "$PYTHON3" -m build --config-setting "cmake.build-type=$BUILD_TYPE" "${EXTRA_CMAKE_ARGS[@]}" "$@"

    # Store the compiled .so for future builds.
    save_so_to_cache "$CACHE_DIR"
fi

echo ""
echo "Build succeeded. Wheel and sdist are in the dist/ directory."
