"""Component Property."""

from ansys.api.edb.v1.component_property_pb2_grpc import ComponentPropertyServiceStub

from ansys.edb.core import ObjBase, messages
from ansys.edb.session import StubAccessor, StubType


class ComponentProperty(ObjBase):
    """Class representing a Component Property."""

    __stub: ComponentPropertyServiceStub = StubAccessor(StubType.component_property)

    def clone(self):
        """Return a clone of the component property.

        Returns
        -------
        ComponentProperty
        """
        return ComponentProperty(self.__stub.Clone(messages.edb_obj_message(self)))
