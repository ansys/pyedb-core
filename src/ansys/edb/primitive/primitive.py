"""Primitive."""

from enum import Enum

from ansys.api.edb.v1 import (
    board_bend_def_pb2,
    board_bend_def_pb2_grpc,
    bondwire_pb2,
    bondwire_pb2_grpc,
    circle_pb2,
    circle_pb2_grpc,
    padstack_instance_pb2,
    padstack_instance_pb2_grpc,
    path_pb2,
    path_pb2_grpc,
    polygon_pb2,
    polygon_pb2_grpc,
    primitive_pb2,
    primitive_pb2_grpc,
    rectangle_pb2,
    rectangle_pb2_grpc,
    text_pb2,
    text_pb2_grpc,
)

from ansys.edb import hierarchy, terminal
from ansys.edb.core import conn_obj, messages, parser
from ansys.edb.definition.padstack_def import PadstackDef
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.layer import Layer
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value
from ansys.edb.utility.layer_map import LayerMap


class _PrimitiveQueryBuilder:
    @staticmethod
    def get_primitive_type(p):
        return p.msg

    @staticmethod
    def add_void(p, hole):
        return primitive_pb2.PrimitiveVoidCreationMessage(target=p.msg, hole=hole.msg)

    @staticmethod
    def set_hfss_prop(p, material_name, solve_inside):
        return primitive_pb2.PrimitiveHfssPropMessage(
            target=p.msg, material_name=material_name, solve_inside=solve_inside
        )

    @staticmethod
    def set_is_negative(p, is_negative):
        return primitive_pb2.SetIsNegativeMessage(target=p.msg, is_negative=is_negative)

    @staticmethod
    def set_layer(p, layer):
        return primitive_pb2.SetLayerMessage(target=p.msg, layer=messages.layer_ref_message(layer))


class PrimitiveType(Enum):
    """Enum representing available primitive types.

    - RECTANGLE
    - CIRCLE
    - POLYGON
    - PATH
    - BONDWIRE
    - PRIM_PLUGIN
    - TEXT
    - PATH_3D
    - BOARD_BEND
    - INVALID_TYPE
    """

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


class RectangleRepresentationType(Enum):
    """Enum representing possible rectangle types.

    - INVALID_RECT_TYPE
       Undefined.
    - CENTER_WIDTH_HEIGHT
       Using center, width and height.
    - LOWER_LEFT_UPPER_RIGHT
       Using lower left point and upper right point.
    """

    INVALID_RECT_TYPE = rectangle_pb2.INVALID_RECT_TYPE
    CENTER_WIDTH_HEIGHT = rectangle_pb2.CENTER_WIDTH_HEIGHT
    LOWER_LEFT_UPPER_RIGHT = rectangle_pb2.LOWER_LEFT_UPPER_RIGHT


class PathEndCapType(Enum):
    """Enum representing possible end cap types.

    - ROUND
    - FLAT
    - EXTENDED
    - CLIPPED
    - INVALID
    """

    ROUND = path_pb2.ROUND
    FLAT = path_pb2.FLAT
    EXTENDED = path_pb2.EXTENDED
    CLIPPED = path_pb2.CLIPPED
    INVALID = path_pb2.INVALID_END_CAP


class PathCornerType(Enum):
    """Enum representing possible corner types.

    - ROUND
    - SHARP
    - MITER
    """

    ROUND = path_pb2.ROUND_CORNER
    SHARP = path_pb2.SHARP_CORNER
    MITER = path_pb2.MITER_CORNER


class BondwireType(Enum):
    """Enum representing possible bondwire types.

    - APD
    - JEDEC4
    - JEDEC5
    - NUM_OF_TYPE
    - INVALID
    """

    APD = bondwire_pb2.APD_BONDWIRE
    JEDEC4 = bondwire_pb2.JEDEC4_BONDWIRE
    JEDEC5 = bondwire_pb2.JEDEC5_BONDWIRE
    NUM_OF_TYPE = bondwire_pb2.NUM_OF_BONDWIRE_TYPE
    INVALID = bondwire_pb2.INVALID_BONDWIRE_TYPE


class BondwireCrossSectionType(Enum):
    """Enum representing possible bondwire cross section types.

    - ROUND
    - RECTANGLE
    - INVALID
    """

    ROUND = bondwire_pb2.BONDWIRE_ROUND
    RECTANGLE = bondwire_pb2.BONDWIRE_RECTANGLE
    INVALID = bondwire_pb2.INVALID_BONDWIRE_CROSS_SECTION_TYPE


class BackDrillType(Enum):
    """Enum representing possible Back Drill types.

    - NO_DRILL
    - LAYER_DRILL
    - DEPTH_DRILL
    """

    NO_DRILL = padstack_instance_pb2.NO_DRILL
    LAYER_DRILL = padstack_instance_pb2.LAYER_DRILL
    DEPTH_DRILL = padstack_instance_pb2.DEPTH_DRILL


