"""Solder ball property."""

from ansys.api.edb.v1.padstack_def_data_pb2 import SolderballShape
import ansys.api.edb.v1.solder_ball_property_pb2 as pb
from ansys.api.edb.v1.solder_ball_property_pb2_grpc import SolderBallPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition.padstack_def_data import (
    SolderballPlacement,
    SolderballShape,
    _PadstackDefDataQueryBuilder,
)
from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    string_property_message,
    value_message,
    value_property_message,
)
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility import Value


class _QueryBuilder:
    @staticmethod
    def diameter_message(diameter1, diameter2):
        return pb.DiameterMessage(
            diameter1=value_message(diameter1),
            diameter2=value_message(diameter2),
        )

    @staticmethod
    def set_diameter_message(target, diameter1, diameter2):
        return pb.SetDiameterMessage(
            target=edb_obj_message(target),
            value=_QueryBuilder.diameter_message(
                diameter1,
                diameter2,
            ),
        )

    @staticmethod
    def set_shape_message(target, shape):
        return _PadstackDefDataQueryBuilder.padstack_def_data_set_solderball_shape_message(
            target, shape
        )

    @staticmethod
    def set_placement_message(target, placement):
        return _PadstackDefDataQueryBuilder.padstack_def_data_set_solderball_placement_message(
            target, placement
        )


class SolderBallProperty(ObjBase):
    """Represents a solder ball property."""

    __stub: SolderBallPropertyServiceStub = StubAccessor(StubType.solder_ball_property)

    @classmethod
    def create(cls):
        """
        Create a solder ball property.

        Returns
        -------
        SolderBallProperty
            Solder ball property created.
        """
        return SolderBallProperty(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def material_name(self):
        """:obj:`str`: Name of the solder ball material."""
        return self.__stub.GetMaterialName(edb_obj_message(self)).value

    @material_name.setter
    def material_name(self, name):
        self.__stub.SetMaterialName(string_property_message(self, name))

    @property
    def height(self):
        """:term:`ValueLike`: Height of the solder ball."""
        return Value(self.__stub.GetHeight(edb_obj_message(self)))

    @height.setter
    def height(self, height):
        self.__stub.SetHeight(value_property_message(self, value_message(height)))

    def get_diameter(self):
        """Get the diameter parameters of the solder ball property.

        Returns
        -------
        diameter1 : :term:`ValueLike`
            Diameter 1 of the solder ball property.
        diameter2 : :term:`ValueLike`
            Diameter 2 of the solder ball property.
        """
        diameter_paramaters = self.__stub.GetDiameter(edb_obj_message(self))
        return Value(diameter_paramaters.diameter1), Value(diameter_paramaters.diameter2)

    def set_diameter(self, diameter1, diameter2):
        """Set the diameter parameters of the solder ball property.

        Parameters
        ----------
        diameter1 : :term:`ValueLike`
            Diameter 1 of the solder ball property.
        diameter2 : :term:`ValueLike`
            Diameter 2 of the solder ball property.
        """
        self.__stub.SetDiameter(_QueryBuilder.set_diameter_message(self, diameter1, diameter2))

    @property
    def uses_solderball(self):
        """:obj:`bool`: Flag indicating if the solder ball is used.

        This property is read-only.
        """
        return self.__stub.UsesSolderball(self.msg).value

    @property
    def shape(self):
        """:class:`SolderballShape`: Solder ball shape."""
        return SolderballShape(self.__stub.GetShape(self.msg).solderball_shape)

    @shape.setter
    def shape(self, shape):
        self.__stub.SetShape(_QueryBuilder.set_shape_message(self, shape))

    @property
    def placement(self):
        """:class:`SolderballPlacement`: Solder ball placement."""
        return SolderballPlacement(self.__stub.GetPlacement(self.msg).solderball_placement)

    @placement.setter
    def placement(self, placement):
        self.__stub.SetPlacement(_QueryBuilder.set_placement_message(self, placement))

    def clone(self):
        """
        Clone a solder ball property.

        Returns
        -------
        SolderBallProperty
            Solder ball property cloned.
        """
        return SolderBallProperty(self.__stub.Clone(edb_obj_message(self)))
