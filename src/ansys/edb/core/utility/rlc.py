"""RLC."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike

from ansys.edb.core.utility.value import Value


class Rlc:
    """Represents an RLC.

    Attributes
    ----------
    r : :term:`ValueLike`, default: 0
        Resistance value. This parameter is only used if
        ``r_enabled=True``.
    r_enabled : bool, default: ``False``
        Whether resistance is enabled.
    l : :term:`ValueLike`, default: 0
        Inductance value. This parameter is only used if
        ``c-l_enabled=True``.
    l_enabled : bool, default: ``False``
        Whether inductance is enabled.
    c : :term:`ValueLike`, default: 0
        Capacitance value. This parameter is only used if
        ``c_enabled=True``.
    c_enabled : bool, default: ``False``
        Whether capacitance is enabled.
    is_parallel : bool, default: ``True``
        Whether the r, l, and c elements are in parallel. If ``False``, these
        elements are in series.
    """

    def __init__(
        self,
        r: ValueLike = Value(0),
        r_enabled: bool = False,
        l: ValueLike = Value(0),
        l_enabled: bool = False,
        c: ValueLike = Value(0),
        c_enabled: bool = False,
        is_parallel: bool = True,
    ):
        """Initialize an RLC object using given values.

        Parameters
        ----------
        r : :term:`ValueLike`, default: 0
            Resistance value. This parameter is only used if ``r_enabled=True``.
        r_enabled : bool, default: ``False``
            Whether resistance is enabled.
        l : :term:`ValueLike`, default: 0
            Inductance value. This parameter is only used if ``c-l_enabled=True``.
        l_enabled : bool, default: ``False``
            Whether inductance is enabled.
        c : :term:`ValueLike`, default: 0
            Capacitance value. This parameter is only used if ``c_enabled=True``.
        c_enabled : bool, default: ``False``
            Whether capacitance is enabled.
        is_parallel : bool, default: ``True``
            Whether the r, l, and c elements are in parallel. If ``False``, these
            elements are in series.
        """
        self.r = r
        self.l = l
        self.c = c
        self.r_enabled = r_enabled
        self.l_enabled = l_enabled
        self.c_enabled = c_enabled
        self.is_parallel = is_parallel


class PinPair:
    """Represents a pin pair.

    Attributes
    ----------
    pin1: str
        Name of the first pin.
    pin2: str
        Name of the second pin.
    """

    def __init__(self, pin1, pin2):
        """Initialize a pin pair object.

        Parameters
        ----------
        pin1: str
            Name of the first pin.
        pin2: str
            Name of the second pin.
        """
        self.pin1 = pin1
        self.pin2 = pin2


class PinPairRlc:
    """Represents a pin pair RLC.

    Attributes
    ----------
    pin_pair : .PinPair
        Pin pair property.
    rlc : .Rlc
        RLC value.
    """

    def __init__(self, pin_pair, rlc):
        """Initialize a pin pair RLC object.

        Parameters
        ----------
        pin_pair: .PinPair
            Pin pair property.
        rlc: .Rlc
            RLC property.
        """
        self.pin_pair = pin_pair
        self.rlc = rlc
