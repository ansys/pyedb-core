"""Component Def Definition."""
from ansys.api.edb.v1.component_def_pb2_grpc import ComponentDefServiceStub

from ansys.edb.core import ObjBase, messages
from ansys.edb.core.utils import map_list
from ansys.edb.definition import component_model, component_pin
from ansys.edb.layout import cell
from ansys.edb.session import StubAccessor, StubType


class ComponentDef(ObjBase):
    """Class representing a Component Definition."""

    __stub: ComponentDefServiceStub = StubAccessor(StubType.component_def)

    @classmethod
    def create(cls, db, comp_def_name, fp):
        """Create a component definition.

        Parameters
        ----------
        db : :class:`Database <ansys.edb.database.Database>`
            Database that the component definition should belong to.
        comp_def_name : str
            Name of the component definition to be created.
        fp : :class:`Cell <ansys.edb.layout.Cell>`
            Footprint cell of the component definition.

        Returns
        -------
        ComponentDef
            Newly created component definition.
        """
        return ComponentDef(
            cls.__stub.Create(messages.component_def_creation_message(db, comp_def_name, fp))
        )

    @classmethod
    def find(cls, db, comp_def_name):
        """Find a component definition in a database.

        Parameters
        ----------
        db : :class:`Database <ansys.edb.database.Database>`
            Database to search the component definition in.
        comp_def_name : str
            Name of the component definition to be searched.

        Returns
        -------
        ComponentDef
            Component definition that was found, None otherwise.
        """
        return ComponentDef(
            cls.__stub.FindByName(messages.object_name_in_layout_message(db, comp_def_name))
        )

    @property
    def name(self):
        """:obj:`str`: Name of the component definition."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def footprint(self):
        """:class:`Cell <ansys.edb.layout.Cell>`: Footprint of the component definition."""
        return cell.Cell(self.__stub.GetFootprintCell(self.msg))

    @footprint.setter
    def footprint(self, value):
        self.__stub.SetFootprintCell(messages.edb_obj_pair_message(self, value))

    @property
    def component_models(self):
        """:obj:`list` of :class:`ComponentModel <ansys.edb.definition.component_model.ComponentModel>`: \
        List of component models associated with this component definition.

        Read-Only.
        """
        objs = self.__stub.GetComponentModels(self.msg).items
        return map_list(objs, component_model.ComponentModel)

    @property
    def component_pins(self):
        """:obj:`list` of :class:`ComponentPin <ansys.edb.definition.ComponentPin>`: \
        List of component pins of this component definition.

        Read-Only.
        """
        objs = self.__stub.GetComponentPins(self.msg).items
        return map_list(objs, component_pin.ComponentPin)
