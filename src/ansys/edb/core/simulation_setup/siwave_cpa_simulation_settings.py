"""SIWave CPA simulation settings."""

from __future__ import annotations

from enum import Enum

import ansys.api.edb.v1.si_wave_cpa_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import SIWaveCPAAdvancedSettingsServiceStub
from ansys.edb.core.session import SIWaveCPAChannelComponentSettingsServiceStub
from ansys.edb.core.session import SIWaveCPADieConfigSettingsServiceStub
from ansys.edb.core.session import SIWaveCPAExternalEnvSettingsServiceStub
from ansys.edb.core.session import SIWaveCPAHotSpotComponentSettingsServiceStub
from ansys.edb.core.session import SIWaveCPANetSettingsServiceStub
from ansys.edb.core.session import SIWaveCPAQ3DSettingsServiceStub
from ansys.edb.core.session import SIWaveCPASettingsServiceStub
from ansys.edb.core.session import SIWaveCPASimulationSettingsServiceStub
from ansys.edb.core.session import SIWaveCPAUnconnectedDiePinSettingsServiceStub
from ansys.edb.core.session import SIWaveCPAVRMSettingsServiceStub
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.simulation_setup.simulation_settings import SimulationSettings
from ansys.edb.core.simulation_setup.simulation_settings import SimulationSettingsBase


class CPASimulationMode(Enum):
    """Provides an enum representing CPA simulation modes."""

    PI = pb.CPA_PI
    SI = pb.CPA_SI


class CPAExtractionMode(Enum):
    """Provides an enum representing CPA extraction modes."""

    L_NETWORK = pb.CPA_L_NETWORK
    T_NETWORK = pb.CPA_T_NETWORK
    MOR_NETWORK = pb.CPA_MOR_NETWORK
    RLCG = pb.CPA_RLCG
    PLOC = pb.CPA_PLOC
    DIE_GROUPS = pb.CPA_DIE_GROUPS


class CPAModelType(Enum):
    """Provides an enum representing CPA model types."""

    RDL_IC = pb.CPA_MODEL_RDL_IC
    PACKAGE = pb.CPA_MODEL_PACKAGE
    PCB = pb.CPA_MODEL_PCB


class CPAAccuracyLevel(Enum):
    """Provides an enum representing CPA accuracy levels."""

    NORMAL = pb.CPA_ACCURACY_NORMAL
    HIGH = pb.CPA_ACCURACY_HIGH


class CPASpiceNetlistTopology(Enum):
    """Provides an enum representing CPA SPICE netlist topologies."""

    PI = pb.CPA_PI
    T_NETWORK = pb.CPA_T_NETWORK
    MOR_NETWORK = pb.CPA_MOR_NETWORK


class CPAPinGroupMode(Enum):
    """Provides an enum representing CPA pin group modes."""

    NONE = pb.CPA_PIN_GROUP_NONE
    HOTSPOT_PIN_GROUP = pb.CPA_HOTSPOT_PIN_GROUP


