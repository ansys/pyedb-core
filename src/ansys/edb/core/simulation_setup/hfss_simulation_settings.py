"""HFSS simulation settings."""

from enum import Enum

import ansys.api.edb.v1.hfss_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages, parser
from ansys.edb.core.session import (
    DCRSettingsServiceStub,
    HFSSAdvancedMeshingSettingsServiceStub,
    HFSSAdvancedSettingsServiceStub,
    HFSSGeneralSettingsServiceStub,
    HFSSOptionsSettingsServiceStub,
    HFSSSolverSettingsServiceStub,
    StubAccessor,
    StubType,
)
from ansys.edb.core.simulation_setup.simulation_settings import (
    AdvancedMeshingSettings,
    AdvancedSettings,
    SettingsOptions,
    SimulationSettings,
    SimulationSettingsBase,
    SolverSettings,
)


class BasisFunctionOrder(Enum):
    """Provides an enum representing basis function order types."""

    ZERO_ORDER = pb.ZERO_ORDER
    FIRST_ORDER = pb.FIRST_ORDER
    SECOND_ORDER = pb.SECOND_ORDER
    MIXED_ORDER = pb.MIXED_ORDER


class SolverType(Enum):
    """Provides an enum representing HFSS solver types."""

    AUTO_SOLVER = pb.AUTO_SOLVER
    DIRECT_SOLVER = pb.DIRECT_SOLVER
    ITERATIVE_SOLVER = pb.ITERATIVE_SOLVER
    NUM_SOLVER_TYPES = pb.NUM_SOLVER_TYPES


class AdaptType(Enum):
    """Provides an enum representing HFSS adaptive solution types."""

    SINGLE = pb.SINGLE
    MULTI_FREQUENCIES = pb.MULTI_FREQUENCIES
    BROADBAND = pb.BROADBAND
    NUM_ADAPT_TYPE = pb.NUM_ADAPT_TYPE


class HFSSSimulationSettings(SimulationSettings):
    """Represents HFSS simulation settings."""

    @property
    def general(self):
        """:class:`.HFSSGeneralSettings`: General settings for HFSS simulations."""
        return HFSSGeneralSettings(self._sim_setup)

    @property
    def options(self):
        """:class:`.HFSSSettingsOptions`: HFSS simulation setting options."""
        return HFSSSettingsOptions(self._sim_setup)

    @property
    def advanced(self):
        """:class:`.HFSSAdvancedSettings`: Advanced settings for HFSS simulations."""
        return HFSSAdvancedSettings(self._sim_setup)

    @property
    def advanced_meshing(self):
        """:class:`.HFSSAdvancedMeshingSettings`: Advanced meshing settings for HFSS simulations."""
        return HFSSAdvancedMeshingSettings(self._sim_setup)

    @property
    def solver(self):
        """:class:`.HFSSSolverSettings`: Solver settings for HFSS simulations."""
        return HFSSSolverSettings(self._sim_setup)

    @property
    def dcr(self):
        """:class:`.HFSSDCRSettings`: DCR settings for HFSS simulations."""
        return HFSSDCRSettings(self._sim_setup)


