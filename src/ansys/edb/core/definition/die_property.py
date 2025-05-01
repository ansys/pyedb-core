"""Die property."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike

from enum import Enum

import ansys.api.edb.v1.die_property_pb2 as die_property_pb2
from ansys.api.edb.v1.die_property_pb2_grpc import DiePropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class DieOrientation(Enum):
    """Enum representing die orientations."""

    CHIP_UP = die_property_pb2.DIE_ORIENTATION_CHIP_UP
    CHIP_DOWN = die_property_pb2.DIE_ORIENTATION_CHIP_DOWN


class DieType(Enum):
    """Enum representing die types."""

    NONE = die_property_pb2.DIE_TYPE_NONE
    FLIPCHIP = die_property_pb2.DIE_TYPE_FLIPCHIP
    WIREBOND = die_property_pb2.DIE_TYPE_WIREBOND


class DieProperty(ObjBase):
    """Represents the properties of a die."""

    __stub: DiePropertyServiceStub = StubAccessor(StubType.die_property)

    @classmethod
    def create(cls) -> DieProperty:
        """
        Create a die property.

        Returns
        -------
        .DieProperty
        """
        return DieProperty(cls.__stub.Create(empty_pb2.Empty()))

    def clone(self) -> DieProperty:
        """
        Clone a die property.

        Returns
        -------
        .DieProperty
        """
        return DieProperty(self.__stub.Clone(messages.edb_obj_message(self)))

    @property
    def die_type(self) -> DieType:
        """:class:`.DieType`: Die type."""
        return DieType(self.__stub.GetDieType(self.msg).die_type)

    @die_type.setter
    def die_type(self, value: DieType):
        self.__stub.SetDieType(messages.set_die_type_message(self, value))

    @property
    def height(self) -> Value:
        """:class:`.Value`: Die height."""
        return Value(self.__stub.GetHeight(messages.edb_obj_message(self)))

    @height.setter
    def height(self, height: ValueLike):
        self.__stub.SetHeight(messages.value_property_message(self, messages.value_message(height)))

    @property
    def die_orientation(self) -> DieOrientation:
        """:class:`.DieOrientation`: Die orientation."""
        return DieOrientation(self.__stub.GetOrientation(self.msg).die_orientation)

    @die_orientation.setter
    def die_orientation(self, value: DieOrientation):
        self.__stub.SetOrientation(messages.set_die_orientation_message(self, value))
