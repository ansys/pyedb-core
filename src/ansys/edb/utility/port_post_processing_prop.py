"""Port Post Processing Prop."""

from ansys.edb.core import ObjBase
from ansys.edb.utility.value import Value


class PortPostProcessingProp(ObjBase):
    """Represents Port Post Processing Prop.

    Parameters
    ----------
    voltage_magnitude : str, int, float, complex, Value
        Excitation voltage magnitude.
    voltage_phase : str, int, float, complex, Value
        Excitation voltage phase.
    deembed_length : str, int, float, complex, Value
        Dembeed distance. Only applied if do_deembed is True.
    renormalization_impedance : str, int, float, complex, Value
        Renormalization impedance. Only applied if do_renormalize is True.
    do_deembed : bool
        Enable port to be deembedded.
    do_renormalize : bool
        Enable port impedance renormalization.
    do_deembed_gap_l : bool
        Enable the gap port inductance to be deembedded.
    """

    def __init__(self, **kwargs):
        """Construct a PortPostProcessingProp object using given values."""
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
        Excitation voltage magnitude.

        Returns
        -------
        Value
        """
        return self._voltage_magnitude if self._msg is None else Value(self._msg.voltage_magnitude)

    @property
    def voltage_phase(self):
        """
        Excitation voltage phase.

        Returns
        -------
        Value
        """
        return self._voltage_phase if self._msg is None else Value(self._msg.voltage_phase)

    @property
    def deembed_length(self):
        """
        Deembed Length. Only applied if do_deembed is True.

        Returns
        -------
        Value
        """
        return self._deembed_length if self._msg is None else Value(self._msg.deembed_length)

    @property
    def renormalization_impedance(self):
        """
        Renormalization Impedance. Only applied if do_renormalize is True.

        Returns
        -------
        Value
        """
        return (
            self._renormalization_impedance
            if self._msg is None
            else Value(self._msg.renormalization_impedance)
        )

    @property
    def do_deembed(self):
        """
        Enable port to be deembedded.

        Returns
        -------
        bool
        """
        return self._do_deembed if self._msg is None else self._msg.do_deembed

    @property
    def do_deembed_gap_l(self):
        """
        Enable the gap port inductance to be deembedded.

        Returns
        -------
        bool
        """
        return self._do_deembed_gap_l if self._msg is None else self._msg.do_deembed_gap_length

    @property
    def do_renormalize(self):
        """
        Enable port impedance renormalization.

        Returns
        -------
        bool
        """
        return self._do_renormalize if self._msg is None else self._msg.do_renormalize
