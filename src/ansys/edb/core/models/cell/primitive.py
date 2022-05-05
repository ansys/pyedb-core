"""Primitive."""

from enum import Enum

import ansys.api.edb.v1.circle_pb2 as circle_pb2
import ansys.api.edb.v1.path_pb2 as path_pb2
import ansys.api.edb.v1.polygon_pb2 as polygon_pb2
import ansys.api.edb.v1.primitive_pb2 as primitive_pb2
import ansys.api.edb.v1.rectangle_pb2 as rectangle_pb2

from ...interfaces.grpc import messages
from ...session import (
    get_circle_stub,
    get_path_stub,
    get_polygon_stub,
    get_primitive_stub,
    get_rectangle_stub,
)
from ...utility.edb_errors import handle_grpc_exception
from ...utility.edb_iterator import EDBIterator
from .conn_obj import ConnObj
from .layer import Layer


class PrimitiveType(Enum):
    """Enum representing available primitive types."""

    RECTANGLE = primitive_pb2.RECTANGLE
    CIRCLE = primitive_pb2.CIRCLE
    POLYGON = primitive_pb2.POLYGON
    PATH = primitive_pb2.PATH
    BONDWIRE = primitive_pb2.BONDWIRE
    PRIM_PLUGIN = primitive_pb2.PRIM_PLUGIN
    TEXT = primitive_pb2.TEXT
    PATH_3D = primitive_pb2.PATH_3D
    BOARD_BEND = primitive_pb2.BOARD_BEND
    INVALID_TYPE = primitive_pb2.INVALID_TYPE


class _PrimitiveQueryBuilder:
    @staticmethod
    def get_primitive_type(p):
        return p._msg

    @staticmethod
    def add_void(p, hole):
        return primitive_pb2.PrimitiveVoidCreationMessage(target=p._msg, hole=hole._msg)

    @staticmethod
    def set_hfss_prop(p, material_name, solve_inside):
        return primitive_pb2.PrimitiveHfssPropMessage(
            target=p._msg, material_name=material_name, solve_inside=solve_inside
        )

    @staticmethod
    def set_is_negative(p, is_negative):
        return primitive_pb2.SetIsNegativeMessage(target=p._msg, is_negative=is_negative)

    @staticmethod
    def set_layer(p, layer):
        return primitive_pb2.SetLayerMessage(target=p._msg, layer=messages.layer_ref_message(layer))


