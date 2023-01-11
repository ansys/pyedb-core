"""Pin Pair Model."""

from ansys.edb.core import messages, parser
from ansys.edb.hierarchy.model import Model
from ansys.edb.session import PinPairModelServiceStub, StubAccessor, StubType


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
        return cls(cls.__stub.Create())

    def rlc(self, pin_pair):
        """Get RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]

        Returns
        -------
        :class:`Rlc<ansys.edb.utility.Rlc>`
        """
        res = self.__stub.GetRlc(messages.string_pair_property_message(pin_pair))
        if res.found:
            return parser.to_rlc(res.rlc)
        else:
            return None

    def set_rlc(self, pin_pair, rlc):
        """Set RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]
        rlc : :class:`Rlc<ansys.edb.utility.Rlc>`
        """
        self.__stub.SetRlc(messages.pin_pair_model_rlc_message(pin_pair, rlc))

    def delete_rlc(self, pin_pair):
        """Delete RLC value for a pin pair.

        Parameters
        ----------
        pin_pair : tuple[str, str]
        """
        self.__stub.DeleteRlc(messages.string_pair_property_message(pin_pair))

    def pin_pairs(self):
        """Get all pin pairs.

        Returns
        -------
        list[tuple[str, str]]
        """
        res = self.__stub.GetPinPairs(messages.edb_obj_message(self))
        return [(pair.first, pair.second) for pair in res.pairs]
