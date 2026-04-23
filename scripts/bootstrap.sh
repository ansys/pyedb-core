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
# Helper: compute a 16-hex-char SHA-256 fingerprint of the C++ source tree
# (deps/*.cpp, deps/*.h, CMakeLists.txt).
# ---------------------------------------------------------------------------
get_source_hash() {
    python3 - "$REPO_ROOT" <<'EOF'
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
    python3 - "$cache_dir" "$REPO_ROOT" <<'EOF'
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
PYTHON_TAG="$(python3 -c "import sys; print('cp{}{}'.format(*sys.version_info[:2]))")"
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
    echo "Running: python3 -m build $*"
    echo ""
    PREBUILT_PYD="$CACHED_SO" python3 -m build "$@"
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

    echo "Running: python3 -m build $*"
    echo ""
    python3 -m build "$@"

    # Store the compiled .so for future builds.
    save_so_to_cache "$CACHE_DIR"
fi

echo ""
echo "Build succeeded. Wheel and sdist are in the dist/ directory."
