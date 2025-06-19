"""RLC component property."""
from __future__ import annotations

from ansys.api.edb.v1.rlc_component_property_pb2_grpc import RLCComponentPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition.component_property import ComponentProperty
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType


class RLCComponentProperty(ComponentProperty):
    """Represents an RLC component property."""

    __stub: RLCComponentPropertyServiceStub = StubAccessor(StubType.rlc_component_property)

    @classmethod
    def create(cls) -> RLCComponentProperty:
        """
        Create an RLC component property.

        Returns
        -------
        .RLCComponentProperty
        """
        return RLCComponentProperty(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def enabled(self) -> bool:
        """:obj:`bool`: Flag indicating if the RLC component property is enabled."""
        return self.__stub.GetEnabled(messages.edb_obj_message(self)).value

    @enabled.setter
    def enabled(self, value: bool):
        self.__stub.SetEnabled(messages.bool_property_message(self, value))
