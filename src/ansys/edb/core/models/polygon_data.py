from enum import Enum
from typing import List, Tuple

import ansys.api.edb.v1.point_data_pb2 as pb

from ..interfaces.grpc import messages
from ..session import get_polygon_data_stub
from .base import ObjBase


class PolygonSenseType(Enum):
    SENSE_UNKNOWN = pb.SENSE_UNKNOWN
    SENSE_CW = pb.SENSE_CW
    SENSE_CCW = pb.SENSE_CCW


class PolygonData(ObjBase):
    def __del__(self):
        self.cleanup()

    @staticmethod
    def create(points: List[Tuple[float, float]], closed: bool, sense=PolygonSenseType.SENSE_CCW):
        return PolygonData(
            get_polygon_data_stub().Create(
                messages.points_data_message((points, closed, sense.value))
            )
        )

    def cleanup(self):
        return get_polygon_data_stub().Cleanup(self._msg)
