"""EDB-Core Python package for the Electronics Database (EDB) format."""

import os
import sys

# Ensure the package directory is on sys.path so that rpc_executor.pyd
# (placed alongside this package at install time) can be imported.
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
if _pkg_dir not in sys.path:
    sys.path.append(_pkg_dir)

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("ansys-edb-core")
