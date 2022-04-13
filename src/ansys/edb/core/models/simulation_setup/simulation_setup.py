from enum import Enum
from typing import List, Tuple

import ansys.api.edb.v1.simulation_setup_pb2 as simulation_setup_pb2
from ansys.edb.cell.cell import Cell
from ansys.edb.session import get_simulation_setup_stub
from ansys.edb.simulation_setup.settings.simulation_setup_info import SimulationSetupInfo
from ansys.edb.utility.edb_errors import handle_grpc_exception
from ansys.edb.utility.obj_base import ObjBase

import ansys.edb.core.communications.grpc.messages as messages


class SimulationSetupType(Enum):
    HFSS = simulation_setup_pb2.HFSS


class _QueryBuilder:
    @staticmethod
    def create(cell: Cell, name: str, sim_type: SimulationSetupType):
        return simulation_setup_pb2.SimulationSetupCreationMessage(
            cell=cell._msg, simulation_setup_name=name, simulation_setup_type=sim_type.value
        )

    @staticmethod
    def get_simulation_setup_info(sim_setup: "SimulationSetup"):
        return sim_setup._msg

    @staticmethod
    def add_adaptive_frequencies(setup, frequencies):
        return simulation_setup_pb2.AdaptiveFrequenciesSetMessage(
            setup=messages.edb_obj_message(setup),
            frequencies=[messages.adaptive_frequency_message(*f) for f in frequencies],
        )

    @staticmethod
    def add_mesh_operations(setup, mesh_ops):
        return simulation_setup_pb2.MeshOperationsSetMessage(
            setup=messages.edb_obj_message(setup),
            mesh_operations=[messages.mesh_operation_message(**m) for m in mesh_ops],
        )

    @staticmethod
    def add_frequency_sweeps(setup, sweeps):
        return simulation_setup_pb2.FrequencySweepsSetMessage(
            setup=messages.edb_obj_message(setup),
            sweeps=[messages.frequency_sweep_message(*s) for s in sweeps],
        )


class SimulationSetup(ObjBase):
    @staticmethod
    @handle_grpc_exception
    def create(cell: Cell, name: str, sim_type: SimulationSetupType) -> "SimulationSetup":
        return SimulationSetup(
            get_simulation_setup_stub().Create(_QueryBuilder.create(cell, name, sim_type))
        )

    @property
    @handle_grpc_exception
    def simulation_setup_info(self) -> SimulationSetupInfo:
        return SimulationSetupInfo(
            get_simulation_setup_stub().GetSimulationSetupInfo(
                _QueryBuilder.get_simulation_setup_info(self)
            )
        )

    @handle_grpc_exception
    def adaptive_frequency(self, frequency: str, max_delta_s: float, max_pass: int):
        return (
            get_simulation_setup_stub()
            .AddAdaptiveFrequencies(
                _QueryBuilder.add_adaptive_frequencies(self, [(frequency, max_delta_s, max_pass)])
            )
            .value
        )

    @handle_grpc_exception
    def mesh_operation(self, name: str, net_layers: List[Tuple[str, str, bool]], num_layers: int):
        return (
            get_simulation_setup_stub()
            .AddMeshOperations(
                _QueryBuilder.add_mesh_operations(
                    self, [{"name": name, "net_layers": net_layers, "num_layers": str(num_layers)}]
                )
            )
            .value
        )

    def frequency_sweep(
        self, name: str, distribution: str, start_f: str, end_f: str, step: str, fast_sweep: bool
    ):
        return (
            get_simulation_setup_stub()
            .AddFrequencySweeps(
                _QueryBuilder.add_frequency_sweeps(
                    self, [(name, distribution, start_f, end_f, step, fast_sweep)]
                )
            )
            .value
        )
