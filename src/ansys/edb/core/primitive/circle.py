"""Circle."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.layout.layout import Layout
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.typing import NetLike, LayerLike, ValueLike

from ansys.api.edb.v1 import circle_pb2, circle_pb2_grpc

from ansys.edb.core.inner import messages, parser
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class Circle(Primitive):
    """Represents a circle object."""

    __stub: circle_pb2_grpc.CircleServiceStub = StubAccessor(StubType.circle)

    @classmethod
    def create(
        cls,
        layout: Layout,
        layer: LayerLike,
        net: NetLike | None,
        center_x: ValueLike,
        center_y: ValueLike,
        radius: ValueLike,
    ) -> Circle:
        """Create a circle.

        Parameters
        ----------
        layout : .Layout
            Layout to create this circle in.
        layer : :term:`LayerLike`
            Layer to place the circle on.
        net : :term:`NetLike` or None
            Net of the circle.
        center_x : :term:`ValueLike`
            X value of the center point.
        center_y : :term:`ValueLike`
            Y value of the center point.
        radius : :term:`ValueLike`
            Radius value of the circle.

        Returns
        -------
        Circle
            Circle created.
        """
        return Circle(
            cls.__stub.Create(
                circle_pb2.CircleCreationMessage(
                    layout=layout.msg,
                    layer=messages.layer_ref_message(layer),
                    net=messages.net_ref_message(net),
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    radius=messages.value_message(radius),
                )
            )
        )

    @classmethod
    @parser.to_polygon_data
    def render(
        cls, center_x: ValueLike, center_y: ValueLike, radius: ValueLike, is_hole: bool
    ) -> PolygonData:
        """Render a circle.

        Parameters
        ----------
        center_x : :term:`ValueLike`
            X value of the center point.
        center_y : :term:`ValueLike`
            Y value of the center point.
        radius : :term:`ValueLike`
            Radius value of the circle.
        is_hole : bool
            Whether the circle object is a hole.

        Returns
        -------
        .PolygonData
            Circle created.
        """
        return cls.__stub.Render(
            circle_pb2.CircleRenderMessage(
                center_x=messages.value_message(center_x),
                center_y=messages.value_message(center_y),
                radius=messages.value_message(radius),
                is_hole=is_hole,
            )
        )

    def get_parameters(self) -> tuple[Value, Value, Value]:
        """Get parameters of the circle.

        Returns
        -------
        tuple of (.Value, .Value, .Value)

            Returns a tuple in this format:

            **(center_x, center_y, radius)**

            **center_x** : X value of center point.

            **center_y** : Y value of center point.

            **radius** : Radius value of the circle.
        """
        circle_param_msg = self.__stub.GetParameters(self.msg)
        return (
            Value(circle_param_msg.center_x),
            Value(circle_param_msg.center_y),
            Value(circle_param_msg.radius),
        )

    def set_parameters(self, center_x: ValueLike, center_y: ValueLike, radius: ValueLike):
        """Set parameters of the circle.

        Parameters
        ----------
        center_x : :term:`ValueLike`
            X value of the center point.
        center_y : :term:`ValueLike`
            Y value of the center point.
        radius : :term:`ValueLike`
            Radius value of the circle.
        """
        self.__stub.SetParameters(
            circle_pb2.SetCircleParametersMessage(
                target=self.msg,
                parameters=circle_pb2.CircleParametersMessage(
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    radius=messages.value_message(radius),
                ),
            )
        )

    @property
    def polygon_data(self) -> PolygonData:
        """:class:`.PolygonData`: \
        Polygon data object of the circle.

        This property is read-only.
        """
        return Circle.render(*self.get_parameters(), self.is_void)

    def can_be_zone_primitive(self) -> bool:
        """:obj:`bool`: Flag indicating if a circle can be a zone."""
        return True
