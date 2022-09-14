"""RLC."""

from ansys.edb.utility.value import Value


class Rlc:
    """Class representing RLC.

    Attributes
    ----------
    r : str, int, float, complex, Value
        Resistance value. Only used if r_enabled is True
    r_enabled : bool
        Resistance enabled.
    l : str, int, float, complex, Value
        Inductance value. Only used if c-l_enabled is True
    l_enabled : bool
        Inductance enabled.
    c : str, int, float, complex, Value
        Capacitance value.  Only used if c_enabled is True
    c_enabled : bool
        Capacitance enabled.
    is_parallel : bool
        True means r,l,c elements are in parallel. Otherwise they are in series.
    """

    def __init__(
        self,
        r=Value(0),
        r_enabled=False,
        l=Value(0),
        l_enabled=False,
        c=Value(0),
        c_enabled=False,
        is_parallel=False,
    ):
        """Construct a Rlc object using given values.

        Parameters
        ----------
        r : str, int, float, complex, Value, optional
            Resistance value. Only used if r_enabled is True
        r_enabled : bool, optional
            Resistance enabled.
        l : str, int, float, complex, Value, optional
            Inductance value. Only used if c-l_enabled is True
        l_enabled : bool, optional
            Inductance enabled.
        c : str, int, float, complex, Value, optional
            Capacitance value.  Only used if c_enabled is True
        c_enabled : bool, optional
            Capacitance enabled.
        is_parallel : bool, optional
            True means r,l,c elements are in parallel. Otherwise they are in series.
        """
        self.r = Value(r)
        self.l = Value(l)
        self.c = Value(c)
        self.r_enabled = bool(r_enabled)
        self.l_enabled = bool(l_enabled)
        self.c_enabled = bool(c_enabled)
        self.is_parallel = bool(is_parallel)


class PinPair:
    """Class representing PinPair.

    Attributes
    ----------
    pin1: str
        Name of the first pin.
    pin2: str
        Name of the second pin.
    """

    def __init__(self, pin1, pin2):
        """Construct a pin pair object.

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
    """Class representing PinPairRlc.

    Attributes
    ----------
    pin_pair : PinPair
            Pin pair property.
    rlc : Rlc
        Rlc value
    """

    def __init__(self, pin_pair, rlc):
        """Construct a pin pair rlc object.

        Parameters
        ----------
        pin_pair: PinPair
            Pin pair property.
        rlc: Rlc
            Rlc property
        """
        self.pin_pair = pin_pair
        self.rlc = rlc
