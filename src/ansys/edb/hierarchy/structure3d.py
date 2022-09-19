"""Structure 3D."""

from enum import Enum

import ansys.api.edb.v1.structure3d_pb2 as structure3d_pb2
from ansys.api.edb.v1.structure3d_pb2_grpc import Structure3DServiceStub

from ansys.edb.core import messages
from ansys.edb.hierarchy.group import Group
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value


class MeshClosure(Enum):
    """Enum representing mesh closure types.

    - OPEN_ENDED
    - ENDS_CLOSED
    - FILLED_CLOSED
    - UNDEFINED_CLOSURE
    """

    OPEN_ENDED = structure3d_pb2.OPEN_ENDED
    ENDS_CLOSED = structure3d_pb2.ENDS_CLOSED
    FILLED_CLOSED = structure3d_pb2.FILLED_CLOSED
    UNDEFINED_CLOSURE = structure3d_pb2.UNDEFINED_CLOSURE


class Structure3D(Group):
    """Class representing a structure3d object."""

    __stub: Structure3DServiceStub = StubAccessor(StubType.structure3d)

    @classmethod
    def create(cls, layout, name):
        """Create Structure3D.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the structure3d.
        name : str
            Name of the structure3d object.

        Returns
        -------
        Structure3D
            Newly created structure3d.
        """
        return Structure3D(cls.__stub.Create(messages.object_name_in_layout_message(layout, name)))

    def get_material(self, evaluate):
        """Get material for the structure3d.

        Parameters
        ----------
        evaluate : bool
            Any references in the material name will be resolved if True.

        Returns
        -------
        str
        """
        return self.__stub.GetMaterial(messages.bool_property_message(self, evaluate)).value

    def set_material(self, mat_name):
        """Set material for the structure3d.

        Parameters
        ----------
        mat_name : str
        """
        self.__stub.SetMaterial(messages.string_property_message(self, mat_name))

    @property
    def thickness(self):
        """:class:`Value <ansys.edb.utility.Value>`: Thickness for the structure3d."""
        return Value(self.__stub.GetThickness(self.msg))

    @thickness.setter
    def thickness(self, value):
        """Set thickness for the structure3d."""
        self.__stub.SetThickness(
            messages.value_property_message(self, messages.value_message(value))
        )

    @property
    def mesh_closure(self):
        """:obj:`MeshClosure`: Mesh closure property for the structure3d."""
        return MeshClosure(self.__stub.GetMeshClosureProp(self.msg).closure_type)

    @mesh_closure.setter
    def mesh_closure(self, value):
        """Set mesh closure property for the structure3d."""
        self.__stub.SetMeshClosureProp(messages.set_closure_message(self, value))
