"""Factory for creating the appropriate point computation backend."""

from __future__ import annotations

from ansys.edb.core.config import ComputationBackend, Config
from ansys.edb.core.geometry.backends.point_backend_base import PointBackend


def get_point_backend(stub=None) -> PointBackend:
    """Get the appropriate point computation backend based on configuration.

    Parameters
    ----------
    stub : point_data_pb2_grpc.PointDataServiceStub, optional
        The gRPC stub for point operations. Required for server backend.

    Returns
    -------
    PointBackend
        The configured computation backend.

    Notes
    -----
    The backend is selected based on the PYEDB_COMPUTATION_BACKEND environment
    variable or the programmatic configuration. The selection logic is:

    - 'server': Always use server backend
    - 'shapely': Use Shapely backend (raises error if not installed)
    - 'build123d': Use Build123d backend (raises error if not installed)
    - 'auto' (default): Use server backend

    Examples
    --------
    >>> # Use server backend explicitly
    >>> import os
    >>> os.environ['PYEDB_COMPUTATION_BACKEND'] = 'server'
    >>> backend = get_point_backend(stub)

    >>> # Use Shapely backend
    >>> from ansys.edb.core.config import Config, ComputationBackend
    >>> Config.set_computation_backend(ComputationBackend.SHAPELY)
    >>> backend = get_point_backend()
    """
    backend_type = Config.get_computation_backend()

    if backend_type == ComputationBackend.SERVER:
        return _get_server_backend(stub)

    elif backend_type == ComputationBackend.SHAPELY:
        return _get_shapely_backend(stub)

    elif backend_type == ComputationBackend.BUILD123D:
        return _get_build123d_backend(stub)

    elif backend_type == ComputationBackend.AUTO:
        # Use server backend by default
        return _get_server_backend(stub)

    else:
        raise ValueError(f"Unknown backend type: {backend_type}")


def _get_server_backend(stub) -> PointBackend:
    """Get the server backend instance.

    Parameters
    ----------
    stub : point_data_pb2_grpc.PointDataServiceStub
        The gRPC stub for point operations.

    Returns
    -------
    PointServerBackend
        Server computation backend.
    """
    if stub is None:
        raise ValueError("Server backend requires a stub parameter")

    from ansys.edb.core.geometry.backends.point_server_backend import PointServerBackend

    return PointServerBackend(stub)


def _get_shapely_backend(stub=None) -> PointBackend:
    """Get the Shapely backend instance.

    Parameters
    ----------
    stub : point_data_pb2_grpc.PointDataServiceStub, optional
        The gRPC stub for point operations.

    Returns
    -------
    PointShapelyBackend
        Shapely computation backend.

    Raises
    ------
    ImportError
        If Shapely is not installed.
    """
    from ansys.edb.core.geometry.backends.point_shapely_backend import PointShapelyBackend

    return PointShapelyBackend(stub)


def _get_build123d_backend(stub=None) -> PointBackend:
    """Get the Build123d backend instance.

    Parameters
    ----------
    stub : point_data_pb2_grpc.PointDataServiceStub, optional
        The gRPC stub for point operations.

    Returns
    -------
    PointBuild123dBackend
        Build123d computation backend.

    Raises
    ------
    ImportError
        If Build123d is not installed.
    """
    from ansys.edb.core.geometry.backends.point_build123d_backend import PointBuild123dBackend

    return PointBuild123dBackend(stub)
