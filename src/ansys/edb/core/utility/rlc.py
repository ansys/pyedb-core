"""RLC."""

from ansys.edb.core.utility.value import Value


class Rlc:
    """Represents an RLC.

    Attributes
    ----------
    r : str, int, float, complex, Value, default: 0
        Resistance value. This parameter is only used if
        ``r_enabled=True``.
    r_enabled : bool, default: False
        Whether resistance is enabled.
    l : str, int, float, complex, Value, default: 0
        Inductance value. This parameter is only used if
        ``c-l_enabled=True``.
    l_enabled : bool, default: False
        Whether inductance is enabled.
    c : str, int, float, complex, Value, default: 0
        Capacitance value. This parameter is only used if
        ``c_enabled=True``.
    c_enabled : bool, default: False
        Whether capacitance is enabled.
    is_parallel : bool, default: True
        Whether the r, l, and c elements are in parallel. If ``False``, these
        elements are in series.
    """

    def __init__(
        self,
        r=Value(0),
        r_enabled=False,
        l=Value(0),
        l_enabled=False,
        c=Value(0),
        c_enabled=False,
        is_parallel=True,
    ):
        """Initialize an RLC object using given values.

        Parameters
        ----------
        r : str, int, float, complex, Value, default: 0
            Resistance value. This parameter is only used if ``r_enabled=True``.
        r_enabled : bool, default: False
            Whether resistance is enabled.
        l : str, int, float, complex, Value, default: 0
            Inductance value. This parameter is only used if ``c-l_enabled=True``.
        l_enabled : bool, default: False
            Whether inductance is enabled.
        c : str, int, float, complex, Value, default: 0
            Capacitance value. This parameter is only used if ``c_enabled=True``.
        c_enabled : bool, default: False
            Whether capacitance is enabled.
        is_parallel : bool, default: True
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
    pin_pair : PinPair
        Pin pair property.
    rlc : Rlc
        RLC value.
    """

    def __init__(self, pin_pair, rlc):
        """Initialize a pin pair RLC object.

        Parameters
        ----------
        pin_pair: PinPair
            Pin pair property.
        rlc: Rlc
            RLC property.
        """
        self.pin_pair = pin_pair
        self.rlc = rlc