class Primitive(conn_obj.ConnObj):
    """Base class representing primitive objects."""

    __stub: primitive_pb2_grpc.PrimitiveServiceStub = StubAccessor(StubType.primitive)
    layout_obj_type = LayoutObjType.PRIMITIVE

    def cast(self):
        """Cast the primitive object to correct concrete type.

        Returns
        -------
        Primitive
        """
        if self.is_null:
            return

        prim_type = self.primitive_type
        if prim_type == PrimitiveType.RECTANGLE:
            return Rectangle(self.msg)
        elif prim_type == PrimitiveType.POLYGON:
            return Polygon(self.msg)
        elif prim_type == PrimitiveType.PATH:
            return Path(self.msg)
        elif prim_type == PrimitiveType.BONDWIRE:
            return Bondwire(self.msg)
        elif prim_type == PrimitiveType.TEXT:
            return Text(self.msg)
        elif prim_type == PrimitiveType.CIRCLE:
            return Circle(self.msg)

    @property
    def primitive_type(self):
        """:class:`PrimitiveType`: Primitive type of the primitive.

        Read-Only.
        """
        return PrimitiveType(
            self.__stub.GetPrimitiveType(_PrimitiveQueryBuilder.get_primitive_type(self)).type
        )

    def add_void(self, hole):
        """Add a void to primitive.

        Parameters
        ----------
        hole : Primitive
            Void to be added to the primitive.
        """
        self.__stub.AddVoid(_PrimitiveQueryBuilder.add_void(self, hole))

    def set_hfss_prop(self, material, solve_inside):
        """Set HFSS properties.

        Parameters
        ----------
        material : str
            Material property name to be set.
        solve_inside : bool
            Whether to do solve inside.
        """
        self.__stub.SetHfssProp(_PrimitiveQueryBuilder.set_hfss_prop(self, material, solve_inside))

    @property
    def layer(self):
        """:class:`Layer <ansys.edb.layer.Layer>`: Layer that the primitive object is on."""
        layer_msg = self.__stub.GetLayer(self.msg)
        return Layer(layer_msg).cast()

    @layer.setter
    def layer(self, layer):
        self.__stub.SetLayer(_PrimitiveQueryBuilder.set_layer(self, layer))

    @property
    def is_negative(self):
        """:obj:`bool`: If the primitive is negative."""
        return self.__stub.GetIsNegative(self.msg).value

    @is_negative.setter
    def is_negative(self, is_negative):
        self.__stub.SetIsNegative(_PrimitiveQueryBuilder.set_is_negative(self, is_negative))

    @property
    def is_void(self):
        """:obj:`bool`: If a primitive is a void."""
        return self.__stub.IsVoid(self.msg).value

    @property
    def has_voids(self):
        """:obj:`bool`: If a primitive has voids inside.

        Read-Only.
        """
        return self.__stub.HasVoids(self.msg).value

    @property
    def voids(self):
        """:obj:`list` of :class:`Primitive <ansys.edb.primitive.Primitive>`: List of void\
        primitive objects inside the primitive.

        Read-Only.
        """
        return [Primitive(msg).cast() for msg in self.__stub.Voids(self.msg).items]

    @property
    def owner(self):
        """:class:`Primitive <ansys.edb.primitive.Primitive>`: Owner of the primitive object.

        Read-Only.
        """
        return Primitive(self.__stub.GetOwner(self.msg)).cast()

    @property
    def is_parameterized(self):
        """:obj:`bool`: Primitive's parametrization.

        Read-Only.
        """
        return self.__stub.IsParameterized(self.msg).value

    def get_hfss_prop(self):
        """
        Get HFSS properties.

        Returns
        -------
        material : str
            Material property name.
        solve_inside : bool
            If solve inside.
        """
        prop_msg = self.__stub.GetHfssProp(self.msg)
        return prop_msg.material_name, prop_msg.solve_inside

    def remove_hfss_prop(self):
        """Remove HFSS properties."""
        self.__stub.RemoveHfssProp(self.msg)

    @property
    def is_zone_primitive(self):
        """:obj:`bool`: If primitive object is a zone.

        Read-Only.
        """
        return self.__stub.IsZonePrimitive(self.msg).value

    @property
    def can_be_zone_primitive(self):
        """:obj:`bool`: If a primitive can be a zone.

        Read-Only.
        """
        return True

    def make_zone_primitive(self, zone_id):
        """Make primitive a zone primitive with a zone specified by the provided id.

        Parameters
        ----------
        zone_id : int
            Id of zone primitive will use.

        """
        self.__stub.MakeZonePrimitive(messages.int_property_message(self, zone_id))


class Rectangle(Primitive):
    """Class representing a rectangle object."""

    __stub: rectangle_pb2_grpc.RectangleServiceStub = StubAccessor(StubType.rectangle)

    @classmethod
    def create(
        cls, layout, layer, net, rep_type, param1, param2, param3, param4, corner_rad, rotation
    ):
        """Create a rectangle.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout this rectangle will be in.
        layer : str or :class:`Layer <ansys.edb.layer.Layer>`
            Layer this rectangle will be on.
        net : str or :class:`Net <ansys.edb.net.Net>` or None
            Net this rectangle will have.
        rep_type : :class:`RectangleRepresentationType`
            Type that defines given parameters meaning.
        param1 : :class:`Value <ansys.edb.utility.Value>`
            X value of lower left point or center point.
        param2 : :class:`Value <ansys.edb.utility.Value>`
            Y value of lower left point or center point.
        param3 : :class:`Value <ansys.edb.utility.Value>`
            X value of upper right point or width.
        param4 : :class:`Value <ansys.edb.utility.Value>`
            Y value of upper right point or height.
        corner_rad : :class:`Value <ansys.edb.utility.Value>`
            Corner radius.
        rotation : :class:`Value <ansys.edb.utility.Value>`
            Rotation.

        Returns
        -------
        Rectangle
            Rectangle that was created.
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

    def get_parameters(self):
        """Get coordinates parameters.

        Returns
        -------
        tuple[
            :class:`RectangleRepresentationType`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`
        ]

            Returns a tuple of the following format:

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

    def set_parameters(self, rep_type, param1, param2, param3, param4, corner_rad, rotation):
        """Set coordinates parameters.

        Parameters
        ----------
        rep_type : :class:`RectangleRepresentationType`
            Type that defines given parameters meaning.
        param1 : :class:`Value <ansys.edb.utility.Value>`
            X value of lower left point or center point.
        param2 : :class:`Value <ansys.edb.utility.Value>`
            Y value of lower left point or center point.
        param3 : :class:`Value <ansys.edb.utility.Value>`
            X value of upper right point or width.
        param4 : :class:`Value <ansys.edb.utility.Value>`
            Y value of upper right point or height.
        corner_rad : :class:`Value <ansys.edb.utility.Value>`
            Corner radius.
        rotation : :class:`Value <ansys.edb.utility.Value>`
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
    def can_be_zone_primitive(self):
        """:obj:`bool`: If a rectangle can be a zone.

        Read-Only.
        """
        return True

    @property
    def polygon_data(self):
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Polygon data object of the rectangle.

        Read-Only.
        """
        return Rectangle.render(*self.get_parameters())

    @classmethod
    @parser.to_polygon_data
    def render(
        cls,
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
        rep_type : :class:`RectangleRepresentationType`
            Type that defines given parameters meaning.
        x_lower_left_or_center_x : :class:`Value <ansys.edb.utility.Value>`
            X value of lower left point or center point.
        y_lower_left_or_center_y : :class:`Value <ansys.edb.utility.Value>`
            Y value of lower left point or center point.
        x_upper_right_or_width : :class:`Value <ansys.edb.utility.Value>`
            X value of upper right point or width.
        y_upper_right_or_height : :class:`Value <ansys.edb.utility.Value>`
            Y value of upper right point or height.
        corner_radius : :class:`Value <ansys.edb.utility.Value>`
            Corner radius.
        rotation : :class:`Value <ansys.edb.utility.Value>`
            Rotation.
        is_hole : bool, optional
            If rectangle is hole.

        Returns
        -------
        :class:`PolygonData <ansys.edb.geometry.PolygonData>`
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


class Circle(Primitive):
    """Class representing a circle object."""

    __stub: circle_pb2_grpc.CircleServiceStub = StubAccessor(StubType.circle)

    @classmethod
    def create(cls, layout, layer, net, center_x, center_y, radius):
        """Create a circle.

        Parameters
        ----------
        layout: :class:`Layout <ansys.edb.layout.Layout>`
            Layout this circle will be in.
        layer: str or :class:`Layer <ansys.edb.layer.Layer>`
            Layer this circle will be on.
        net: str or :class:`Net <ansys.edb.net.Net>` or None
            Net this circle will have.
        center_x: :class:`Value <ansys.edb.utility.Value>`
            X value of center point.
        center_y: :class:`Value <ansys.edb.utility.Value>`
            Y value of center point.
        radius: :class:`Value <ansys.edb.utility.Value>`
            Radius value of the circle.

        Returns
        -------
        Circle
            Circle object created.
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
    def render(cls, center_x, center_y, radius, is_hole):
        """Render a circle.

        Parameters
        ----------
        center_x: :class:`Value <ansys.edb.utility.Value>`
            X value of center point.
        center_y: :class:`Value <ansys.edb.utility.Value>`
            Y value of center point.
        radius: :class:`Value <ansys.edb.utility.Value>`
            Radius value of the circle.
        is_hole: bool
            If circle object is a hole.

        Returns
        -------
        :class:`PolygonData <ansys.edb.geometry.PolygonData>`
            Polygon data object created.
        """
        return cls.__stub.Render(
            circle_pb2.CircleRenderMessage(
                center_x=messages.value_message(center_x),
                center_y=messages.value_message(center_y),
                radius=messages.value_message(radius),
                is_hole=is_hole,
            )
        )

    def get_parameters(self):
        """Get parameters of a circle.

        Returns
        -------
        tuple[
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`
        ]

            Returns a tuple of the following format:

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

    def set_parameters(self, center_x, center_y, radius):
        """Set parameters of a circle.

         Parameters
         ----------
        center_x: :class:`Value <ansys.edb.utility.Value>`
            X value of center point.
        center_y: :class:`Value <ansys.edb.utility.Value>`
            Y value of center point.
        radius: :class:`Value <ansys.edb.utility.Value>`
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

    def get_polygon_data(self):
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Polygon data object of the Circle object."""
        return Circle.render(*self.get_parameters(), self.is_void)

    def can_be_zone_primitive(self):
        """:obj:`bool`: If a circle can be a zone."""
        return True


