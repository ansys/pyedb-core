"""Polygon Data."""

from enum import Enum

import ansys.api.edb.v1.point_data_pb2 as pb

from ansys.edb import geometry
from ansys.edb.core import ObjBase, messages
from ansys.edb.session import get_polygon_data_stub
from ansys.edb.utility import conversions


class PolygonSenseType(Enum):
    """Direction of polygon sense."""

    SENSE_UNKNOWN = pb.SENSE_UNKNOWN
    SENSE_CW = pb.SENSE_CW
    SENSE_CCW = pb.SENSE_CCW


class PolygonData(ObjBase):
    """Class representing a polygon data object."""

    def __init__(self, msg=None, lower_left=None, upper_right=None):
        """Create a polygon.

        Parameters
        ----------
        msg : EDBObjMessage, optional
            deprecated - will be removed.
        lower_left : ansys.edb.typing.PointLike, optional
        upper_right : ansys.edb.typing.PointLike, optional
        """
        super().__init__(msg)
        if lower_left is not None and upper_right is not None:
            lower_left = conversions.to_point(lower_left)
            upper_right = conversions.to_point(upper_right)
            self._points = [
                geometry.PointData(lower_left.x, lower_left.y),
                geometry.PointData(upper_right.x, lower_left.y),
                geometry.PointData(upper_right.x, upper_right.y),
                geometry.PointData(lower_left.x, upper_right.y),
            ]

    def __len__(self):
        """Get the number of coordinates.

        Returns
        -------
        int
        """
        return len(self._points)

    @property
    def points(self):
        """Get the list of coordinates.

        Returns
        -------
        list[geometry.PointData]
        """
        return self._points

    @staticmethod
    def create(points, closed, sense=PolygonSenseType.SENSE_CCW):
        """Create a polygon data.

        Parameters
        ----------
        points : list[ansys.edb.typing.PointLike]
        closed : bool
        sense : PolygonSenseType, optional

        Returns
        -------
        PolygonData
        """
        return PolygonData(
            msg=get_polygon_data_stub().Create(
                messages.points_data_message((points, closed, sense.value))
            )
        )
