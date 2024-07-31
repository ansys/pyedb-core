"""Component definition."""
from ansys.api.edb.v1.component_def_pb2_grpc import ComponentDefServiceStub

from ansys.edb.core.definition import component_model, component_pin
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.inner.utils import map_list
from ansys.edb.core.session import StubAccessor, StubType


class ComponentDef(ObjBase):
    """Represents a component definition."""

    __stub: ComponentDefServiceStub = StubAccessor(StubType.component_def)

    @classmethod
    def create(cls, db, comp_def_name, fp):
        """Create a component definition in a given database.

        Parameters
        ----------
        db : :class:`.Database`
            Database to create the component definition in.
        comp_def_name : str
            Name of the component definition to create.
        fp : :class:`.Cell`
            Footprint cell of the component definition, optional

        Returns
        -------
        ComponentDef
            Component definition created.
        """
        return ComponentDef(
            cls.__stub.Create(messages.component_def_creation_message(db, comp_def_name, fp))
        )

    @classmethod
    def find(cls, db, comp_def_name):
        """Find a component definition in a given database.

        Parameters
        ----------
        db : :class:`.Database`
            Database to search for the component definition.
        comp_def_name : str
            Name of the component definition.

        Returns
        -------
        ComponentDef
            Component definition found, ``None`` otherwise.
        """
        return ComponentDef(
            cls.__stub.FindByName(messages.object_name_in_layout_message(db, comp_def_name))
        )

    @property
    def definition_type(self):
        """:class:`DefinitionObjType`: Definition type."""
        return DefinitionObjType.COMPONENT_DEF

    @property
    def name(self):
        """:obj:`str`: Name of the component definition."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def footprint(self):
        """:class:`.Cell`: Footprint of the component definition."""
        from ansys.edb.core.layout import cell

        return cell.Cell(self.__stub.GetFootprintCell(self.msg))

    @footprint.setter
    def footprint(self, value):
        self.__stub.SetFootprintCell(messages.edb_obj_pair_message(self, value))

    @property
    def component_models(self):
        """:obj:`list` of :class:`.ComponentModel`: All component models associated with the component definition.

        This property is read-only.
        """
        objs = self.__stub.GetComponentModels(self.msg).items
        return map_list(objs, component_model.ComponentModel)

    @property
    def component_pins(self):
        """:obj:`list` of :class:`.ComponentPin`: All component pins of the component definition.

        This property is read-only.
        """
        objs = self.__stub.GetComponentPins(self.msg).items
        return map_list(objs, component_pin.ComponentPin)

    def add_component_model(self, value):
        """Add a component model to this component def.

        Parameters
        ----------
        value : :class:`Component Model <ansys.edb.core.definition.ComponentModel>`
            Component Model to be added.

        Notes
        -----
        Once a component model is added to one component def, it cannot be added to any other, even when removed.
        """
        self.__stub.AddComponentModel(messages.pointer_property_message(self, value))

    def remove_component_model(self, value):
        """Remove a component model from this component def.

        Parameters
        ----------
        value : :class:`Component Model <ansys.edb.core.definition.ComponentModel>`
            Component Model to be removed.

        Notes
        -----
        Once a component model is added to one component def, it cannot be added to any other, even when removed.
        """
        self.__stub.RemoveComponentModel(messages.pointer_property_message(self, value))
