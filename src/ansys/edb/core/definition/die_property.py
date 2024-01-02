"""Die property."""

from enum import Enum

import ansys.api.edb.v1.die_property_pb2 as die_property_pb2
from ansys.api.edb.v1.die_property_pb2_grpc import DiePropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.inner.base import ObjBase
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    set_die_orientation_message,
    set_die_type_message,
    value_message,
    value_property_message,
)
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class DieOrientation(Enum):
    """Provides an enum representing die orientations.

    - CHIP_UP
    - CHIP_DOWN
    """

    CHIP_UP = die_property_pb2.DIE_ORIENTATION_CHIP_UP
    CHIP_DOWN = die_property_pb2.DIE_ORIENTATION_CHIP_DOWN


class DieType(Enum):
    """Provides an enum representing die types.

    - NONE
    - FLIPCHIP
    - WIREBOND
    """

    NONE = die_property_pb2.DIE_TYPE_NONE
    FLIPCHIP = die_property_pb2.DIE_TYPE_FLIPCHIP
    WIREBOND = die_property_pb2.DIE_TYPE_WIREBOND


class DieProperty(ObjBase):
    """Represents a die property."""

    __stub: DiePropertyServiceStub = StubAccessor(StubType.die_property)

    @classmethod
    def create(cls):
        """
        Create a die property.

        Returns
        -------
        DieProperty
            Die property created.
        """
        return DieProperty(cls.__stub.Create(empty_pb2.Empty()))

    def clone(self):
        """
        Clone a die property.

        Returns
        -------
        DieProperty
            Cloned die property created.
        """
        return DieProperty(self.__stub.Clone(edb_obj_message(self)))

    @property
    def die_type(self):
        """:obj:`DieType`: Die type."""
        return DieType(self.__stub.GetDieType(self.msg).die_type)

    @die_type.setter
    def die_type(self, value):
        self.__stub.SetDieType(set_die_type_message(self, value))

    @property
    def height(self):
        """:class:`Value <ansys.edb.core.utility.Value>`: Height of the die property.

        This attribute can be set with the :term:`ValueLike` term.
        """
        return Value(self.__stub.GetHeight(edb_obj_message(self)))

    @height.setter
    def height(self, height):
        self.__stub.SetHeight(value_property_message(self, value_message(height)))

    @property
    def die_orientation(self):
        """:obj:`DieOrientation`: Die orientation."""
        return DieOrientation(self.__stub.GetOrientation(self.msg).die_orientation)

    @die_orientation.setter
    def die_orientation(self, value):
        self.__stub.SetOrientation(set_die_orientation_message(self, value))