class SIWaveCPASimulationSettings(SimulationSettings):
    """Represents SIWave CPA simulation settings."""

    __stub: SIWaveCPASimulationSettingsServiceStub = StubAccessor(StubType.siwave_cpa_sim_settings)

    @property
    def use_channel_setup(self) -> bool:
        """:obj:`bool`: Flag indicating if channel setup is used."""
        return self.__stub.GetUseChannelSetup(self.msg).value

    @use_channel_setup.setter
    def use_channel_setup(self, use_channel_setup: bool):
        self.__stub.SetUseChannelSetup(messages.bool_property_message(self, use_channel_setup))

    @property
    def simulation_mode(self) -> CPASimulationMode:
        """:class:`.CPASimulationMode`: Simulation mode."""
        return CPASimulationMode(self.__stub.GetSimulationMode(self.msg).sim_mode)

    @simulation_mode.setter
    def simulation_mode(self, simulation_mode: CPASimulationMode):
        self.__stub.SetSimulationMode(
            pb.CPASimulationModePropertyMessage(target=self.msg, sim_mode=simulation_mode.value)
        )

    @property
    def use_q3d_solver(self) -> bool:
        """:obj:`bool`: Flag indicating if the Q3D solver is used."""
        return self.__stub.GetUseQ3DSolver(self.msg).value

    @use_q3d_solver.setter
    def use_q3d_solver(self, use_q3d_solver: bool):
        self.__stub.SetUseQ3DSolver(messages.bool_property_message(self, use_q3d_solver))

    @property
    def hotspot_pin_group_threshold(self) -> float:
        """:obj:`float`: Threshold for hotspot pin group detection."""
        return self.__stub.GetHotspotPinGroupThreshold(self.msg).value

    @hotspot_pin_group_threshold.setter
    def hotspot_pin_group_threshold(self, hotspot_pin_group_threshold: float):
        self.__stub.SetHotspotPinGroupThreshold(messages.double_property_message(self, hotspot_pin_group_threshold))

    @property
    def hotspot_pin_group_size(self) -> int:
        """:obj:`int`: Size of a hotspot pin group."""
        return self.__stub.GetHotspotPinGroupSize(self.msg).value

    @hotspot_pin_group_size.setter
    def hotspot_pin_group_size(self, hotspot_pin_group_size: int):
        self.__stub.SetHotspotPinGroupSize(messages.uint64_property_message(self, hotspot_pin_group_size))

    @property
    def hotspot_max_num_pin_groups(self) -> int:
        """:obj:`int`: Maximum number of hotspot pin groups."""
        return self.__stub.GetHotspotMaxNumPinGroups(self.msg).value

    @hotspot_max_num_pin_groups.setter
    def hotspot_max_num_pin_groups(self, hotspot_max_num_pin_groups: int):
        self.__stub.SetHotspotMaxNumPinGroups(messages.uint64_property_message(self, hotspot_max_num_pin_groups))

    @property
    def settings(self) -> SIWaveCPASettings:
        """:class:`.SIWaveCPASettings`: General CPA settings."""
        return SIWaveCPASettings(self)

    @property
    def advanced_settings(self) -> SIWaveCPAAdvancedSettings:
        """:class:`.SIWaveCPAAdvancedSettings`: Advanced CPA settings."""
        return SIWaveCPAAdvancedSettings(self)

    @property
    def q3d_settings(self) -> SIWaveCPAQ3DSettings:
        """:class:`.SIWaveCPAQ3DSettings`: Q3D settings for CPA simulations."""
        return SIWaveCPAQ3DSettings(self)

    @property
    def net_settings(self) -> SIWaveCPANetSettings:
        """:class:`.SIWaveCPANetSettings`: Net settings for CPA simulations."""
        return SIWaveCPANetSettings(self)

    @property
    def external_env_settings(self) -> SIWaveCPAExternalEnvSettings:
        """:class:`.SIWaveCPAExternalEnvSettings`: External environment settings for CPA simulations."""
        return SIWaveCPAExternalEnvSettings(self)

    @property
    def die_config_settings(self) -> SIWaveCPADieConfigSettings:
        """:class:`.SIWaveCPADieConfigSettings`: Die configuration settings for CPA simulations."""
        return SIWaveCPADieConfigSettings(self)

    @property
    def channel_component_settings(self) -> SIWaveCPAChannelComponentSettings:
        """:class:`.SIWaveCPAChannelComponentSettings`: Channel component settings for CPA simulations."""
        return SIWaveCPAChannelComponentSettings(self)

    @property
    def vrm_settings(self) -> SIWaveCPAVRMSettings:
        """:class:`.SIWaveCPAVRMSettings`: VRM settings for CPA simulations."""
        return SIWaveCPAVRMSettings(self)

    @property
    def unconnected_die_pin_settings(self) -> SIWaveCPAUnconnectedDiePinSettings:
        """:class:`.SIWaveCPAUnconnectedDiePinSettings`: Unconnected die pin settings for CPA simulations."""
        return SIWaveCPAUnconnectedDiePinSettings(self)

    @property
    def hot_spot_component_settings(self) -> SIWaveCPAHotSpotComponentSettings:
        """:class:`.SIWaveCPAHotSpotComponentSettings`: Hot spot component settings for CPA simulations."""
        return SIWaveCPAHotSpotComponentSettings(self)


