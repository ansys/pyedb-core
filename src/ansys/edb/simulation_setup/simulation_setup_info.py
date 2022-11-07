"""Simulation Setup Info."""

from ansys.api.edb.v1.simulation_setup_info_pb2 import (
    SetSweepDataListMessage,
    SweepDataListMessage,
    SweepDataMessage,
)

from ansys.edb import simulation_setup
from ansys.edb.core import ObjBase
from ansys.edb.session import get_simulation_setup_info_stub


class _QueryBuilder:
    @staticmethod
    def get_simulation_settings(sim_setup_info):
        return sim_setup_info.msg

    @staticmethod
    def get_sweep_data_list(sim_setup_info):
        return sim_setup_info.msg

    @staticmethod
    def set_sweep_data_list(sim_setup_info, sweep_data_list):
        new_sweep_data_list_msgs = [
            SweepDataMessage(
                name=data.name, frequency_string=data.frequency_string, fast_sweep=data.fast_sweep
            )
            for data in sweep_data_list
        ]
        new_sweep_data_list_msg = SweepDataListMessage(sweep_data=new_sweep_data_list_msgs)
        return SetSweepDataListMessage(
            simulation_setup_info=sim_setup_info.msg, sweep_data_list=new_sweep_data_list_msg
        )


class SimulationSetupInfo(ObjBase):
    """Class representing a simulation setup info."""

    @property
    def simulation_settings(self):
        """:obj:`HFSSSimulationSettings` : Simulation settings.

        Read-Only.
        """
        # TODO: Add support for sim types other than HFSS
        return simulation_setup.HFSSSimulationSettings(
            get_simulation_setup_info_stub().GetSimulationSettings(
                _QueryBuilder.get_simulation_settings(self)
            )
        )

    @property
    def sweep_data_list(self):
        r""":obj:`list`\[:class:`SweepData`\] : Sweep data list."""
        sweep_data_list_msg = get_simulation_setup_info_stub().GetSweepDataList(
            _QueryBuilder.get_sweep_data_list(self)
        )
        return [
            simulation_setup.SweepData._create(sweep_data_msg)
            for sweep_data_msg in sweep_data_list_msg.sweep_data
        ]

    @sweep_data_list.setter
    def sweep_data_list(self, sweep_data_list):
        get_simulation_setup_info_stub().SetSweepDataList(
            _QueryBuilder.set_sweep_data_list(self, sweep_data_list)
        )
