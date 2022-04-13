from typing import List

from ansys.api.edb.v1.simulation_setup_info_pb2 import (
    SetSweepDataListMessage,
    SweepDataListMessage,
    SweepDataMessage,
)

from ....session import get_simulation_setup_info_stub
from ....utility.edb_errors import handle_grpc_exception
from ...base import ObjBase
from .hfss_simulation_settings import HFSSSimulationSettings
from .simulation_settings import SimulationSettings
from .sweep_data import SweepData


class _QueryBuilder:
    @staticmethod
    def get_simulation_settings(sim_setup_info: "SimulationSetupInfo"):
        return sim_setup_info._msg

    @staticmethod
    def get_sweep_data_list(sim_setup_info: "SimulationSetupInfo"):
        return sim_setup_info._msg

    @staticmethod
    def set_sweep_data_list(
        sim_setup_info: "SimulationSetupInfo", sweep_data_list: List[SweepData]
    ):
        new_sweep_data_list_msgs = [
            SweepDataMessage(
                name=data.name, frequency_string=data.frequency_string, fast_sweep=data.fast_sweep
            )
            for data in sweep_data_list
        ]
        new_sweep_data_list_msg = SweepDataListMessage(sweep_data=new_sweep_data_list_msgs)
        return SetSweepDataListMessage(
            simulation_setup_info=sim_setup_info._msg, sweep_data_list=new_sweep_data_list_msg
        )


class SimulationSetupInfo(ObjBase):
    @property
    @handle_grpc_exception
    def simulation_settings(self) -> SimulationSettings:
        # TODO: Add support for sim types other than HFSS
        return HFSSSimulationSettings(
            get_simulation_setup_info_stub().GetSimulationSettings(
                _QueryBuilder.get_simulation_settings(self)
            )
        )

    @property
    @handle_grpc_exception
    def sweep_data_list(self) -> List[SweepData]:
        sweep_data_list_msg = get_simulation_setup_info_stub().GetSweepDataList(
            _QueryBuilder.get_sweep_data_list(self)
        )
        return [
            SweepData._create(sweep_data_msg) for sweep_data_msg in sweep_data_list_msg.sweep_data
        ]

    @sweep_data_list.setter
    def sweep_data_list(self, sweep_data_list: List[SweepData]) -> None:
        get_simulation_setup_info_stub().SetSweepDataList(
            _QueryBuilder.set_sweep_data_list(self, sweep_data_list)
        )