class Text(Primitive):
    """Class representing a text object."""

    __stub: text_pb2_grpc.TextServiceStub = StubAccessor(StubType.text)

    @classmethod
    def create(cls, layout, layer, center_x, center_y, text):
        """Create a text object.

        Parameters
        ----------
        layout: :class:`Layout <ansys.edb.layout.Layout>`
            Layout this text will be in.
        layer: str or Layer
            Layer this text will be on.
        center_x: :class:`Value <ansys.edb.utility.Value>`
            X value of center point.
        center_y: :class:`Value <ansys.edb.utility.Value>`
            Y value of center point.
        text: str
            Text string.

        Returns
        -------
        Text
            The text Object that was created.
        """
        return Text(
            cls.__stub.Create(
                text_pb2.TextCreationMessage(
                    layout=layout.msg,
                    layer=messages.layer_ref_message(layer),
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    text=text,
                )
            )
        )

    def get_text_data(self):
        """Get the text data of a text.

        Returns
        -------
        tuple[
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            str
        ]
            Returns a tuple of the following format:

            **(center_x, center_y, text)**

            **center_x** : X value of center point.

            **center_y** : Y value of center point.

            **radius** : Text object's String value.
        """
        text_data_msg = self.__stub.GetTextData(self.msg)
        return (
            Value(text_data_msg.center_x),
            Value(text_data_msg.center_y),
            text_data_msg.text,
        )

    def set_text_data(self, center_x, center_y, text):
        """Set the text data of a text.

        Parameters
        ----------
        center_x: :class:`Value <ansys.edb.utility.Value>`
            X value of center point.
        center_y: :class:`Value <ansys.edb.utility.Value>`
            Y value of center point.
        text: str
            Text object's String value.
        """
        self.__stub.SetTextData(
            text_pb2.SetTextDataMessage(
                target=self.msg,
                data=text_pb2.TextDataMessage(
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    text=text,
                ),
            )
        )


class _PolygonQueryBuilder:
    @staticmethod
    def create(layout, layer, net, points):
        return polygon_pb2.PolygonCreationMessage(
            layout=layout.msg,
            layer=messages.layer_ref_message(layer),
            net=messages.net_ref_message(net),
            points=messages.polygon_data_message(points),
        )


