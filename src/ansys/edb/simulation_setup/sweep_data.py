"""Sweep Data."""

from ansys.api.edb.v1.simulation_setup_info_pb2 import SweepDataMessage


class SweepData:
    r"""Class representing a sweep data setting.

    Attributes
    ----------
    name : str
      Name of this sweep.
    distribution : str
      Type of sweep (see table below).
    start_f : str
      Start frequency is number with optional frequency units.
    end_f : str
      End frequency is number with optional frequency units.
    step : str
      Step is either frequency with optional frequency units or an integer when a count is needed.
    fast_sweep : bool, optional
      True if this is a fast sweep.

    Notes
    -----
    Here are the choices for the distribution parameter

    .. list-table:: Values for distribution parameter
       :widths: 20 45 25
       :header-rows: 1

       * - Distribution
         - Description
         - Example
       * - LIN
         - linear (start, stop, step)
         - LIN 2GHz 4GHz 100MHz or LIN 1dBm 10dBm 1dB
       * - LINC
         - linear (start, stop, count)
         - LINC 2GHz 4GHz 11
       * - ESTP
         - Exponential step (start, stop, count)
         - ESTP 2MHz 10MHz 3
       * - DEC
         - decade (start, stop, number of decades)
         - DEC 10KHz 10GHz 6
       * - OCT
         - octave (start, stop, number of octaves)
         - OCT 10MHz 160MHz 5

    """

    def __init__(
        self,
        name,
        distribution,
        start_f,
        end_f,
        step,
        fast_sweep=False,
    ):
        """Initialize a sweep data setting."""
        self.name = name
        self.frequency_string = distribution + " " + start_f + " " + end_f + " " + step
        self.fast_sweep = fast_sweep

    @staticmethod
    def _create(msg: SweepDataMessage):
        return SweepData(msg.name, msg.frequency_string, msg.fast_sweep)
