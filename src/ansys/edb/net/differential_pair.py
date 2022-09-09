"""Differential pair."""

from ansys.edb.core import messages
from ansys.edb.core.layout_obj import LayoutObjType
from ansys.edb.net.net import Net
from ansys.edb.net.net_class import NetClass
from ansys.edb.session import DifferentialPairServiceStub, StubAccessor, StubType


class DifferentialPair(NetClass):
    """Differential pair class."""

    __stub: DifferentialPairServiceStub = StubAccessor(StubType.differential_pair)
    layout_obj_type = LayoutObjType.DIFFERENTIAL_PAIR

    @classmethod
    def create(cls, layout, name, pos_net=None, neg_net=None):
        """Create a differential pair.

        Parameters
        ----------
        layout : :class:`Layout<ansys.edb.layout.Layout>`
            Layout on which differential pair is placed.
        name : str
            Name of differential pair.
        pos_net : :class:`Net<ansys.edb.net.Net>` or str, optional
            Positive net. must be provided with negative net if non-None.
        neg_net : :class:`Net<ansys.edb.net.Net>` or str, optional
            Negative net. must be provided with positive net if non-None.

        Returns
        -------
        DifferentialPair
        """
        return cls(
            cls.__stub.Create(
                messages.differential_pair_creation_message(layout, name, pos_net, neg_net)
            )
        )

    @classmethod
    def find(cls, layout, name):
        """Find a differential pair by name.

        Parameters
        ----------
        layout : :class:`Layout<ansys.edb.layout.Layout>`
        name : str

        Returns
        -------
        DifferentialPair
        """
        return cls(cls.__stub.FindByName(messages.string_property_message(layout, name)))

    @property
    def differential_pair(self):
        """Get the differential pair.

        Returns
        -------
        tuple(Net, Net)
        """
        msg = self.__stub.GetDifferentialPair(self.msg)
        return Net(msg.positive_net.id), Net(msg.negative_net.id)

    @differential_pair.setter
    def differential_pair(self, value):
        """Set the differential pair (positive net, negative net)."""
        self.__stub.SetDifferentialPair(
            messages.differential_pair_net_refs_message(self, value[0], value[1])
        )

    @property
    def positive_net(self):
        """Get the positive net of a differential pair.

        Returns
        -------
        Net
        """
        return self.differential_pair[0]

    @property
    def negative_net(self):
        """Get the negative net of a differential pair.

        Returns
        -------
        Net
        """
        return self.differential_pair[1]

    @property
    def is_power_ground(self):
        """Get if the differential pair is grounded.

        Returns
        -------
        bool
        """
        return False

    def add_net(self, net):
        """Add a net. this method is invalid for DifferentialPair.

        Use differential_pair = (pos_net, neg_net) instead.

        Parameters
        ----------
        net : Net
        """
        raise TypeError("net cannot be added to differential pair.")

    def remove_net(self, net):
        """Remove a net. this method is invalid for DifferentialPair.

        Use .differential_pair = (pos_net, neg_net) instead.

        Parameters
        ----------
        net : Net
        """
        raise TypeError("net cannot be removed from differential pair.")

    def nets(self):
        """Get the list of nets. this method is invalid for DifferentialPair.

        Use .differential_pair instead.
        """
        raise TypeError("differential pairs do not have nets.")
