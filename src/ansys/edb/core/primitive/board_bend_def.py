"""Primitive classes."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.layout.layout import Layout
    from ansys.edb.core.typing import ValueLike, PointLike
    from ansys.edb.core.geometry.polygon_data import PolygonData

from ansys.api.edb.v1 import board_bend_def_pb2, board_bend_def_pb2_grpc

from ansys.edb.core.inner import messages, parser
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class BoardBendDef(Primitive):
    """Represents a board bend definition instance."""

    __stub: board_bend_def_pb2_grpc.BoardBendDefServiceStub = StubAccessor(StubType.board_bend_def)

    @classmethod
    def create(
        cls,
        layout: Layout,
        zone_prim: Primitive,
        bend_middle: PointLike,
        bend_radius: ValueLike,
        bend_angle: ValueLike,
    ) -> BoardBendDef:
        """Create a board bend definition.

        Parameters
        ----------
        layout : .Layout
            Layout to create the board bend definition in.
        zone_prim : .Primitive
            Zone primitive to create the board bend definition on.
        bend_middle : tuple of (:term:`Point2DLike`, :term:`Point2DLike`)
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
    def boundary_primitive(self) -> Primitive:
        """:class:`.Primitive`: Zone primitive the board bend is placed on.

        This property is read-only.
        """
        return Primitive(self.__stub.GetBoundaryPrim(self.msg)).cast()

    @property
    @parser.to_point_data_pair
    def bend_middle(self) -> tuple[PointLike, PointLike]:
        """(:term:`Point2DLike`, :term:`Point2DLike`): Tuple of the bend middle based on starting and ending points."""
        return self.__stub.GetBendMiddle(self.msg)

    @bend_middle.setter
    def bend_middle(self, bend_middle: tuple[PointLike, PointLike]):
        self.__stub.SetBendMiddle(messages.point_pair_property_message(self, bend_middle))

    @property
    def radius(self) -> Value:
        """:class:`.Value`: Radius of the bend."""
        return Value(self.__stub.GetRadius(self.msg))

    @radius.setter
    def radius(self, val: ValueLike):
        self.__stub.SetRadius(messages.value_property_message(self, val))

    @property
    def angle(self) -> Value:
        """:class:`.Value`: Angle of the bend."""
        return Value(self.__stub.GetAngle(self.msg))

    @angle.setter
    def angle(self, val: ValueLike):
        self.__stub.SetAngle(messages.value_property_message(self, val))

    @property
    @parser.to_polygon_data_list
    def bent_regions(self) -> list[PolygonData]:
        """:obj:`list` of :class:`.PolygonData`: Bent region polygons.

        This list of a collection of polygon data represents the areas bent by the bend definition.

        This property is read-only.
        """
        return self.__stub.GetBentRegions(self.msg)
