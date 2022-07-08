"""Adaptive Frequency Data."""


class AdaptiveFrequencyData:
    """Class representing adaptive frequency."""

    def __init__(self, adaptive_frequency="5e9", max_delta="0.02", max_passes=10):
        """Initialize an adaptive frequency.

        Parameters
        ----------
        adaptive_frequency : str, optional
        max_delta : str, optional
        max_passes : int, optional
        """
        self.adaptive_frequency = adaptive_frequency
        self.max_delta = max_delta
        self.max_passes = max_passes

    @staticmethod
    def _create(msg: "AdaptiveFrequencyDataMessage"):
        return AdaptiveFrequencyData(msg.adaptive_frequency, msg.max_delta, msg.max_passes)
