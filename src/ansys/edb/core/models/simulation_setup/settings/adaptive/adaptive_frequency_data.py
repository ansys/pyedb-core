from ansys.api.edb.v1.adaptive_settings_pb2 import AdaptiveFrequencyDataMessage


class AdaptiveFrequencyData:
    def __init__(
        self, adaptive_frequency: str = "5e9", max_delta: str = "0.02", max_passes: int = 10
    ):
        self.adaptive_frequency = adaptive_frequency
        self.max_delta = max_delta
        self.max_passes = max_passes

    @staticmethod
    def _create(msg: AdaptiveFrequencyDataMessage):
        return AdaptiveFrequencyData(msg.adaptive_frequency, msg.max_delta, msg.max_passes)
