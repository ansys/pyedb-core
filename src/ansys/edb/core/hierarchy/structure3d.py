"""Structure 3D."""

from enum import Enum

import ansys.api.edb.v1.structure3d_pb2 as structure3d_pb2
from ansys.api.edb.v1.structure3d_pb2_grpc import Structure3DServiceStub

from ansys.edb.core.hierarchy.group import Group
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class MeshClosure(Enum):
    """Provides an enum representing mesh closure types."""

    OPEN_ENDED = structure3d_pb2.OPEN_ENDED
    ENDS_CLOSED = structure3d_pb2.ENDS_CLOSED
    FILLED_CLOSED = structure3d_pb2.FILLED_CLOSED
    UNDEFINED_CLOSURE = structure3d_pb2.UNDEFINED_CLOSURE


class Structure3D(Group):
    """Represents a 3D structure."""

    __stub: Structure3DServiceStub = StubAccessor(StubType.structure3d)

    @classmethod
    def create(cls, layout, name):
        """Create a 3D structure.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the 3D structure in.
        name : str
            Name of the 3D structure.

        Returns
        -------
        Structure3D
            3D structure created.
        """
        return Structure3D(cls.__stub.Create(messages.object_name_in_layout_message(layout, name)))

    def get_material(self, evaluate):
        """Get the material for the 3D structure.

        Parameters
        ----------
        evaluate : bool
            Whether to resolve any references in the material name.

        Returns
        -------
        str
        """
        return self.__stub.GetMaterial(messages.bool_property_message(self, evaluate)).value

    def set_material(self, mat_name):
        """Set material for the 3D structure.

        Parameters
        ----------
        mat_name : str
            Material name.
        """
        self.__stub.SetMaterial(messages.string_property_message(self, mat_name))

    @property
    def thickness(self):
        """:class:`.Value`: Thickness for the 3D structure."""
        return Value(self.__stub.GetThickness(self.msg))

    @thickness.setter
    def thickness(self, value):
        self.__stub.SetThickness(
            messages.value_property_message(self, messages.value_message(value))
        )

    @property
    def mesh_closure(self):
        """:obj:`MeshClosure`: Mesh closure property for the 3D structure."""
        return MeshClosure(self.__stub.GetMeshClosureProp(self.msg).closure_type)

    @mesh_closure.setter
    def mesh_closure(self, value):
        self.__stub.SetMeshClosureProp(messages.set_closure_message(self, value))
