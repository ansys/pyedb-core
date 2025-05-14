"""Component model definition."""
from enum import Enum

from ansys.api.edb.v1.component_model_pb2 import ComponentModelType as pb_comp_model_Type
from ansys.api.edb.v1.component_model_pb2_grpc import (
    ComponentModelServiceStub,
    DynamicLinkComponentModelServiceStub,
    NPortComponentModelServiceStub,
)
import google.protobuf.wrappers_pb2 as proto_wrappers

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType


class ComponentModelType(Enum):
    """Enum representing component model types."""

    N_PORT = pb_comp_model_Type.N_PORT
    DYNAMIC_LINK = pb_comp_model_Type.DYNAMIC_LINK
    UNKNOWN_COMPONENT_MODEL_TYPE = pb_comp_model_Type.UNKNOWN_MODEL_TYPE


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

    @classmethod
    def find_by_name(cls, comp_def, value):
        """Find a component model by name in a given component def.

        Parameters
        ----------
        comp_def : :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>`
            Component def to search for the component model.
        value : str
            Name of the component model.

        Returns
        -------
        ComponentModel
            Component model that is found, ``None`` otherwise.
        """
        return ComponentModel(
            cls.__stub.FindByName(messages.string_property_message(comp_def, value))
        ).cast()

    @classmethod
    def find_by_id(cls, comp_def, value):
        """Find a component model by ID in a given component def.

        Parameters
        ----------
        comp_def : :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>`
            Component def to search for the component model.
        value : int
            ID of the component model.

        Returns
        -------
        ComponentModel
            Component model that is found, ``None`` otherwise.
        """
        return ComponentModel(
            cls.__stub.FindById(messages.int_property_message(comp_def, value))
        ).cast()

    @property
    def name(self) -> str:
        """:obj:`str`: The name of the component model.

        This property is read-only.
        """
        return self.__stub.GetName(self.msg).value

    @property
    def component_model_type(self) -> ComponentModelType:
        """:class:`.ComponentModelType`: The type of the component model.

        This property is read-only.
        """
        return ComponentModelType(self.__stub.GetType(self.msg).type)

    @property
    def component_model_id(self) -> int:
        """:obj:`int`: The id of the component model.

        This property is read-only.
        """
        return self.__stub.GetId(self.msg).value

    def cast(self) -> "ComponentModel":
        """Cast the component model object to the correct concrete type.

        Returns
        -------
        .ComponentModel
        """
        comp_model_type = (
            ComponentModelType.UNKNOWN_COMPONENT_MODEL_TYPE
            if self.is_null
            else self.component_model_type
        )
        if comp_model_type == ComponentModelType.N_PORT:
            return NPortComponentModel(self.msg)
        elif comp_model_type == ComponentModelType.DYNAMIC_LINK:
            return DynamicLinkComponentModel(self.msg)
        return ComponentModel(self.msg)


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
        :class:`.ComponentDef` instance.
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
        :class:`.ComponentDef` class.
        """
        return DynamicLinkComponentModel(cls.__stub.Create(proto_wrappers.StringValue(value=name)))

    @property
    def design_name(self):
        """:obj:`str`: Name of the design associated with the dynamic link component model."""
        return self.__stub.GetDesignName(self.msg).value

    @design_name.setter
    def design_name(self, value):
        self.__stub.SetDesignName(messages.string_property_message(self, value))
