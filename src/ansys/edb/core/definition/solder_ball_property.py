"""Solder ball property."""

import ansys.api.edb.v1.padstack_def_data_pb2 as padstack_def_data_pb2
from ansys.api.edb.v1.padstack_def_data_pb2 import SolderballShape
import ansys.api.edb.v1.solder_ball_property_pb2 as solder_ball_property_pb2
from ansys.api.edb.v1.solder_ball_property_pb2_grpc import SolderBallPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition.padstack_def_data import SolderballPlacement, SolderballShape
from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    string_property_message,
    value_message,
    value_property_message,
)
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


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
        self.__stub.SetDiameter(
            solder_ball_property_pb2.SetDiameterMessage(
                target=edb_obj_message(self),
                value=solder_ball_property_pb2.DiameterMessage(
                    diameter1=value_message(diameter1),
                    diameter2=value_message(diameter2),
                ),
            )
        )

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
        self.__stub.SetShape(
            padstack_def_data_pb2.PadstackDefDataSetSolderballShapeMessage(
                target=self.msg, solderball_shape=shape.value
            )
        )

    @property
    def placement(self):
        """:class:`SolderballPlacement`: Solder ball placement."""
        return SolderballPlacement(self.__stub.GetPlacement(self.msg).solderball_placement)

    @placement.setter
    def placement(self, placement):
        self.__stub.SetPlacement(
            padstack_def_data_pb2.PadstackDefDataSetSolderballPlacementMessage(
                target=self.msg, solderball_placement=placement.value
            )
        )

    def clone(self):
        """
        Clone a solder ball property.

        Returns
        -------
        SolderBallProperty
            Solder ball property cloned.
        """
        return SolderBallProperty(self.__stub.Clone(edb_obj_message(self)))
