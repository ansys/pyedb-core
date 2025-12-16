"""Geometry computation backends."""

from ansys.edb.core.geometry.backends.backend_factory import get_backend
from ansys.edb.core.geometry.backends.base import PolygonBackend

__all__ = ["PolygonBackend", "get_backend"]
