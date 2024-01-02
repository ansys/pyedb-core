"""Cell Instance."""

from ansys.api.edb.v1.cell_instance_pb2_grpc import CellInstanceServiceStub

from ansys.edb.core import layout
from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.hierarchy.hierarchy_obj import HierarchyObj
from ansys.edb.core.inner.messages import (
    bool_property_message,
    cell_instance_creation_message,
    cell_instance_parameter_override_message,
    object_name_in_layout_message,
    pointer_property_message,
    string_property_message,
)
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.transform3d import Transform3D
from ansys.edb.core.utility.value import Value


class CellInstance(HierarchyObj):
    """Class representing a cell instance object."""

    __stub: CellInstanceServiceStub = StubAccessor(StubType.cell_instance)
    layout_obj_type = LayoutObjType.CELL_INSTANCE

    @classmethod
    def create(cls, layout, name, ref):
        """Create a cell instance object with a layout.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout that owns the cell instance.
        name : str
            Name of cell instance to be created.
        ref : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout that the cell instance refers to.

        Returns
        -------
        CellInstance
            Newly created cell instance.
        """
        return CellInstance(cls.__stub.Create(cell_instance_creation_message(layout, name, ref)))

    @classmethod
    def create_with_component(cls, layout, name, ref):
        """Create a cell instance object with a component definition.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout that owns the cell instance.
        name : str
            Name of the cell instance to be created.
        ref : :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>`
            The component this cell instance refers to.

        Returns
        -------
        CellInstance
            Newly created cell instance.
        """
        return CellInstance(
            cls.__stub.CreateWithComponent(cell_instance_creation_message(layout, name, ref))
        )

    @classmethod
    def find(cls, layout, name):
        """Find a cell instance in layout by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.core.layout.Layout>`
            Layout to search the cell instance in.
        name : str
            Name of the cell instance to be searched.

        Returns
        -------
        CellInstance
            Cell instance that is found, None otherwise.
        """
        return CellInstance(cls.__stub.FindByName(object_name_in_layout_message(layout, name)))

    @property
    def reference_layout(self):
        """:class:`Layout <ansys.edb.core.layout.Layout>`: Reference layout of the cell instance.

        Read-Only.
        """
        return layout.Layout(self.__stub.GetReferenceLayout(self.msg))

    @property
    def term_instances(self):
        """:obj:`list` of :class:`TerminalInstances <ansys.edb.core.terminal.TerminalInstances>`: List of terminal \
        instances associated with this cell instance.

        Read-Only.
        """
        from ansys.edb.core.terminal.terminals import TerminalInstance

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
        self.__stub.Set3DPlacement(bool_property_message(self, value))

    @property
    def transform3d(self):
        """:class:`Transform3D <ansys.edb.core.utility.Transform3D>`: \
        3D transformation information of this cell instance.

        :obj:`placement_3d` must be True for the transformation to be applied.
        """
        return Transform3D(self.__stub.Get3DTransform(self.msg))

    @transform3d.setter
    def transform3d(self, value):
        """Set the 3D transformation for this cell instance. The cell instance must be 3D placed."""
        self.__stub.Set3DTransform(pointer_property_message(self, value))

    def get_parameter_override(self, param_name):
        """Get the override of the cell instance parameter by name.

        Parameters
        ----------
        param_name : str
            Name of the parameter to override.

        Returns
        -------
        :class:`Value <ansys.edb.core.utility.Value>`
            Override value for the parameter.
        """
        return Value(self.__stub.GetParameterOverride(string_property_message(self, param_name)))

    def set_parameter_override(self, param_name, param_value):
        """Set override value for the given cell instance parameter.

        Parameters
        ----------
        param_name : str
            Name of the parameter to override.
        param_value : :class:`Value <ansys.edb.core.utility.Value>`
            Value to override with.
        """
        self.__stub.SetParameterOverride(
            cell_instance_parameter_override_message(self, param_name, param_value)
        )
