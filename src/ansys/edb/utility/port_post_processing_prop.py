"""Port Post Processing Prop."""

from ansys.edb.core import ObjBase
from ansys.edb.utility.value import Value


class PortPostProcessingProp(ObjBase):
    """Class representing Port Post Processing Prop."""

    def __init__(self, **kwargs):
        """Construct a port post processing prop from message."""
        if "msg" in kwargs:
            self._msg = kwargs.get("msg")
        else:
            self._msg = None
            self._voltage_magnitude = kwargs.get("voltage_magnitude", 0)
            self._voltage_phase = kwargs.get("voltage_phase", 0)
            self._deembed_length = kwargs.get("deembed_length", 0)
            self._renormalization_impedance = kwargs.get("renormalization_impedance", 50)
            self._do_deembed = kwargs.get("do_deembed", False)
            self._do_deembed_gap_l = kwargs.get("do_deembed_gap_l", False)
            self._do_renormalize = kwargs.get("do_renormalize", False)

    @property
    def voltage_magnitude(self):
        """
        Voltage magnitude.

        Returns
        -------
        float
        """
        return self._voltage_magnitude if self._msg is None else Value(self._msg.voltage_magnitude)

    @property
    def voltage_phase(self):
        """
        Voltage phase.

        Returns
        -------
        float
        """
        return self._voltage_phase if self._msg is None else Value(self._msg.voltage_phase)

    @property
    def deembed_length(self):
        """
        Deembed Length.

        Returns
        -------
        float
        """
        return self._deembed_length if self._msg is None else Value(self._msg.deembed_length)

    @property
    def renormalization_impedance(self):
        """
        Renormalization Impedance.

        Returns
        -------
        float
        """
        return (
            self._renormalization_impedance
            if self._msg is None
            else Value(self._msg.renormalization_impedance)
        )

    @property
    def do_deembed(self):
        """
        Whether to deembed or not.

        Returns
        -------
        bool
        """
        return self._do_deembed if self._msg is None else self._msg.do_deembed

    @property
    def do_deembed_gap_l(self):
        """
        Whether to deembed gap length or not.

        Returns
        -------
        bool
        """
        return self._do_deembed_gap_l if self._msg is None else self._msg.do_deembed_gap_length

    @property
    def do_renormalize(self):
        """
        Whether to renormalize or not.

        Returns
        -------
        bool
        """
        return self._do_renormalize if self._msg is None else self._msg.do_renormalize