class Primitive(ConnObj):
    """Base class representing primitive objects."""

    @staticmethod
    @handle_grpc_exception
    def _create(msg):
        prim_type = Primitive(msg).get_primitive_type()
        if prim_type == PrimitiveType.RECTANGLE:
            return Rectangle(msg)
        elif prim_type == PrimitiveType.POLYGON:
            return Polygon(msg)
        elif prim_type == PrimitiveType.PATH:
            return Path(msg)
        else:
            return None

    @handle_grpc_exception
    def get_primitive_type(self):
        """Get the type of a primitive.

        Returns
        -------
        PrimitiveType
        """
        return PrimitiveType(
            get_primitive_stub()
            .GetPrimitiveType(_PrimitiveQueryBuilder.get_primitive_type(self))
            .type
        )

    @handle_grpc_exception
    def add_void(self, hole):
        """Add a void to primitive.

        Parameters
        ----------
        hole : Primitive
        """
        return get_primitive_stub().AddVoid(_PrimitiveQueryBuilder.add_void(self, hole)).value

    @handle_grpc_exception
    def set_hfss_prop(self, material, solve_inside):
        """Set HFSS properties.

        Parameters
        ----------
        material : str
        solve_inside : bool

        Returns
        -------
        bool
        """
        return (
            get_primitive_stub()
            .SetHfssProp(_PrimitiveQueryBuilder.set_hfss_prop(self, material, solve_inside))
            .value
        )

    @handle_grpc_exception
    def get_layer(self):
        """Get a layer on which this primitive exists.

        Returns
        -------
        Layer
        """
        layer_msg = get_primitive_stub().GetLayer(self._msg)
        return Layer._create(layer_msg)

    @handle_grpc_exception
    def set_layer(self, layer) -> bool:
        """Set the layer.

        Parameters
        ----------
        layer : Layer

        Returns
        -------
        bool
        """
        return get_primitive_stub().SetLayer(_PrimitiveQueryBuilder.set_layer(self, layer)).value

    @handle_grpc_exception
    def get_is_negative(self):
        """Get if the primitive is negative.

        Returns
        -------
        bool
        """
        return get_primitive_stub().GetIsNegative(self._msg).value

    @handle_grpc_exception
    def set_is_negative(self, is_negative):
        """Update if negative.

        Parameters
        ----------
        is_negative : bool

        Returns
        -------
        bool
        """
        return (
            get_primitive_stub()
            .SetIsNegative(_PrimitiveQueryBuilder.set_is_negative(self, is_negative))
            .value
        )

    @handle_grpc_exception
    def is_void(self):
        """Determine if a primitive is a void.

        Returns
        -------
        bool
        """
        return get_primitive_stub().IsVoid(self._msg).value

    @handle_grpc_exception
    def has_voids(self):
        """
        Determine if a primitive contains voids inside.

        Returns
        -------
        bool
        """
        return get_primitive_stub().HasVoids(self._msg).value

    @property
    @handle_grpc_exception
    def voids(self):
        """
        Get list of voids inside a primitive.

        Returns
        -------
        EDBIterator
        """
        return EDBIterator(get_primitive_stub().Voids(self._msg), Primitive._create)

    @handle_grpc_exception
    def get_owner(self):
        """
        Get an owner of a primitive.

        Returns
        -------
        Primitive
        """
        return Primitive._create(get_primitive_stub().GetOwner(self._msg))

    @handle_grpc_exception
    def is_parameterized(self):
        """
        Determine if a primitive is parametrized.

        Returns
        -------
        bool
        """
        return get_primitive_stub().IsParameterized(self._msg).value

    @handle_grpc_exception
    def get_hfss_prop(self):
        """
        Get HFSS properties.

        Returns
        -------
        material : str
        solve_inside : bool
        """
        prop_msg = get_primitive_stub().GetHfssProp(self._msg)
        return prop_msg.material_name, prop_msg.solve_inside

    @handle_grpc_exception
    def remove_hfss_prop(self):
        """
        Remove HFSS properties.

        Returns
        -------
        bool
        """
        return get_primitive_stub().RemoveHfssProp(self._msg).value

    @handle_grpc_exception
    def is_zone_primitive(self):
        """
        Determine if a primitive is a zone.

        Returns
        -------
        bool
        """
        return get_primitive_stub().IsZonePrimitive(self._msg).value

    def can_be_zone_primitive(self):
        """
        Determine if a primitive can be a zone.

        Returns
        -------
        bool
        """
        return True


