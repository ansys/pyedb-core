"""Pin Pair Model."""

import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    pin_pair_model_rlc_message,
    string_pair_property_message,
)
from ansys.edb.core.inner.parser import to_rlc
from ansys.edb.core.session import PinPairModelServiceStub, StubAccessor, StubType


class PinPairModel(Model):
    """Class representing a Pin Pair model object."""

    __stub: PinPairModelServiceStub = StubAccessor(StubType.pin_pair_model)

    @classmethod
    def create(cls):
        """Create a new pin pair model.

        Returns
        -------
        PinPairModel
        """
        return cls(cls.__stub.Create(empty_pb2.Empty()))

    def rlc(self, pin_pair):
        """Get RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]

        Returns
        -------
        :class:`Rlc<ansys.edb.core.utility.Rlc>`
        """
        res = self.__stub.GetRlc(string_pair_property_message(self, pin_pair))
        if res.found:
            return to_rlc(res.rlc)
        else:
            return None

    def set_rlc(self, pin_pair, rlc):
        """Set RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]
        rlc : :class:`Rlc<ansys.edb.core.utility.Rlc>`
        """
        self.__stub.SetRlc(pin_pair_model_rlc_message(self, pin_pair, rlc))

    def delete_rlc(self, pin_pair):
        """Delete RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]
        """
        self.__stub.DeleteRlc(string_pair_property_message(self, pin_pair))

    def pin_pairs(self):
        """Get all pin pairs.

        Returns
        -------
        list[tuple[str, str]]
        """
        res = self.__stub.GetPinPairs(edb_obj_message(self))
        return [(pair.first, pair.second) for pair in res.pairs]
