"""Simulation Setup."""

from enum import Enum

import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2
import ansys.api.edb.v1.simulation_setup_pb2 as simulation_setup_pb2

from ansys.edb import simulation_setup
from ansys.edb.core import ObjBase, messages
from ansys.edb.session import get_simulation_setup_stub


class SimulationSetupType(Enum):
    """Enum representing available simulation setup types.

    - HFSS
    """

    HFSS = edb_defs_pb2.HFSS


class _QueryBuilder:
    @staticmethod
    def create(cell, name: str, sim_type: SimulationSetupType):
        return simulation_setup_pb2.SimulationSetupCreationMessage(
            cell=cell.msg, simulation_setup_name=name, simulation_setup_type=sim_type.value
        )

    @staticmethod
    def get_simulation_setup_info(sim_setup: "SimulationSetup"):
        return sim_setup.msg

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
    """Simulation Setup."""

    @staticmethod
    def create(cell, name, sim_type):
        """Create a simulation setup.

        Parameters
        ----------
        cell : :class:`Cell <ansys.edb.layout.Cell>`
            Cell to be simulated.
        name : str
            Name of this simulation setup.
        sim_type : SimulationSetupType
            Type of this simulation setup.

        Returns
        -------
        SimulationSetup
            Newly created simulation setup.
        """
        return SimulationSetup(
            get_simulation_setup_stub().Create(_QueryBuilder.create(cell, name, sim_type))
        )

    @property
    def simulation_setup_info(self):
        """:obj:`SimulationSetupInfo` : Get simulation setup info.

        Read-Only.
        """
        return simulation_setup.SimulationSetupInfo(
            get_simulation_setup_stub().GetSimulationSetupInfo(
                _QueryBuilder.get_simulation_setup_info(self)
            )
        )

    def adaptive_frequency(self, frequency, max_delta_s, max_pass):
        """Add an adaptive frequency to this simulation setup.

        Parameters
        ----------
        frequency : str
            Frequency where adaptive calculations are performed.
        max_delta_s : str
            Adaptive calculations are repeated until the S-parameters change by less than this amount.
        max_pass : int
            Adaptive calculations are stopped after this number of passes even if max_delta_s isn't attained.
        """
        return (
            get_simulation_setup_stub()
            .AddAdaptiveFrequencies(
                _QueryBuilder.add_adaptive_frequencies(self, [(frequency, max_delta_s, max_pass)])
            )
            .value
        )

    def mesh_operation(self, name, net_layers, num_layers):
        """Add a mesh operation to this simulation setup.

        Parameters
        ----------
        name : str, optional
            Name of the operation.
        net_layers : list[tuple(str, str, bool)], optional
            Each entry has net name, layer name, and isSheet which is True if it is a sheet object.
        num_layers : int
            Number of entries in net_layers
        """
        return (
            get_simulation_setup_stub()
            .AddMeshOperations(
                _QueryBuilder.add_mesh_operations(
                    self, [{"name": name, "net_layers": net_layers, "num_layers": str(num_layers)}]
                )
            )
            .value
        )

    def frequency_sweep(self, name, distribution, start_f, end_f, step, fast_sweep):
        r"""Add a frequency sweep to this simulation setup.

        Parameters
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
        fast_sweep : bool
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
        return (
            get_simulation_setup_stub()
            .AddFrequencySweeps(
                _QueryBuilder.add_frequency_sweeps(
                    self, [(name, distribution, start_f, end_f, step, fast_sweep)]
                )
            )
            .value
        )
