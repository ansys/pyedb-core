"""Primitive classes."""
from __future__ import annotations

from enum import Enum

from ansys.api.edb.v1 import primitive_pb2, primitive_pb2_grpc

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import conn_obj, factory, messages, utils
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType


class PrimitiveType(Enum):
    """Provides an enum representing primitive types."""

    RECTANGLE = primitive_pb2.RECTANGLE
    CIRCLE = primitive_pb2.CIRCLE
    POLYGON = primitive_pb2.POLYGON
    PATH = primitive_pb2.PATH
    BONDWIRE = primitive_pb2.BONDWIRE
    PRIM_PLUGIN = primitive_pb2.PRIM_PLUGIN
    TEXT = primitive_pb2.TEXT
    PATH_3D = primitive_pb2.PATH_3D
    BOARD_BEND = primitive_pb2.BOARD_BEND
    PRIM_INST_COLLECTION = primitive_pb2.PRIM_INST_COLLECTION
    INVALID_TYPE = primitive_pb2.INVALID_TYPE


class Primitive(conn_obj.ConnObj):
    """Represents a primitive object."""

    __stub: primitive_pb2_grpc.PrimitiveServiceStub = StubAccessor(StubType.primitive)
    layout_obj_type = LayoutObjType.PRIMITIVE
    """:class:`.LayoutObjType`: Layout object type of the Primitive class."""

    def cast(self) -> Primitive | None:
        """Cast the primitive object to the correct concrete type.

        Returns
        -------
        .Primitive
        """
        return None if self.is_null else factory.create_primitive(self.msg, self.primitive_type)

    @property
    def primitive_type(self) -> PrimitiveType:
        """:class:`.PrimitiveType`: Primitive type of the primitive.

        This property is read-only.
        """
        return PrimitiveType(self.__stub.GetPrimitiveType(self.msg).type)

    def add_void(self, hole):
        """Add a void to the primitive.

        Parameters
        ----------
        hole : .Primitive
            Void to add.
        """
        self.__stub.AddVoid(
            primitive_pb2.PrimitiveVoidCreationMessage(target=self.msg, hole=hole.msg)
        )

    def set_hfss_prop(self, material: str, solve_inside: bool):
        """Set HFSS properties.

        Parameters
        ----------
        material : str
            Material property name to set.
        solve_inside : bool
            Whether to solve inside.
        """
        self.__stub.SetHfssProp(
            primitive_pb2.PrimitiveHfssPropMessage(
                target=self.msg, material_name=material, solve_inside=solve_inside
            )
        )

    @property
    def layer(self) -> Layer:
        """:class:`.Layer`: Layer that the primitive object is on."""
        layer_msg = self.__stub.GetLayer(self.msg)
        return Layer(layer_msg).cast()

    @layer.setter
    def layer(self, layer: Layer):
        self.__stub.SetLayer(
            primitive_pb2.SetLayerMessage(target=self.msg, layer=messages.layer_ref_message(layer))
        )

    @property
    def is_negative(self) -> bool:
        """:obj:`bool`: Flag indicating if the primitive is negative."""
        return self.__stub.GetIsNegative(self.msg).value

    @is_negative.setter
    def is_negative(self, is_negative: bool):
        self.__stub.SetIsNegative(
            primitive_pb2.SetIsNegativeMessage(target=self.msg, is_negative=is_negative)
        )

    @property
    def is_void(self) -> bool:
        """:obj:`bool`: Flag indicating if a primitive is a void.

        This property is read-only.
        """
        return self.__stub.IsVoid(self.msg).value

    @property
    def has_voids(self) -> bool:
        """:obj:`bool`: Flag indicating if a primitive has voids inside.

        This property is read-only.
        """
        return self.__stub.HasVoids(self.msg).value

    @property
    def voids(self) -> list[Primitive]:
        """:obj:`list` of :class:`.Primitive`: List of void\
        primitive objects inside the primitive.

        This property is read-only.
        """
        return utils.query_lyt_object_collection(
            self, LayoutObjType.PRIMITIVE, self.__stub.Voids, self.__stub.StreamVoids, False
        )

    @property
    def owner(self) -> Primitive:
        """:class:`.Primitive`: Owner of the primitive object.

        This property is read-only.
        """
        return Primitive(self.__stub.GetOwner(self.msg)).cast()

    @property
    def is_parameterized(self) -> bool:
        """:obj:`bool`: Whether the primitive is parametrized.

        This property is read-only.
        """
        return self.__stub.IsParameterized(self.msg).value

    def get_hfss_prop(self) -> tuple[str, bool]:
        """Get HFSS properties.

        Returns
        -------
        tuple of (str, bool)

            Returns a tuple in this format:

            **(material, solve_inside)**

            **material** :  Name of the material property.

            **solve_inside** : Whether to solve inside.
        """
        prop_msg = self.__stub.GetHfssProp(self.msg)
        return prop_msg.material_name, prop_msg.solve_inside

    def remove_hfss_prop(self):
        """Remove HFSS properties."""
        self.__stub.RemoveHfssProp(self.msg)

    @property
    def is_zone_primitive(self) -> bool:
        """:obj:`bool`: Flag indicating if the primitive object is a zone.

        This property is read-only.
        """
        return self.__stub.IsZonePrimitive(self.msg).value

    @property
    def can_be_zone_primitive(self) -> bool:
        """:obj:`bool`: Flag indicating if the primitive can be a zone.

        This property is read-only.
        """
        return True

    def make_zone_primitive(self, zone_id: int):
        """Make the primitive a zone primitive with a zone specified by the provided ID.

        Parameters
        ----------
        zone_id : int
            ID of the zone primitive to use.
        """
        self.__stub.MakeZonePrimitive(messages.int_property_message(self, zone_id))