class SIWaveCPASettings(SimulationSettingsBase):
    """Represents SIWave CPA general settings."""

    __stub: SIWaveCPASettingsServiceStub = StubAccessor(StubType.siwave_cpa_settings)

    @property
    def extract_mode(self) -> CPAExtractionMode:
        """:class:`.CPAExtractionMode`: Extraction mode."""
        return CPAExtractionMode(self.__stub.GetExtractMode(self.msg).extract_mode)

    @extract_mode.setter
    def extract_mode(self, extract_mode: CPAExtractionMode):
        self.__stub.SetExtractMode(
            pb.CPAExtractionModePropertyMessage(target=self.msg, extract_mode=extract_mode.value)
        )

    @property
    def extract_frequency(self) -> str:
        """:obj:`str`: Extraction frequency."""
        return self.__stub.GetExtractFrequency(self.msg).value

    @extract_frequency.setter
    def extract_frequency(self, extract_frequency: str):
        self.__stub.SetExtractFrequency(messages.string_property_message(self, extract_frequency))

    @property
    def compute_capacitance(self) -> bool:
        """:obj:`bool`: Flag indicating if capacitance is computed."""
        return self.__stub.GetComputeCapacitance(self.msg).value

    @compute_capacitance.setter
    def compute_capacitance(self, compute_capacitance: bool):
        self.__stub.SetComputeCapacitance(messages.bool_property_message(self, compute_capacitance))

    @property
    def compute_dc(self) -> bool:
        """:obj:`bool`: Flag indicating if DC is computed."""
        return self.__stub.GetComputeDC(self.msg).value

    @compute_dc.setter
    def compute_dc(self, compute_dc: bool):
        self.__stub.SetComputeDC(messages.bool_property_message(self, compute_dc))

    @property
    def compute_dc_inductance(self) -> bool:
        """:obj:`bool`: Flag indicating if DC inductance is computed."""
        return self.__stub.GetComputeDCInductance(self.msg).value

    @compute_dc_inductance.setter
    def compute_dc_inductance(self, compute_dc_inductance: bool):
        self.__stub.SetComputeDCInductance(messages.bool_property_message(self, compute_dc_inductance))

    @property
    def compute_dc_capacitance(self) -> bool:
        """:obj:`bool`: Flag indicating if DC capacitance is computed."""
        return self.__stub.GetComputeDCCapacitance(self.msg).value

    @compute_dc_capacitance.setter
    def compute_dc_capacitance(self, compute_dc_capacitance: bool):
        self.__stub.SetComputeDCCapacitance(messages.bool_property_message(self, compute_dc_capacitance))

    @property
    def compute_ac(self) -> bool:
        """:obj:`bool`: Flag indicating if AC is computed."""
        return self.__stub.GetComputeAC(self.msg).value

    @compute_ac.setter
    def compute_ac(self, compute_ac: bool):
        self.__stub.SetComputeAC(messages.bool_property_message(self, compute_ac))

    @property
    def ground_pwr_gnd_nets_for_si(self) -> bool:
        """:obj:`bool`: Flag indicating if power/ground nets are grounded for SI."""
        return self.__stub.GetGroundPwrGndNetsForSI(self.msg).value

    @ground_pwr_gnd_nets_for_si.setter
    def ground_pwr_gnd_nets_for_si(self, ground_pwr_gnd_nets_for_si: bool):
        self.__stub.SetGroundPwrGndNetsForSI(messages.bool_property_message(self, ground_pwr_gnd_nets_for_si))

    @property
    def return_net(self) -> str:
        """:obj:`str`: Return net."""
        return self.__stub.GetReturnNet(self.msg).value

    @return_net.setter
    def return_net(self, return_net: str):
        self.__stub.SetReturnNet(messages.string_property_message(self, return_net))

    @property
    def auto_select_small_hole_size(self) -> bool:
        """:obj:`bool`: Flag indicating if small hole size is automatically selected."""
        return self.__stub.GetAutoSelectSmallHoleSize(self.msg).value

    @auto_select_small_hole_size.setter
    def auto_select_small_hole_size(self, auto_select_small_hole_size: bool):
        self.__stub.SetAutoSelectSmallHoleSize(messages.bool_property_message(self, auto_select_small_hole_size))

    @property
    def small_hole_size(self) -> str:
        """:obj:`str`: Small hole size threshold."""
        return self.__stub.GetSmallHoleSize(self.msg).value

    @small_hole_size.setter
    def small_hole_size(self, small_hole_size: str):
        self.__stub.SetSmallHoleSize(messages.string_property_message(self, small_hole_size))

    @property
    def model_type(self) -> CPAModelType:
        """:class:`.CPAModelType`: Model type."""
        return CPAModelType(self.__stub.GetModelType(self.msg).model_type)

    @model_type.setter
    def model_type(self, model_type: CPAModelType):
        self.__stub.SetModelType(pb.CPAModelTypePropertyMessage(target=self.msg, model_type=model_type.value))

    @property
    def use_local_analysis(self) -> bool:
        """:obj:`bool`: Flag indicating if local analysis is used."""
        return self.__stub.GetUseLocalAnalysis(self.msg).value

    @use_local_analysis.setter
    def use_local_analysis(self, use_local_analysis: bool):
        self.__stub.SetUseLocalAnalysis(messages.bool_property_message(self, use_local_analysis))

    @property
    def perform_erc(self) -> bool:
        """:obj:`bool`: Flag indicating if ERC is performed."""
        return self.__stub.GetPerformERC(self.msg).value

    @perform_erc.setter
    def perform_erc(self, perform_erc: bool):
        self.__stub.SetPerformERC(messages.bool_property_message(self, perform_erc))

    @property
    def exclude_nonfunctional_pads(self) -> bool:
        """:obj:`bool`: Flag indicating if non-functional pads are excluded."""
        return self.__stub.GetExcludeNonfunctionalPads(self.msg).value

    @exclude_nonfunctional_pads.setter
    def exclude_nonfunctional_pads(self, exclude_nonfunctional_pads: bool):
        self.__stub.SetExcludeNonfunctionalPads(messages.bool_property_message(self, exclude_nonfunctional_pads))


