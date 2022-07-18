"""Cell Instance."""

from ansys.api.edb.v1.cell_instance_pb2_grpc import CellInstanceServiceStub

from ansys.edb.core.hierarchy.hierarchy_obj import HierarchyObj
from ansys.edb.core.interface.grpc import messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.transform3d import Transform3D
from ansys.edb.core.utility.value import Value


class CellInstance(HierarchyObj):
    """Class for representing cell instance hierarchy object."""

    __stub: CellInstanceServiceStub = StubAccessor(StubType.cell_instance)

    @classmethod
    def create(cls, layout, name, ref):
        """Create a cell instance object with layout.

        Parameters
        ----------
        layout: Layout
        name: str
        ref: Layout

        Returns
        -------
        CellInstance
            Cell instance created.
        """
        return CellInstance(
            cls.__stub.Create(messages.cell_instance_creation_message(layout, name, ref))
        )

    @classmethod
    def create_with_component(cls, layout, name, ref):
        """Create a cell instance object with component.

        Parameters
        ----------
        layout: Layout
        name: str
        ref: Component

        Returns
        -------
        CellInstance
            Cell instance created.
        """
        return CellInstance(
            cls.__stub.CreateWithComponent(
                messages.cell_instance_creation_message(layout, name, ref)
            )
        )

    @classmethod
    def find(cls, layout, name):
        """Find a cell instance by name in the given layout.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        CellInstance
        """
        return CellInstance(
            cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name))
        )

    @property
    def reference_layout(self):
        """Get the reference layout of the cell instance.

        Returns
        -------
        Layout
        """
        from ansys.edb.core.layout.layout import Layout

        return Layout(self.__stub.GetReferenceLayout(self.msg))

    @property
    def term_instances(self):
        """Get the list of terminal instances associated with this cell instance.

        Returns
        -------
        list of ansys.edb.core.terminal.TerminalInstances
        """
        from ansys.edb.core.terminal.terminals import TerminalInstance

        terms = self.__stub.GetTermInsts(self.msg).items
        return [TerminalInstance(ti) for ti in terms]

    @property
    def placement_3d(self):
        """Get if cell instance is 3D placed in the owning layout.

        Returns
        -------
        bool
        """
        return self.__stub.GetIs3DPlacement(self.msg).value

    @placement_3d.setter
    def placement_3d(self, value):
        """Set the cell instance as 3D placed in the owning layout.

        Parameters
        ----------
        value : bool
        """
        self.__stub.Set3DPlacement(messages.bool_property_message(self, value))

    @property
    def transform3d(self):
        """Get the 3D transformation of this cell instance inside the owning layout.

        Returns
        -------
        Transform3D
        """
        t3d_message = self.__stub.Get3DTransform(self.msg)
        return Transform3D(
            [t3d_message.anchor.x, t3d_message.anchor.y, t3d_message.anchor.z],
            [t3d_message.rotAxisFrom.x, t3d_message.rotAxisFrom.y, t3d_message.rotAxisFrom.z],
            [t3d_message.rotAxisTo.x, t3d_message.rotAxisTo.y, t3d_message.rotAxisTo.z],
            t3d_message.rotAngle,
            [t3d_message.offset.x, t3d_message.offset.y, t3d_message.offset.z],
        )

    @transform3d.setter
    def transform3d(self, value):
        """Set the 3D transformation for this cell instance. The cell instance must be 3D placed.

        Parameters
        ----------
        value : Transform3D
        """
        self.__stub.Set3DTransform(messages.transform3d_property_message(self, value))

    def get_parameter_override(self, value):
        """Get value of the queried parameter.

        Parameters
        ----------
        value : str

        Returns
        -------
        Value
            value of the queried parameter
        """
        return Value(
            self.__stub.GetParameterOverride(messages.string_property_message(self, value))
        )

    def set_parameter_override(self, param_name, param_value):
        """Set override value for the given parameter.

        Parameters
        ----------
        param_name : str
        param_value : value
        """
        self.__stub.SetParameterOverride(
            messages.cell_instance_parameter_override_message(self, param_name, param_value)
        )
