"""SIWave simulation settings."""

from enum import Enum

import ansys.api.edb.v1.siwave_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import (
    SIWaveAdvancedSettingsServiceStub,
    SIWaveDCAdvancedSettingsServiceStub,
    SIWaveDCSettingsServiceStub,
    SIWaveGeneralSettingsServiceStub,
    SIWaveSParameterSettingsServiceStub,
    StubAccessor,
    StubType,
)
from ansys.edb.core.simulation_setup.simulation_settings import (
    SimulationSettings,
    SimulationSettingsBase,
)


class SParamInterpolation(Enum):
    """Provides an enum representing s parameter interpolation types."""

    POINT_IN = pb.POINT_IN
    LINEAR_IN = pb.LINEAR_IN
    STEP_IN = pb.STEP_IN


class SParamExtrapolation(Enum):
    """Provides an enum representing s parameter extrapolation types."""

    ZERO_EX = pb.ZERO_EX
    SAME_EX = pb.SAME_EX
    LINEAR_EX = pb.LINEAR_EX
    CONSTANT_EX = pb.CONSTANT_EX


class SParamDCBehavior(Enum):
    """Provides an enum representing s parameter DC behavior types."""

    ZERO_DC = pb.ZERO_DC
    SAME_DC = pb.SAME_DC
    LINEAR_DC = pb.LINEAR_DC
    CONSTANT_DC = pb.CONSTANT_DC
    ONE_PORT_CAPACITOR_DC = pb.ONE_PORT_CAPACITOR_DC
    OPEN_DC = pb.OPEN_DC


class SIWaveSimulationSettings(SimulationSettings):
    """Represents SIWave simulation settings."""

    @property
    def general(self):
        """:class:`.SIWaveGeneralSettings`: General settings for SIWave simulations."""
        return SIWaveGeneralSettings(self._sim_setup)

    @property
    def advanced(self):
        """:class:`.SIWaveAdvancedSettings`: Advanced settings for SIWave simulations."""
        return SIWaveAdvancedSettings(self._sim_setup)

    @property
    def dc(self):
        """:class:`.SIWaveDCSettings`: DC settings for SIWave simulations."""
        return SIWaveDCSettings(self._sim_setup)

    @property
    def dc_advanced(self):
        """:class:`.SIWaveDCAdvancedSettings`: Advanced DC settings for SIWave simulations."""
        return SIWaveDCAdvancedSettings(self._sim_setup)

    @property
    def s_parameter(self):
        """:class:`.SIWaveSParameterSettings`: S parameter settings for SIWave simulations."""
        return SIWaveSParameterSettings(self._sim_setup)


class SIWaveGeneralSettings(SimulationSettingsBase):
    """Represents general settings for SIWave simulations."""

    __stub: SIWaveGeneralSettingsServiceStub = StubAccessor(StubType.siwave_general_sim_settings)

    @property
    def use_si_settings(self):
        """:obj:`bool`: Flag indicating if SI or PI settings are used."""
        return self.__stub.GetUseSISettings(self.msg).value

    @use_si_settings.setter
    def use_si_settings(self, use_si_settings):
        self.__stub.SetUseSISettings(messages.bool_property_message(self, use_si_settings))

    @property
    def use_custom_settings(self):
        """:obj:`bool`: Flag indicating if custom settings are used rather than SI or PI settings."""
        return self.__stub.GetUseCustomSettings(self.msg).value

    @use_custom_settings.setter
    def use_custom_settings(self, use_si_settings):
        self.__stub.SetUseCustomSettings(messages.bool_property_message(self, use_si_settings))

    @property
    def si_slider_pos(self):
        """:obj:`int`: SI slider position value."""
        return self.__stub.GetSISliderPos(self.msg).value

    @si_slider_pos.setter
    def si_slider_pos(self, si_slider_pos):
        self.__stub.SetSISliderPos(messages.int_property_message(self, si_slider_pos))

    @property
    def pi_slider_pos(self):
        """:obj:`int`: PI slider position value."""
        return self.__stub.GetPISliderPos(self.msg).value

    @pi_slider_pos.setter
    def pi_slider_pos(self, pi_slider_pos):
        self.__stub.SetPISliderPos(messages.int_property_message(self, pi_slider_pos))