class Polygon(Primitive):
    """Class representing a polygon object."""

    __stub: polygon_pb2_grpc.PolygonServiceStub = StubAccessor(StubType.polygon)

    @classmethod
    def create(cls, layout, layer, net, polygon_data):
        """Create a polygon.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout the polygon will be in.
        layer : str or :class:`Layer <ansys.edb.layer.Layer>`
            Layer this Polygon will be in.
        net : str or :class:`Net <ansys.edb.net.Net>` or None
            Net of the Polygon object.
        polygon_data : :class:`PolygonData <ansys.edb.geometry.PolygonData>`
            The outer contour of the Polygon.

        Returns
        -------
        Polygon
            Polygon object created.
        """
        return Polygon(
            cls.__stub.Create(_PolygonQueryBuilder.create(layout, layer, net, polygon_data))
        )

    @property
    @parser.to_polygon_data
    def polygon_data(self):
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Outer contour of the Polygon object."""
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
        """:obj:`bool`: If a polygon can be a zone.

        Read-Only.
        """
        return True


class _PathQueryBuilder:
    @staticmethod
    def create(layout, layer, net, width, end_cap1, end_cap2, corner, points):
        return path_pb2.PathCreationMessage(
            layout=layout.msg,
            layer=messages.layer_ref_message(layer),
            net=messages.net_ref_message(net),
            width=messages.value_message(width),
            end_cap1=end_cap1.value,
            end_cap2=end_cap2.value,
            corner=corner.value,
            points=messages.polygon_data_message(points),
        )


class Path(Primitive):
    """Class representing a path object."""

    __stub: path_pb2_grpc.PathServiceStub = StubAccessor(StubType.path)

    @classmethod
    def create(cls, layout, layer, net, width, end_cap1, end_cap2, corner_style, points):
        """Create a path.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout this Path will be in.
        layer : str or :class:`Layer <ansys.edb.layer.Layer>`
            Layer this Path will be on.
        net : str or :class:`Net <ansys.edb.net.Net>` or None
            Net this Path will have.
        width: :class:`Value <ansys.edb.utility.Value>`
            Path width.
        end_cap1: :class:`PathEndCapType`
            End cap style of path start end cap.
        end_cap2: :class:`PathEndCapType`
            End cap style of path end end cap.
        corner_style: :class:`PathCornerType`
            Corner style.
        points : :class:`PolygonData <ansys.edb.geometry.PolygonData>`
            Centerline polygonData to set.

        Returns
        -------
        Path
            Path object created.
        """
        return Path(
            cls.__stub.Create(
                _PathQueryBuilder.create(
                    layout, layer, net, width, end_cap1, end_cap2, corner_style, points
                )
            )
        )

    @classmethod
    @parser.to_polygon_data
    def render(cls, width, end_cap1, end_cap2, corner_style, path):
        """Render a Path object.

        Parameters
        ----------
        width: :class:`Value <ansys.edb.utility.Value>`
            Path width.
        end_cap1: :class:`PathEndCapType`
            End cap style of path start end cap.
        end_cap2: :class:`PathEndCapType`
            End cap style of path end end cap.
        corner_style: :class:`PathCornerType`
            Corner style.
        path: :class:`PolygonData <ansys.edb.geometry.PolygonData>`
            PolygonData to set.

        Returns
        -------
        :class:`PolygonData <ansys.edb.geometry.PolygonData>`
            PolygonData object created.
        """
        return cls.__stub.Render(
            path_pb2.PathRenderMessage(
                width=messages.value_message(width),
                end_cap1=end_cap1.value,
                end_cap2=end_cap2.value,
                corner_style=corner_style.value,
                path=messages.polygon_data_message(path),
            )
        )

    @property
    @parser.to_polygon_data
    def polygon_data(self):
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Polygon data of this Path."""
        return self.__stub.GetPolygonData(self.msg)

    @property
    @parser.to_polygon_data
    def center_line(self):
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Center line for this Path."""
        return self.__stub.GetCenterLine(self.msg)

    @center_line.setter
    def center_line(self, center_line):
        path_pb2.SetCenterLineMessage(
            target=self.msg, center_line=messages.polygon_data_message(center_line)
        )

    def get_end_cap_style(self):
        """Get path end cap styles.

        Returns
        -------
        tuple[
            :class:`PathEndCapType`,
            :class:`PathEndCapType`
        ]

            Returns a tuple of the following format:

            **(end_cap1, end_cap2)**

            **end_cap1** : End cap style of path start end cap.

            **end_cap2** : End cap style of path end end cap.
        """
        end_cap_msg = self.__stub.GetEndCapStyle(self.msg)
        return PathEndCapType(end_cap_msg.end_cap1), PathEndCapType(end_cap_msg.end_cap2)

    def set_end_cap_style(self, end_cap1, end_cap2):
        """Set path end cap styles.

        Parameters
        ----------
        end_cap1: :class:`PathEndCapType`
            End cap style of path start end cap.
        end_cap2: :class:`PathEndCapType`
            End cap style of path end end cap.
        """
        self.__stub.SetEndCapStyle(
            path_pb2.SetEndCapStyleMessage(
                target=self.msg,
                end_cap=path_pb2.EndCapStyleMessage(
                    end_cap1=end_cap1.value, end_cap2=end_cap2.value
                ),
            )
        )

    def get_clip_info(self):
        """Get data used to clip the path.

        Returns
        -------
        tuple[:class:`PolygonData <ansys.edb.geometry.PolygonData>`, bool]

            Returns a tuple of the following format:

            **(clipping_poly, keep_inside)**

            **clipping_poly** : PolygonData used to clip the path.

            **keep_inside** : Indicates whether the part of the path inside the polygon is preserved.
        """
        clip_info_msg = self.__stub.GetClipInfo(self.msg)
        return (
            parser.to_polygon_data(clip_info_msg.clipping_poly),
            clip_info_msg.keep_inside,
        )

    def set_clip_info(self, clipping_poly, keep_inside=True):
        """Set data used to clip the path.

        Parameters
        ----------
        clipping_poly: :class:`PolygonData <ansys.edb.geometry.PolygonData>`
            PolygonData used to clip the path.
        keep_inside: bool
            Indicates whether the part of the path inside the polygon should be preserved.
        """
        self.__stub.SetClipInfo(
            path_pb2.SetClipInfoMessage(
                target=self.msg,
                clipping_poly=messages.polygon_data_message(clipping_poly),
                keep_inside=keep_inside,
            )
        )

    @property
    def corner_style(self):
        """:class:`PathCornerType`: Path's corner style."""
        return PathCornerType(self.__stub.GetCornerStyle(self.msg).corner_style)

    @corner_style.setter
    def corner_style(self, corner_type):
        self.__stub.SetCornerStyle(
            path_pb2.SetCornerStyleMessage(
                target=self.msg,
                corner_style=path_pb2.CornerStyleMessage(corner_style=corner_type.value),
            )
        )

    @property
    def width(self):
        """:class:`Value <ansys.edb.utility.Value>`: Path width."""
        return Value(self.__stub.GetWidth(self.msg).width)

    @width.setter
    def width(self, width):
        self.__stub.SetWidth(
            path_pb2.SetWidthMessage(
                target=self.msg,
                width=path_pb2.WidthMessage(width=messages.value_message(width)),
            )
        )

    @property
    def miter_ratio(self):
        """:class:`Value <ansys.edb.utility.Value>`: Miter ratio."""
        return Value(self.__stub.GetMiterRatio(self.msg).miter_ratio)

    @miter_ratio.setter
    def miter_ratio(self, miter_ratio):
        self.__stub.SetMiterRatio(
            path_pb2.SetMiterRatioMessage(
                target=self.msg,
                miter_ratio=path_pb2.MiterRatioMessage(
                    miter_ratio=messages.value_message(miter_ratio)
                ),
            )
        )

    @property
    def can_be_zone_primitive(self):
        """:obj:`bool`: If a path can be a zone.

        Read-Only.
        """
        return True


class _BondwireQueryBuilder:
    @staticmethod
    def create(
        layout,
        net,
        bondwire_type,
        definition_name,
        placement_layer,
        width,
        material,
        start_context,
        start_layer_name,
        start_x,
        start_y,
        end_context,
        end_layer_name,
        end_x,
        end_y,
    ):
        return bondwire_pb2.BondwireCreateMessage(
            layout=layout.msg,
            net=messages.net_ref_message(net),
            bondwire_type=bondwire_type.value,
            definition_name=definition_name,
            placement_layer=placement_layer,
            width=messages.value_message(width),
            material=material,
            start_context=messages.edb_obj_message(start_context),
            start_layer_name=start_layer_name,
            start_x=messages.value_message(start_x),
            start_y=messages.value_message(start_y),
            end_context=messages.edb_obj_message(end_context),
            end_layer_name=end_layer_name,
            end_x=messages.value_message(end_x),
            end_y=messages.value_message(end_y),
        )

    @staticmethod
    def bondwire_bool_message(b, evaluated):
        return bondwire_pb2.BondwireBoolMessage(target=b.msg, evaluated=evaluated)

    @staticmethod
    def set_material_message(b, material):
        return bondwire_pb2.SetMaterialMessage(target=b.msg, material=material)

    @staticmethod
    def set_bondwire_type_message(b, bondwire_type):
        return bondwire_pb2.SetBondwireTypeMessage(target=b.msg, type=bondwire_type.value)

    @staticmethod
    def get_cross_section_type_message(bondwire_cross_section_type):
        return bondwire_pb2.GetCrossSectionTypeMessage(type=bondwire_cross_section_type.value)

    @staticmethod
    def set_cross_section_type_message(b, bondwire_cross_section_type):
        return bondwire_pb2.SetCrossSectionTypeMessage(
            target=b.msg, type=bondwire_cross_section_type.value
        )

    @staticmethod
    def set_cross_section_height_message(b, height):
        return bondwire_pb2.SetCrossSectionHeightMessage(
            target=b.msg, height=messages.value_message(height)
        )

    @staticmethod
    def set_definition_name_message(b, definition_name):
        return bondwire_pb2.SetDefinitionNameMessage(target=b.msg, definition_name=definition_name)

    @staticmethod
    def get_elevation_message(b, cell_instance):
        return bondwire_pb2.GetElevationMessage(
            bw=b.msg, cell_instance=messages.edb_obj_message(cell_instance)
        )

    @staticmethod
    def set_elevation_message(b, cell_instance, lyrname):
        return bondwire_pb2.SetElevationMessage(
            target=_BondwireQueryBuilder.get_elevation_message(b, cell_instance), lyrname=lyrname
        )

    @staticmethod
    def bondwire_value_message(b, value):
        return bondwire_pb2.BondwireValueMessage(target=b.msg, value=messages.value_message(value))

    @staticmethod
    def bondwire_traj_message(x1, y1, y2, x2):
        return bondwire_pb2.BondwireTrajMessage(
            x1=messages.value_message(x1),
            y1=messages.value_message(y1),
            x2=messages.value_message(x2),
            y2=messages.value_message(y2),
        )

    @staticmethod
    def set_bondwire_traj_message(b, x1, y1, y2, x2):
        return bondwire_pb2.SetBondwireTrajMessage(
            target=b.msg, traj=_BondwireQueryBuilder.bondwire_traj_message(x1, y1, x2, y2)
        )


