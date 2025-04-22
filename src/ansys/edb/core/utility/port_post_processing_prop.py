"""Port postprocessing properties."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike

from ansys.edb.core.utility.value import Value


class PortPostProcessingProp:
    """Represents the port postprocessing properties."""

    def __init__(
        self,
        voltage_magnitude: ValueLike = 0,
        voltage_phase: ValueLike = 0,
        deembed_length: ValueLike = 0,
        renormalization_impedance: ValueLike = 50,
        do_deembed: bool = False,
        do_deembed_gap_l: bool = False,
        do_renormalize: bool = False,
    ):
        """Initialize port postprocessing properties.

        Parameters
        ----------
        voltage_magnitude : :term:`ValueLike`, optional
            Excitation voltage magnitude. The default is 0.
        voltage_phase : :term:`ValueLike`, optional
            Excitation voltage phase.  The default is 0.
        deembed_length : :term:`ValueLike`, optional
            Dembeed distance.  The default is 0. This parameter is only
            applied if ``do_deembed=True``.
        renormalization_impedance : :term:`ValueLike`, optional
            Renormalization impedance. The default is 0. This parameter is only
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
    def voltage_magnitude(self) -> Value:
        """:class:`.Value`: Excitation voltage magnitude.

        This property can be set to :term:`ValueLike`.
        """
        return self._voltage_magnitude

    @voltage_magnitude.setter
    def voltage_magnitude(self, value: ValueLike):
        self._voltage_magnitude = Value(value)

    @property
    def voltage_phase(self):
        """:class:`.Value`: Excitation voltage phase.

        This property can be set to :term:`ValueLike`.
        """
        return self._voltage_phase

    @voltage_phase.setter
    def voltage_phase(self, value: ValueLike):
        self._voltage_phase = Value(value)

    @property
    def deembed_length(self):
        """:class:`.Value`: Deembed length.

        This property can be set to :term:`ValueLike`.
        This property is only applied if ``do_deembed=True``.
        """
        return self._deembed_length

    @deembed_length.setter
    def deembed_length(self, value: ValueLike):
        self._deembed_length = Value(value)

    @property
    def renormalization_impedance(self):
        """:class:`.Value`: Renormalization impedance.

        This property can be set to :term:`ValueLike`.
        This property is only applied if ``do_renormalize=True``.
        """
        return self._renormalization_impedance

    @renormalization_impedance.setter
    def renormalization_impedance(self, value):
        self._renormalization_impedance = Value(value)