class SIWaveAdvancedSettings(SimulationSettingsBase):
    """Represents advanced settings for SIWave simulations."""

    __stub: SIWaveAdvancedSettingsServiceStub = StubAccessor(StubType.siwave_advanced_sim_settings)

    @property
    def include_co_plane_coupling(self):
        """:obj:`bool`: Flag indicating if the co-plane coupling is included."""
        return self.__stub.GetIncludeCoPlaneCoupling(self.msg).value

    @include_co_plane_coupling.setter
    def include_co_plane_coupling(self, include_co_plane_coupling):
        self.__stub.SetIncludeCoPlaneCoupling(
            messages.bool_property_message(self, include_co_plane_coupling)
        )

    @property
    def include_inter_plane_coupling(self):
        """:obj:`bool`: Flag indicating if the inter-plane coupling is included."""
        return self.__stub.GetIncludeInterPlaneCoupling(self.msg).value

    @include_inter_plane_coupling.setter
    def include_inter_plane_coupling(self, include_inter_plane_coupling):
        self.__stub.SetIncludeInterPlaneCoupling(
            messages.bool_property_message(self, include_inter_plane_coupling)
        )

    @property
    def include_split_plane_coupling(self):
        """:obj:`bool`: Flag indicating if the split-plane coupling is included."""
        return self.__stub.GetIncludeSplitPlaneCoupling(self.msg).value

    @include_split_plane_coupling.setter
    def include_split_plane_coupling(self, include_split_plane_coupling):
        self.__stub.SetIncludeSplitPlaneCoupling(
            messages.bool_property_message(self, include_split_plane_coupling)
        )

    @property
    def include_fringe_plane_coupling(self):
        """:obj:`bool`: Flag indicating if the fringe-plane coupling is included."""
        return self.__stub.GetIncludeFringePlaneCoupling(self.msg).value

    @include_fringe_plane_coupling.setter
    def include_fringe_plane_coupling(self, include_fringe_plane_coupling):
        self.__stub.SetIncludeFringePlaneCoupling(
            messages.bool_property_message(self, include_fringe_plane_coupling)
        )

    @property
    def include_trace_plane_coupling(self):
        """:obj:`bool`: Flag indicating if the trace-plane coupling is included."""
        return self.__stub.GetIncludeTracePlaneCoupling(self.msg).value

    @include_trace_plane_coupling.setter
    def include_trace_plane_coupling(self, include_trace_plane_coupling):
        self.__stub.SetIncludeTracePlaneCoupling(
            messages.bool_property_message(self, include_trace_plane_coupling)
        )

    @property
    def cross_talk_threshold(self):
        """:obj:`str`: Cross-talk threshold."""
        return self.__stub.GetCrossTalkThreshold(self.msg).value

    @cross_talk_threshold.setter
    def cross_talk_threshold(self, cross_talk_threshold):
        self.__stub.SetCrossTalkThreshold(
            messages.string_property_message(self, cross_talk_threshold)
        )

    @property
    def max_coupled_lines(self):
        """:obj:`int`: Maximum number of coupled lines."""
        return self.__stub.GetMaxCoupledLines(self.msg).value

    @max_coupled_lines.setter
    def max_coupled_lines(self, max_coupled_lines):
        self.__stub.SetMaxCoupledLines(messages.int_property_message(self, max_coupled_lines))

    @property
    def min_void_area(self):
        """:obj:`str`: Minimum void area."""
        return self.__stub.GetMinVoidArea(self.msg).value

    @min_void_area.setter
    def min_void_area(self, min_void_area):
        self.__stub.SetMinVoidArea(messages.string_property_message(self, min_void_area))

    @property
    def min_pad_area_to_mesh(self):
        """:obj:`str`: Minimum pad area to mesh."""
        return self.__stub.GetMinPadAreaToMesh(self.msg).value

    @min_pad_area_to_mesh.setter
    def min_pad_area_to_mesh(self, min_pad_area_to_mesh):
        self.__stub.SetMinPadAreaToMesh(
            messages.string_property_message(self, min_pad_area_to_mesh)
        )

    @property
    def min_plane_area_to_mesh(self):
        """:obj:`str`: Minimum plane area to mesh."""
        return self.__stub.GetMinPlaneAreaToMesh(self.msg).value

    @min_plane_area_to_mesh.setter
    def min_plane_area_to_mesh(self, min_plane_area_to_mesh):
        self.__stub.SetMinPlaneAreaToMesh(
            messages.string_property_message(self, min_plane_area_to_mesh)
        )

    @property
    def snap_length_threshold(self):
        """:obj:`str`: Snapping length threshold."""
        return self.__stub.GetSnapLengthThreshold(self.msg).value

    @snap_length_threshold.setter
    def snap_length_threshold(self, snap_length_threshold):
        self.__stub.SetSnapLengthThreshold(
            messages.string_property_message(self, snap_length_threshold)
        )

    @property
    def mesh_automatic(self):
        """:obj:`bool`: Flag indicating it mesh refinement frequency is automatically determined."""
        return self.__stub.GetMeshAutomatic(self.msg).value

    @mesh_automatic.setter
    def mesh_automatic(self, mesh_automatic):
        self.__stub.SetMeshAutomatic(messages.bool_property_message(self, mesh_automatic))

    @property
    def mesh_frequency(self):
        """:obj:`str`: Mesh refinement frequency."""
        return self.__stub.GetMeshFrequency(self.msg).value

    @mesh_frequency.setter
    def mesh_frequency(self, mesh_frequency):
        self.__stub.SetMeshFrequency(messages.string_property_message(self, mesh_frequency))

    @property
    def return_current_distribution(self):
        """:obj:`bool`: Flag indicating if return current distribution is traced."""
        return self.__stub.Get3DReturnCurrentDistribution(self.msg).value

    @return_current_distribution.setter
    def return_current_distribution(self, return_current_distribution):
        self.__stub.Set3DReturnCurrentDistribution(
            messages.bool_property_message(self, return_current_distribution)
        )

    @property
    def include_vi_sources(self):
        """:obj:`bool`: Flag indicating if voltage/current source connections/parasitics are included."""
        return self.__stub.GetIncludeVISources(self.msg).value

    @include_vi_sources.setter
    def include_vi_sources(self, include_vi_sources):
        self.__stub.SetIncludeVISources(messages.bool_property_message(self, include_vi_sources))

    @property
    def include_inf_gnd(self):
        """:obj:`bool`: Flag indicating if an infinite ground plane is included."""
        return self.__stub.GetIncludeInfGnd(self.msg).value

    @include_inf_gnd.setter
    def include_inf_gnd(self, include_inf_gnd):
        self.__stub.SetIncludeInfGnd(messages.bool_property_message(self, include_inf_gnd))

    @property
    def inf_gnd_location(self):
        """:obj:`str`: Infinite ground plane location."""
        return self.__stub.GetInfGndLocation(self.msg).value

    @inf_gnd_location.setter
    def inf_gnd_location(self, inf_gnd_location):
        self.__stub.SetInfGndLocation(messages.string_property_message(self, inf_gnd_location))

    @property
    def perform_erc(self):
        """:obj:`bool`: Flag indicating if ERC is performed during simulation setup."""
        return self.__stub.GetPerformERC(self.msg).value

    @perform_erc.setter
    def perform_erc(self, perform_erc):
        self.__stub.SetPerformERC(messages.bool_property_message(self, perform_erc))

    @property
    def ignore_non_functional_pads(self):
        """:obj:`bool`: Flag indicating if non-functional pads are ignored."""
        return self.__stub.GetIgnoreNonFunctionalPads(self.msg).value

    @ignore_non_functional_pads.setter
    def ignore_non_functional_pads(self, ignore_non_functional_pads):
        self.__stub.SetIgnoreNonFunctionalPads(
            messages.bool_property_message(self, ignore_non_functional_pads)
        )


