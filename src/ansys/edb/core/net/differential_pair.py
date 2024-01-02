"""Differential pair."""

from ansys.edb.core.inner.layout_obj import LayoutObjType
from ansys.edb.core.inner.messages import (
    differential_pair_creation_message,
    differential_pair_net_refs_message,
    string_property_message,
)
from ansys.edb.core.net.net import Net
from ansys.edb.core.net.net_class import NetClass
from ansys.edb.core.session import DifferentialPairServiceStub, StubAccessor, StubType


class DifferentialPair(NetClass):
    """Differential pair class."""

    __stub: DifferentialPairServiceStub = StubAccessor(StubType.differential_pair)
    layout_obj_type = LayoutObjType.DIFFERENTIAL_PAIR

    @classmethod
    def create(cls, layout, name, pos_net=None, neg_net=None):
        """Create a differential pair.

        User must either provide both nets or omit both nets

        Parameters
        ----------
        layout : :class:`Layout<ansys.edb.core.layout.Layout>`
            Layout on which new differential pair is placed.
        name : str
            Name of new differential pair.
        pos_net : Net or str, optional
            Positive net or name of positive net.
        neg_net : Net or str, optional
            Negative net or name of negative net.

        Returns
        -------
        DifferentialPair
            Newly created differential pair.
        """
        return cls(
            cls.__stub.Create(differential_pair_creation_message(layout, name, pos_net, neg_net))
        )

    @classmethod
    def find_by_name(cls, layout, name):
        """Find a differential pair in a layout by name.

        Parameters
        ----------
        layout : :class:`Layout<ansys.edb.core.layout.Layout>`
            Layout being searched for differential pair
        name : str
            Name of the differential pair to find

        Returns
        -------
        DifferentialPair
            The differential pair that was found. Check the returned differential pair's \
            :obj:`is_null <ansys.edb.core.net.DifferentialPair.is_null>` property to see if it exists.
        """
        return cls(cls.__stub.FindByName(string_property_message(layout, name)))

    @property
    def differential_pair(self):
        r""":obj:`tuple`\(:class:`Net`, :class:`Net`\): The nets (positive, negative) in the differential pair."""
        msg = self.__stub.GetDifferentialPair(self.msg)
        return Net(msg.positive_net.id), Net(msg.negative_net.id)

    @differential_pair.setter
    def differential_pair(self, value):
        self.__stub.SetDifferentialPair(
            differential_pair_net_refs_message(self, value[0], value[1])
        )

    @property
    def positive_net(self):
        """:class:`Net`: The positive net of a differential pair."""
        return self.differential_pair[0]

    @positive_net.setter
    def positive_net(self, value):
        self.__stub.SetDifferentialPair(
            differential_pair_net_refs_message(self, value, self.differential_pair[1])
        )

    @property
    def negative_net(self):
        """:class:`Net`: The negative net of a differential pair."""
        return self.differential_pair[1]

    @negative_net.setter
    def negative_net(self, value):
        self.__stub.SetDifferentialPair(
            differential_pair_net_refs_message(self, self.differential_pair[0], value)
        )

    @property
    def is_power_ground(self):
        """Invalid for differential pair."""
        return False

    def add_net(self, net):
        """Invalid for differential pair.

        Use :obj:`ansys.edb.core.net.DifferentialPair.differential_pair` = (pos_net, neg_net) instead.
        """
        raise TypeError("net cannot be added to differential pair.")

    def remove_net(self, net):
        """Invalid for differential pair."""
        raise TypeError("net cannot be removed from differential pair.")

    @property
    def nets(self):
        """Invalid for differential pair.

        Use :obj:`ansys.edb.core.net.DifferentialPair.differential_pair` instead.
        """
        return self.differential_pair
