"""Net."""

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import layout_obj, messages
from ansys.edb.core.net.extended_net import ExtendedNet
from ansys.edb.core.net.net_class import NetClass
from ansys.edb.core.primitive.primitive import PadstackInstance, Primitive
from ansys.edb.core.session import NetServiceStub, StubAccessor, StubType
from ansys.edb.core.terminal.terminals import Terminal, TerminalInstance


class Net(layout_obj.LayoutObj):
    """Represents a net."""

    layout_obj_type = LayoutObjType.NET
    no_net_name = "<NO-NET>"
    __stub: NetServiceStub = StubAccessor(StubType.net)

    def _layout_objs(self, obj_type):
        """Get layout objects on a net."""
        return self.__stub.GetLayoutObjects(
            messages.net_get_layout_obj_message(self, obj_type)
        ).items

    @classmethod
    def create(cls, layout, name):
        """Create a net.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the net in.
        name : str
            Name of the net.

        Returns
        -------
        Net
            Net created.
        """
        return Net(cls.__stub.Create(messages.string_property_message(layout, name)))

    @classmethod
    def find_by_name(cls, layout, name):
        """Find a net by name in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the net.
        name : str
            Name of net.

        Returns
        -------
        Net
            Net found. Check the :obj:`is_null <.Net.is_null>` property
            of the returned net to see if it exists.
        """
        return Net(cls.__stub.FindByName(messages.string_property_message(layout, name)))

    @property
    def name(self):
        """:class:`str`: Name of the net."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def is_power_ground(self):
        """:class:`bool`: Flag indicating if the net belongs to a power/ground :class:`.NetClass` instance.

        This property is read-only.
        """
        return self.__stub.GetIsPowerGround(self.msg).value

    @is_power_ground.setter
    def is_power_ground(self, value):
        self.__stub.SetIsPowerGround(messages.bool_property_message(self, value))

    @property
    def primitives(self):
        r""":obj:`list` of :class:`.Primitive`: All primitives on the net.

        This property is read-only.
        """
        return [Primitive(lo).cast() for lo in self._layout_objs(LayoutObjType.PRIMITIVE)]

    @property
    def padstack_instances(self):
        """:obj:`list` of :class:`.PadstackInstance`: All padstack instances on the net \
        object instance."""
        return [PadstackInstance(lo) for lo in self._layout_objs(LayoutObjType.PADSTACK_INSTANCE)]

    @property
    def terminals(self):
        """:obj:`list` of :class:`.Terminal`: All terminal instances on the \
            net object instance."""
        return [Terminal(lo).cast() for lo in self._layout_objs(LayoutObjType.TERMINAL)]

    @property
    def terminal_instances(self):
        """:obj:`list` of :class:`.Layer`: All terminal instances on the net object instance."""
        return [TerminalInstance(lo) for lo in self._layout_objs(LayoutObjType.TERMINAL_INSTANCE)]

    @property
    def net_classes(self):
        r""":obj:`list` of :class:`.NetClass`: All net classes on the net.

        This property is read-only.
        """
        return [NetClass(lo) for lo in self._layout_objs(LayoutObjType.NET_CLASS)]

    @property
    def extended_net(self):
        """:class:`.ExtendedNet` or :class:`None`: Extended net that the net belongs to.

        :class:`None` means that the net does not belong to an extended net.

        This property is read-only.
        """
        en = ExtendedNet(self._layout_objs(LayoutObjType.NET_CLASS)[0])
        return None if en.is_null else en
