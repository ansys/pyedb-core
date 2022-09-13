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

    def __init__(self, **kwargs):
        """Construct a Rlc object using given values."""
        if "msg" in kwargs:
            rlc_msg = kwargs["msg"]
            self.r = Value(rlc_msg.r)
            self.l = Value(rlc_msg.l)
            self.c = Value(rlc_msg.c)
            self.r_enabled = bool(rlc_msg.r_enabled.value)
            self.l_enabled = bool(rlc_msg.l_enabled.value)
            self.c_enabled = bool(rlc_msg.c_enabled.value)
            self.is_parallel = bool(rlc_msg.is_parallel.value)
        else:
            self.r = kwargs.get("r", 0)
            self.l = kwargs.get("l", 0)
            self.c = kwargs.get("c", 0)
            self.r_enabled = kwargs.get("r_enabled", False)
            self.l_enabled = kwargs.get("l_enabled", False)
            self.c_enabled = kwargs.get("c_enabled", False)
            self.is_parallel = kwargs.get("is_parallel", True)


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
