"""Port Post Processing Prop."""

from ansys.edb.utility.value import Value


class PortPostProcessingProp:
    """Represents Port Post Processing Prop."""

    def __init__(
        self,
        voltage_magnitude=0,
        voltage_phase=0,
        deembed_length=0,
        renormalization_impedance=50,
        do_deembed=False,
        do_deembed_gap_l=False,
        do_renormalize=False,
    ):
        """Initialize post processing properties.

        Parameters
        ----------
        voltage_magnitude : str, int, float, complex, Value, optional
            Excitation voltage magnitude.
        voltage_phase : str, int, float, complex, Value, optional
            Excitation voltage phase.
        deembed_length : str, int, float, complex, Value, optional
            Dembeed distance. Only applied if do_deembed is True.
        renormalization_impedance : str, int, float, complex, Value, optional
            Renormalization impedance. Only applied if do_renormalize is True.
        do_deembed : bool, optional
            Enable port to be deembedded.
        do_deembed_gap_l : bool, optional
            Enable port impedance renormalization.
        do_renormalize : bool, optional
            Enable the gap port inductance to be deembedded.
        """
        self.voltage_magnitude = voltage_magnitude
        self.voltage_phase = voltage_phase
        self.deembed_length = deembed_length
        self.renormalization_impedance = renormalization_impedance
        self.do_deembed = do_deembed
        """Enable port to be deembedded.

        Returns
        -------
        bool
        """
        self.do_deembed_gap_l = do_deembed_gap_l
        """Enable port impedance renormalization.

        Returns
        -------
        bool
        """
        self.do_renormalize = do_renormalize
        """Enable port impedance renormalization.

        Returns
        -------
        bool
        """

    @property
    def voltage_magnitude(self):
        """
        Excitation voltage magnitude.

        Returns
        -------
        Value
        """
        return self._voltage_magnitude

    @voltage_magnitude.setter
    def voltage_magnitude(self, value):
        """Set excitation voltage magnitude."""
        self._voltage_magnitude = Value(value)

    @property
    def voltage_phase(self):
        """
        Excitation voltage phase.

        Returns
        -------
        Value
        """
        return self._voltage_phase

    @voltage_phase.setter
    def voltage_phase(self, value):
        """Set excitation voltage phase."""
        self._voltage_phase = Value(value)

    @property
    def deembed_length(self):
        """
        Deembed Length. Only applied if do_deembed is True.

        Returns
        -------
        Value
        """
        return self._deembed_length

    @deembed_length.setter
    def deembed_length(self, value):
        """Set deembed length."""
        self._deembed_length = Value(value)

    @property
    def renormalization_impedance(self):
        """
        Renormalization Impedance. Only applied if do_renormalize is True.

        Returns
        -------
        Value
        """
        return self._renormalization_impedance

    @renormalization_impedance.setter
    def renormalization_impedance(self, value):
        """Set renormalization impedance."""
        self._renormalization_impedance = Value(value)
