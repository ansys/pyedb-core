"""Component definition."""
from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.ansys.edb.core.database import ProductIdType

from ansys.api.edb.v1.component_def_pb2_grpc import ComponentDefServiceStub

from ansys.edb.core.definition import component_model, component_pin
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.inner.messages import (
    edb_obj_collection_property_message,
    edb_obj_pair_message,
    get_product_property_ids_message,
    get_product_property_message,
    set_product_property_message,
)
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
        return map_list(objs, lambda msg: component_model.ComponentModel(msg).cast())

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
        self.__stub.AddComponentModel(messages.edb_obj_pair_message(self, value))

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

    def reorder_pins(self, reordered_pins: List[component_pin.ComponentPin]):
        """Reorders the existing pins in the components definition to be in the same order \
        as in the provided list.

        Parameters
        ----------
        reordered_pins : list of .ComponentPin
            The component pins in the new order. These must be the same pins \
            that already exist in the component definition.
        """
        self.__stub.ReorderPins(edb_obj_collection_property_message(self, reordered_pins))

    def remove_pin(self, pin_to_remove: component_pin.ComponentPin):
        """Remove the provided component pin from the component definition. \
        the pin will be deleted and set to :meth:`null <.is_null>`.

        Parameters
        ----------
        pin_to_remove : .ComponentPin
            The pin to be removed.
        """
        self.__stub.RemovePin(edb_obj_pair_message(self, pin_to_remove))
        pin_to_remove.msg = None

    def get_product_property(self, prod_id: ProductIdType, attr_it: int) -> str:
        """Get the product property for a given product ID and attribute ID.

        Parameters
        ----------
        prod_id : .ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.

        Returns
        -------
        str
            Product property for the given product ID and attribute ID.
        """
        return self.__stub.GetProductProperty(
            get_product_property_message(self, prod_id, attr_it)
        ).value

    def set_product_property(self, prod_id: ProductIdType, attr_it: int, prop_value: str):
        """Set the product property for the given product ID and attribute ID.

        Parameters
        ----------
        prod_id : .ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.
        prop_value : str
            New value for the product property.
        """
        self.__stub.SetProductProperty(
            set_product_property_message(self, prod_id, attr_it, prop_value)
        )

    def get_product_property_ids(self, prod_id: ProductIdType) -> List[int]:
        """Get the list of property IDs for a given property ID.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.

        Returns
        -------
        list[int]
            Attribute IDs for the given product ID.
        """
        attr_ids = self.__stub.GetProductPropertyIds(
            get_product_property_ids_message(self, prod_id)
        ).ids
        return [attr_id for attr_id in attr_ids]
