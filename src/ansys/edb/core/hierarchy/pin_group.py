"""Pin group."""

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import messages
from ansys.edb.core.inner.conn_obj import ConnObj
from ansys.edb.core.primitive.primitive import PadstackInstance
from ansys.edb.core.session import StubAccessor, StubType


class PinGroup(ConnObj):
    """Represents a pin group object."""

    __stub = StubAccessor(StubType.pin_group)
    layout_obj_type = LayoutObjType.PIN_GROUP

    @classmethod
    def create(cls, layout, name, padstack_instances):
        """Create a pin group.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the pin group in.
        name : str
            Name of the pin group.
        padstack_instances : list[:class:`.PadstackInstance`]
            List of padstack instances.

        Returns
        -------
        PinGroup
            Pin group created.
        """
        return PinGroup(
            cls.__stub.Create(messages.pin_group_creation_message(layout, name, padstack_instances))
        )

    @classmethod
    def find(cls, layout, name):
        """Find a pin group by name in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the pin group.
        name : str
            Name of the pin group.

        Returns
        -------
        PinGroup
            Pin group found, ``None`` otherwise.
        """
        return PinGroup(cls.__stub.FindByName(messages.pin_group_lookup_message(layout, name)))

    @classmethod
    def unique_name(cls, layout, prefix):
        """Get a unique pin group name in the layout using a given prefix.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the pin group.
        prefix : str
            Prefix of the unique name.

        Returns
        -------
        str
            Name of the pin group found.
        """
        return cls.__stub.GetUniqueName(
            messages.pin_group_get_unique_name_message(layout, prefix)
        ).value

    @property
    def name(self):
        """:obj:`str`: Name of the pin group.

        This property is read-only.
        """
        return self.__stub.GetName(self.msg).value

    @property
    def pins(self):
        """:obj:`list` of :class:`PadstackInstances <.PadstackInstance>`: \
        Padstack instances.

        This property is read-only.
        """
        ps = self.__stub.GetPins(self.msg).items
        return [PadstackInstance(p) for p in ps]

    def add_pins(self, pins):
        """Add a list of padstack instances to the group.

        Parameters
        ----------
        pins : list[:class:`.PadstackInstance`]
            List of padstick instances.
        """
        self.__stub.AddPins(messages.pin_group_pins_modify_message(self, pins))

    def remove_pins(self, pins):
        """Remove a list of padstack instances from the group.

        Parameters
        ----------
        pins : list[:class:`.PadstackInstance`]
            List of padstick instances.
        """
        self.__stub.RemovePins(messages.pin_group_pins_modify_message(self, pins))