class HFSSGeneralSettings(SimulationSettingsBase):
    """Represents general settings for HFSS simulations."""

    __stub: HFSSGeneralSettingsServiceStub = StubAccessor(StubType.hfss_general_sim_settings)

    @property
    def single_frequency_adaptive_solution(self):
        """.SingleFrequencyAdaptiveSolution`: Settings for a single frequency adaptive solution."""
        return parser.to_single_frequency_adaptive_solution(
            self.__stub.GetSingleFrequencyAdaptiveSolution(self.msg)
        )

    @single_frequency_adaptive_solution.setter
    def single_frequency_adaptive_solution(self, single_frequency_adaptive_solution):
        self.__stub.SetSingleFrequencyAdaptiveSolution(
            pb.SingleFrequencyAdaptiveSolutionPropertyMessage(
                target=self.msg,
                adaptive_frequency=messages.single_frequency_adaptive_solution_msg(
                    single_frequency_adaptive_solution
                ),
            )
        )

    @property
    def multi_frequency_adaptive_solution(self):
        """:class:`.MultiFrequencyAdaptiveSolution`: Settings for a multi-frequency adaptive solution."""
        return parser.to_multi_frequency_adaptive_solution(
            self.__stub.GetMultiFrequencyAdaptiveSolution(self.msg)
        )

    @multi_frequency_adaptive_solution.setter
    def multi_frequency_adaptive_solution(self, multi_frequency_adaptive_solution):
        self.__stub.SetMultiFrequencyAdaptiveSolution(
            pb.MultiFrequencyAdaptiveSolutionPropertyMessage(
                target=self.msg,
                adaptive_frequency=messages.multi_frequency_adaptive_solution_msg(
                    multi_frequency_adaptive_solution
                ),
            )
        )

    @property
    def broadband_adaptive_solution(self):
        """:class:`.BroadbandAdaptiveSolution`: Settings for a broadband adaptive solution."""
        return parser.to_broadband_adaptive_solution(
            self.__stub.GetBroadbandFrequencyAdaptiveSolution(self.msg)
        )

    @broadband_adaptive_solution.setter
    def broadband_adaptive_solution(self, broadband_adaptive_solution):
        self.__stub.SetBroadbandFrequencyAdaptiveSolution(
            pb.BroadbandFrequencyAdaptiveSolutionPropertyMessage(
                target=self.msg,
                adaptive_frequency=messages.broadband_solution_msg(broadband_adaptive_solution),
            )
        )

    @property
    def adaptive_solution_type(self):
        """:class:`AdaptType`: Adaptive solution type that is set for the simulation."""
        return AdaptType(self.__stub.GetAdaptType(self.msg).adapt_type)

    @adaptive_solution_type.setter
    def adaptive_solution_type(self, adaptive_solution_type):
        self.__stub.SetAdaptType(
            pb.AdaptTypePropertyMessage(target=self.msg, adapt_type=adaptive_solution_type.value)
        )

    @property
    def save_fields(self):
        """:obj:`bool`: Flag indicating if field data is to be saved during the simulation."""
        return self.__stub.GetSaveFieldsFlag(self.msg).value

    @save_fields.setter
    def save_fields(self, save_fields):
        self.__stub.SetSaveFieldsFlag(messages.bool_property_message(self, save_fields))

    @property
    def save_rad_fields_only(self):
        """:obj:`bool`: Flag indicating if only radiated field data is to be saved during the simulation."""
        return self.__stub.GetSaveRadFieldsOnlyFlag(self.msg).value

    @save_rad_fields_only.setter
    def save_rad_fields_only(self, save_rad_fields_only):
        self.__stub.SetSaveRadFieldsOnlyFlag(
            messages.bool_property_message(self, save_rad_fields_only)
        )

    @property
    def use_mesh_region(self):
        """:obj:`bool`: Flag indicating if mesh regions are used."""
        return self.__stub.GetUseMeshRegion(self.msg).value

    @use_mesh_region.setter
    def use_mesh_region(self, use_mesh_region):
        self.__stub.SetUseMeshRegion(messages.bool_property_message(self, use_mesh_region))

    @property
    def mesh_region_name(self):
        """:obj:`str`: Name of the mesh region to use."""
        return self.__stub.GetMeshRegionName(self.msg).value

    @mesh_region_name.setter
    def mesh_region_name(self, mesh_region_name):
        self.__stub.SetMeshRegionName(messages.string_property_message(self, mesh_region_name))

    @property
    def use_parallel_refinement(self):
        """:obj:`bool`: Flag indicating if parallel refinement is used."""
        return self.__stub.GetUseParallelRefinement(self.msg).value

    @use_parallel_refinement.setter
    def use_parallel_refinement(self, use_parallel_refinement):
        self.__stub.SetUseParallelRefinement(
            messages.bool_property_message(self, use_parallel_refinement)
        )


