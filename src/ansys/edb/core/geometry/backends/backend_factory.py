"""Factory for creating the appropriate polygon computation backend."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from ansys.edb.core.config import Config, ComputationBackend
from ansys.edb.core.geometry.backends.base import PolygonBackend


def get_backend(stub=None) -> PolygonBackend:
    """Get the appropriate polygon computation backend based on configuration.

    Parameters
    ----------
    stub : polygon_data_pb2_grpc.PolygonDataServiceStub, optional
        The gRPC stub for polygon operations. Required for server backend.

    Returns
    -------
    PolygonBackend
        The configured computation backend.

    Notes
    -----
    The backend is selected based on the PYEDB_COMPUTATION_BACKEND environment
    variable or the programmatic configuration. The selection logic is:

    - 'server': Always use server backend
    - 'shapely': Use Shapely backend (raises error if not installed)
    - 'auto' (default): Try Shapely first, fallback to server if not available

    Examples
    --------
    >>> # Use server backend explicitly
    >>> import os
    >>> os.environ['PYEDB_COMPUTATION_BACKEND'] = 'server'
    >>> backend = get_backend(stub)

    >>> # Use Shapely backend
    >>> from ansys.edb.core.config import Config, ComputationBackend
    >>> Config.set_computation_backend(ComputationBackend.SHAPELY)
    >>> backend = get_backend()
    """
    backend_type = Config.get_computation_backend()

    if backend_type == ComputationBackend.SERVER:
        return _get_server_backend(stub)

    elif backend_type == ComputationBackend.SHAPELY:
        return _get_shapely_backend()

    elif backend_type == ComputationBackend.AUTO:
        # Try Shapely first, fallback to server
        try:
            return _get_shapely_backend()
        except ImportError:
            warnings.warn(
                "Shapely is not installed. Falling back to server backend. "
                "For better performance, install Shapely: pip install shapely. "
                "Check the pyproject.toml file for the correct Shapely version.",
                UserWarning,
                stacklevel=2,
            )
            return _get_server_backend(stub)

    else:
        raise ValueError(f"Unknown backend type: {backend_type}")


def _get_server_backend(stub) -> PolygonBackend:
    """Get the server backend instance.

    Parameters
    ----------
    stub : polygon_data_pb2_grpc.PolygonDataServiceStub
        The gRPC stub for polygon operations.

    Returns
    -------
    ServerBackend
        Server computation backend.
    """
    if stub is None:
        raise ValueError("Server backend requires a stub parameter")

    from ansys.edb.core.geometry.backends.server_backend import ServerBackend

    return ServerBackend(stub)


def _get_shapely_backend() -> PolygonBackend:
    """Get the Shapely backend instance.

    Returns
    -------
    ShapelyBackend
        Shapely computation backend.

    Raises
    ------
    ImportError
        If Shapely is not installed.
    """
    from ansys.edb.core.geometry.backends.shapely_backend import ShapelyBackend

    return ShapelyBackend()
