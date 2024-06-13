"""Padstack definition data."""

from __future__ import annotations

from enum import Enum

import ansys.api.edb.v1.padstack_def_data_pb2 as pb
from ansys.api.edb.v1.padstack_def_data_pb2_grpc import PadstackDefDataServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.inner import ObjBase, messages, parser
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility import conversions
from ansys.edb.core.utility.value import Value


class PadType(Enum):
    """Provides an enum representing pad types."""

    REGULAR_PAD = pb.REGULAR_PAD
    ANTI_PAD = pb.ANTI_PAD
    THERMAL_PAD = pb.THERMAL_PAD
    HOLE = pb.HOLE
    UNKNOWN_GEOM_TYPE = pb.UNKNOWN_GEOM_TYPE


class PadGeometryType(Enum):
    """Provides an enum representing pad geometry types."""

    PADGEOMTYPE_NO_GEOMETRY = pb.PADGEOMTYPE_NO_GEOMETRY
    PADGEOMTYPE_CIRCLE = pb.PADGEOMTYPE_CIRCLE
    PADGEOMTYPE_SQUARE = pb.PADGEOMTYPE_SQUARE
    PADGEOMTYPE_RECTANGLE = pb.PADGEOMTYPE_RECTANGLE
    PADGEOMTYPE_OVAL = pb.PADGEOMTYPE_OVAL
    PADGEOMTYPE_BULLET = pb.PADGEOMTYPE_BULLET
    PADGEOMTYPE_NSIDED_POLYGON = pb.PADGEOMTYPE_NSIDED_POLYGON
    PADGEOMTYPE_POLYGON = pb.PADGEOMTYPE_POLYGON
    PADGEOMTYPE_ROUND45 = pb.PADGEOMTYPE_ROUND45
    PADGEOMTYPE_ROUND90 = pb.PADGEOMTYPE_ROUND90
    PADGEOMTYPE_SQUARE45 = pb.PADGEOMTYPE_SQUARE45
    PADGEOMTYPE_SQUARE90 = pb.PADGEOMTYPE_SQUARE90
    PADGEOMTYPE_INVALID_GEOMETRY = pb.PADGEOMTYPE_INVALID_GEOMETRY


class PadstackHoleRange(Enum):
    """Provides an enum representing pad hole ranges."""

    THROUGH = pb.THROUGH
    BEGIN_ON_UPPER_PAD = pb.BEGIN_ON_UPPER_PAD
    END_ON_LOWER_PAD = pb.END_ON_LOWER_PAD
    UPPER_PAD_TO_LOWER_PAD = pb.UPPER_PAD_TO_LOWER_PAD
    UNKNOWN_RANGE = pb.UNKNOWN_RANGE


class SolderballShape(Enum):
    """Provides an enum representing solder ball shapes."""

    NO_SOLDERBALL = pb.NO_SOLDERBALL
    SOLDERBALL_CYLINDER = pb.SOLDERBALL_CYLINDER
    SOLDERBALL_SPHEROID = pb.SOLDERBALL_SPHEROID
    UNKNOWN_SOLDERBALL_SHAPE = pb.UNKNOWN_SOLDERBALL_SHAPE


class SolderballPlacement(Enum):
    """Provides an enum representing solder ball placement."""

    ABOVE_PADSTACK = pb.ABOVE_PADSTACK
    BELOW_PADSTACK = pb.BELOW_PADSTACK
    UNKNOWN_PLACEMENT = pb.UNKNOWN_PLACEMENT


class ConnectionPtDirection(Enum):
    """Provides an enum representing connection pt direction."""

    PS_NO_DIRECTION = pb.PS_NO_DIRECTION
    PS_ANY_DIRECTION = pb.PS_ANY_DIRECTION
    PS_0_DIRECTION = pb.PS_0_DIRECTION
    PS_45_DIRECTION = pb.PS_45_DIRECTION
    PS_90_DIRECTION = pb.PS_90_DIRECTION
    PS_135_DIRECTION = pb.PS_135_DIRECTION
    PS_180_DIRECTION = pb.PS_180_DIRECTION
    PS_225_DIRECTION = pb.PS_225_DIRECTION
    PS_270_DIRECTION = pb.PS_270_DIRECTION
    PS_315_DIRECTION = pb.PS_315_DIRECTION
    PS_UNKNOWN_DIRECTION = pb.PS_UNKNOWN_DIRECTION


