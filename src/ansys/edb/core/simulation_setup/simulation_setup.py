"""Simulation Setup."""

from enum import Enum

from ansys.api.edb.v1 import edb_defs_pb2
from ansys.api.edb.v1.simulation_setup_pb2 import (
    HFSSRegionComputeResourceMessage,
    InterpolatingSweepDataMessage,
    SimulationSetupCreationMessage,
    SweepDataListMessage,
    SweepDataListPropertyMessage,
    SweepDataMessage,
)

from ansys.edb.core.inner import messages
from ansys.edb.core.inner.base import ObjBase
from ansys.edb.core.inner.utils import map_list
from ansys.edb.core.session import SimulationSetupServiceStub, StubAccessor, StubType
from ansys.edb.core.simulation_setup.adaptive_solutions import MatrixConvergenceDataEntry


class SimulationSetupType(Enum):
    """Enum representing available simulation setup types."""

    HFSS = edb_defs_pb2.HFSS_SIM
    SI_WAVE = edb_defs_pb2.SI_WAVE_SIM
    SI_WAVE_DCIR = edb_defs_pb2.SI_WAVE_DCIR_SIM
    RAPTOR_X = edb_defs_pb2.RAPTOR_X_SIM


class FreqSweepType(Enum):
    """Enum representing frequency sweep types."""

    INTERPOLATING_SWEEP = edb_defs_pb2.INTERPOLATING_SWEEP
    DISCRETE_SWEEP = edb_defs_pb2.DISCRETE_SWEEP
    BROADBAND_SWEEP = edb_defs_pb2.BROADBAND_SWEEP


class HFSSRegionComputeResource:
    """Class representing HFSS region computation resources.

    Attributes
    ----------
    region_id : int
      HFSS region id
    resource_percentage : float
      Resource percentage to allocate to HFSS region
    """

    def __init__(self, region_id, resource_percentage):
        """Construct a HFSSRegionComputeResource object using given values.

        Parameters
        ----------
        region_id : int
        resource_percentage : float
        """
        self.region_id = region_id
        self.resource_percentage = resource_percentage


class InterpolatingSweepData:
    """Class representing interpolating frequency sweep data.

    Attributes
    ----------
    relative_s_error : float
      S-parameter error tolerance.
    enforce_causality : bool
      Enforce causality.
    enforce_passivity : bool
      Enforce passivity.
    passivity_tolerance : float
      Tolerance for passivity enforcement.
    max_solutions : int
      Max solutions.
    use_s_matrix : bool
      Use S matrix.
    use_port_impedance : bool
      Use port impedance.
    use_prop_const : bool
      Use propagation constants.
    use_full_basis : bool
      Use full basis.
    fast_sweep : bool
      Use fast sweep.
    adaptive_sampling : bool
      Use adaptive sampling.
    enforce_dc_and_causality : bool
      Enforce dc point and causality.
    matrix_conv_entry_list : list[MatrixConvergenceDataEntry]
      Matrix convergence data for frequency sweep.
    min_subranges : int
      Minimum number of subranges.
    min_solutions : int
      Minimum number of solutions.
    """

    def __init__(self):
        """Initialize interpolating sweep data settings."""
        self.relative_s_error = 0.005
        self.enforce_causality = False
        self.enforce_passivity = True
        self.passivity_tolerance = 0.0001
        self.max_solutions = 250
        self.use_s_matrix = True
        self.use_port_impedance = True
        self.use_prop_const = True
        self.use_full_basis = True
        self.fast_sweep = False
        self.adaptive_sampling = False
        self.enforce_dc_and_causality = False
        self.matrix_conv_entry_list = []
        self.min_subranges = 1
        self.min_solutions = 0


