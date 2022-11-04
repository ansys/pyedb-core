"""Adaptive Frequency Data."""


class AdaptiveFrequencyData:
    """Class representing adaptive frequency.

    Parameters
    ----------
    adaptive_frequency : str, optional
        Frequency where adaptive calculations are performed.
    max_delta : str, optional
        Adaptive calculations are repeated until the S-parameters change by less than this amount.
    max_passes : int, optional
        Adaptive calculations are stopped after this number of passes even if max_delta isn't attained.
    """

    def __init__(self, adaptive_frequency="5e9", max_delta="0.02", max_passes=10):
        """__init__ for AdaptiveFrequencyData."""
        self.adaptive_frequency = adaptive_frequency
        self.max_delta = max_delta
        self.max_passes = max_passes

    @staticmethod
    def _create(msg: "AdaptiveFrequencyDataMessage"):
        return AdaptiveFrequencyData(msg.adaptive_frequency, msg.max_delta, msg.max_passes)
