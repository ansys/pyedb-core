"""Rectangle."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.layout.layout import Layout
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.typing import NetLike, LayerLike, ValueLike

from enum import Enum

from ansys.api.edb.v1 import rectangle_pb2, rectangle_pb2_grpc

from ansys.edb.core.inner import messages, parser
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class RectangleRepresentationType(Enum):
    """Provides an enum representing rectangle types."""

    INVALID_RECT_TYPE = rectangle_pb2.INVALID_RECT_TYPE
    CENTER_WIDTH_HEIGHT = rectangle_pb2.CENTER_WIDTH_HEIGHT
    LOWER_LEFT_UPPER_RIGHT = rectangle_pb2.LOWER_LEFT_UPPER_RIGHT


class Rectangle(Primitive):
    """Represents a rectangle object."""

    __stub: rectangle_pb2_grpc.RectangleServiceStub = StubAccessor(StubType.rectangle)

    @classmethod
    def create(
        cls,
        layout: Layout,
        layer: LayerLike,
        net: NetLike | None,
        rep_type: RectangleRepresentationType,
        param1: ValueLike,
        param2: ValueLike,
        param3: ValueLike,
        param4: ValueLike,
        corner_rad: ValueLike,
        rotation: ValueLike,
    ) -> Rectangle:
        """Create a rectangle.

        Parameters
        ----------
        layout : .Layout
            Layout to create the rectangle in.
        layer : :term:`LayerLike`
            Layer the rectangle is to created on.
        net : :term:`NetLike` or None
            Net the rectangle is to have.
        rep_type : .RectangleRepresentationType
            Type that defines the meaning of the given parameters.
        param1 : :term:`ValueLike`
            X value of the lower-left point or center point.
        param2 : :term:`ValueLike`
            Y value of the lower-left point or center point.
        param3 : :term:`ValueLike`
            X value of the upper-right point or width.
        param4 : :term:`ValueLike`
            Y value of the upper-right point or height.
        corner_rad : :term:`ValueLike`
            Corner radius.
        rotation : :term:`ValueLike`
            Rotation.

        Returns
        -------
        Rectangle
            Rectangle created.
        """
        return Rectangle(
            cls.__stub.Create(
                rectangle_pb2.RectangleCreationMessage(
                    layout=layout.msg,
                    layer=messages.layer_ref_message(layer),
                    net=messages.net_ref_message(net),
                    representation_type=rep_type.value,
                    parameter1=messages.value_message(param1),
                    parameter2=messages.value_message(param2),
                    parameter3=messages.value_message(param3),
                    parameter4=messages.value_message(param4),
                    corner_radius=messages.value_message(corner_rad),
                    rotation=messages.value_message(rotation),
                )
            )
        )

    def get_parameters(
        self,
    ) -> tuple[RectangleRepresentationType, Value, Value, Value, Value, Value, Value]:
        """Get coordinate parameters.

        Returns
        -------
        tuple of (.RectangleRepresentationType, .Value, .Value, .Value, .Value, .Value, .Value)

            Returns a tuple in this format:

            **(representation_type, parameter1, parameter2, parameter3, parameter4, corner_radius, rotation)**

            **representation_type** : Type that defines given parameters meaning.

            **parameter1** : X value of lower left point or center point.

            **parameter2** : Y value of lower left point or center point.

            **parameter3** : X value of upper right point or width.

            **parameter4** : Y value of upper right point or height.

            **corner_radius** : Corner radius.

            **rotation** : Rotation.
        """
        rect_param_msg = self.__stub.GetParameters(self.msg)
        return (
            RectangleRepresentationType(rect_param_msg.representation_type),
            Value(rect_param_msg.parameter1),
            Value(rect_param_msg.parameter2),
            Value(rect_param_msg.parameter3),
            Value(rect_param_msg.parameter4),
            Value(rect_param_msg.corner_radius),
            Value(rect_param_msg.rotation),
        )

    def set_parameters(
        self,
        rep_type: RectangleRepresentationType,
        param1: ValueLike,
        param2: ValueLike,
        param3: ValueLike,
        param4: ValueLike,
        corner_rad: ValueLike,
        rotation: ValueLike,
    ):
        """Set coordinate parameters.

        Parameters
        ----------
        rep_type : .RectangleRepresentationType
            Type that defines the meaning of the given parameters.
        param1 : :term:`ValueLike`
            X value of the lower-left point or center point.
        param2 : :term:`ValueLike`
            Y value of the lower-left point or center point.
        param3 : :term:`ValueLike`
            X value of the upper-right point or width.
        param4 : :term:`ValueLike`
            Y value of the upper-right point or height.
        corner_rad : :term:`ValueLike`
            Corner radius.
        rotation : :term:`ValueLike`
            Rotation.
        """
        self.__stub.SetParameters(
            rectangle_pb2.SetRectangleParametersMessage(
                target=self.msg,
                parameters=rectangle_pb2.RectangleParametersMessage(
                    representation_type=rep_type.value,
                    parameter1=messages.value_message(param1),
                    parameter2=messages.value_message(param2),
                    parameter3=messages.value_message(param3),
                    parameter4=messages.value_message(param4),
                    corner_radius=messages.value_message(corner_rad),
                    rotation=messages.value_message(rotation),
                ),
            )
        )

    @property
    def can_be_zone_primitive(self) -> bool:
        """:obj:`bool`: Flag indicating if the rectangle can be a zone.

        This property is read-only.
        """
        return True

    @property
    @parser.to_polygon_data
    def polygon_data(self) -> PolygonData:
        """:class:`.PolygonData`: \
        Polygon data object of the rectangle.

        This property is read-only.
        """
        return self.__stub.GetPolygonData(self.msg)

    @classmethod
    @parser.to_polygon_data
    def render(
        cls,
        rep_type: RectangleRepresentationType,
        x_lower_left_or_center_x: ValueLike,
        y_lower_left_or_center_y: ValueLike,
        x_upper_right_or_width: ValueLike,
        y_upper_right_or_height: ValueLike,
        corner_radius: ValueLike,
        rotation: ValueLike,
        is_hole: bool = False,
    ) -> PolygonData:
        """Get the polygon data of a rectangle.

        Parameters
        ----------
        rep_type : .RectangleRepresentationType
            Type that defines the meaning of the given parameters.
        x_lower_left_or_center_x : :term:`ValueLike`
            X value of the lower-left point or center point.
        y_lower_left_or_center_y : :term:`ValueLike`
            Y value of the lower-left point or center point.
        x_upper_right_or_width : :term:`ValueLike`
            X value of the upper-right point or width.
        y_upper_right_or_height : :term:`ValueLike`
            Y value of the upper-right point or height.
        corner_radius : :term:`ValueLike`
            Corner radius.
        rotation : :term:`ValueLike`
            Rotation.
        is_hole : bool, default: False
            Whether the rectangle is hole.

        Returns
        -------
        :class:`.PolygonData`
            Polygon data object created.
        """
        if rep_type == RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT:
            width = x_upper_right_or_width - x_lower_left_or_center_x
            height = y_upper_right_or_height - y_lower_left_or_center_y
            center_x = x_lower_left_or_center_x + width / 2.0
            center_y = y_lower_left_or_center_y + height / 2.0
            polygon_data = cls.__stub.Render(
                rectangle_pb2.RectanglePolygonDataMessage(
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    width=messages.value_message(width),
                    height=messages.value_message(height),
                    corner_radius=messages.value_message(corner_radius),
                    rotation=messages.value_message(rotation),
                    ishole=is_hole,
                )
            )
        elif rep_type == RectangleRepresentationType.CENTER_WIDTH_HEIGHT:
            polygon_data = cls.__stub.Render(
                rectangle_pb2.RectanglePolygonDataMessage(
                    center_x=messages.value_message(x_lower_left_or_center_x),
                    center_y=messages.value_message(y_lower_left_or_center_y),
                    width=messages.value_message(x_upper_right_or_width),
                    height=messages.value_message(y_upper_right_or_height),
                    corner_radius=messages.value_message(corner_radius),
                    rotation=messages.value_message(rotation),
                    ishole=is_hole,
                )
            )
        else:
            polygon_data = None
        return polygon_data