class Bondwire(Primitive):
    """Class representing a bondwire object."""

    __stub: bondwire_pb2_grpc.BondwireServiceStub = StubAccessor(StubType.bondwire)

    @classmethod
    def create(
        cls,
        layout,
        bondwire_type,
        definition_name,
        placement_layer,
        width,
        material,
        start_context,
        start_layer_name,
        start_x,
        start_y,
        end_context,
        end_layer_name,
        end_x,
        end_y,
        net,
    ):
        """Create a bondwire object.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout this bondwire will be in.
        bondwire_type : :class:`BondwireType`
            Type of bondwire: kAPDBondWire or kJDECBondWire types.
        definition_name : str
            Bondwire definition name.
        placement_layer : str
            Layer name this bondwire will be on.
        width : :class:`Value <ansys.edb.utility.Value>`
            Bondwire width.
        material : str
            Bondwire material name.
        start_context : :class:`CellInstance <ansys.edb.hierarchy.CellInstance>`
            Start context: None means top level.
        start_layer_name : str
            Name of start layer.
        start_x : :class:`Value <ansys.edb.utility.Value>`
            X value of start point.
        start_y : :class:`Value <ansys.edb.utility.Value>`
            Y value of start point.
        end_context : :class:`CellInstance <ansys.edb.hierarchy.CellInstance>`
            End context: None means top level.
        end_layer_name : str
            Name of end layer.
        end_x : :class:`Value <ansys.edb.utility.Value>`
            X value of end point.
        end_y : :class:`Value <ansys.edb.utility.Value>`
            Y value of end point.
        net : str or :class:`Net <ansys.edb.net.Net>` or None
            Net of the Bondwire.

        Returns
        -------
        Bondwire
            Bondwire object created.
        """
        return Bondwire(
            cls.__stub.Create(
                _BondwireQueryBuilder.create(
                    layout,
                    net,
                    bondwire_type,
                    definition_name,
                    placement_layer,
                    width,
                    material,
                    start_context,
                    start_layer_name,
                    start_x,
                    start_y,
                    end_context,
                    end_layer_name,
                    end_x,
                    end_y,
                )
            )
        )

    def get_material(self, evaluated=True):
        """Get material of the bondwire.

        Parameters
        ----------
        evaluated : bool, optional
            True if an evaluated material name is wanted.

        Returns
        -------
        str
            Material name.
        """
        return self.__stub.GetMaterial(_BondwireQueryBuilder.bondwire_bool_message(self, evaluated))

    def set_material(self, material):
        """Set the material of a bondwire.

        Parameters
        ----------
        material : str
            Material name.
        """
        self.__stub.SetMaterial(_BondwireQueryBuilder.set_material_message(self, material))

    @property
    def type(self):
        """:class:`BondwireType`: Bondwire-type of a bondwire object."""
        btype_msg = self.__stub.GetType(self.msg)
        return BondwireType(btype_msg.type)

    @type.setter
    def type(self, bondwire_type):
        self.__stub.SetType(_BondwireQueryBuilder.set_bondwire_type_message(self, bondwire_type))

    @property
    def cross_section_type(self):
        """:class:`BondwireCrossSectionType`: Bondwire-cross-section-type of a bondwire object."""
        return BondwireCrossSectionType(self.__stub.GetCrossSectionType(self.msg).type)

    @cross_section_type.setter
    def cross_section_type(self, bondwire_type):
        self.__stub.SetCrossSectionType(
            _BondwireQueryBuilder.set_cross_section_type_message(self, bondwire_type)
        )

    @property
    def cross_section_height(self):
        """:class:`Value <ansys.edb.utility.Value>`: Bondwire-cross-section height of a bondwire object."""
        return Value(self.__stub.GetCrossSectionHeight(self.msg))

    @cross_section_height.setter
    def cross_section_height(self, height):
        self.__stub.SetCrossSectionHeight(
            _BondwireQueryBuilder.set_cross_section_height_message(self, height)
        )

    def get_definition_name(self, evaluated=True):
        """Get definition name of a bondwire object.

        Parameters
        ----------
        evaluated : bool, optional
            True if an evaluated (in variable namespace) material name is wanted.

        Returns
        -------
        str
            Bondwire name.
        """
        return self.__stub.GetDefinitionName(
            _BondwireQueryBuilder.bondwire_bool_message(self, evaluated)
        ).value

    def set_definition_name(self, definition_name):
        """Set the definition name of a bondwire.

        Parameters
        ----------
        definition_name : str
            Bondwire name to be set.
        """
        self.__stub.SetDefinitionName(
            _BondwireQueryBuilder.set_definition_name_message(self, definition_name)
        )

    def get_traj(self):
        """Get trajectory parameters of a bondwire object.

        Returns
        -------
        tuple[
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`
        ]

            Returns a tuple of the following format:

            **(x1, y1, x2, y2)**

            **x1** : X value of the start point.

            **y1** : Y value of the start point.

            **x1** : X value of the end point.

            **y1** : Y value of the end point.
        """
        traj_msg = self.__stub.GetTraj(self.msg)
        return (
            Value(traj_msg.x1),
            Value(traj_msg.y1),
            Value(traj_msg.x2),
            Value(traj_msg.y2),
        )

    def set_traj(self, x1, y1, x2, y2):
        """Set the parameters of the trajectory of a bondwire.

        Parameters
        ----------
        x1 : :class:`Value <ansys.edb.utility.Value>`
            X value of the start point.
        y1 : :class:`Value <ansys.edb.utility.Value>`
            Y value of the start point.
        x2 : :class:`Value <ansys.edb.utility.Value>`
            X value of the end point.
        y2 : :class:`Value <ansys.edb.utility.Value>`
            Y value of the end point.
        """
        self.__stub.SetTraj(_BondwireQueryBuilder.set_bondwire_traj_message(self, x1, y1, x2, y2))

    @property
    def width(self):
        """:class:`Value <ansys.edb.utility.Value>`: Width of a bondwire object."""
        val = self.__stub.GetWidthValue(self.msg)
        return Value(val)

    @width.setter
    def width(self, width):
        self.__stub.SetWidthValue(_BondwireQueryBuilder.bondwire_value_message(self, width))

    def get_start_elevation(self, start_context):
        """Get the start elevation layer of a bondwire object.

        Parameters
        ----------
        start_context : :class:`CellInstance <ansys.edb.hierarchy.CellInstance>`
            Start cell context of the bondwire.

        Returns
        -------
        :class:`Layer <ansys.edb.layer.Layer>`
            Start context of the bondwire.
        """
        return Layer(
            self.__stub.GetStartElevation(
                _BondwireQueryBuilder.get_elevation_message(self, start_context)
            )
        ).cast()

    def set_start_elevation(self, start_context, layer):
        """Set the start elevation of a bondwire.

        Parameters
        ----------
        start_context : :class:`CellInstance <ansys.edb.hierarchy.CellInstance>`
            Start cell context of the bondwire. None means top level.
        layer : str or :class:`Layer <ansys.edb.layer.Layer>`
            Start layer of the bondwire.
        """
        self.__stub.SetStartElevation(
            _BondwireQueryBuilder.set_elevation_message(self, start_context, layer)
        )

    def get_end_elevation(self, end_context):
        """Get the end elevation layer of a bondwire object.

        Parameters
        ----------
        end_context : :class:`CellInstance <ansys.edb.hierarchy.CellInstance>`
            End cell context of the bondwire.

        Returns
        -------
        :class:`Layer <ansys.edb.layer.Layer>`
            End context of the bondwire.
        """
        return Layer(
            self.__stub.GetEndElevation(
                _BondwireQueryBuilder.get_elevation_message(self, end_context)
            )
        ).cast()

    def set_end_elevation(self, end_context, layer):
        """Set the end elevation of a bondwire.

        Parameters
        ----------
        end_context : :class:`CellInstance <ansys.edb.hierarchy.CellInstance>`
            End cell context of the bondwire. None means top level.
        layer : str or :class:`Layer <ansys.edb.layer.Layer>`
            End layer of the bondwire.
        """
        self.__stub.SetEndElevation(
            _BondwireQueryBuilder.set_elevation_message(self, end_context, layer)
        )