class SIWaveDCSettings(SimulationSettingsBase):
    """Represents DC settings for SIWave simulations."""

    __stub: SIWaveDCSettingsServiceStub = StubAccessor(StubType.siwave_dc_sim_settings)

    @property
    def use_dc_custom_settings(self):
        """:obj:`bool`: Flag indicating if custom DC settings are used."""
        return self.__stub.GetUseDCCustomSettings(self.msg).value

    @use_dc_custom_settings.setter
    def use_dc_custom_settings(self, use_dc_custom_settings):
        self.__stub.SetUseDCCustomSettings(
            messages.bool_property_message(self, use_dc_custom_settings)
        )

    @property
    def compute_inductance(self):
        """:obj:`bool`: Flag indicating if inductance is calculated."""
        return self.__stub.GetComputeInductance(self.msg).value

    @compute_inductance.setter
    def compute_inductance(self, compute_inductance):
        self.__stub.SetComputeInductance(messages.bool_property_message(self, compute_inductance))

    @property
    def plot_jv(self):
        """:obj:`bool`: Flag indicating if current density and voltage distribution are plotted."""
        return self.__stub.GetPlotJV(self.msg).value

    @plot_jv.setter
    def plot_jv(self, plot_jv):
        self.__stub.SetPlotJV(messages.bool_property_message(self, plot_jv))

    @property
    def contact_radius(self):
        """:obj:`str`: Circuit element contact radius."""
        return self.__stub.GetContactRadius(self.msg).value

    @contact_radius.setter
    def contact_radius(self, contact_radius):
        self.__stub.SetContactRadius(messages.string_property_message(self, contact_radius))

    @property
    def dc_slider_pos(self):
        """:obj:`int`: DC slider position."""
        return self.__stub.GetDCSliderPos(self.msg).value

    @dc_slider_pos.setter
    def dc_slider_pos(self, dc_slider_pos):
        self.__stub.SetDCSliderPos(messages.int_property_message(self, dc_slider_pos))


