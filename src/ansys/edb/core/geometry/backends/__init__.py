"""Geometry computation backends."""

from ansys.edb.core.geometry.backends.base import PolygonBackend
from ansys.edb.core.geometry.backends.backend_factory import get_backend

__all__ = ["PolygonBackend", "get_backend"]
