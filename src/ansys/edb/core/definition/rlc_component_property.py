"""RLC Component Property."""

from ansys.api.edb.v1.rlc_component_property_pb2_grpc import RLCComponentPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition.component_property import ComponentProperty
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType


class RLCComponentProperty(ComponentProperty):
    """Class representing a RLCComponentProperty Property."""

    __stub: RLCComponentPropertyServiceStub = StubAccessor(StubType.rlc_component_property)

    @classmethod
    def create(cls):
        """
        Create RLC Component Property.

        Returns
        -------
        RLCComponentProperty
            RLC component property created.
        """
        return RLCComponentProperty(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def enabled(self):
        """:obj:`bool`: True if enabled, false otherwise."""
        return self.__stub.GetEnabled(messages.edb_obj_message(self)).value

    @enabled.setter
    def enabled(self, value):
        self.__stub.SetEnabled(messages.bool_property_message(self, value))
