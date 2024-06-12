"""Differential pair."""

from ansys.edb.core.inner import messages
from ansys.edb.core.inner.layout_obj import LayoutObjType
from ansys.edb.core.net.net import Net
from ansys.edb.core.net.net_class import NetClass
from ansys.edb.core.session import DifferentialPairServiceStub, StubAccessor, StubType


class DifferentialPair(NetClass):
    """Represents a differential pair."""

    __stub: DifferentialPairServiceStub = StubAccessor(StubType.differential_pair)
    layout_obj_type = LayoutObjType.DIFFERENTIAL_PAIR

    @classmethod
    def create(cls, layout, name, pos_net=None, neg_net=None):
        """Create a differential pair.

        You must either provide both nets or omit both nets.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the differential pair in.
        name : str
            Name of the new differential pair.
        pos_net : Net or str, default: None
            Positive net or name of the positive net.
        neg_net : Net or str, default: None
            Negative net or the name of negative net.

        Returns
        -------
        DifferentialPair
            Differential pair created.
        """
        return cls(
            cls.__stub.Create(
                messages.differential_pair_creation_message(layout, name, pos_net, neg_net)
            )
        )

    @classmethod
    def find_by_name(cls, layout, name):
        """Find a differential pair by name in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the differential pair.
        name : str
            Name of the differential pair.

        Returns
        -------
        DifferentialPair
            Differential pair that was found. Check the :obj:`is_null
            <.DifferentialPair.is_null>`
            property of the returned differential pair to see if it exists.
        """
        return cls(cls.__stub.FindByName(messages.string_property_message(layout, name)))

    @property
    def differential_pair(self):
        r""":obj:`tuple`\(:class:`.Net`, :class:`.Net`\): Nets (positive, negative) in the differential pair."""
        msg = self.__stub.GetDifferentialPair(self.msg)
        return Net(msg.positive_net.id), Net(msg.negative_net.id)

    @differential_pair.setter
    def differential_pair(self, value):
        self.__stub.SetDifferentialPair(
            messages.differential_pair_net_refs_message(self, value[0], value[1])
        )

    @property
    def positive_net(self):
        """:class:`.Net`: Positive net in the differential pair."""
        return self.differential_pair[0]

    @positive_net.setter
    def positive_net(self, value):
        self.__stub.SetDifferentialPair(
            messages.differential_pair_net_refs_message(self, value, self.differential_pair[1])
        )

    @property
    def negative_net(self):
        """:class:`.Net`: Negative net in the differential pair."""
        return self.differential_pair[1]

    @negative_net.setter
    def negative_net(self, value):
        self.__stub.SetDifferentialPair(
            messages.differential_pair_net_refs_message(self, self.differential_pair[0], value)
        )

    @property
    def is_power_ground(self):
        """Flag indicating if the new is power/ground.

        This property is invalid for a differential pair.
        """
        return False

    def add_net(self, net):
        """Add a net.

        This method is invalid for a differential pair. Use
        :obj:`ansys.edb.core.net.differential_pair.DifferentialPair` = (pos_net, neg_net) instead.
        """
        raise TypeError("Net cannot be added to a differential pair.")

    def remove_net(self, net):
        """Remove a net.

        This method is invalid for a differential pair.
        """
        raise TypeError("Net cannot be removed from a differential pair.")

    @property
    def nets(self):
        """This property is invalid for a differential pair.

        Use :obj:`ansys.edb.core.net.differential_pair.DifferentialPair` instead.
        """
        return self.differential_pair
