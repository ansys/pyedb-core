"""Component Property."""

from ansys.api.edb.v1.component_property_pb2_grpc import ComponentPropertyServiceStub

from ansys.edb.core import ObjBase, messages
from ansys.edb.definition import package_def
from ansys.edb.hierarchy import model
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value


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

    @property
    def package_mounting_offset(self):
        """:class:`Value <ansys.edb.utility.Value>`: Offset of the package definition object.

        Property can be set with :term:`ValueLike`
        """
        return Value(self.__stub.GetPackageMountingOffset(messages.edb_obj_message(self)))

    @package_mounting_offset.setter
    def package_mounting_offset(self, offset):
        self.__stub.SetPackageMountingOffset(
            messages.value_property_message(self, messages.value_message(offset))
        )

    @property
    def package_def(self):
        """:obj:`PackageDef` : Package definition object."""
        return package_def.PackageDef(self.__stub.GetPackageDef(messages.edb_obj_message(self)))

    @package_def.setter
    def package_def(self, value):
        self.__stub.SetPackageDef(messages.pointer_property_message(target=self, value=value))

    @property
    def model(self):
        """:class:`Model <ansys.edb.hierarchy.Model>` : Model object.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return model.Model(self.__stub.GetModel(messages.edb_obj_message(self)))

    @model.setter
    def model(self, value):
        self.__stub.SetModel(messages.pointer_property_message(target=self, value=value))
