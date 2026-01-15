"""Factory for creating arc computation backends based on configuration."""

from __future__ import annotations

from ansys.edb.core.config import ComputationBackend, Config
from ansys.edb.core.geometry.backends.arc_backend_base import ArcBackend


def get_arc_backend(stub=None) -> ArcBackend:
    """Return an ArcBackend instance according to the current configuration.

    Parameters
    ----------
    stub : optional
        gRPC stub for server-backed computations.
    """
    backend_type = Config.get_computation_backend()

    if backend_type == ComputationBackend.SERVER:
        return _get_server_backend(stub)
    elif backend_type == ComputationBackend.SHAPELY:
        return _get_shapely_backend(stub)
    elif backend_type == ComputationBackend.BUILD123D:
        return _get_build123d_backend(stub)
    elif backend_type == ComputationBackend.AUTO:
        return _get_server_backend(stub)
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")


def _get_server_backend(stub) -> ArcBackend:
    """Return the server backend; requires a stub."""
    if stub is None:
        raise ValueError("Server backend requires a stub parameter")

    from ansys.edb.core.geometry.backends.arc_server_backend import ArcServerBackend

    return ArcServerBackend(stub)


def _get_shapely_backend(stub=None) -> ArcBackend:
    """Return the Shapely backend instance."""
    from ansys.edb.core.geometry.backends.arc_shapely_backend import ArcShapelyBackend

    return ArcShapelyBackend(stub)


def _get_build123d_backend(stub=None) -> ArcBackend:
    """Return the Build123d backend instance."""
    from ansys.edb.core.geometry.backends.arc_build123d_backend import ArcBuild123dBackend

    return ArcBuild123dBackend(stub)