class SIWaveDCAdvancedSettings(SimulationSettingsBase):
    """Represents advanced DC settings for SIWave simulations."""

    __stub: SIWaveDCAdvancedSettingsServiceStub = StubAccessor(
        StubType.siwave_dc_advanced_sim_settings
    )

    @property
    def dc_min_plane_area_to_mesh(self):
        """:obj:`str`: Geometry with an area smaller than this value is ignored."""
        return self.__stub.GetDCMinPlaneAreaToMesh(self.msg).value

    @dc_min_plane_area_to_mesh.setter
    def dc_min_plane_area_to_mesh(self, dc_min_plane_area_to_mesh):
        self.__stub.SetDCMinPlaneAreaToMesh(
            messages.string_property_message(self, dc_min_plane_area_to_mesh)
        )

    @property
    def dc_min_void_area_to_mesh(self):
        """:obj:`str`: Voids with an area smaller than this value are ignored."""
        return self.__stub.GetDCMinVoidAreaToMesh(self.msg).value

    @dc_min_void_area_to_mesh.setter
    def dc_min_void_area_to_mesh(self, dc_min_void_area_to_mesh):
        self.__stub.SetDCMinVoidAreaToMesh(
            messages.string_property_message(self, dc_min_void_area_to_mesh)
        )

    @property
    def max_init_mesh_edge_length(self):
        """:obj:`str`: Initial maximum edge length."""
        return self.__stub.GetMaxInitMeshEdgeLength(self.msg).value

    @max_init_mesh_edge_length.setter
    def max_init_mesh_edge_length(self, max_init_mesh_edge_length):
        self.__stub.SetMaxInitMeshEdgeLength(
            messages.string_property_message(self, max_init_mesh_edge_length)
        )

    @property
    def perform_adaptive_refinement(self):
        """:obj:`bool`: Flag indicating if adaptive refinement is performed."""
        return self.__stub.GetPerformAdaptiveRefinement(self.msg).value

    @perform_adaptive_refinement.setter
    def perform_adaptive_refinement(self, perform_adaptive_refinement):
        self.__stub.SetPerformAdaptiveRefinement(
            messages.bool_property_message(self, perform_adaptive_refinement)
        )

    @property
    def max_num_passes(self):
        """:obj:`int`: Maximum number of adaptive mesh refinement passes."""
        return self.__stub.GetMaxNumPasses(self.msg).value

    @max_num_passes.setter
    def max_num_passes(self, max_num_passes):
        self.__stub.SetMaxNumPasses(messages.int_property_message(self, max_num_passes))

    @property
    def min_num_passes(self):
        """:obj:`int`: Minimum number of adaptive mesh refinement passes."""
        return self.__stub.GetMinNumPasses(self.msg).value

    @min_num_passes.setter
    def min_num_passes(self, min_num_passes):
        self.__stub.SetMinNumPasses(messages.int_property_message(self, min_num_passes))

    @property
    def percent_local_refinement(self):
        """:obj:`int`: Percent of local refinement used for adaptive mesh refinement."""
        return self.__stub.GetPercentLocalRefinement(self.msg).value

    @percent_local_refinement.setter
    def percent_local_refinement(self, percent_local_refinement):
        self.__stub.SetPercentLocalRefinement(
            messages.int_property_message(self, percent_local_refinement)
        )

    @property
    def energy_error(self):
        """:obj:`float`: Percent of energy error used for adaptive mesh refinement."""
        return self.__stub.GetEnergyError(self.msg).value

    @energy_error.setter
    def energy_error(self, energy_error):
        self.__stub.SetEnergyError(messages.double_property_message(self, energy_error))

    @property
    def mesh_bws(self):
        """:obj:`bool`: Flag indicating if bondwires are meshed."""
        return self.__stub.GetMeshBws(self.msg).value

    @mesh_bws.setter
    def mesh_bws(self, mesh_bws):
        self.__stub.SetMeshBws(messages.bool_property_message(self, mesh_bws))

    @property
    def refine_bws(self):
        """:obj:`bool`: Flag indicating if the mesh along bondwires is refined."""
        return self.__stub.GetRefineBws(self.msg).value

    @refine_bws.setter
    def refine_bws(self, refine_bws):
        self.__stub.SetRefineBws(messages.bool_property_message(self, refine_bws))

    @property
    def mesh_vias(self):
        """:obj:`bool`: Flag indicating if vias are meshed."""
        return self.__stub.GetMeshVias(self.msg).value

    @mesh_vias.setter
    def mesh_vias(self, mesh_vias):
        self.__stub.SetMeshVias(messages.bool_property_message(self, mesh_vias))

    @property
    def refine_vias(self):
        """:obj:`bool`: Flag indicating if the mesh along vias is refined."""
        return self.__stub.GetRefineVias(self.msg).value

    @refine_vias.setter
    def refine_vias(self, refine_vias):
        self.__stub.SetRefineVias(messages.bool_property_message(self, refine_vias))

    @property
    def num_bw_sides(self):
        """:obj:`int`: Number of sides to use to approximate cylindrical bondwires."""
        return self.__stub.GetNumBwSides(self.msg).value

    @num_bw_sides.setter
    def num_bw_sides(self, num_bw_sides):
        self.__stub.SetNumBwSides(messages.int_property_message(self, num_bw_sides))

    @property
    def num_via_sides(self):
        """:obj:`int`: Number of sides to use to approximate cylindrical vias."""
        return self.__stub.GetNumViaSides(self.msg).value

    @num_via_sides.setter
    def num_via_sides(self, num_via_sides):
        self.__stub.SetNumViaSides(messages.int_property_message(self, num_via_sides))