class SIWaveCPAAdvancedSettings(SimulationSettingsBase):
    """Represents SIWave CPA advanced settings."""

    __stub: SIWaveCPAAdvancedSettingsServiceStub = StubAccessor(StubType.siwave_cpa_advanced_settings)

    @property
    def ignore_geometry_below_size(self) -> str:
        """:obj:`str`: Minimum geometry size. Geometry smaller than this value is ignored."""
        return self.__stub.GetIgnoreGeometryBelowSize(self.msg).value

    @ignore_geometry_below_size.setter
    def ignore_geometry_below_size(self, ignore_geometry_below_size: str):
        self.__stub.SetIgnoreGeometryBelowSize(messages.string_property_message(self, ignore_geometry_below_size))

    @property
    def ignore_voids_below_size(self) -> str:
        """:obj:`str`: Minimum void size. Voids smaller than this value are ignored."""
        return self.__stub.GetIgnoreVoidsBelowSize(self.msg).value

    @ignore_voids_below_size.setter
    def ignore_voids_below_size(self, ignore_voids_below_size: str):
        self.__stub.SetIgnoreVoidsBelowSize(messages.string_property_message(self, ignore_voids_below_size))

    @property
    def snap_vertex_distance(self) -> str:
        """:obj:`str`: Snap vertex distance threshold."""
        return self.__stub.GetSnapVertexDistance(self.msg).value

    @snap_vertex_distance.setter
    def snap_vertex_distance(self, snap_vertex_distance: str):
        self.__stub.SetSnapVertexDistance(messages.string_property_message(self, snap_vertex_distance))

    @property
    def thermal_aware_sim(self) -> bool:
        """:obj:`bool`: Flag indicating if thermal-aware simulation is enabled."""
        return self.__stub.GetThermalAwareSim(self.msg).value

    @thermal_aware_sim.setter
    def thermal_aware_sim(self, thermal_aware_sim: bool):
        self.__stub.SetThermalAwareSim(messages.bool_property_message(self, thermal_aware_sim))

    @property
    def use_uniform_temperature(self) -> bool:
        """:obj:`bool`: Flag indicating if uniform temperature is used."""
        return self.__stub.GetUseUniformTemperature(self.msg).value

    @use_uniform_temperature.setter
    def use_uniform_temperature(self, use_uniform_temperature: bool):
        self.__stub.SetUseUniformTemperature(messages.bool_property_message(self, use_uniform_temperature))

    @property
    def design_temperature(self) -> str:
        """:obj:`str`: Design temperature."""
        return self.__stub.GetDesignTemperature(self.msg).value

    @design_temperature.setter
    def design_temperature(self, design_temperature: str):
        self.__stub.SetDesignTemperature(messages.string_property_message(self, design_temperature))

    @property
    def sitemp_file_path(self) -> str:
        """:obj:`str`: Path to the SITemp file."""
        return self.__stub.GetSitempFilePath(self.msg).value

    @sitemp_file_path.setter
    def sitemp_file_path(self, sitemp_file_path: str):
        self.__stub.SetSitempFilePath(messages.string_property_message(self, sitemp_file_path))

    @property
    def output_spice_topology(self) -> CPASpiceNetlistTopology:
        """:class:`.CPASpiceNetlistTopology`: Output SPICE netlist topology."""
        return CPASpiceNetlistTopology(self.__stub.GetOutputSpiceTopology(self.msg).topology)

    @output_spice_topology.setter
    def output_spice_topology(self, output_spice_topology: CPASpiceNetlistTopology):
        self.__stub.SetOutputSpiceTopology(
            pb.CPASpiceNetlistTopologyPropertyMessage(target=self.msg, topology=output_spice_topology.value)
        )