class HFSSSettingsOptions(SettingsOptions):
    """Represents options for HFSS simulation settings."""

    __stub: HFSSOptionsSettingsServiceStub = StubAccessor(StubType.hfss_options_sim_settings)

    @property
    def use_max_refinement(self):
        """:obj:`bool`: Flag indicating if maximum refinement values are used during simulation."""
        return self.__stub.GetUseMaxRefinement(self.msg).value

    @use_max_refinement.setter
    def use_max_refinement(self, use_max_refinement):
        self.__stub.SetUseMaxRefinement(messages.bool_property_message(self, use_max_refinement))

    @property
    def max_refinement_per_pass(self):
        """:obj:`int`: Maximum mesh refinement per adaptive pass."""
        return self.__stub.GetMaxRefinementPerPass(self.msg).value

    @max_refinement_per_pass.setter
    def max_refinement_per_pass(self, max_refinement_per_pass):
        self.__stub.SetMaxRefinementPerPass(
            messages.int_property_message(self, max_refinement_per_pass)
        )

    @property
    def min_passes(self):
        """:obj:`int`: Minimum number of adaptive passes."""
        return self.__stub.GetMinPasses(self.msg).value

    @min_passes.setter
    def min_passes(self, min_refinement_passes):
        self.__stub.SetMinPasses(messages.int_property_message(self, min_refinement_passes))

    @property
    def min_converged_passes(self):
        """:obj:`int`: Minimum number of converged adaptive passes."""
        return self.__stub.GetMinConvergedPasses(self.msg).value

    @min_converged_passes.setter
    def min_converged_passes(self, min_refinement_passes):
        self.__stub.SetMinConvergedPasses(
            messages.int_property_message(self, min_refinement_passes)
        )

    @property
    def order_basis(self):
        """:class:`.BasisFunctionOrder`: Basis function order."""
        return BasisFunctionOrder(self.__stub.GetBasisFunctionOrder(self.msg).basis_function_order)

    @order_basis.setter
    def order_basis(self, order_basis):
        self.__stub.SetBasisFunctionOrder(
            pb.BasisFunctionOrderPropertyMessage(
                target=self.msg, basis_function_order=order_basis.value
            )
        )

    @property
    def solver_type(self):
        """:class:`.SolverType`: HFSS solver type."""
        return SolverType(self.__stub.GetSolverTypeOrder(self.msg).solver_type)

    @solver_type.setter
    def solver_type(self, solver_type):
        self.__stub.SetSolverTypeOrder(
            pb.SolverTypePropertyMessage(target=self.msg, solver_type=solver_type.value)
        )

    @property
    def relative_residual(self):
        """:class:`float`: Relative residual value that the HFSS iterative solver is to use."""
        return self.__stub.GetRelativeResidual(self.msg).value

    @relative_residual.setter
    def relative_residual(self, relative_residual):
        self.__stub.SetRelativeResidual(messages.double_property_message(self, relative_residual))

    @property
    def use_shell_elements(self):
        """:class:`bool`: Flag indicating whether to use shell elements."""
        return self.__stub.GetUseShellElements(self.msg).value

    @use_shell_elements.setter
    def use_shell_elements(self, use_shell_elements):
        self.__stub.SetUseShellElements(messages.bool_property_message(self, use_shell_elements))

    @property
    def enhanced_low_frequency_accuracy(self):
        """:obj:`bool`: Flag indicating if enhanced low-frequency accuracy is enabled during simulation."""
        return self.__stub.GetEnhancedLowFrequencyAccuracy(self.msg).value

    @enhanced_low_frequency_accuracy.setter
    def enhanced_low_frequency_accuracy(self, enhanced_low_frequency_accuracy):
        self.__stub.SetEnhancedLowFrequencyAccuracy(
            messages.bool_property_message(self, enhanced_low_frequency_accuracy)
        )


class HFSSSolverSettings(SolverSettings):
    """Representis solver settings for HFSS simulations."""

    __stub: HFSSSolverSettingsServiceStub = StubAccessor(StubType.hfss_solver_sim_settings)

    @property
    def max_delta_z0(self):
        """:obj:`float`: Maximum percent change in characteristic impedance of ports between adaptive passes."""
        return self.__stub.GetMaxDeltaZ0(self.msg).value

    @max_delta_z0.setter
    def max_delta_z0(self, max_delta_z0):
        self.__stub.SetMaxDeltaZ0(messages.double_property_message(self, max_delta_z0))

    @property
    def set_triangles_for_wave_port(self):
        """:obj:`bool`: Flag indicating ifthe minimum and maximum triangle values for waveports are used."""
        return self.__stub.GetSetTrianglesForWaveport(self.msg).value

    @set_triangles_for_wave_port.setter
    def set_triangles_for_wave_port(self, set_triangles_for_wave_port):
        self.__stub.SetSetTrianglesForWaveport(
            messages.bool_property_message(self, set_triangles_for_wave_port)
        )

    @property
    def min_triangles_for_wave_port(self):
        """:obj:`int`: Minimum number of triangles to use for meshing waveports."""
        return self.__stub.GetMinTrianglesForWavePort(self.msg).value

    @min_triangles_for_wave_port.setter
    def min_triangles_for_wave_port(self, min_triangles_for_wave_port):
        self.__stub.SetMinTrianglesForWavePort(
            messages.int_property_message(self, min_triangles_for_wave_port)
        )

    @property
    def max_triangles_for_wave_port(self):
        """:obj:`int`: Maximum number of triangles to use for meshing waveports."""
        return self.__stub.GetMaxTrianglesForWavePort(self.msg).value

    @max_triangles_for_wave_port.setter
    def max_triangles_for_wave_port(self, max_triangles_for_wave_port):
        self.__stub.SetMaxTrianglesForWavePort(
            messages.int_property_message(self, max_triangles_for_wave_port)
        )

    @property
    def enable_intra_plane_coupling(self):
        """:obj:`bool`: Flag indicating if intra-plane coupling of power/ground nets is enabled to enhance accuracy."""
        return self.__stub.GetIntraPlaneCouplingEnabled(self.msg).value

    @enable_intra_plane_coupling.setter
    def enable_intra_plane_coupling(self, enable_intra_plane_coupling):
        self.__stub.SetIntraPlaneCouplingEnabled(
            messages.bool_property_message(self, enable_intra_plane_coupling)
        )