class Rectangle(Primitive):
    """Class representing a rectangle object."""

    class RectangleRepresentationType(Enum):
        """Enum representing possible rectangle types."""

        INVALID_RECT_TYPE = rectangle_pb2.INVALID_RECT_TYPE
        CENTER_WIDTH_HEIGHT = rectangle_pb2.CENTER_WIDTH_HEIGHT
        LOWER_LEFT_UPPER_RIGHT = rectangle_pb2.LOWER_LEFT_UPPER_RIGHT

    @staticmethod
    @handle_grpc_exception
    def create(layout, layer, net, rep_type, param1, param2, param3, param4, corner_rad, rotation):
        """Create a rectangle.

        Parameters
        ----------
        layout : Layout
        layer : str
        net : str
        rep_type : Rectangle.RectangleRepresentationType
        param1 : float
        param2 : float
        param3 : float
        param4 : float
        corner_rad : float
        rotation : float

        Returns
        -------
        Rectangle
        """
        return Rectangle(
            get_rectangle_stub().Create(
                rectangle_pb2.RectangleCreationMessage(
                    layout=layout.id,
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

    @handle_grpc_exception
    def get_parameters(self):
        """Get coordinates parameters."""
        rect_param_msg = get_rectangle_stub().GetParameters(self._msg)
        return (
            Rectangle.RectangleRepresentationType(rect_param_msg.representation_type),
            messages.value_message_to_value(rect_param_msg.parameter1),
            messages.value_message_to_value(rect_param_msg.parameter2),
            messages.value_message_to_value(rect_param_msg.parameter3),
            messages.value_message_to_value(rect_param_msg.parameter4),
            messages.value_message_to_value(rect_param_msg.corner_radius),
            messages.value_message_to_value(rect_param_msg.rotation),
        )

    @handle_grpc_exception
    def set_parameters(self, rep_type, param1, param2, param3, param4, corner_rad, rot):
        """Set coordinates parameters.

        Parameters
        ----------
        rep_type : Rectangle.RectangleRepresentationType
        param1 : float
        param2 : float
        param3 : float
        param4 : float
        corner_rad : float
        rot : float

        Returns
        -------
        bool
        """
        return (
            get_rectangle_stub()
            .SetParameters(
                rectangle_pb2.SetRectangleParametersMessage(
                    target=self._msg,
                    parameters=rectangle_pb2.RectangleParametersMessage(
                        representation_type=rep_type.value,
                        parameter1=messages.value_message(param1),
                        parameter2=messages.value_message(param2),
                        parameter3=messages.value_message(param3),
                        parameter4=messages.value_message(param4),
                        corner_radius=messages.value_message(corner_rad),
                        rotation=messages.value_message(rot),
                    ),
                )
            )
            .value
        )

    def can_be_zone_primitive(self):
        """Determine if rectangle can be a zone.

        Returns
        -------
        bool
        """
        return True

    def get_polygon_data(self):
        """Get polygon data of a rectangle.

        Returns
        -------
        PolygonData
        """
        return Rectangle.render(self, *self.get_parameters())

    @staticmethod
    @handle_grpc_exception
    def render(
        rep_type,
        x_lower_left_or_center_x,
        y_lower_left_or_center_y,
        x_upper_right_or_width,
        y_upper_right_or_height,
        corner_radius,
        rotation,
        is_hole=False,
    ):
        """Get the polygon data of a rectangle.

        Parameters
        ----------
        rep_type : Rectangle.RectangleRepresentationType
        x_lower_left_or_center_x : float
        y_lower_left_or_center_y : float
        x_upper_right_or_width : float
        y_upper_right_or_height : float
        corner_radius : float
        rotation : float
        is_hole : bool, optional

        Returns
        -------
        PolygonData
        """
        if rep_type == Rectangle.RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT:
            width = x_upper_right_or_width - x_lower_left_or_center_x
            height = y_upper_right_or_height - y_lower_left_or_center_y
            center_x = x_lower_left_or_center_x + width / 2.0
            center_y = y_lower_left_or_center_y + height / 2.0
            polygon_data = get_rectangle_stub().Render(
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
        elif rep_type == Rectangle.RectangleRepresentationType.CENTER_WIDTH_HEIGHT:
            polygon_data = get_rectangle_stub().Render(
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


class Circle(Primitive):
    """Class representing a circle object."""

    @staticmethod
    @handle_grpc_exception
    def create(layout, layer_name, net, center_x, center_y, radius):
        """Create a circle.

        Parameters
        ----------
        layout: Layout,
        layer_name: LayerRef,
        net: NetRef,
        center_x: Value,
        center_y: Value,
        radius: Value

        Returns
        -------
        Circle
        """
        return Circle(
            get_circle_stub().Create(
                circle_pb2.CircleCreationMessage(
                    layout=layout.id,
                    layer=messages.layer_ref_message(layer_name),
                    net=messages.net_ref_message(net),
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    radius=messages.value_message(radius),
                )
            )
        )

    @staticmethod
    @handle_grpc_exception
    def render(center_x, center_y, radius, is_hole):
        """Render a circle.

        Parameters
        ----------
        center_x: Value,
        center_y: Value,
        radius: Value,
        is_hole: bool

        Returns
        -------
        PolygonData
        """
        return get_circle_stub().Render(
            circle_pb2.CircleRenderMessage(
                center_x=messages.value_message(center_x),
                center_y=messages.value_message(center_y),
                radius=messages.value_message(radius),
                is_hole=is_hole,
            )
        )

    @handle_grpc_exception
    def get_parameters(self):
        """Get parameters of a circle.

        Returns
        -------
        Tuple[Value, Value, Value]
        """
        circle_param_msg = get_circle_stub().GetParameters(self._msg)
        return (
            messages.value_message_to_value(circle_param_msg.center_x),
            messages.value_message_to_value(circle_param_msg.center_y),
            messages.value_message_to_value(circle_param_msg.radius),
        )

    @handle_grpc_exception
    def set_parameters(self, center_x, center_y, radius):
        """Set parameters of a circle.

         Parameters
         ----------
        center_x: Value,
        center_y: Value,
        radius: Value

         Returns
         -------
         bool
        """
        return (
            get_circle_stub()
            .SetParameters(
                circle_pb2.SetCircleParametersMessage(
                    target=self._msg,
                    parameters=circle_pb2.CircleParametersMessage(
                        center_x=messages.value_message(center_x),
                        center_y=messages.value_message(center_y),
                        radius=messages.value_message(radius),
                    ),
                )
            )
            .value
        )

    def get_polygon_data(self):
        """Get polygon data of a circle.

        Returns
        -------
        PolygonData
        """
        return Circle.render(*self.get_parameters(), self.is_void())

    def can_be_zone_primitive(self):
        """Determine if circle can be a zone.

        Returns
        -------
        bool
        """
        return True


class _PolygonQueryBuilder:
    @staticmethod
    def create(layout, layer: str, net, points):
        return polygon_pb2.PolygonCreationMessage(
            layout=layout.id,
            layer=messages.layer_ref_message(layer),
            net=messages.net_ref_message(net),
            points=messages.points_message(points),
        )


class Polygon(Primitive):
    """Class representing a polygon object."""

    @staticmethod
    @handle_grpc_exception
    def create(layout, layer_name, net, polygon_data):
        """Create a polygon.

        Parameters
        ----------
        layout : Layout
        layer_name : str
        net : str
        polygon_data : PolygonData

        Returns
        -------
        Polygon
        """
        return Polygon(
            get_polygon_stub().Create(
                _PolygonQueryBuilder.create(layout, layer_name, net, polygon_data)
            )
        )


class PathEndCapType(Enum):
    """Enum representing possible end cap types."""

    ROUND = path_pb2.ROUND
    FLAT = path_pb2.FLAT
    EXTENDED = path_pb2.EXTENDED
    CLIPPED = path_pb2.CLIPPED
    INVALID = path_pb2.INVALID_END_CAP


class PathCornerType(Enum):
    """Enum representing possible corner types."""

    ROUND = path_pb2.ROUND_CORNER
    SHARP = path_pb2.SHARP_CORNER
    MITER = path_pb2.MITER_CORNER


class _PathQueryBuilder:
    @staticmethod
    def create(layout, layer, net, width, end_cap1, end_cap2, corner, points):
        return path_pb2.PathCreationMessage(
            layout=layout.id,
            layer=messages.layer_ref_message(layer),
            net=messages.net_ref_message(net),
            width=messages.value_message(width),
            end_cap1=end_cap1.value,
            end_cap2=end_cap2.value,
            corner=corner.value,
            points=messages.points_message(points),
        )


class Path(Primitive):
    """Class representing a path object."""

    @staticmethod
    @handle_grpc_exception
    def create(layout, layer, net, width, end_cap1, end_cap2, corner, points):
        """Create a path."""
        return Path(
            get_path_stub().Create(
                _PathQueryBuilder.create(
                    layout, layer, net, width, end_cap1, end_cap2, corner, points
                )
            )
        )
