"""Pin Group."""

from ansys.edb.core.core import LayoutObjType, ObjBase, messages
from ansys.edb.core.primitive import PadstackInstance
from ansys.edb.core.session import StubAccessor, StubType


class PinGroup(ObjBase):
    """Class representing a pin group."""

    __stub = StubAccessor(StubType.pin_group)
    layout_type = LayoutObjType.PIN_GROUP

    @classmethod
    def create(cls, layout, name, padstack_instances):
        """Create a pin group.

        Parameters
        ----------
        layout : Layout
        name : str
        padstack_instances : list of PadstackInstance

        Returns
        -------
        PinGroup
        """
        return PinGroup(
            cls.__stub.Create(messages.pin_group_creation_message(layout, name, padstack_instances))
        )

    @classmethod
    def find(cls, layout, name):
        """Find a pin group by name.

        Parameters
        ----------
        layout : Layout
        name : str

        Returns
        -------
        PinGroup
        """
        return PinGroup(cls.__stub.FindByName(messages.pin_group_lookup_message(layout, name)))

    @classmethod
    def unique_name(cls, layout, prefix):
        """Return a unique pin group name in the layout.

        Parameters
        ----------
        layout : Layout
        prefix : str

        Returns
        -------
        str
        """
        return cls.__stub.GetUniqueName(
            messages.pin_group_get_unique_name_message(layout, prefix)
        ).value

    @property
    def name(self):
        """Get the name.

        Returns
        -------
        str
        """
        return self.__stub.GetName(self.msg).value

    @property
    def pins(self):
        """Get the list of padstack instances.

        Returns
        -------
        list of PadstackInstance
        """
        ps = self.__stub.GetPins(self.msg).items
        return [PadstackInstance(p) for p in ps]

    def add_pins(self, pins):
        """Add the list of padstack instances to the group.

        Parameters
        ----------
        pins : list of PadstackInstance
        """
        self.__stub.AddPins(messages.pin_group_pins_modify_message(self, pins))

    def remove_pins(self, pins):
        """Remove the list of padstack instances from the group.

        Parameters
        ----------
        pins : list of PadstackInstance
        """
        self.__stub.RemovePins(messages.pin_group_pins_modify_message(self, pins))
