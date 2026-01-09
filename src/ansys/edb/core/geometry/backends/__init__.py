"""Geometry computation backends."""

from ansys.edb.core.geometry.backends.point_backend_base import PointBackend
from ansys.edb.core.geometry.backends.point_backend_factory import get_point_backend
from ansys.edb.core.geometry.backends.polygon_backend_base import PolygonBackend
from ansys.edb.core.geometry.backends.polygon_backend_factory import get_backend

__all__ = ["PolygonBackend", "get_backend", "PointBackend", "get_point_backend"]
