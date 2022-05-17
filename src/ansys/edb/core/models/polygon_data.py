"""Polygon Data."""

from enum import Enum

import ansys.api.edb.v1.point_data_pb2 as pb

from ..interfaces.grpc import messages
from ..session import get_polygon_data_stub
from .base import ObjBase


class PolygonSenseType(Enum):
    """Direction of polygon sense."""

    SENSE_UNKNOWN = pb.SENSE_UNKNOWN
    SENSE_CW = pb.SENSE_CW
    SENSE_CCW = pb.SENSE_CCW


class PolygonData(ObjBase):
    """Class representing a polygon data object."""

    def __del__(self):
        """Clean up resources."""
        self.cleanup()

    @staticmethod
    def create(points, closed, sense=PolygonSenseType.SENSE_CCW):
        """Create a polygon data.

        Parameters
        ----------
        points : list of tuple of float, float
        closed : bool
        sense : PolygonSenseType, optional

        Returns
        -------
        PolygonData
        """
        return PolygonData(
            get_polygon_data_stub().Create(
                messages.points_data_message((points, closed, sense.value))
            )
        )

    def cleanup(self):
        """Clean up resources."""
        return get_polygon_data_stub().Cleanup(self.msg)
