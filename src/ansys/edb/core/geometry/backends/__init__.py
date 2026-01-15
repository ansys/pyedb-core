"""Geometry computation backends."""

from ansys.edb.core.geometry.backends.arc_backend_base import ArcBackend
from ansys.edb.core.geometry.backends.arc_backend_factory import get_arc_backend
from ansys.edb.core.geometry.backends.point_backend_base import PointBackend
from ansys.edb.core.geometry.backends.point_backend_factory import get_point_backend
from ansys.edb.core.geometry.backends.polygon_backend_base import PolygonBackend
from ansys.edb.core.geometry.backends.polygon_backend_factory import get_polygon_backend

__all__ = [
    "ArcBackend",
    "get_arc_backend",
    "PointBackend",
    "get_point_backend",
    "PolygonBackend",
    "get_polygon_backend",
]
