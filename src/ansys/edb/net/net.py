"""Net."""

from ansys.edb.core import layout_obj, messages
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.net.extended_net import ExtendedNet
from ansys.edb.net.net_class import NetClass
from ansys.edb.primitive import PadstackInstance, Primitive
from ansys.edb.session import NetServiceStub, StubAccessor, StubType
from ansys.edb.terminal import Terminal, TerminalInstance


class Net(layout_obj.LayoutObj):
    """Class representing net."""

    layout_obj_type = LayoutObjType.NET_CLASS
    no_net_name = "<NO-NET>"
    __stub: NetServiceStub = StubAccessor(StubType.net)

    def _layout_objs(self, obj_type):
        """Get layout objects on a net."""
        return self.__stub.GetLayoutObjects(messages.net_get_layout_obj_message(self, obj_type))

    @classmethod
    def create(cls, layout, name):
        """Create a net.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
        name : str

        Returns
        -------
        Net
        """
        return Net(cls.__stub.Create(messages.string_property_message(layout, name)))

    @classmethod
    def find_by_name(cls, layout, name):
        """Find a net in a layout by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
        name : str

        Returns
        -------
        Net
        """
        return Net(cls.__stub.FindByName(messages.string_property_message(layout, name)))

    @property
    def name(self):
        """Get name of a net.

        Returns
        -------
        str
        """
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        """Set name of a net."""
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def is_power_ground(self):
        """Get whether a net is grounded.

        Returns
        -------
        bool
        """
        return self.__stub.GetIsPowerGround(self.msg).value

    @is_power_ground.setter
    def is_power_ground(self, value):
        """Set if a net is grounded."""
        self.__stub.SetIsPowerGround(messages.bool_property_message(self, value))

    @property
    def primitives(self):
        """Get a list of primitives on a net.

        Returns
        -------
        list[:class:`Primitive <ansys.edb.primitive.Primitive>`]
        """
        return [Primitive(lo).cast() for lo in self._layout_objs(LayoutObjType.PRIMITIVE)]

    @property
    def padstack_instances(self):
        """Get a list of padstack instances on a net.

        Returns
        -------
        list[:class:`PadstackInstance <ansys.edb.primitive.PadstackInstance>`]
        """
        return [PadstackInstance(lo) for lo in self._layout_objs(LayoutObjType.PADSTACK_INSTANCE)]

    @property
    def terminals(self):
        """Get a list of terminals on a net.

        Returns
        -------
        list[:class:`Terminal <ansys.edb.terminal.Terminal>`]
        """
        return [Terminal(lo).cast() for lo in self._layout_objs(LayoutObjType.TERMINAL)]

    @property
    def terminal_instances(self):
        """Get a list of terminal instances on a net.

        Returns
        -------
        list[:class:`TerminalInstance <ansys.edb.terminal.TerminalInstance>`]
        """
        return [TerminalInstance(lo) for lo in self._layout_objs(LayoutObjType.TERMINAL_INSTANCE)]

    @property
    def net_classes(self):
        """Get a list of net classes on a net.

        Returns
        -------
        list[:class:`NetClass <ansys.edb.net.NetClass>`]
        """
        return [NetClass(lo) for lo in self._layout_objs(LayoutObjType.NET_CLASS)]

    @property
    def extended_net(self):
        """Get an extended net.

        Returns
        -------
        :class:`ExtendedNet <ansys.edb.net.ExtendedNet>`
        """
        en = ExtendedNet(self._layout_objs(LayoutObjType.NET_CLASS)[0])
        return None if en.is_null else en