class SIWaveCPAQ3DSettings(SimulationSettingsBase):
    """Represents SIWave CPA Q3D settings."""

    __stub: SIWaveCPAQ3DSettingsServiceStub = StubAccessor(StubType.siwave_cpa_q3d_settings)

    @property
    def custom_refinement(self) -> bool:
        """:obj:`bool`: Flag indicating if custom refinement is used."""
        return self.__stub.GetCustomRefinement(self.msg).value

    @custom_refinement.setter
    def custom_refinement(self, custom_refinement: bool):
        self.__stub.SetCustomRefinement(messages.bool_property_message(self, custom_refinement))

    @property
    def max_num_cg_passes(self) -> int:
        """:obj:`int`: Maximum number of CG solver passes."""
        return self.__stub.GetMaxNumCGPasses(self.msg).value

    @max_num_cg_passes.setter
    def max_num_cg_passes(self, max_num_cg_passes: int):
        self.__stub.SetMaxNumCGPasses(messages.uint64_property_message(self, max_num_cg_passes))

    @property
    def min_num_cg_passes(self) -> int:
        """:obj:`int`: Minimum number of CG solver passes."""
        return self.__stub.GetMinNumCGPasses(self.msg).value

    @min_num_cg_passes.setter
    def min_num_cg_passes(self, min_num_cg_passes: int):
        self.__stub.SetMinNumCGPasses(messages.uint64_property_message(self, min_num_cg_passes))

    @property
    def cg_percent_error(self) -> float:
        """:obj:`float`: CG solver percent error."""
        return self.__stub.GetCGPercentError(self.msg).value

    @cg_percent_error.setter
    def cg_percent_error(self, cg_percent_error: float):
        self.__stub.SetCGPercentError(messages.double_property_message(self, cg_percent_error))

    @property
    def cg_percent_refinement(self) -> float:
        """:obj:`float`: CG solver percent refinement."""
        return self.__stub.GetCGPercentRefinement(self.msg).value

    @cg_percent_refinement.setter
    def cg_percent_refinement(self, cg_percent_refinement: float):
        self.__stub.SetCGPercentRefinement(messages.double_property_message(self, cg_percent_refinement))

    @property
    def cg_accuracy_level(self) -> CPAAccuracyLevel:
        """:class:`.CPAAccuracyLevel`: CG solver accuracy level."""
        return CPAAccuracyLevel(self.__stub.GetCGAccuracyLevel(self.msg).accuracy_level)

    @cg_accuracy_level.setter
    def cg_accuracy_level(self, cg_accuracy_level: CPAAccuracyLevel):
        self.__stub.SetCGAccuracyLevel(
            pb.CPAAccuracyLevelPropertyMessage(target=self.msg, accuracy_level=cg_accuracy_level.value)
        )

    @property
    def max_num_rl_passes(self) -> int:
        """:obj:`int`: Maximum number of RL solver passes."""
        return self.__stub.GetMaxNumRLPasses(self.msg).value

    @max_num_rl_passes.setter
    def max_num_rl_passes(self, max_num_rl_passes: int):
        self.__stub.SetMaxNumRLPasses(messages.uint64_property_message(self, max_num_rl_passes))

    @property
    def min_num_rl_passes(self) -> int:
        """:obj:`int`: Minimum number of RL solver passes."""
        return self.__stub.GetMinNumRLPasses(self.msg).value

    @min_num_rl_passes.setter
    def min_num_rl_passes(self, min_num_rl_passes: int):
        self.__stub.SetMinNumRLPasses(messages.uint64_property_message(self, min_num_rl_passes))

    @property
    def rl_percent_error(self) -> float:
        """:obj:`float`: RL solver percent error."""
        return self.__stub.GetRLPercentError(self.msg).value

    @rl_percent_error.setter
    def rl_percent_error(self, rl_percent_error: float):
        self.__stub.SetRLPercentError(messages.double_property_message(self, rl_percent_error))

    @property
    def rl_percent_refinement(self) -> float:
        """:obj:`float`: RL solver percent refinement."""
        return self.__stub.GetRLPercentRefinement(self.msg).value

    @rl_percent_refinement.setter
    def rl_percent_refinement(self, rl_percent_refinement: float):
        self.__stub.SetRLPercentRefinement(messages.double_property_message(self, rl_percent_refinement))

    @property
    def max_num_dc_passes(self) -> int:
        """:obj:`int`: Maximum number of DC solver passes."""
        return self.__stub.GetMaxNumDCPasses(self.msg).value

    @max_num_dc_passes.setter
    def max_num_dc_passes(self, max_num_dc_passes: int):
        self.__stub.SetMaxNumDCPasses(messages.uint64_property_message(self, max_num_dc_passes))

    @property
    def min_num_dc_passes(self) -> int:
        """:obj:`int`: Minimum number of DC solver passes."""
        return self.__stub.GetMinNumDCPasses(self.msg).value

    @min_num_dc_passes.setter
    def min_num_dc_passes(self, min_num_dc_passes: int):
        self.__stub.SetMinNumDCPasses(messages.uint64_property_message(self, min_num_dc_passes))

    @property
    def dc_percent_error(self) -> float:
        """:obj:`float`: DC solver percent error."""
        return self.__stub.GetDCPercentError(self.msg).value

    @dc_percent_error.setter
    def dc_percent_error(self, dc_percent_error: float):
        self.__stub.SetDCPercentError(messages.double_property_message(self, dc_percent_error))

    @property
    def dc_percent_refinement(self) -> float:
        """:obj:`float`: DC solver percent refinement."""
        return self.__stub.GetDCPercentRefinement(self.msg).value

    @dc_percent_refinement.setter
    def dc_percent_refinement(self, dc_percent_refinement: float):
        self.__stub.SetDCPercentRefinement(messages.double_property_message(self, dc_percent_refinement))

    @property
    def dielectric_extension(self) -> str:
        """:obj:`str`: Dielectric extension."""
        return self.__stub.GetDielectricExtension(self.msg).value

    @dielectric_extension.setter
    def dielectric_extension(self, dielectric_extension: str):
        self.__stub.SetDielectricExtension(messages.string_property_message(self, dielectric_extension))

    @property
    def terminal_diam(self) -> str:
        """:obj:`str`: Terminal diameter."""
        return self.__stub.GetTerminalDiam(self.msg).value

    @terminal_diam.setter
    def terminal_diam(self, terminal_diam: str):
        self.__stub.SetTerminalDiam(messages.string_property_message(self, terminal_diam))