class _PadstackInstanceQueryBuilder:
    @staticmethod
    def create_message(
        layout,
        net,
        name,
        padstack_def,
        rotation,
        top_layer,
        bottom_layer,
        solder_ball_layer,
        layer_map,
    ):
        return padstack_instance_pb2.PadstackInstCreateMessage(
            layout=layout.msg,
            net=net.msg,
            name=name,
            padstack_def=padstack_def.msg,
            rotation=messages.value_message(rotation),
            top_layer=top_layer.msg,
            bottom_layer=bottom_layer.msg,
            solder_ball_layer=messages.edb_obj_message(solder_ball_layer),
            layer_map=messages.edb_obj_message(layer_map),
        )

    @staticmethod
    def set_name_message(padstack_inst, name):
        return messages.edb_obj_name_message(padstack_inst, name)

    @staticmethod
    def position_and_rotation_message(x, y, rotation):
        return padstack_instance_pb2.PadstackInstPositionAndRotationMessage(
            position=messages.point_message((x, y)),
            rotation=messages.value_message(rotation),
        )

    @staticmethod
    def set_position_and_rotation_message(padstack_inst, x, y, rotation):
        return padstack_instance_pb2.PadstackInstSetPositionAndRotationMessage(
            target=padstack_inst.msg,
            params=_PadstackInstanceQueryBuilder.position_and_rotation_message(x, y, rotation),
        )

    @staticmethod
    def layer_range_message(top_layer, bottom_layer):
        return padstack_instance_pb2.PadstackInstLayerRangeMessage(
            top_layer=top_layer.msg,
            bottom_layer=bottom_layer.msg,
        )

    @staticmethod
    def set_layer_range_message(padstack_inst, top_layer, bottom_layer):
        return padstack_instance_pb2.PadstackInstSetLayerRangeMessage(
            target=padstack_inst.msg,
            range=_PadstackInstanceQueryBuilder.layer_range_message(top_layer, bottom_layer),
        )

    @staticmethod
    def set_solderball_layer_message(padstack_inst, solderball_layer):
        return padstack_instance_pb2.PadstackInstSetSolderBallLayerMessage(
            target=padstack_inst.msg,
            layer=solderball_layer.msg,
        )

    @staticmethod
    def back_drill_message(padstack_inst, from_bottom):
        return padstack_instance_pb2.PadstackInstBackDrillByLayerMessage(
            target=padstack_inst.msg,
            from_bottom=messages.bool_message(from_bottom),
        )

    @staticmethod
    def back_drill_by_layer_message(drill_to_layer, diameter, offset):
        return padstack_instance_pb2.PadstackInstBackDrillByLayerMessage(
            drill_to_layer=drill_to_layer.msg,
            diameter=messages.value_message(diameter),
            offset=messages.value_message(offset),
        )

    @staticmethod
    def back_drill_by_depth_message(drill_depth, diameter):
        return padstack_instance_pb2.PadstackInstBackDrillByDepthMessage(
            drill_depth=messages.value_message(drill_depth),
            diameter=messages.value_message(diameter),
        )

    @staticmethod
    def set_back_drill_by_layer_message(
        padstack_inst, drill_to_layer, offset, diameter, from_bottom
    ):
        return padstack_instance_pb2.PadstackInstSetBackDrillByLayerMessage(
            target=padstack_inst.msg,
            drill_to_layer=drill_to_layer.msg,
            offset=messages.value_message(offset),
            diameter=messages.value_message(diameter),
            from_bottom=from_bottom,
        )

    @staticmethod
    def set_back_drill_by_depth_message(padstack_inst, drill_depth, diameter, from_bottom):
        return padstack_instance_pb2.PadstackInstSetBackDrillByDepthMessage(
            target=padstack_inst.msg,
            drill_depth=messages.value_message(drill_depth),
            diameter=messages.value_message(diameter),
            from_bottom=from_bottom,
        )

    @staticmethod
    def hole_overrides_message(is_hole_override, hole_override):
        return padstack_instance_pb2.PadstackInstHoleOverridesMessage(
            is_hole_override=is_hole_override,
            hole_override=messages.value_message(hole_override),
        )

    @staticmethod
    def set_hole_overrides_message(padstack_inst, is_hole_override, hole_override):
        return padstack_instance_pb2.PadstackInstSetHoleOverridesMessage(
            target=padstack_inst.msg,
            hole_override_msg=_PadstackInstanceQueryBuilder.hole_overrides_message(
                is_hole_override, hole_override
            ),
        )

    @staticmethod
    def set_is_layout_pin_message(padstack_inst, is_layout_pin):
        return padstack_instance_pb2.PadstackInstSetIsLayoutPinMessage(
            target=padstack_inst.msg,
            is_layout_pin=is_layout_pin,
        )

    @staticmethod
    def is_in_pin_group_message(padstack_inst, pin_group):
        return padstack_instance_pb2.PadstackInstIsInPinGroupMessage(
            target=padstack_inst.msg,
            pin_group=pin_group.msg,
        )

    @staticmethod
    def get_back_drill_message(padstack_inst, from_bottom):
        return padstack_instance_pb2.PadstackInstGetBackDrillMessage(
            target=padstack_inst.msg,
            from_bottom=from_bottom,
        )