class PadstackDefData(ObjBase):
    """Represents a padstack data definition."""

    __stub: PadstackDefDataServiceStub = StubAccessor(StubType.padstack_def_data)

    @classmethod
    def create(cls):
        """
        Create a padstack data definition.

        Returns
        -------
        PadstackDefData
            Padstack data definition created.
        """
        return PadstackDefData(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def material(self):
        """:obj:`str`: Material name of the hole of the padstack definition data object."""
        return self.__stub.GetMaterial(self.msg)

    @material.setter
    def material(self, name):
        self.__stub.SetMaterial(pb.PadstackDefDataSetMaterialMessage(target=self.msg, name=name))

    @property
    def layer_names(self):
        """:obj:`list` of :obj:`str`: List of layer names in the padstack definition data object.

        This property is read-only.
        """
        layer_names_msg = self.__stub.GetLayerNames(self.msg).names
        return layer_names_msg

    @property
    def layer_ids(self):
        """:obj:`list` of :obj:`int`: All layer IDs in the padstack definition data object.

        This property is read-only.
        """
        layer_ids_msg = self.__stub.GetLayerIds(self.msg)
        return layer_ids_msg.ids

    def add_layers(self, names):
        """
        Add layers to the padstack definition data object.

        Parameters
        ----------
        names : List[str]
            List of layer names.
        """
        return self.__stub.AddLayers(
            pb.PadstackDefDataAddLayersMessage(
                target=self.msg, layer_names=pb.PadstackDefDataGetLayerNamesMessage(names=names)
            )
        )

    def get_pad_parameters(self, layer, pad_type):
        """
        Get pad parameters by layer name and pad type in their original values in the database.

        Parameters
        ----------
        layer : Union[str, int, None]
            Layer name.
        pad_type : PadType
            Pad type.

        Returns
        -------
        tuple[:class:`PadGeometryType`, list of :class:`.Value`, \
        :class:`.Value`, :class:`.Value`,
        :class:`.Value`]

        or

        tuple[:class:`.PolygonData`, \
        :class:`.Value`, \
        :class:`.Value`, :class:`.Value`]

            The tuple is in this format for other than polygons: ``(pad_type, sizes, offset_x, offset_y, rotation)``.

            For polygons, the tuple is in this format: ``(fp, offset_x, offset_y, rotation)``.

            - ``pad_type``: Pad type
            - ``sizes``: Pad parameters
            - ``offset_x``: X offset
            - ``offset_y``: Y offset
            - ``rotation``: Rotation
            - ``fp``: Polygon geometry
        """
        message = self.__stub.GetPadParameters(
            PadstackDefData._padstack_def_data_get_pad_parameters_message(self, layer, pad_type)
        )
        if message.HasField("generic"):
            return (
                PadGeometryType(message.generic.geometry_type),
                [Value(s) for s in message.generic.sizes],
                Value(message.generic.offset_x),
                Value(message.generic.offset_y),
                Value(message.generic.rotation),
            )
        else:
            return (
                parser.to_polygon_data(message.polygon.fp),
                Value(message.polygon.offset_x),
                Value(message.polygon.offset_y),
                Value(message.polygon.rotation),
            )

    def set_pad_parameters(
        self, layer, pad_type, offset_x, offset_y, rotation, type_geom=None, sizes=None, fp=None
    ):
        """
        Set pad parameters by layer name and pad type in their original values in the database.

        Parameters
        ----------
        layer : Union[str, int, None]
            Layer name.
        pad_type : PadType
            Pad type.
        offset_x : :class:`.Value`
            X offset.
        offset_y : :class:`.Value`
            Y offset.
        rotation : :class:`.Value`
            Rotation.
        type_geom : PadGeometryType, default: None
            Pad geometry type. The default is ``None`` if setting polygonal pad parameters.
        sizes : List[:class:`.Value`], default: None
            List of pad sizes. The default is ``None`` if setting polygonal pad parameters.
        fp : :class:`.PolygonData`, default: None
            Polygon geometry. The default is ``None`` if not setting polygonal pad parameters.
        """
        p1 = PadstackDefData._padstack_def_data_get_pad_parameters_message(self, layer, pad_type)
        message = None
        if fp is None:
            p2 = pb.PadstackDefDataGetPadParametersParametersMessage(
                geometry_type=type_geom.value,
                sizes=[messages.value_message(val) for val in sizes],
                offset_x=messages.value_message(offset_x),
                offset_y=messages.value_message(offset_y),
                rotation=messages.value_message(rotation),
            )
            message = pb.PadstackDefDataPadParametersSetMessage(
                generic=pb.PadstackDefDataSetPadParametersMessage(
                    params1=p1,
                    params2=p2,
                )
            )
        else:
            message = pb.PadstackDefDataPadParametersSetMessage(
                polygon=pb.PadstackDefDataSetPolygonalPadParametersMessage(
                    params1=p1,
                    fp=messages.polygon_data_message(fp),
                    offset_x=messages.value_message(offset_x),
                    offset_y=messages.value_message(offset_y),
                    rotation=messages.value_message(rotation),
                )
            )

        self.__stub.SetPadParameters(message)

    def get_hole_parameters(self):
        """
        Get hole parameters in their original values in the database.

        Returns
        -------
        tuple[:class:`.PolygonData`, \
        :class:`.Value`, \
        :class:`.Value`, :class:`.Value`]
            The tuple is in this format: ``(fp, offset_x, offset_y, rotation)``.

            - ``fp``: Polygon geometry
            - ``offset_x``: X offset
            - ``offset_y``: Y offset
            - ``rotation`` : Rotation
        """
        return self.get_pad_parameters(None, PadType.HOLE)

    def set_hole_parameters(self, offset_x, offset_y, rotation, type_geom, sizes):
        """
        Set hole parameters.

        Parameters
        ----------
        offset_x : :class:`.Value`
            X offset.
        offset_y : :class:`.Value`
            Y offset.
        rotation : :class:`.Value`
            Rotation.
        type_geom : PadGeometryType
            Pad geometry type.
        sizes : List[:class:`.Value`]
            List of pad sizes.
        """
        return self.set_pad_parameters(
            -1, PadType.HOLE, offset_x, offset_y, rotation, type_geom, sizes
        )

    @property
    def hole_range(self):
        """:class:`PadstackHoleRange`: Hole range of the padstack data definition."""
        return PadstackHoleRange(self.__stub.GetHoleRange(self.msg).hole_range)

    @hole_range.setter
    def hole_range(self, hole_range):
        self.__stub.SetHoleRange(
            pb.PadstackDefDataSetHoleRangeMessage(target=self.msg, hole_range=hole_range.value)
        )

    @property
    def plating_percentage(self):
        """:class:`.Value`: Hole plating percentage."""
        return Value(self.__stub.GetPlatingPercentage(self.msg))

    @plating_percentage.setter
    def plating_percentage(self, plating_percentage):
        self.__stub.SetPlatingPercentage(
            pb.PadstackDefDataSetPlatingPercentage(
                target=self.msg, plating_percentage=messages.value_message(plating_percentage)
            )
        )

    @property
    def solder_ball_shape(self):
        """:class:`SolderballShape`: Solder ball shape."""
        return SolderballShape(self.__stub.GetSolderBallShape(self.msg).solderball_shape)

    @solder_ball_shape.setter
    def solder_ball_shape(self, solderball_shape):
        self.__stub.SetSolderBallShape(
            pb.PadstackDefDataSetSolderballShapeMessage(
                target=self.msg, solderball_shape=solderball_shape.value
            )
        )

    @property
    def solder_ball_placement(self):
        """:class:`SolderballPlacement`: Solder ball placement or orientation."""
        return SolderballPlacement(self.__stub.GetSolderBallPlacement(self.msg))

    @solder_ball_placement.setter
    def solder_ball_placement(self, solderball_placement):
        self.__stub.SetSolderBallPlacement(
            pb.PadstackDefDataSetSolderballPlacementMessage(
                target=self.msg, solderball_placement=solderball_placement.value
            )
        )

    @property
    def solder_ball_param(self):
        """:obj:`tuple` of [:class:`.Value`, \
        :class:`.Value`]: Solder ball parameters ``(d1, d2)`` \
        in their original values in the database.

        - ``d1`` is the diameter for a cylinder solder ball or the top diameter for a spheroid
          solder ball.
        - ``d2`` is the middle diameter for a spheroid solder ball. It is not used for a cylinder solder ball.
        """
        params = self.__stub.GetSolderBallParam(self.msg)
        return (
            Value(params.d1),
            Value(params.d2),
        )

    @solder_ball_param.setter
    def solder_ball_param(self, params):
        self.__stub.SetSolderBallParam(
            pb.PadstackDefDataSetSolderBallParamMessage(
                target=self.msg,
                d1=messages.value_message(params[0]),
                d2=messages.value_message(params[1]),
            )
        )

    @property
    def solder_ball_material(self):
        """:obj:`str`: Name of the solder ball material."""
        return self.__stub.GetSolderBallMaterial(self.msg)

    @solder_ball_material.setter
    def solder_ball_material(self, material):
        self.__stub.SetSolderBallMaterial(
            pb.PadstackDefDataSetSolderBallMaterialMessage(target=self.msg, material=material)
        )

    def get_connection_pt(self, layer):
        """
        Get connection point position and direction by layer name.

        Parameters
        ----------
        layer : str
            Layer name.

        Returns
        -------
        tuple[:class:`.PointData`, :class:`ConnectionPtDirection`]
            The tuple is in a ``(position, direction)`` format:

            - ``position``: Position of the connection point.
            - ``direction``: Direction of the connection point.
        """
        msg = self.__stub.GetConnectionPt(
            pb.PadstackDefDataGetConnectionPtMessage(target=self.msg, layer=layer)
        )
        return parser.to_point_data(msg), ConnectionPtDirection(msg.direction)

    def set_connection_pt(self, layer, position, direction):
        """
        Set connection point position and direction.

        Parameters
        ----------
        layer : str
            Layer name.
        position : ansys.edb.core.typing.PointLike
            Position.
        direction : :class:`ConnectionPtDirection`
            Direction.
        """
        pos = conversions.to_point(position)
        self.__stub.SetConnectionPt(
            pb.PadstackDefDataSetConnectionPtMessage(
                target=self.msg,
                layer=layer,
                x=messages.value_message(pos.x),
                y=messages.value_message(pos.y),
                direction=direction.value,
            )
        )

    @staticmethod
    def _padstack_def_data_get_pad_parameters_message(target, layer, pad_type):
        return pb.PadstackDefDataGetPadParametersMessage(
            target=target.msg,
            layer_name=layer if isinstance(layer, str) else None,
            layer_id=layer if isinstance(layer, int) else None,
            pad_type=pad_type.value,
        )
