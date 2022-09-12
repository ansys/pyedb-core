"""RLC."""

from ansys.edb.utility.value import Value


class Rlc:
    """Class representing RLC.

    Parameters
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
            self._r = Value(rlc_msg.r) if rlc_msg.r is not None else 0.0
            self._l = Value(rlc_msg.l) if rlc_msg.l is not None else 0.0
            self._c = Value(rlc_msg.c) if rlc_msg.c is not None else 0.0
            self._r_enabled = (
                bool(rlc_msg.r_enabled.value) if rlc_msg.r_enabled is not None else False
            )
            self._l_enabled = (
                bool(rlc_msg.l_enabled.value) if rlc_msg.l_enabled is not None else False
            )
            self._c_enabled = (
                bool(rlc_msg.c_enabled.value) if rlc_msg.c_enabled is not None else False
            )
            self._is_parallel = (
                bool(rlc_msg.is_parallel.value) if rlc_msg.c_enabled is not None else False
            )
        else:
            self._r = kwargs.get("r", 0)
            self._l = kwargs.get("l", 0)
            self._c = kwargs.get("c", 0)
            self._r_enabled = kwargs.get("r_enabled", False)
            self._l_enabled = kwargs.get("l_enabled", False)
            self._c_enabled = kwargs.get("c_enabled", False)
            self._is_parallel = kwargs.get("is_parallel", True)

    @property
    def r(self):
        """Return resistance value.

        Returns
        -------
        Value
            Resistance value in Ohms
        """
        return self._r if self._msg is None else Value(self._msg.r)

    @r.setter
    def r(self, resistance):
        """Set resistance value."""
        self._r = resistance

    @property
    def l(self):
        """Return induction value.

        Returns
        -------
        Value
            Impedance value in Henries.
        """
        return self._l if self._msg is None else Value(self._msg.l)

    @l.setter
    def l(self, induction):
        """Set induction value."""
        self._l = induction

    @property
    def c(self):
        """Return capacitance value.

        Returns
        -------
        Value
            Capacitance value in Farads.
        """
        return self._c if self._msg is None else Value(self._msg.c)

    @c.setter
    def c(self, capacitance):
        """Set capacitance value."""
        self._c = capacitance

    @property
    def r_enabled(self):
        """Return whether resistance is enabled.

        Returns
        -------
        bool
        """
        return self._r_enabled if self._msg is None else self._msg.r_enabled.value

    @r_enabled.setter
    def r_enabled(self, resistance_enabled):
        """Set resistance is enabled or not."""
        self._r_enabled = resistance_enabled

    @property
    def l_enabled(self):
        """Return whether induction is enabled.

        Returns
        -------
        bool
        """
        return self._l_enabled if self._msg is None else self._msg.l_enabled.value

    @l_enabled.setter
    def l_enabled(self, induction_enabled):
        """Set induction is enabled or not."""
        self._l_enabled = induction_enabled

    @property
    def c_enabled(self):
        """Return whether capacitance is enabled.

        Returns
        -------
        bool
        """
        return self._c_enabled if self._msg is None else self._msg.c_enabled.value

    @c_enabled.setter
    def c_enabled(self, capacitance_enabled):
        """Set capacitance is enabled or not."""
        self._c_enabled = capacitance_enabled

    @property
    def is_parallel(self):
        """Return if parallel.

        Returns
        -------
        bool
        """
        return self._is_parallel if self._msg is None else self._msg.is_parallel.value

    @is_parallel.setter
    def is_parallel(self, is_parallel):
        """Set parallel or not."""
        self._is_parallel = is_parallel