class PadstackInstance(Primitive):
    """Class representing a Padstack Instance object."""

    __stub: padstack_instance_pb2_grpc.PadstackInstanceServiceStub = StubAccessor(
        StubType.padstack_instance
    )
    layout_obj_type = LayoutObjType.PADSTACK_INSTANCE

    @classmethod
    def create(
        cls,
        layout,
        net,
        name,
        padstack_def,
        rotation,
        top_layer,
        bottom_layer,
        solder_ball_layer,
        layer_map,
    ):
        """Create a PadstackInstance object.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout this padstack instance will be in.
        net : :class:`Net <ansys.edb.net.Net>`
            Net of this padstack instance.
        name : str
            Name of padstack instance.
        padstack_def : PadstackDef
            Padstack definition of this padstack instance.
        rotation : :class:`Value <ansys.edb.utility.Value>`
            Rotation of this padstack instance.
        top_layer : :class:`Layer <ansys.edb.layer.Layer>`
            Top layer of this padstack instance.
        bottom_layer : :class:`Layer <ansys.edb.layer.Layer>`
            Bottom layer of this padstack instance.
        solder_ball_layer : :class:`Layer <ansys.edb.layer.Layer>`
            Solder ball layer of this padstack instance, or None for none.
        layer_map : :class:`LayerMap <ansys.edb.utility.LayerMap>`
            Layer map of this padstack instance. None or empty means do auto-mapping.

        Returns
        -------
        PadstackInstance
            Padstack instance object created.
        """
        return PadstackInstance(
            cls.__stub.Create(
                _PadstackInstanceQueryBuilder.create_message(
                    layout,
                    net,
                    name,
                    padstack_def,
                    rotation,
                    top_layer,
                    bottom_layer,
                    solder_ball_layer,
                    layer_map,
                )
            )
        )

    @property
    def padstack_def(self):
        """:class:`PadstackDef <ansys.edb.definition.padstack_def>`: PadstackDef of a Padstack Instance."""
        return PadstackDef(self.__stub.GetPadstackDef(self.msg))

    @property
    def name(self):
        """:obj:`str`: Name of a Padstack Instance."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, name):
        self.__stub.SetName(_PadstackInstanceQueryBuilder.set_name_message(self, name))

    def get_position_and_rotation(self):
        """Get the position and rotation of a Padstack Instance.

        Returns
        -------
        tuple[
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`
        ]

            Returns a tuple of the following format:

            **(x, y, rotation)**

            **x** : X coordinate.

            **y** : Y coordinate.

            **rotation** : Rotation in radians.
        """
        params = self.__stub.GetPositionAndRotation(self.msg)
        return (
            Value(params.position.x),
            Value(params.position.y),
            Value(params.rotation),
        )

    def set_position_and_rotation(self, x, y, rotation):
        """Set the position and rotation of a Padstack Instance.

        Parameters
        ----------
        x : :class:`Value <ansys.edb.utility.Value>`
            x : X coordinate.
        y : :class:`Value <ansys.edb.utility.Value>`
            y : Y coordinate.
        rotation : :class:`Value <ansys.edb.utility.Value>`
            rotation : Rotation in radians.
        """
        self.__stub.SetPositionAndRotation(
            _PadstackInstanceQueryBuilder.set_position_and_rotation_message(self, x, y, rotation)
        )

    def get_layer_range(self):
        """Get the top and bottom layers of a Padstack Instance.

        Returns
        -------
        tuple[
            :class:`Layer <ansys.edb.layer.Layer>`,
            :class:`Layer <ansys.edb.layer.Layer>`
        ]

            Returns a tuple of the following format:

            **(top_layer, bottom_layer)**

            **top_layer** : Top layer of the Padstack instance

            **bottom_layer** : Bottom layer of the Padstack instance
        """
        params = self.__stub.GetLayerRange(self.msg)
        return (
            Layer(params.top_layer).cast(),
            Layer(params.bottom_layer).cast(),
        )

    def set_layer_range(self, top_layer, bottom_layer):
        """Set the top and bottom layers of a Padstack Instance.

        Parameters
        ----------
        top_layer : :class:`Layer <ansys.edb.layer.Layer>`
            Top layer of the Padstack instance.
        bottom_layer : :class:`Layer <ansys.edb.layer.Layer>`
            Bottom layer of the Padstack instance.
        """
        self.__stub.SetLayerRange(
            _PadstackInstanceQueryBuilder.set_layer_range_message(self, top_layer, bottom_layer)
        )

    @property
    def solderball_layer(self):
        """:class:`Layer <ansys.edb.layer.Layer>`: SolderBall Layer of Padstack Instance."""
        return Layer(self.__stub.GetSolderBallLayer(self.msg)).cast()

    @solderball_layer.setter
    def solderball_layer(self, solderball_layer):
        self.__stub.SetSolderBallLayer(
            _PadstackInstanceQueryBuilder.set_solderball_layer_message(self, solderball_layer)
        )

    @property
    def layer_map(self):
        """:class:`LayerMap <ansys.edb.utility.LayerMap>`: Layer Map of the Padstack Instance."""
        return LayerMap(self.__stub.GetLayerMap(self.msg))

    @layer_map.setter
    def layer_map(self, layer_map):
        self.__stub.SetLayerMap(messages.pointer_property_message(self, layer_map))

    def get_hole_overrides(self):
        """Get the hole overrides of Padstack Instance.

        Returns
        -------
        tuple[
            bool,
            :class:`Value <ansys.edb.utility.Value>`
        ]

            Returns a tuple of the following format:

            **(is_hole_override, hole_override)**

            **is_hole_override** : If padstack instance is hole override.

            **hole_override** : Hole override diameter of this padstack instance.
        """
        params = self.__stub.GetHoleOverrides(self.msg)
        return (
            params.is_hole_override,
            Value(params.hole_override),
        )

    def set_hole_overrides(self, is_hole_override, hole_override):
        """Set the hole overrides of Padstack Instance.

        Parameters
        ----------
        is_hole_override : bool
            If padstack instance is hole override.
        hole_override : :class:`Value <ansys.edb.utility.Value>`
            Hole override diameter of this padstack instance.
        """
        self.__stub.SetHoleOverrides(
            _PadstackInstanceQueryBuilder.set_hole_overrides_message(
                self, is_hole_override, hole_override
            )
        )

    @property
    def is_layout_pin(self):
        """:obj:`bool`: If padstack instance is layout pin."""
        return self.__stub.GetIsLayoutPin(self.msg).value

    @is_layout_pin.setter
    def is_layout_pin(self, is_layout_pin):
        self.__stub.SetIsLayoutPin(
            _PadstackInstanceQueryBuilder.set_is_layout_pin_message(self, is_layout_pin)
        )

    def get_back_drill_type(self, from_bottom):
        """Get the back drill type of Padstack Instance.

        Parameters
        ----------
        from_bottom : bool
            True to get drill type from bottom.

        Returns
        -------
        :class:`BackDrillType`
            Back-Drill Type of padastack instance.
        """
        return BackDrillType(
            self.__stub.GetBackDrillType(
                _PadstackInstanceQueryBuilder.get_back_drill_message(self, from_bottom)
            ).type
        )

    def get_back_drill_by_layer(self, from_bottom):
        """Get the back drill by layer.

        Parameters
        ----------
        from_bottom : bool
            True to get drill type from bottom.

        Returns
        -------
        tuple[
            bool,
            :class:`Value <ansys.edb.utility.Value>`,
            :class:`Value <ansys.edb.utility.Value>`
        ]

            Returns a tuple of the following format:

            **(drill_to_layer, offset, diameter)**

            **drill_to_layer** : Layer drills to. If drill from top, drill stops at the upper elevation of the layer.\
            If from bottom, drill stops at the lower elevation of the layer.

            **offset** : Layer offset (or depth if layer is empty).

            **diameter** : Drilling diameter.
        """
        params = self.__stub.GetBackDrillByLayer(
            _PadstackInstanceQueryBuilder.get_back_drill_message(self, from_bottom)
        )

        return (
            Layer(params.drill_to_layer).cast(),
            Value(params.offset),
            Value(params.diameter),
        )

    def set_back_drill_by_layer(self, drill_to_layer, offset, diameter, from_bottom):
        """Set the back drill by layer.

        Parameters
        ----------
        drill_to_layer : :class:`Layer <ansys.edb.layer.Layer>`
            Layer drills to. If drill from top, drill stops at the upper elevation of the layer.
            If from bottom, drill stops at the lower elevation of the layer.
        offset : :class:`Value <ansys.edb.utility.Value>`
            Layer offset (or depth if layer is empty).
        diameter : :class:`Value <ansys.edb.utility.Value>`
            Drilling diameter.
        from_bottom : bool
            True to set drill type from bottom.
        """
        self.__stub.SetBackDrillByLayer(
            _PadstackInstanceQueryBuilder.set_back_drill_by_layer_message(
                self, drill_to_layer, offset, diameter, from_bottom
            )
        )

    def get_back_drill_by_depth(self, from_bottom):
        """Get the back drill by depth.

        Parameters
        ----------
        from_bottom : bool
            True to get drill type from bottom.

        Returns
        -------
        tuple[
            bool,
            :class:`Value <ansys.edb.utility.Value>`
        ]
            Returns a tuple of the following format:

            **(drill_depth, diameter)**

            **drill_depth** : Drilling depth, may not align with layer.

            **diameter** : Drilling diameter.
        """
        params = self.__stub.GetBackDrillByDepth(
            _PadstackInstanceQueryBuilder.get_back_drill_message(self, from_bottom)
        )
        return Value(params.drill_depth), Value(params.diameter)

    def set_back_drill_by_depth(self, drill_depth, diameter, from_bottom):
        """Set the back drill by Depth.

        Parameters
        ----------
        drill_depth : :class:`Value <ansys.edb.utility.Value>`
            Drilling depth, may not align with layer.
        diameter : :class:`Value <ansys.edb.utility.Value>`
            Drilling diameter.
        from_bottom : bool
            True to set drill type from bottom.
        """
        self.__stub.SetBackDrillByDepth(
            _PadstackInstanceQueryBuilder.set_back_drill_by_depth_message(
                self, drill_depth, diameter, from_bottom
            )
        )

    def get_padstack_instance_terminal(self):
        """:class:`TerminalInstance <ansys.edb.terminal.TerminalInstance>`: Padstack Instance's terminal."""
        return terminal.TerminalInstance(self.__stub.GetPadstackInstanceTerminal(self.msg))

    def is_in_pin_group(self, pin_group):
        """Check if Padstack instance is in the Pin Group.

        Parameters
        ----------
        pin_group : :class:`PinGroup <ansys.edb.hierarchy.PinGroup>`
            Pin group to check if padstack instance is in.

        Returns
        -------
        bool
            True if padstack instance is in pin group.
        """
        return self.__stub.IsInPinGroup(
            _PadstackInstanceQueryBuilder.is_in_pin_group_message(self, pin_group)
        ).value

    @property
    def pin_groups(self):
        """:obj:`list` of :class:`PinGroup <ansys.edb.hierarchy.PinGroup>`: Pin groups of Padstack instance object.

        Read-Only.
        """
        pins = self.__stub.GetPinGroups(self.msg).items
        return [hierarchy.PinGroup(p) for p in pins]


class BoardBendDef(Primitive):
    """Class representing board bending definitions."""

    __stub: board_bend_def_pb2_grpc.BoardBendDefServiceStub = StubAccessor(StubType.board_bend_def)

    @classmethod
    def create(cls, layout, zone_prim, bend_middle, bend_radius, bend_angle):
        """Create a board bend definition.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout this board bend definition will be in.
        zone_prim : :class:`Primitive <Primitive>`
            Zone primitive this board bend definition exists on.
        bend_middle : :term:`PointDataTuple`
            Tuple containing the starting and ending points of the line that represents the middle of the bend.
        bend_radius : :term:`ValueLike`
            Radius of the bend.
        bend_angle : :term:`ValueLike`
            Angle of the bend.

        Returns
        -------
        BoardBendDef
            BoardBendDef that was created.
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
        """:class:`Primitive <Primitive>`: Zone primitive the board bend is placed on.

        Read-Only.
        """
        return Primitive(self.__stub.GetBoundaryPrim(self.msg)).cast()

    @property
    @parser.to_point_data_pair
    def bend_middle(self):
        """:term:`PointDataTuple`: Tuple of the bend middle starting and ending points."""
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
        """:obj:`list` of :class:`PolygonData <ansys.edb.geometry.PolygonData>`: Bent region polygons.

            Collection of polygon data representing the areas bent by this bend definition.

        Read-Only.
        """
        return self.__stub.GetBentRegions(self.msg)