class HFSSAdvancedSettings(AdvancedSettings):
    """Represents advanced settings for HFSS simulations."""

    __stub: HFSSAdvancedSettingsServiceStub = StubAccessor(StubType.hfss_advanced_sim_settings)

    @property
    def ic_mode_auto_resolution(self):
        """:obj:`bool`: Flag indicating if model resolution is automatically calculated for IC designs."""
        return self.__stub.GetICModeAutoResolution(self.msg).value

    @ic_mode_auto_resolution.setter
    def ic_mode_auto_resolution(self, ic_mode_auto_resolution):
        self.__stub.SetICModeAutoResolution(
            messages.bool_property_message(self, ic_mode_auto_resolution)
        )

    @property
    def ic_mode_length(self):
        """:obj:`str`: Model resolution to use when manually setting the model resolution of IC designs."""
        return self.__stub.GetICModeLength(self.msg).value

    @ic_mode_length.setter
    def ic_mode_length(self, ic_mode_length):
        self.__stub.SetICModeLength(messages.string_property_message(self, ic_mode_length))


class HFSSAdvancedMeshingSettings(AdvancedMeshingSettings):
    """Represents advanced meshing settings for HFSS simulations."""

    __stub: HFSSAdvancedMeshingSettingsServiceStub = StubAccessor(
        StubType.hfss_advanced_sim_meshing_settings
    )

    @property
    def layer_snap_tol(self):
        """:obj:`str`: Snapping tolerance for hierarchical layer alignment.

        Unitless values represent a fraction of the total stackup height.
        """
        return self.__stub.GetLayerAlignment(self.msg).value

    @layer_snap_tol.setter
    def layer_snap_tol(self, layer_snap_tol):
        self.__stub.SetLayerAlignment(messages.string_property_message(self, layer_snap_tol))


class HFSSDCRSettings(SimulationSettingsBase):
    """Represents DCR settings for HFSS simulations."""

    __stub: DCRSettingsServiceStub = StubAccessor(StubType.hfss_dcr_sim_settings)

    @property
    def max_passes(self):
        """:obj:`int`: Maximum number of conduction adaptive passes."""
        return self.__stub.GetMaxPasses(self.msg).value

    @max_passes.setter
    def max_passes(self, max_passes):
        self.__stub.SetMaxPasses(messages.int_property_message(self, max_passes))

    @property
    def min_passes(self):
        """:obj:`int`: Minimum number of conduction adaptive passes."""
        return self.__stub.GetMinPasses(self.msg).value

    @min_passes.setter
    def min_passes(self, min_passes):
        self.__stub.SetMinPasses(messages.int_property_message(self, min_passes))

    @property
    def min_converged_passes(self):
        """:obj:`int`: Minimum number of converged conduction adaptive passes."""
        return self.__stub.GetMinConvergedPasses(self.msg).value

    @min_converged_passes.setter
    def min_converged_passes(self, min_converged_passes):
        self.__stub.SetMinConvergedPasses(messages.int_property_message(self, min_converged_passes))

    @property
    def percent_error(self):
        """:obj:`float`: Percent error during conduction adaptive passes."""
        return self.__stub.GetPercentError(self.msg).value

    @percent_error.setter
    def percent_error(self, percent_error):
        self.__stub.SetPercentError(messages.double_property_message(self, percent_error))

    @property
    def percent_refinement_per_pass(self):
        """:obj:`float`: Mesh refinement percentage per conduction adaptive pass."""
        return self.__stub.GetPercentRefinementPerPass(self.msg).value

    @percent_refinement_per_pass.setter
    def percent_refinement_per_pass(self, percent_refinement_per_pass):
        self.__stub.SetPercentRefinementPerPass(
            messages.double_property_message(self, percent_refinement_per_pass)
        )
