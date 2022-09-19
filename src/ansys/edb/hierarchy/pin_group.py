"""Pin Group."""

from ansys.edb.core import ObjBase, messages
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.primitive import PadstackInstance
from ansys.edb.session import StubAccessor, StubType


class PinGroup(ObjBase):
    """Class representing a pin group object."""

    __stub = StubAccessor(StubType.pin_group)
    layout_obj_type = LayoutObjType.PIN_GROUP

    @classmethod
    def create(cls, layout, name, padstack_instances):
        """Create a pin group.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the pin group.
        name : str
            Name of pin group to be created.
        padstack_instances : list[:class:`PadstackInstance <ansys.edb.primitive.PadstackInstance>`]

        Returns
        -------
        PinGroup
            Newly created pin group.
        """
        return PinGroup(
            cls.__stub.Create(messages.pin_group_creation_message(layout, name, padstack_instances))
        )

    @classmethod
    def find(cls, layout, name):
        """Find a pin group by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout to search the pin group in.
        name : str
            Name of the pin group.

        Returns
        -------
        PinGroup
            Pin group that is found, None otherwise.
        """
        return PinGroup(cls.__stub.FindByName(messages.pin_group_lookup_message(layout, name)))

    @classmethod
    def unique_name(cls, layout, prefix):
        """Return a unique pin group name in the layout using the given prefix.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout to search the pin group in.
        prefix : str
            Prefix of the unique name.

        Returns
        -------
        str
        """
        return cls.__stub.GetUniqueName(
            messages.pin_group_get_unique_name_message(layout, prefix)
        ).value

    @property
    def name(self):
        """:obj:`str`: Name of the object.

        Read-Only.
        """
        return self.__stub.GetName(self.msg).value

    @property
    def pins(self):
        """:obj:`list` of :class:`PadstackInstances <ansys.edb.primitive.PadstackInstance>`: List of padstack instances.

        Read-Only.
        """
        ps = self.__stub.GetPins(self.msg).items
        return [PadstackInstance(p) for p in ps]

    def add_pins(self, pins):
        """Add the list of padstack instances to the group.

        Parameters
        ----------
        pins : list[:class:`PadstackInstance <ansys.edb.primitive.PadstackInstance>`]
        """
        self.__stub.AddPins(messages.pin_group_pins_modify_message(self, pins))

    def remove_pins(self, pins):
        """Remove the list of padstack instances from the group.

        Parameters
        ----------
        pins : list[:class:`PadstackInstance <ansys.edb.primitive.PadstackInstance>`]
        """
        self.__stub.RemovePins(messages.pin_group_pins_modify_message(self, pins))
