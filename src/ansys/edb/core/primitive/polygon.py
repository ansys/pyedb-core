"""Polygon."""

from ansys.api.edb.v1 import polygon_pb2, polygon_pb2_grpc

from ansys.edb.core.inner import messages, parser
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType


class Polygon(Primitive):
    """Represents a polygon object."""

    __stub: polygon_pb2_grpc.PolygonServiceStub = StubAccessor(StubType.polygon)

    @classmethod
    def create(cls, layout, layer, net, polygon_data):
        """Create a polygon.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the polygon in.
        layer : str or :class:`.Layer`
            Layer to place the polygon on.
        net : str or :class:`.Net` or None
            Net of the polygon.
        polygon_data : :class:`.PolygonData`
            Outer contour of the polygon.

        Returns
        -------
        Polygon
            Polygon created.
        """
        return Polygon(
            cls.__stub.Create(
                polygon_pb2.PolygonCreationMessage(
                    layout=layout.msg,
                    layer=messages.layer_ref_message(layer),
                    net=messages.net_ref_message(net),
                    points=messages.polygon_data_message(polygon_data),
                )
            )
        )

    @property
    @parser.to_polygon_data
    def polygon_data(self):
        """:class:`.PolygonData`: Outer contour of the polygon."""
        return self.__stub.GetPolygonData(self.msg)

    @polygon_data.setter
    def polygon_data(self, poly):
        self.__stub.SetPolygonData(
            polygon_pb2.SetPolygonDataMessage(
                target=self.msg, poly=messages.polygon_data_message(poly)
            )
        )

    @property
    def can_be_zone_primitive(self):
        """:obj:`bool`: Flag indicating if a polygon can be a zone.

        This property is read-only.
        """
        return True
