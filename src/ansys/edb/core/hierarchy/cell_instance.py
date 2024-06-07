"""Cell instance."""

from ansys.api.edb.v1.cell_instance_pb2_grpc import CellInstanceServiceStub

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.hierarchy import hierarchy_obj
from ansys.edb.core.inner import messages
from ansys.edb.core.layout import layout
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.transform3d import Transform3D
from ansys.edb.core.utility.value import Value


class CellInstance(hierarchy_obj.HierarchyObj):
    """Represents a cell instance object."""

    __stub: CellInstanceServiceStub = StubAccessor(StubType.cell_instance)
    layout_obj_type = LayoutObjType.CELL_INSTANCE

    @classmethod
    def create(cls, layout, name, ref):
        """Create a cell instance with a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the cell instance in.
        name : str
            Name of the cell instance.
        ref : :class:`.Layout`
            Layout that the cell instance refers to.

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
        """Create a cell instance with a component definition.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the cell instance in.
        name : str
            Name of the cell instance.
        ref : :class:`.ComponentDef`
            Component that the cell instance refers to.

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
        """Find a cell instance by name in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the cell instance.
        name : str
            Name of the cell instance.

        Returns
        -------
        CellInstance
            Cell instance that is found, ``None`` otherwise.
        """
        return CellInstance(
            cls.__stub.FindByName(messages.object_name_in_layout_message(layout, name))
        )

    @property
    def reference_layout(self):
        """:class:`.Layout`: Reference layout of the cell instance.

        This property is read-only.
        """
        return layout.Layout(self.__stub.GetReferenceLayout(self.msg))

    @property
    def term_instances(self):
        """:obj:`list` of :class:`.TerminalInstance`: Terminal \
        instances associated with the cell instance.

        This property is read-only.
        """
        from ansys.edb.core.terminal.terminals import TerminalInstance

        terms = self.__stub.GetTermInsts(self.msg).items
        return [TerminalInstance(ti) for ti in terms]

    @property
    def placement_3d(self):
        """:obj:`bool`: Flag indicating if the cell instance is 3D placed in the owning layout.

        If ``True``, transformation can be set using the :obj:`transform3d` object.
        """
        return self.__stub.GetIs3DPlacement(self.msg).value

    @placement_3d.setter
    def placement_3d(self, value):
        """Set the cell instance as 3D placed in the owning layout."""
        self.__stub.Set3DPlacement(messages.bool_property_message(self, value))

    @property
    def transform3d(self):
        """:class:`.Transform3D`: \
        3D transformation information of the cell instance.

        For the transformation to be applied, the :obj:`placement_3d` property
        must be set to ``True``.
        """
        return Transform3D(self.__stub.Get3DTransform(self.msg))

    @transform3d.setter
    def transform3d(self, value):
        """Set the 3D transformation for the cell instance.

        The cell instance must be 3D placed.
        """
        self.__stub.Set3DTransform(messages.pointer_property_message(self, value))

    def get_parameter_override(self, param_name):
        """Get the override of the cell instance parameter by name.

        Parameters
        ----------
        param_name : str
            Name of the cell instance parameter.

        Returns
        -------
        :class:`.Value`
            Override value for the cell instance parameter.
        """
        return Value(
            self.__stub.GetParameterOverride(messages.string_property_message(self, param_name))
        )

    def set_parameter_override(self, param_name, param_value):
        """Set an override value for a given cell instance parameter.

        Parameters
        ----------
        param_name : str
            Name of the cell instance parameter.
        param_value : :class:`.Value`
            Value to override with.
        """
        self.__stub.SetParameterOverride(
            messages.cell_instance_parameter_override_message(self, param_name, param_value)
        )
