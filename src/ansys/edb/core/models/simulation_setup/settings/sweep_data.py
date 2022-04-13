from ansys.api.edb.v1.simulation_setup_info_pb2 import SweepDataMessage


class SweepData:
    def __init__(
        self,
        name: str,
        distribution: str,
        start_f: str,
        end_f: str,
        step: str,
        fast_sweep: bool = False,
    ):
        self.name = name
        self.frequency_string = distribution + " " + start_f + " " + end_f + " " + step
        self.fast_sweep = fast_sweep

    @staticmethod
    def _create(msg: SweepDataMessage) -> "SweepData":
        return SweepData(msg.name, msg.frequency_string, msg.fast_sweep)
