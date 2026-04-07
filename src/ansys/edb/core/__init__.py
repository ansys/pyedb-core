"""EDB-Core Python package for the Electronics Database (EDB) format."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("ansys-edb-core")
