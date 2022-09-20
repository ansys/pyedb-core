"""Cell Instance."""

from ansys.api.edb.v1.cell_instance_pb2_grpc import CellInstanceServiceStub

from ansys.edb import layout
from ansys.edb.core import messages
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.hierarchy import hierarchy_obj
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Transform3D, Value


class CellInstance(hierarchy_obj.HierarchyObj):
    """Class representing a cell instance object."""

    __stub: CellInstanceServiceStub = StubAccessor(StubType.cell_instance)
    layout_obj_type = LayoutObjType.CELL_INSTANCE

    @classmethod
    def create(cls, layout, name, ref):
        """Create a cell instance object with a layout.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the cell instance.
        name : str
            Name of cell instance to be created.
        ref : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that the cell instance refers to.

        Returns
        -------
        CellInstance
            Newly created cell instance.
        """
        return CellInstance(
            cls.__stub.Create(messages.cell_instance_creation_message(layout, name, ref))
        )

    @classmethod
    def create_with_component(cls, layout, name, ref):
        """Create a cell instance object with a component definition.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the cell instance.
        name : str
            Name of the cell instance to be created.
        ref : :class:`ComponentDef <ansys.edb.definition.ComponentDef>`
            The component this cell instance refers to.

        Returns
        -------
        CellInstance
            Newly created cell instance.
        """
        return CellInstance(
            cls.__stub.CreateWithComponent(
                messages.cell_instance_creation_message(layout, name, ref)
            )
        )

    @classmethod
    def find(cls, layout, name):
        """Find a cell instance in layout by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout to search the cell instance in.
        name : str
            Name of the cell instance to be searched.

        Returns
        -------
        CellInstance
            Cell instance that is found, None otherwise.
        """
        return CellInstance(
            cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name))
        )

    @property
    def reference_layout(self):
        """:class:`Layout <ansys.edb.layout.Layout>`: Reference layout of the cell instance.

        Read-Only.
        """
        return layout.Layout(self.__stub.GetReferenceLayout(self.msg))

    @property
    def term_instances(self):
        """:obj:`list` of :class:`TerminalInstances <ansys.edb.terminal.TerminalInstances>`: List of terminal \
        instances associated with this cell instance.

        Read-Only.
        """
        from ansys.edb.terminal import TerminalInstance

        terms = self.__stub.GetTermInsts(self.msg).items
        return [TerminalInstance(ti) for ti in terms]

    @property
    def placement_3d(self):
        """:obj:`bool`: Determine if this cell instance is 3D placed in the owning layout.

        If True, transformation can be set using :obj:`transform3d`.
        """
        return self.__stub.GetIs3DPlacement(self.msg).value

    @placement_3d.setter
    def placement_3d(self, value):
        """Set the cell instance as 3D placed in the owning layout."""
        self.__stub.Set3DPlacement(messages.bool_property_message(self, value))

    @property
    def transform3d(self):
        """:class:`Transform3D <ansys.edb.utility.Transform3D>`: 3D transformation information of this cell instance.

        :obj:`placement_3d` must be True for the transformation to be applied.
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
        """Set the 3D transformation for this cell instance. The cell instance must be 3D placed."""
        self.__stub.Set3DTransform(messages.transform3d_property_message(self, value))

    def get_parameter_override(self, param_name):
        """Get the override of the cell instance parameter by name.

        Parameters
        ----------
        param_name : str
            Name of the parameter to override.

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
            Override value for the parameter.
        """
        return Value(
            self.__stub.GetParameterOverride(messages.string_property_message(self, param_name))
        )

    def set_parameter_override(self, param_name, param_value):
        """Set override value for the given cell instance parameter.

        Parameters
        ----------
        param_name : str
            Name of the parameter to override.
        param_value : :class:`Value <ansys.edb.utility.Value>`
            Value to override with.
        """
        self.__stub.SetParameterOverride(
            messages.cell_instance_parameter_override_message(self, param_name, param_value)
        )