class SIWaveCPANetSettings(SimulationSettingsBase):
    """Represents SIWave CPA net settings."""

    __stub: SIWaveCPANetSettingsServiceStub = StubAccessor(StubType.siwave_cpa_net_settings)

    @property
    def auto_select_nets_for_simulation(self) -> bool:
        """:obj:`bool`: Flag indicating if nets are automatically selected for simulation."""
        return self.__stub.GetAutoSelectNetsForSimulation(self.msg).value

    @auto_select_nets_for_simulation.setter
    def auto_select_nets_for_simulation(self, auto_select_nets_for_simulation: bool):
        self.__stub.SetAutoSelectNetsForSimulation(
            messages.bool_property_message(self, auto_select_nets_for_simulation)
        )

    @property
    def ignore_dummy_nets_for_selected_nets(self) -> bool:
        """:obj:`bool`: Flag indicating if dummy nets are ignored for selected nets."""
        return self.__stub.GetIgnoreDummyNetsForSelectedNets(self.msg).value

    @ignore_dummy_nets_for_selected_nets.setter
    def ignore_dummy_nets_for_selected_nets(self, ignore_dummy_nets_for_selected_nets: bool):
        self.__stub.SetIgnoreDummyNetsForSelectedNets(
            messages.bool_property_message(self, ignore_dummy_nets_for_selected_nets)
        )

    @property
    def included_nets(self) -> list[str]:
        """:obj:`list` of :obj:`str`: Nets included in the CPA simulation."""
        return list(self.__stub.GetIncludedNets(self.msg).nets)

    @included_nets.setter
    def included_nets(self, included_nets: list[str]):
        self.__stub.SetIncludedNets(pb.CPAIncludedNetsPropertyMessage(target=self.msg, nets=included_nets))