class SIWaveSParameterSettings(SimulationSettingsBase):
    """Represents s parameter settings for SIWave simulations."""

    __stub: SIWaveSParameterSettingsServiceStub = StubAccessor(StubType.siwave_s_param_sim_settings)

    @property
    def use_state_space(self):
        """:obj:`bool`: Flag indicating if state space is used. If ``False``, a custom model is used."""
        return self.__stub.GetUseStateSpace(self.msg).value

    @use_state_space.setter
    def use_state_space(self, use_state_space):
        self.__stub.SetUseStateSpace(messages.bool_property_message(self, use_state_space))

    @property
    def interpolation(self):
        """:obj:`SParamInterpolation`: Interpolation type."""
        return SParamInterpolation(self.__stub.GetInterpolation(self.msg).interpolation)

    @interpolation.setter
    def interpolation(self, interpolation):
        self.__stub.SetInterpolation(
            pb.SParamInterpolationPropertyMessage(
                target=self.msg, interpolation=interpolation.value
            )
        )

    @property
    def extrapolation(self):
        """:obj:`SParamExtrapolation`: Extrapolation type."""
        return SParamExtrapolation(self.__stub.GetExtrapolation(self.msg).extrapolation)

    @extrapolation.setter
    def extrapolation(self, extrapolation):
        self.__stub.SetExtrapolation(
            pb.SParamExtrapolationPropertyMessage(
                target=self.msg, extrapolation=extrapolation.value
            )
        )

    @property
    def dc_behavior(self):
        """:obj:`SParamDCBehavior`: DC behavior type."""
        return SParamDCBehavior(self.__stub.GetDCBehavior(self.msg).dc_behavior)

    @dc_behavior.setter
    def dc_behavior(self, dc_behavior):
        self.__stub.SetDCBehavior(
            pb.SParamDCBehaviorPropertyMessage(target=self.msg, dc_behavior=dc_behavior.value)
        )
