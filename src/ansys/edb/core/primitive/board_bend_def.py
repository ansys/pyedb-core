"""Primitive classes."""

from ansys.api.edb.v1 import board_bend_def_pb2, board_bend_def_pb2_grpc

from ansys.edb.core.inner import messages, parser
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class BoardBendDef(Primitive):
    """Represents a board bend definition instance."""

    __stub: board_bend_def_pb2_grpc.BoardBendDefServiceStub = StubAccessor(StubType.board_bend_def)

    @classmethod
    def create(cls, layout, zone_prim, bend_middle, bend_radius, bend_angle):
        """Create a board bend definition.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the board bend definition in.
        zone_prim : :class:`.Primitive`
            Zone primitive to create the board bend definition on.
        bend_middle : (:term:`Point2DLike`, :term:`Point2DLike`)
            Tuple containing the starting and ending points of the line that represents
            the middle of the bend.
        bend_radius : :term:`ValueLike`
            Radius of the bend.
        bend_angle : :term:`ValueLike`
            Angle of the bend.

        Returns
        -------
        BoardBendDef
            Board bend definition created.
        """
        return BoardBendDef(
            cls.__stub.Create(
                board_bend_def_pb2.BoardBendDefCreateMessage(
                    layout=layout.msg,
                    zone_prim=zone_prim.msg,
                    middle=messages.point_pair_message(bend_middle),
                    radius=messages.value_message(bend_radius),
                    angle=messages.value_message(bend_angle),
                )
            )
        )

    @property
    def boundary_primitive(self):
        """:class:`.Primitive`: Zone primitive the board bend is placed on.

        This property is read-only.
        """
        return Primitive(self.__stub.GetBoundaryPrim(self.msg)).cast()

    @property
    @parser.to_point_data_pair
    def bend_middle(self):
        """(:term:`Point2DLike`, :term:`Point2DLike`): Tuple of the bend middle based on starting and ending points."""
        return self.__stub.GetBendMiddle(self.msg)

    @bend_middle.setter
    def bend_middle(self, bend_middle):
        self.__stub.SetBendMiddle(messages.point_pair_property_message(self, bend_middle))

    @property
    def radius(self):
        """:term:`ValueLike`: Radius of the bend."""
        return Value(self.__stub.GetRadius(self.msg))

    @radius.setter
    def radius(self, val):
        self.__stub.SetRadius(messages.value_property_message(self, val))

    @property
    def angle(self):
        """:term:`ValueLike`: Angle of the bend."""
        return Value(self.__stub.GetAngle(self.msg))

    @angle.setter
    def angle(self, val):
        self.__stub.SetAngle(messages.value_property_message(self, val))

    @property
    @parser.to_polygon_data_list
    def bent_regions(self):
        """:obj:`list` of :class:`.PolygonData`: Bent region polygons.

        This list of a collection of polygon data represents the areas bent by the bend definition.

        This property is read-only.
        """
        return self.__stub.GetBentRegions(self.msg)
