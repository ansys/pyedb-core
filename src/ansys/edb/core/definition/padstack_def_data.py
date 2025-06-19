"""Padstack definition data."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike, PointLike
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.geometry.polygon_data import PolygonData

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
    """Enum representing pad hole ranges."""

    THROUGH = pb.THROUGH
    BEGIN_ON_UPPER_PAD = pb.BEGIN_ON_UPPER_PAD
    END_ON_LOWER_PAD = pb.END_ON_LOWER_PAD
    UPPER_PAD_TO_LOWER_PAD = pb.UPPER_PAD_TO_LOWER_PAD
    UNKNOWN_RANGE = pb.UNKNOWN_RANGE


class SolderballShape(Enum):
    """Enum representing solder ball shapes."""

    NO_SOLDERBALL = pb.NO_SOLDERBALL
    SOLDERBALL_CYLINDER = pb.SOLDERBALL_CYLINDER
    SOLDERBALL_SPHEROID = pb.SOLDERBALL_SPHEROID
    UNKNOWN_SOLDERBALL_SHAPE = pb.UNKNOWN_SOLDERBALL_SHAPE


class SolderballPlacement(Enum):
    """Enum representing solder ball placement."""

    ABOVE_PADSTACK = pb.ABOVE_PADSTACK
    BELOW_PADSTACK = pb.BELOW_PADSTACK
    UNKNOWN_PLACEMENT = pb.UNKNOWN_PLACEMENT


class ConnectionPtDirection(Enum):
    """Enum representing connection pt direction."""

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
    """Represents the padstack specific data of a padstack definition."""

    __stub: PadstackDefDataServiceStub = StubAccessor(StubType.padstack_def_data)

    @classmethod
    def create(cls) -> PadstackDefData:
        """
        Create a padstack definition data object.

        Returns
        -------
        .PadstackDefData
        """
        return PadstackDefData(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def material(self) -> str:
        """:obj:`str`: The padstack hole material."""
        return self.__stub.GetMaterial(self.msg)

    @material.setter
    def material(self, name: str):
        self.__stub.SetMaterial(pb.PadstackDefDataSetMaterialMessage(target=self.msg, name=name))

    @property
    def layer_names(self) -> List[str]:
        """:obj:`list` of :obj:`str`: Names of the padstack definition layers.

        This property is read-only.
        """
        layer_names_msg = self.__stub.GetLayerNames(self.msg).names
        return list(layer_names_msg)

    @property
    def layer_ids(self) -> List[int]:
        """:obj:`list` of :obj:`int`: IDs of the padstack definition layers.

        This property is read-only.
        """
        layer_ids_msg = self.__stub.GetLayerIds(self.msg)
        return list(layer_ids_msg.ids)

    def add_layers(self, names: List[str]):
        """
        Add layers to the padstack definition.

        Parameters
        ----------
        names : list of str
        """
        return self.__stub.AddLayers(
            pb.PadstackDefDataAddLayersMessage(
                target=self.msg, layer_names=pb.PadstackDefDataGetLayerNamesMessage(names=names)
            )
        )

    def get_pad_parameters(
        self, layer: str | int, pad_type: PadType
    ) -> (
        Tuple[PadGeometryType, List[Value], Value, Value, Value]
        | Tuple[PolygonData, Value, Value, Value]
        | Tuple[()]
    ):
        """
        Get pad parameters by layer name and pad type.

        Parameters
        ----------
        layer : str or int
            Layer name or ID.
        pad_type : .PadType
            Pad type.

        Returns
        -------
        tuple of (.PadGeometryType, list of .Value, .Value, .Value, .Value) or \
        tuple of (.PolygonData, .Value, .Value, .Value)

            - The tuple is in this format for non-polygonal pad geometry: \
            (``pad_type``, :term:`Pad Geometry Parameters`, ``offset_x``, ``offset_y``, ``rotation``).
            - For polygonal pad geometry, the tuple is in this format: \
            (``poly``, ``offset_x``, ``offset_y``, ``rotation``).
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
        elif message.HasField("polygon"):
            return (
                parser.to_polygon_data(message.polygon.fp),
                Value(message.polygon.offset_x),
                Value(message.polygon.offset_y),
                Value(message.polygon.rotation),
            )
        else:
            return ()

    def set_pad_parameters(
        self,
        layer: str | int,
        pad_type: PadType,
        offset_x: ValueLike,
        offset_y: ValueLike,
        rotation: ValueLike,
        type_geom: PadGeometryType = None,
        sizes: List[ValueLike] = None,
        poly: PolygonData = None,
    ):
        """
        Set pad parameters by layer and pad type.

        Parameters
        ----------
        layer : str or int
            Layer name or ID.
        pad_type : .PadType
            Pad type.
        offset_x : :term:`ValueLike`
            X offset.
        offset_y : :term:`ValueLike`
            Y offset.
        rotation : :term:`ValueLike`
            Rotation.
        type_geom : .PadGeometryType, default: None
            Pad geometry type. The default is :obj:`None` if setting polygonal pad parameters.
        sizes : list of :term:`ValueLike`, default: None
            List of :term:`Pad Geometry Parameters`. The default is :obj:`None` if setting polygonal pad parameters.
        poly : .PolygonData, default: None
            Polygon geometry. The default is :obj:`None` if not setting polygonal pad parameters.
        """
        p1 = PadstackDefData._padstack_def_data_get_pad_parameters_message(self, layer, pad_type)
        message = None
        if poly is None:
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
                    fp=messages.polygon_data_message(poly),
                    offset_x=messages.value_message(offset_x),
                    offset_y=messages.value_message(offset_y),
                    rotation=messages.value_message(rotation),
                )
            )

        self.__stub.SetPadParameters(message)

    def get_hole_parameters(
        self,
    ) -> (
        Tuple[PadGeometryType, List[Value], Value, Value, Value]
        | Tuple[PolygonData, Value, Value, Value]
        | Tuple[()]
    ):
        """
        Get the hole parameters of the padstack definition.

        Returns
        -------
        tuple of (.PadGeometryType, list of .Value, .Value, .Value, .Value) or \
        tuple of (.PolygonData, .Value, .Value, .Value)

            - The tuple is in this format for non-polygonal hole geometry: \
            (``pad_type``, :term:`Pad Geometry Parameters`, ``offset_x``, ``offset_y``, ``rotation``).
            - For polygonal hole geometry, the tuple is in this format: \
            (``poly``, ``offset_x``, ``offset_y``, ``rotation``).
        """
        return self.get_pad_parameters(None, PadType.HOLE)

    def set_hole_parameters(
        self,
        offset_x: ValueLike,
        offset_y: ValueLike,
        rotation: ValueLike,
        type_geom: PadGeometryType = None,
        sizes: List[ValueLike] = None,
        poly: PolygonData = None,
    ):
        """
        Set hole parameters.

        Parameters
        ----------
        layer : str or int
            Layer name or ID.
        pad_type : .PadType
            Pad type.
        offset_x : :term:`ValueLike`
            X offset.
        offset_y : :term:`ValueLike`
            Y offset.
        rotation : :term:`ValueLike`
            Rotation.
        type_geom : .PadGeometryType, default: None
            Pad geometry type. The default is :obj:`None` if setting polygonal pad parameters.
        sizes : list of :term:`ValueLike`, default: None
            List of :term:`Pad Geometry Parameters`. The default is :obj:`None` if setting polygonal pad parameters.
        poly : .PolygonData, default: None
            Polygon geometry. The default is :obj:`None` if not setting polygonal pad parameters.
        """
        return self.set_pad_parameters(
            -1, PadType.HOLE, offset_x, offset_y, rotation, type_geom, sizes, poly
        )

    @property
    def hole_range(self) -> PadstackHoleRange:
        """:class:`.PadstackHoleRange`: Hole range of the padstack data definition."""
        return PadstackHoleRange(self.__stub.GetHoleRange(self.msg).hole_range)

    @hole_range.setter
    def hole_range(self, hole_range: PadstackHoleRange):
        self.__stub.SetHoleRange(
            pb.PadstackDefDataSetHoleRangeMessage(target=self.msg, hole_range=hole_range.value)
        )

    @property
    def plating_percentage(self) -> Value:
        """:term:`ValueLike`: Hole plating percentage."""
        return Value(self.__stub.GetPlatingPercentage(self.msg))

    @plating_percentage.setter
    def plating_percentage(self, plating_percentage: ValueLike):
        self.__stub.SetPlatingPercentage(
            pb.PadstackDefDataSetPlatingPercentage(
                target=self.msg, plating_percentage=messages.value_message(plating_percentage)
            )
        )

    @property
    def solder_ball_shape(self) -> SolderballShape:
        """:class:`.SolderballShape`: Solder ball shape."""
        return SolderballShape(self.__stub.GetSolderBallShape(self.msg).solderball_shape)

    @solder_ball_shape.setter
    def solder_ball_shape(self, solderball_shape: SolderballShape):
        self.__stub.SetSolderBallShape(
            pb.PadstackDefDataSetSolderballShapeMessage(
                target=self.msg, solderball_shape=solderball_shape.value
            )
        )

    @property
    def solder_ball_placement(self) -> SolderballPlacement:
        """:class:`.SolderballPlacement`: Solder ball placement."""
        return SolderballPlacement(self.__stub.GetSolderBallPlacement(self.msg))

    @solder_ball_placement.setter
    def solder_ball_placement(self, solderball_placement: SolderballPlacement):
        self.__stub.SetSolderBallPlacement(
            pb.PadstackDefDataSetSolderballPlacementMessage(
                target=self.msg, solderball_placement=solderball_placement.value
            )
        )

    @property
    def solder_ball_param(self) -> Tuple[Value, Value]:
        """:obj:`tuple` of (:class:`.Value`, :class:`.Value`): Solder ball parameters ``(d1, d2)``.

        - ``d1`` is the diameter for a cylindrical solder ball or the top diameter for a spheroidal solder ball.
        - ``d2`` is the middle diameter for a spheroidal solder ball. It is not used for a cylindrical solder ball.
        """
        params = self.__stub.GetSolderBallParam(self.msg)
        return (
            Value(params.d1),
            Value(params.d2),
        )

    @solder_ball_param.setter
    def solder_ball_param(self, params: Tuple[ValueLike, ValueLike]):
        self.__stub.SetSolderBallParam(
            pb.PadstackDefDataSetSolderBallParamMessage(
                target=self.msg,
                d1=messages.value_message(params[0]),
                d2=messages.value_message(params[1]),
            )
        )

    @property
    def solder_ball_material(self) -> str:
        """:obj:`str`: Name of the solder ball material."""
        return self.__stub.GetSolderBallMaterial(self.msg).value

    @solder_ball_material.setter
    def solder_ball_material(self, material: str):
        self.__stub.SetSolderBallMaterial(
            pb.PadstackDefDataSetSolderBallMaterialMessage(target=self.msg, material=material)
        )

    def get_connection_pt(self, layer: str) -> Tuple[PointData, ConnectionPtDirection]:
        """
        Get connection point position and direction of the padstack definition by layer name.

        Parameters
        ----------
        layer : str
            Layer name.

        Returns
        -------
        tuple of (.PointData, .ConnectionPtDirection)
            The tuple is of the format ``(position, direction)``:

            - ``position``: Position of the connection point.
            - ``direction``: Direction of the connection point.
        """
        msg = self.__stub.GetConnectionPt(
            pb.PadstackDefDataGetConnectionPtMessage(target=self.msg, layer=layer)
        )
        return parser.to_point_data(msg), ConnectionPtDirection(msg.direction)

    def set_connection_pt(self, layer: str, position: PointLike, direction: ConnectionPtDirection):
        """
        Set connection point position and direction of the padstack definition by layer.

        Parameters
        ----------
        layer : str
            Layer name.
        position : :term:`Point2DLike`
        direction : .ConnectionPtDirection
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