class SweepData:
    r"""Class representing a sweep data setting.

    Attributes
    ----------
    name : str
      Name of this sweep.
    distribution : str
      Sweep distribution type (see table below).
    start_f : str
      Start frequency is number with optional frequency units.
    end_f : str
      End frequency is number with optional frequency units.
    step : str
      Step is either frequency with optional frequency units or an integer when a count is needed.
    enabled : bool
      True if this is enabled.
    type : FreqSweepType
      Type of sweep.
    use_q3d_for_dc : bool
      Use Q3D solver for dc calculations.
    save_fields : bool
      Save fields during simulations.
    save_rad_fields_only : bool
      Save only radiation fields during simulations.
    compute_dc_point : bool
      Calculate DC point during simulations.
    siwave_with_3dddm : bool
      SIwave with 3D DDM.
    use_hfss_solver_regions : bool
      SIwave with HFSS solver regions.
    use_hfss_solver_region_sch_gen : bool
      SIwave with HFSS solver regions schematic.
    use_hfss_solver_region_parallel_solve : bool
      SIwave with HFSS solver parallel region simulation.
    use_adp_solution_for_all_sweep_freq : bool
      Enable Using Adaptive Solution for all frequency points.
    num_parallel_hfss_regions : int
      SIwave with HFSS regions: number of regions to solve in parallel.
    parallel_hfss_regions_sim_cfg : list[HFSSRegionComputeResource]
      List of CHFSSRegionComputeResource assignments for parallel region sims.
    auto_s_mat_only_solve : bool
      Auto/Manual SMatrix only solve.
    min_freq_s_mat_only_solve : str
      Minimum frequency SMatrix only solve.
    frequencies : list[str]
      Frequency points in the frequency sweep.
    steady_state_start : float
      Frequency of Steady State Start.
    mesh_freq_choice : int
      Meshing frequencies of the observation mesh.
    mesh_freq_points : list[str]
      Frequency points in meshing frequencies.
    mesh_freq_range_start : str
      Start meshing frequency.
    mesh_freq_range_stop : str
      Stop meshing frequency.
    interpolation_data : InterpolatingSweepData
      Data for interpolating frequency sweeps.

    Notes
    -----
    Here are the choices for the distribution parameter:

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

    def __init__(self, name, distribution, start_f, end_f, step):
        """Initialize a sweep data setting."""
        self.name = name
        self.distribution = distribution
        self.start_f = start_f
        self.end_f = end_f
        self.step = step
        self.enabled = True
        self.type = FreqSweepType.INTERPOLATING_SWEEP
        self.use_q3d_for_dc = False
        self.save_fields = False
        self.save_rad_fields_only = False
        self.compute_dc_point = False
        self.siwave_with_3dddm = False
        self.use_hfss_solver_regions = False
        self.use_hfss_solver_region_sch_gen = False
        self.use_hfss_solver_region_parallel_solve = False
        self.use_adp_solution_for_all_sweep_freq = False
        self.num_parallel_hfss_regions = 1
        self.parallel_hfss_regions_sim_cfg = []
        self.auto_s_mat_only_solve = True
        self.min_freq_s_mat_only_solve = "1MHz"
        self.frequencies = []
        self.steady_state_start = -1.0
        self.mesh_freq_choice = -1
        self.mesh_freq_points = []
        self.mesh_freq_range_start = "-1.0"
        self.mesh_freq_range_stop = "-1.0"
        self.interpolation_data = InterpolatingSweepData()

    @property
    def frequency_string(self):
        """:obj:`str`: String representing the frequency sweep data."""
        return self.distribution + " " + self.start_f + " " + self.end_f + " " + self.step


def _hfss_region_compute_resource_message(res):
    """Create a ``HFSSRegionComputeResourceMessage`` from a ``HFSSRegionComputeResource``."""
    return HFSSRegionComputeResourceMessage(
        region_id=res.region_id, compute_resource_percentage=res.resource_percentage
    )


def _interpolating_sweep_data_msg(interp_sweep_data):
    """Create a ``InterpolatingSweepDataMessage`` from a ``InterpolatingSweepData``."""
    return InterpolatingSweepDataMessage(
        relative_s_error=interp_sweep_data.relative_s_error,
        enforce_causality=interp_sweep_data.enforce_causality,
        enforce_passivity=interp_sweep_data.enforce_passivity,
        passivity_tolerance=interp_sweep_data.passivity_tolerance,
        max_solutions=interp_sweep_data.max_solutions,
        interp_use_s_matrix=interp_sweep_data.use_s_matrix,
        interp_use_port_impedance=interp_sweep_data.use_port_impedance,
        interp_use_prop_const=interp_sweep_data.use_prop_const,
        interp_use_full_basis=interp_sweep_data.use_full_basis,
        fast_sweep=interp_sweep_data.fast_sweep,
        adaptive_sampling=interp_sweep_data.adaptive_sampling,
        enforce_dc_and_causality=interp_sweep_data.enforce_dc_and_causality,
        matrix_conv_entry_list=messages.mx_convergence_entry_msg_list(
            interp_sweep_data.matrix_conv_entry_list
        ),
        interp_min_solutions=interp_sweep_data.min_solutions,
        interp_min_subranges=interp_sweep_data.min_subranges,
    )


def _sweep_data_msg(sweep_data):
    """Create a ``SweepDataMessage`` from a ``SweepData``."""
    return SweepDataMessage(
        name=sweep_data.name,
        frequency_string=sweep_data.frequency_string,
        enabled=sweep_data.enabled,
        type=sweep_data.type.value,
        use_q3d_for_dc=sweep_data.use_q3d_for_dc,
        save_fields=sweep_data.save_fields,
        save_rad_fields_only=sweep_data.save_rad_fields_only,
        compute_dc_point=sweep_data.compute_dc_point,
        siwave_with_3dddm=sweep_data.siwave_with_3dddm,
        use_hfss_solver_regions=sweep_data.use_hfss_solver_regions,
        use_hfss_solver_region_sch_gen=sweep_data.use_hfss_solver_region_sch_gen,
        use_hfss_solver_region_parallel_solve=sweep_data.use_hfss_solver_region_parallel_solve,
        use_adp_solution_for_all_sweep_freq=sweep_data.use_adp_solution_for_all_sweep_freq,
        num_parallel_hfss_regions=sweep_data.num_parallel_hfss_regions,
        parallel_hfss_regions_sim_cfg=map_list(
            sweep_data.parallel_hfss_regions_sim_cfg, _hfss_region_compute_resource_message
        ),
        auto_s_mat_only_solve=sweep_data.auto_s_mat_only_solve,
        min_freq_s_mat_only_solve=sweep_data.min_freq_s_mat_only_solve,
        frequencies=sweep_data.frequencies,
        steady_state_start=sweep_data.steady_state_start,
        mesh_freq_choice=sweep_data.mesh_freq_choice,
        mesh_freq_points=sweep_data.mesh_freq_points,
        mesh_freq_range_start=sweep_data.mesh_freq_range_start,
        mesh_freq_range_stop=sweep_data.mesh_freq_range_stop,
        interp_sweep_data=_interpolating_sweep_data_msg(sweep_data.interpolation_data),
    )


def _msg_to_matrix_convergence_entry(msg):
    """Create a ``MatrixConvergenceDataEntry`` from a ``MatrixConvergenceEntryMessage``."""
    return MatrixConvergenceDataEntry(msg.port_1, msg.port_2, msg.mag_limit, msg.phase_limit)


def _msg_to_hfss_region_compute_resource(msg):
    """Create a ``HFSSRegionComputeResource`` from a ``HFSSRegionComputeResourceMessage``."""
    return HFSSRegionComputeResource(msg.region_id, msg.compute_resource_percentage)


def _msg_to_interpolating_sweep_data(msg):
    """Create a ``InterpolatingSweepData`` from a ``InterpolatingSweepDataMessage``."""
    interp_sweep_data = InterpolatingSweepData()
    interp_sweep_data.relative_s_error = msg.relative_s_error
    interp_sweep_data.enforce_passivity = msg.enforce_passivity
    interp_sweep_data.enforce_causality = msg.enforce_causality
    interp_sweep_data.passivity_tolerance = msg.passivity_tolerance
    interp_sweep_data.max_solutions = msg.max_solutions
    interp_sweep_data.use_s_matrix = msg.interp_use_s_matrix
    interp_sweep_data.use_port_impedance = msg.interp_use_port_impedance
    interp_sweep_data.use_prop_const = msg.interp_use_prop_const
    interp_sweep_data.use_full_basis = msg.interp_use_full_basis
    interp_sweep_data.fast_sweep = msg.fast_sweep
    interp_sweep_data.adaptive_sampling = msg.adaptive_sampling
    interp_sweep_data.enforce_dc_and_causality = msg.enforce_dc_and_causality
    interp_sweep_data.matrix_conv_entry_list = map_list(
        msg.matrix_conv_entry_list, _msg_to_matrix_convergence_entry
    )
    interp_sweep_data.min_subranges = msg.interp_min_subranges
    interp_sweep_data.min_solutions = msg.interp_min_solutions
    return interp_sweep_data


def _msg_to_sweep_data(msg):
    """Create a ``SweepData`` from a ``SweepDataMessage``."""
    freq_str_params = msg.frequency_string.split()
    sweep_data = SweepData(
        msg.name, freq_str_params[0], freq_str_params[1], freq_str_params[2], freq_str_params[3]
    )
    sweep_data.enabled = msg.enabled
    sweep_data.type = FreqSweepType(msg.type)
    sweep_data.use_q3d_for_dc = msg.use_q3d_for_dc
    sweep_data.save_fields = msg.save_fields
    sweep_data.save_rad_fields_only = msg.save_rad_fields_only
    sweep_data.compute_dc_point = msg.compute_dc_point
    sweep_data.siwave_with_3dddm = msg.siwave_with_3dddm
    sweep_data.use_hfss_solver_regions = msg.use_hfss_solver_regions
    sweep_data.use_hfss_solver_region_sch_gen = msg.use_hfss_solver_region_sch_gen
    sweep_data.use_hfss_solver_region_parallel_solve = msg.use_hfss_solver_region_parallel_solve
    sweep_data.use_adp_solution_for_all_sweep_freq = msg.use_adp_solution_for_all_sweep_freq
    sweep_data.num_parallel_hfss_regions = msg.num_parallel_hfss_regions
    sweep_data.parallel_hfss_regions_sim_cfg = map_list(
        msg.parallel_hfss_regions_sim_cfg, _msg_to_hfss_region_compute_resource
    )
    sweep_data.auto_s_mat_only_solve = msg.auto_s_mat_only_solve
    sweep_data.min_freq_s_mat_only_solve = msg.min_freq_s_mat_only_solve
    sweep_data.frequencies = msg.frequencies
    sweep_data.steady_state_start = msg.steady_state_start
    sweep_data.mesh_freq_choice = msg.mesh_freq_choice
    sweep_data.mesh_freq_points = msg.mesh_freq_points
    sweep_data.mesh_freq_range_start = msg.mesh_freq_range_start
    sweep_data.mesh_freq_range_stop = msg.mesh_freq_range_stop
    sweep_data.interpolation_data = _msg_to_interpolating_sweep_data(msg.interp_sweep_data)
    return sweep_data


class SimulationSetup(ObjBase):
    """Class representing base simulation setup data."""

    __stub: SimulationSetupServiceStub = StubAccessor(StubType.sim_setup)

    @classmethod
    def _create(cls, cell, sim_setup_name, sim_setup_type):
        return cls(
            SimulationSetup.__stub.Create(
                SimulationSetupCreationMessage(
                    cell=cell.msg, name=sim_setup_name, type=sim_setup_type.value
                )
            )
        )

    @property
    def name(self):
        """:obj:`str`: Name of simulation setup."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, name):
        self.__stub.SetName(messages.string_property_message(self, name))

    @property
    def position(self):
        """:obj:`int`: Position of the simulation in the setup order."""
        return self.__stub.GetPosition(self.msg).value

    @position.setter
    def position(self, position):
        self.__stub.SetPosition(messages.int_property_message(self, position))

    @property
    def sweep_data(self):
        """:obj:`list` of :class:`.SweepData`: Frequency sweeps of the simulation setup."""
        sweep_data = []
        for sweep_data_msg in self.__stub.GetSweepData(self.msg).sweep_data:
            sweep_data.append(_msg_to_sweep_data(sweep_data_msg))
        return sweep_data

    @sweep_data.setter
    def sweep_data(self, sweep_data):
        sweep_data_msgs = []
        for sweep in sweep_data:
            sweep_data_msgs.append(_sweep_data_msg(sweep))
        self.__stub.SetSweepData(
            SweepDataListPropertyMessage(
                target=self.msg, sweeps=SweepDataListMessage(sweep_data=sweep_data_msgs)
            )
        )

    @property
    def type(self):
        """:class:`.SimulationSetupType`: Type of the simulation setup."""
        return SimulationSetupType(self.__stub.GetType(self.msg).type)

    def cast(self):
        """Cast the base SimulationSetup object to correct subclass, if possible.

        Returns
        -------
        SimulationSetup
        """
        from ansys.edb.core.simulation_setup.hfss_simulation_setup import HfssSimulationSetup
        from ansys.edb.core.simulation_setup.raptor_x_simulation_setup import RaptorXSimulationSetup
        from ansys.edb.core.simulation_setup.siwave_dcir_simulation_setup import (
            SIWaveDCIRSimulationSetup,
        )
        from ansys.edb.core.simulation_setup.siwave_simulation_setup import SIWaveSimulationSetup

        if self.is_null:
            return

        sim_type = self.type
        if sim_type == SimulationSetupType.HFSS:
            return HfssSimulationSetup(self.msg)
        elif sim_type == SimulationSetupType.SI_WAVE:
            return SIWaveSimulationSetup(self.msg)
        elif sim_type == SimulationSetupType.SI_WAVE_DCIR:
            return SIWaveDCIRSimulationSetup(self.msg)
        elif sim_type == SimulationSetupType.RAPTOR_X:
            return RaptorXSimulationSetup(self.msg)