class SIWaveCPAExternalEnvSettings(SimulationSettingsBase):
    """Represents SIWave CPA external environment settings."""

    __stub: SIWaveCPAExternalEnvSettingsServiceStub = StubAccessor(StubType.siwave_cpa_external_env_settings)

    @property
    def top_fill_material(self) -> str:
        """:obj:`str`: Top fill material."""
        return self.__stub.GetTopFillMaterial(self.msg).value

    @top_fill_material.setter
    def top_fill_material(self, top_fill_material: str):
        self.__stub.SetTopFillMaterial(messages.string_property_message(self, top_fill_material))

    @property
    def bottom_fill_material(self) -> str:
        """:obj:`str`: Bottom fill material."""
        return self.__stub.GetBottomFillMaterial(self.msg).value

    @bottom_fill_material.setter
    def bottom_fill_material(self, bottom_fill_material: str):
        self.__stub.SetBottomFillMaterial(messages.string_property_message(self, bottom_fill_material))

    @property
    def pcb_material(self) -> str:
        """:obj:`str`: PCB material."""
        return self.__stub.GetPcbMaterial(self.msg).value

    @pcb_material.setter
    def pcb_material(self, pcb_material: str):
        self.__stub.SetPcbMaterial(messages.string_property_message(self, pcb_material))

    @property
    def include_metal_plane1(self) -> bool:
        """:obj:`bool`: Flag indicating if metal plane 1 is included."""
        return self.__stub.GetIncludeMetalPlane1(self.msg).value

    @include_metal_plane1.setter
    def include_metal_plane1(self, include_metal_plane1: bool):
        self.__stub.SetIncludeMetalPlane1(messages.bool_property_message(self, include_metal_plane1))

    @property
    def ground_metal_plane1(self) -> bool:
        """:obj:`bool`: Flag indicating if metal plane 1 is grounded."""
        return self.__stub.GetGroundMetalPlane1(self.msg).value

    @ground_metal_plane1.setter
    def ground_metal_plane1(self, ground_metal_plane1: bool):
        self.__stub.SetGroundMetalPlane1(messages.bool_property_message(self, ground_metal_plane1))

    @property
    def height_metal_plane1(self) -> str:
        """:obj:`str`: Height of metal plane 1."""
        return self.__stub.GetHeightMetalPlane1(self.msg).value

    @height_metal_plane1.setter
    def height_metal_plane1(self, height_metal_plane1: str):
        self.__stub.SetHeightMetalPlane1(messages.string_property_message(self, height_metal_plane1))

    @property
    def include_metal_plane2(self) -> bool:
        """:obj:`bool`: Flag indicating if metal plane 2 is included."""
        return self.__stub.GetIncludeMetalPlane2(self.msg).value

    @include_metal_plane2.setter
    def include_metal_plane2(self, include_metal_plane2: bool):
        self.__stub.SetIncludeMetalPlane2(messages.bool_property_message(self, include_metal_plane2))

    @property
    def ground_metal_plane2(self) -> bool:
        """:obj:`bool`: Flag indicating if metal plane 2 is grounded."""
        return self.__stub.GetGroundMetalPlane2(self.msg).value

    @ground_metal_plane2.setter
    def ground_metal_plane2(self, ground_metal_plane2: bool):
        self.__stub.SetGroundMetalPlane2(messages.bool_property_message(self, ground_metal_plane2))

    @property
    def height_metal_plane2(self) -> str:
        """:obj:`str`: Height of metal plane 2."""
        return self.__stub.GetHeightMetalPlane2(self.msg).value

    @height_metal_plane2.setter
    def height_metal_plane2(self, height_metal_plane2: str):
        self.__stub.SetHeightMetalPlane2(messages.string_property_message(self, height_metal_plane2))


class SIWaveCPADieConfigSettings(SimulationSettingsBase):
    """Represents SIWave CPA die configuration settings."""

    __stub: SIWaveCPADieConfigSettingsServiceStub = StubAccessor(StubType.siwave_cpa_die_config_settings)

    def get_all_die_configs(self) -> dict[str, pb.CPADieConfigMessage]:
        """:obj:`dict` { :obj:`str` : :class:`CPADieConfigMessage` }: All die configurations, keyed by part reference designator."""
        response = self.__stub.GetAllDieConfigs(self.msg)
        return {entry.part_ref_des: entry.config for entry in response.entries}

    def add_die_config(self, part_ref_des: str, config: pb.CPADieConfigMessage):
        """Add a die configuration for a given part reference designator.

        Parameters
        ----------
        part_ref_des : str
            Part reference designator.
        config : CPADieConfigMessage
            Die configuration message.
        """
        self.__stub.AddDieConfig(
            pb.CPADieConfigPropertyMessage(target=self.msg, part_ref_des=part_ref_des, config=config)
        )

    def remove_die_config(self, part_ref_des: str):
        """Remove the die configuration for a given part reference designator.

        Parameters
        ----------
        part_ref_des : str
            Part reference designator.
        """
        self.__stub.RemoveDieConfig(pb.CPADieConfigRemoveMessage(target=self.msg, part_ref_des=part_ref_des))


class SIWaveCPAChannelComponentSettings(SimulationSettingsBase):
    """Represents SIWave CPA channel component settings."""

    __stub: SIWaveCPAChannelComponentSettingsServiceStub = StubAccessor(StubType.siwave_cpa_channel_component_settings)

    def get_part_is_internal_to_netlist(self, ref_des: str) -> bool:
        """Get whether a part is internal to the netlist.

        Parameters
        ----------
        ref_des : str
            Reference designator of the part.

        Returns
        -------
        bool
        """
        return self.__stub.GetPartIsInternalToNetlist(messages.edb_obj_name_message(self, ref_des)).value

    def set_part_is_internal_to_netlist(self, ref_des: str, internal: bool):
        """Set whether a part is internal to the netlist.

        Parameters
        ----------
        ref_des : str
            Reference designator of the part.
        internal : bool
            Whether the part is internal to the netlist.
        """
        self.__stub.SetPartIsInternalToNetlist(
            pb.CPAChannelComponentPropertyMessage(target=self.msg, ref_des=ref_des, internal=internal)
        )


