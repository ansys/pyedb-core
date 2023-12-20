"""Component model definition."""
from ansys.api.edb.v1.component_model_pb2_grpc import (
    ComponentModelServiceStub,
    DynamicLinkComponentModelServiceStub,
    NPortComponentModelServiceStub,
)
import google.protobuf.wrappers_pb2 as proto_wrappers

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class ComponentModel(ObjBase):
    """Represents a component model."""

    __stub: ComponentModelServiceStub = StubAccessor(StubType.component_model)

    @property
    def reference_file(self):
        """:obj:`str`: Name of the reference file associated with the component model."""
        return self.__stub.GetReferenceFile(self.msg).value

    @reference_file.setter
    def reference_file(self, value):
        self.__stub.SetReferenceFile(messages.string_property_message(self, value))


class NPortComponentModel(ComponentModel):
    """Represents an NPort component model."""

    __stub: NPortComponentModelServiceStub = StubAccessor(StubType.nport_component_model)

    @classmethod
    def create(cls, name):
        """Create an NPort component model.

        Parameters
        ----------
        name : str
            Name of the NPport component model.

        Returns
        -------
        NPortComponentModel
            NPort component model created.

        Notes
        -----
        The component model does not belong to a specific database until it is added to a
        :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>` instance.
        """
        return NPortComponentModel(cls.__stub.Create(proto_wrappers.StringValue(value=name)))


class DynamicLinkComponentModel(ComponentModel):
    """Represents a dynamic link component model."""

    __stub: DynamicLinkComponentModelServiceStub = StubAccessor(StubType.dyn_link_component_model)

    @classmethod
    def create(cls, name):
        """Create a dynamic link component model.

        Parameters
        ----------
        name : str
            Name of the dynamic link component model.

        Returns
        -------
        DynamicLinkComponentModel
            Dynamic link component model created.

        Notes
        -----
        The component model does not belong to a specific database until it is added to a
        :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>` class.
        """
        return DynamicLinkComponentModel(cls.__stub.Create(proto_wrappers.StringValue(value=name)))

    @property
    def design_name(self):
        """:obj:`str`: Name of the design associated with the dynamic link component model."""
        return self.__stub.GetDesignName(self.msg).value

    @design_name.setter
    def design_name(self, value):
        self.__stub.SetDesignName(messages.string_property_message(self, value))
