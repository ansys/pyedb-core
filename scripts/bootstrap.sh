#!/usr/bin/env bash
# bootstrap.sh – Developer build helper for pyedb-core on Linux / macOS.
#
# Usage:
#   ./scripts/bootstrap.sh               # build sdist + wheel
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
# Resolve the Python interpreter to use for the build.
#
# The system Python may lack development headers (python3-devel not installed).
# If uv is available in the venv, prefer the uv-managed Python which ships as
# a self-contained build and always includes full headers.  Fall back to the
# plain 'python3' command if uv is not present.
# ---------------------------------------------------------------------------
UV="$REPO_ROOT/.venv/bin/uv"
if [ -x "$UV" ]; then
    # Install a managed Python if one isn't already present, then resolve its path.
    "$UV" python install 3.11 --quiet 2>/dev/null || true
    PYTHON3="$("$UV" python find --system 3.11 2>/dev/null || echo "")"
fi
# Fallback: use whatever python3 is on PATH.
PYTHON3="${PYTHON3:-python3}"

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
CACHE_DIR="$REPO_ROOT/.pyd-cache/$PYTHON_TAG/$SOURCE_HASH"
CACHED_SO="$(find "$CACHE_DIR" -name 'rpc_executor*.so' 2>/dev/null | head -1 || true)"

if [ -n "$CACHED_SO" ]; then
    # -----------------------------------------------------------------------
    # Cache hit: set PREBUILT_PYD so CMakeLists.txt installs the cached file
    # directly (LANGUAGES NONE - no C++ compiler required for this build).
    # -----------------------------------------------------------------------
    echo ""
    echo "Cache hit [$SOURCE_HASH] - skipping C++ compilation."
    echo "Using: $CACHED_SO"
    echo ""
    echo "Running: $PYTHON3 -m build $*"
    echo ""
    PREBUILT_PYD="$CACHED_SO" "$PYTHON3" -m build "$@"
else
    # -----------------------------------------------------------------------
    # Cache miss: full C++ compilation required.
    # -----------------------------------------------------------------------
    echo ""
    echo "Cache miss [$SOURCE_HASH] - full C++ compilation required."
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

    echo "Running: $PYTHON3 -m build $*"
    echo ""
    "$PYTHON3" -m build "$@"

    # Store the compiled .so for future builds.
    save_so_to_cache "$CACHE_DIR"
fi

echo ""
echo "Build succeeded. Wheel and sdist are in the dist/ directory."
