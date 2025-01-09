# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
