"""Port postprocessing properties."""

from ansys.edb.core.utility.value import Value


class PortPostProcessingProp:
    """Represents the port postprocessing properties."""

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
        """Initialize port postprocessing properties.

        Parameters
        ----------
        voltage_magnitude : str or int or float or complex or Value, optional
            Excitation voltage magnitude. The default is ``0``.
        voltage_phase : str or int or float or complex or Value, optional
            Excitation voltage phase.  The default is ``0``.
        deembed_length : str or int or float or complex or Value, optional
            Dembeed distance.  The default is ``0``. This parameter is only
            applied if ``do_deembed=True``.
        renormalization_impedance : str or int or float or complex or Value, optional
            Renormalization impedance. The default is ``0``. This parameter is only
            applied if ``do_renormalize=True``.
        do_deembed : bool, optional
            Whether to enable the port to be deembedded. The default is ``False``.
        do_deembed_gap_l : bool, optional
            Whether to enable port impedance renormalization. The default is ``False``.
        do_renormalize : bool, optional
            Whether to enable the gap port inductance to be deembedded.  The default
            is ``False``.
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
            ``True`` when successful, ``False`` when failed.
        """
        self.do_deembed_gap_l = do_deembed_gap_l
        """Enable port impedance renormalization.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        self.do_renormalize = do_renormalize
        """Enable port impedance renormalization.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """

    @property
    def voltage_magnitude(self):
        """Excitation voltage magnitude."""
        return self._voltage_magnitude

    @voltage_magnitude.setter
    def voltage_magnitude(self, value):
        self._voltage_magnitude = Value(value)

    @property
    def voltage_phase(self):
        """Excitation voltage phase."""
        return self._voltage_phase

    @voltage_phase.setter
    def voltage_phase(self, value):
        self._voltage_phase = Value(value)

    @property
    def deembed_length(self):
        """
        Deembed length.

        This property is only applied if ``do_deembed=True``.
        """
        return self._deembed_length

    @deembed_length.setter
    def deembed_length(self, value):
        self._deembed_length = Value(value)

    @property
    def renormalization_impedance(self):
        """
        Renormalization impedance.

        This property is only applied if ``do_renormalize=True``.
        """
        return self._renormalization_impedance

    @renormalization_impedance.setter
    def renormalization_impedance(self, value):
        self._renormalization_impedance = Value(value)