class SIWaveCPAVRMSettings(SimulationSettingsBase):
    """Represents SIWave CPA VRM settings."""

    __stub: SIWaveCPAVRMSettingsServiceStub = StubAccessor(StubType.siwave_cpa_vrm_settings)

    def get_all_vrm_configs(self) -> dict[str, pb.CPAVRMConfigMessage]:
        """:obj:`dict` { :obj:`str` : :class:`CPAVRMConfigMessage` }: All VRM configurations, keyed by part reference designator."""
        response = self.__stub.GetAllVRMConfigs(self.msg)
        return {entry.part_ref_des: entry.config for entry in response.entries}

    def get_vrm_config(self, part_ref_des: str) -> pb.CPAVRMConfigEntryMessage:
        """Get the VRM configuration for a given part reference designator.

        Parameters
        ----------
        part_ref_des : str
            Part reference designator.

        Returns
        -------
        CPAVRMConfigEntryMessage
        """
        return self.__stub.GetVRMConfig(pb.CPAGetVRMConfigMessage(target=self.msg, part_ref_des=part_ref_des))

    def add_vrm_config(self, part_ref_des: str, config: pb.CPAVRMConfigMessage):
        """Add a VRM configuration for a given part reference designator.

        Parameters
        ----------
        part_ref_des : str
            Part reference designator.
        config : CPAVRMConfigMessage
            VRM configuration message.
        """
        self.__stub.AddVRMConfig(
            pb.CPAVRMConfigPropertyMessage(target=self.msg, part_ref_des=part_ref_des, config=config)
        )

    def remove_vrm_config(self, part_ref_des: str):
        """Remove the VRM configuration for a given part reference designator.

        Parameters
        ----------
        part_ref_des : str
            Part reference designator.
        """
        self.__stub.RemoveVRMConfig(pb.CPAVRMConfigRemoveMessage(target=self.msg, part_ref_des=part_ref_des))


class SIWaveCPAUnconnectedDiePinSettings(SimulationSettingsBase):
    """Represents SIWave CPA unconnected die pin settings."""

    __stub: SIWaveCPAUnconnectedDiePinSettingsServiceStub = StubAccessor(
        StubType.siwave_cpa_unconnected_die_pin_settings
    )

    def get_pin_supply_voltages(self) -> dict[str, str]:
        """:obj:`dict` { :obj:`str` : :obj:`str` }: Pin supply voltage map keyed by pin name."""
        return dict(self.__stub.GetPinSupplyVoltages(self.msg).pin_supply_voltages)

    def set_pin_supply_voltage(self, pin: str, voltage: str):
        """Set the supply voltage for a given pin.

        Parameters
        ----------
        pin : str
            Pin name.
        voltage : str
            Supply voltage value.
        """
        self.__stub.SetPinSupplyVoltage(
            pb.CPAPinSupplyVoltagePropertyMessage(target=self.msg, pin=pin, voltage=voltage)
        )


class SIWaveCPAHotSpotComponentSettings(SimulationSettingsBase):
    """Represents SIWave CPA hot spot component settings."""

    __stub: SIWaveCPAHotSpotComponentSettingsServiceStub = StubAccessor(StubType.siwave_cpa_hot_spot_component_settings)

    def get_hot_spot_components(self) -> list[str]:
        """:obj:`list` of :obj:`str`: List of hot spot component reference designators."""
        return list(self.__stub.GetHotSpotComponents(self.msg).ref_des)

    def get_hot_spot_enabled(self, ref_des: str) -> bool:
        """Get whether the hot spot analysis is enabled for a given component.

        Parameters
        ----------
        ref_des : str
            Reference designator of the component.

        Returns
        -------
        bool
        """
        return self.__stub.GetHotSpotEnabled(messages.edb_obj_name_message(self, ref_des)).value

    def set_hot_spot_enabled(self, ref_des: str, enabled: bool):
        """Set whether the hot spot analysis is enabled for a given component.

        Parameters
        ----------
        ref_des : str
            Reference designator of the component.
        enabled : bool
            Whether hot spot analysis is enabled.
        """
        self.__stub.SetHotSpotEnabled(
            pb.CPAHotSpotComponentPropertyMessage(target=self.msg, ref_des=ref_des, enabled=enabled)
        )
