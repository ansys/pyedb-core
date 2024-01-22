"""Padstack definition data."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import ansys.api.edb.v1.padstack_def_data_pb2 as pb
from ansys.api.edb.v1.padstack_def_data_pb2_grpc import PadstackDefDataServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.inner import ObjBase, messages, parser
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility import Value


class _PadstackDefDataQueryBuilder:
    """Provides for creating gRPC messages for padstack data definition."""

    if TYPE_CHECKING:
        from padstack_def_data import PadstackDefData

    @staticmethod
    def padstack_def_data_set_material_message(target, material):
        return pb.PadstackDefDataSetMaterialMessage(target=target.msg, name=material)

    @staticmethod
    def padstack_def_data_get_layer_names_message(names):
        return pb.PadstackDefDataGetLayerNamesMessage(names=names)

    @staticmethod
    def padstack_def_data_get_layer_ids_message(ids):
        return pb.PadstackDefDataGetLayerIdsMessage(ids=ids)

    @staticmethod
    def padstack_def_data_add_layers_message(target, names):
        return pb.PadstackDefDataAddLayersMessage(
            target=target.msg,
            layer_names=_PadstackDefDataQueryBuilder.padstack_def_data_get_layer_names_message(
                names
            ),
        )

    @staticmethod
    def padstack_def_data_get_pad_parameters_message(target, layer, pad_type):
        return pb.PadstackDefDataGetPadParametersMessage(
            target=target.msg,
            layer_name=layer if isinstance(layer, str) else None,
            layer_id=layer if isinstance(layer, int) else None,
            pad_type=pad_type.value,
        )

    @staticmethod
    def padstack_def_data_get_pad_parameters_parameters_message(
        geometry_type, sizes, offset_x, offset_y, rotation
    ):
        return pb.PadstackDefDataGetPadParametersParametersMessage(
            geometry_type=geometry_type.value,
            sizes=[messages.value_message(val) for val in sizes],
            offset_x=messages.value_message(offset_x),
            offset_y=messages.value_message(offset_y),
            rotation=messages.value_message(rotation),
        )

    @staticmethod
    def padstack_def_data_set_pad_parameters_message(
        target, layer, pad_type, offset_x, offset_y, rotation, type_geom, sizes, fp
    ):
        p1 = _PadstackDefDataQueryBuilder.padstack_def_data_get_pad_parameters_message(
            target=target, layer=layer, pad_type=pad_type
        )
        if fp is None:
            p2 = _PadstackDefDataQueryBuilder.padstack_def_data_get_pad_parameters_parameters_message(
                geometry_type=type_geom,
                sizes=sizes,
                offset_x=offset_x,
                offset_y=offset_y,
                rotation=rotation,
            )
            return pb.PadstackDefDataPadParametersSetMessage(
                generic=pb.PadstackDefDataSetPadParametersMessage(
                    params1=p1,
                    params2=p2,
                )
            )
        else:
            return pb.PadstackDefDataPadParametersSetMessage(
                polygon=pb.PadstackDefDataSetPolygonalPadParametersMessage(
                    params1=p1,
                    fp=messages.polygon_data_message(fp),
                    offset_x=messages.value_message(offset_x),
                    offset_y=messages.value_message(offset_y),
                    rotation=messages.value_message(rotation),
                )
            )

    @staticmethod
    def padstack_def_data_padstack_hole_range_message(hole_range):
        return pb.PadstackDefDataPadstackHoleRangeMessage(hole_range=hole_range.value)

    @staticmethod
    def padstack_def_data_set_hole_range_message(target, hole_range):
        return pb.PadstackDefDataSetHoleRangeMessage(target=target.msg, hole_range=hole_range.value)

    @staticmethod
    def padstack_def_data_set_plating_percentage(target, plating_percentage):
        return pb.PadstackDefDataSetPlatingPercentage(
            target=target.msg, plating_percentage=messages.value_message(plating_percentage)
        )

    @staticmethod
    def padstack_def_data_solderball_shape_message(solderball_shape):
        return pb.PadstackDefDataSolderballShapeMessage(solderball_shape=solderball_shape)

    @staticmethod
    def padstack_def_data_set_solderball_shape_message(target, solderball_shape):
        return pb.PadstackDefDataSetSolderballShapeMessage(
            target=target.msg, solderball_shape=solderball_shape.value
        )

    @staticmethod
    def padstack_def_data_solderball_placement_message(target, solderball_placement):
        return pb.PadstackDefDataSolderballPlacementMessage(
            target=target.msg, solderball_placement=solderball_placement
        )

    @staticmethod
    def padstack_def_data_set_solderball_placement_message(target, solderball_placement):
        return pb.PadstackDefDataSetSolderballPlacementMessage(
            target=target.msg, solderball_placement=solderball_placement.value
        )

    @staticmethod
    def padstack_def_data_get_solder_ball_param_message(d1, d2):
        return pb.PadstackDefDataGetSolderBallParamMessage(
            d1=messages.value_message(d1), d2=messages.value_message(d2)
        )

    @staticmethod
    def padstack_def_data_set_solder_ball_param_message(target, d1, d2):
        return pb.PadstackDefDataSetSolderBallParamMessage(
            target=target.msg, d1=messages.value_message(d1), d2=messages.value_message(d2)
        )

    @staticmethod
    def padstack_def_data_set_solder_ball_material_message(target, material):
        return pb.PadstackDefDataSetSolderBallMaterialMessage(target=target.msg, material=material)


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
        self.__stub.SetMaterial(
            _PadstackDefDataQueryBuilder.padstack_def_data_set_material_message(self, name)
        )

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
            _PadstackDefDataQueryBuilder.padstack_def_data_add_layers_message(self, names)
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
        tuple[:class:`PadGeometryType`, list of :class:`Value <ansys.edb.core.utility.Value>`, \
        :class:`Value <ansys.edb.core.utility.Value>`, :class:`Value <ansys.edb.core.utility.Value>`,
        :class:`Value <ansys.edb.core.utility.Value>`]

        or

        tuple[:class:`PolygonData <ansys.edb.core.geometry.PolygonData>`, \
        :class:`Value <ansys.edb.core.utility.Value>`, \
        :class:`Value <ansys.edb.core.utility.Value>`, :class:`Value <ansys.edb.core.utility.Value>`]

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
            _PadstackDefDataQueryBuilder.padstack_def_data_get_pad_parameters_message(
                self, layer, pad_type
            )
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
        offset_x : :class:`Value <ansys.edb.core.utility.Value>`
            X offset.
        offset_y : :class:`Value <ansys.edb.core.utility.Value>`
            Y offset.
        rotation : :class:`Value <ansys.edb.core.utility.Value>`
            Rotation.
        type_geom : PadGeometryType, default: None
            Pad geometry type. The default is ``None`` if setting polygonal pad parameters.
        sizes : List[:class:`Value <ansys.edb.core.utility.Value>`], default: None
            List of pad sizes. The default is ``None`` if setting polygonal pad parameters.
        fp : :class:`PolygonData <ansys.edb.core.geometry.PolygonData>`, default: None
            Polygon geometry. The default is ``None`` if not setting polygonal pad parameters.
        """
        self.__stub.SetPadParameters(
            _PadstackDefDataQueryBuilder.padstack_def_data_set_pad_parameters_message(
                self, layer, pad_type, offset_x, offset_y, rotation, type_geom, sizes, fp
            )
        )

    def get_hole_parameters(self):
        """
        Get hole parameters in their original values in the database.

        Returns
        -------
        tuple[:class:`PolygonData <ansys.edb.core.geometry.PolygonData>`, \
        :class:`Value <ansys.edb.core.utility.Value>`, \
        :class:`Value <ansys.edb.core.utility.Value>`, :class:`Value <ansys.edb.core.utility.Value>`]

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
        offset_x : :class:`Value <ansys.edb.core.utility.Value>`
            X offset.
        offset_y : :class:`Value <ansys.edb.core.utility.Value>`
            Y offset.
        rotation : :class:`Value <ansys.edb.core.utility.Value>`
            Rotation.
        type_geom : PadGeometryType
            Pad geometry type.
        sizes : List[:class:`Value <ansys.edb.core.utility.Value>`]
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
            _PadstackDefDataQueryBuilder.padstack_def_data_set_hole_range_message(self, hole_range)
        )

    @property
    def plating_percentage(self):
        """:class:`Value <ansys.edb.core.utility.Value>`: Hole plating percentage."""
        return Value(self.__stub.GetPlatingPercentage(self.msg))

    @plating_percentage.setter
    def plating_percentage(self, plating_percentage):
        self.__stub.SetPlatingPercentage(
            _PadstackDefDataQueryBuilder.padstack_def_data_set_plating_percentage(
                self, plating_percentage
            )
        )

    @property
    def solder_ball_shape(self):
        """:class:`SolderballShape`: Solder ball shape."""
        return SolderballShape(self.__stub.GetSolderBallShape(self.msg).solderball_shape)

    @solder_ball_shape.setter
    def solder_ball_shape(self, solderball_shape):
        self.__stub.SetSolderBallShape(
            _PadstackDefDataQueryBuilder.padstack_def_data_set_solderball_shape_message(
                self, solderball_shape
            )
        )

    @property
    def solder_ball_placement(self):
        """:class:`SolderballPlacement`: Solder ball placement or orientation."""
        return SolderballPlacement(self.__stub.GetSolderBallPlacement(self.msg))

    @solder_ball_placement.setter
    def solder_ball_placement(self, solderball_placement):
        self.__stub.SetSolderBallPlacement(
            _PadstackDefDataQueryBuilder.padstack_def_data_set_solderball_placement_message(
                self, solderball_placement
            )
        )

    @property
    def solder_ball_param(self):
        """:obj:`tuple` of [:class:`Value <ansys.edb.core.utility.Value>`, \
        :class:`Value <ansys.edb.core.utility.Value>`]: Solder ball parameters ``(d1, d2)`` \
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
            _PadstackDefDataQueryBuilder.padstack_def_data_set_solder_ball_param_message(
                self, params[0], params[1]
            )
        )

    @property
    def solder_ball_material(self):
        """:obj:`str`: Name of the solder ball material."""
        return self.__stub.GetSolderBallMaterial(self.msg)

    @solder_ball_material.setter
    def solder_ball_material(self, material):
        self.__stub.SetSolderBallMaterial(
            _PadstackDefDataQueryBuilder.padstack_def_data_set_solder_ball_material_message(
                self, material
            )
        )
