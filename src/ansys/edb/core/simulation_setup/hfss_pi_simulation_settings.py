"""HFSSPI simulation settings."""
from __future__ import annotations

from enum import Enum
from typing import List

import ansys.api.edb.v1.hfss_pi_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import (
    HFSSPIGeneralSettingsServiceStub,
    HFSSPINetProcessingSettingsServiceStub,
    HFSSPIPowerGroundNetsServiceStub,
    HFSSPISignalNetsSettingsServiceStub,
    StubAccessor,
    StubType,
)
from ansys.edb.core.simulation_setup.simulation_settings import (
    SimulationSettings,
    SimulationSettingsBase,
)


class HFSSPISimulationPreference(Enum):
    """Provides an enum representing HFSSPI simulation preferences."""

    BALANCED = pb.BALANCED
    ACCURACY = pb.ACCURACY


class HFSSPIModelType(Enum):
    """Provides an enum representing HFSSPI model types."""

    RDL = pb.RDL
    PACKAGE = pb.PACKAGE
    PCB = pb.PCB


class SurfaceRoughnessModel(Enum):
    """Provides an enum representing HFSSPI surface roughness models."""

    NONE = pb.NONE
    EXPONENTIAL = pb.EXPONENTIAL
    HAMMERSTAD = pb.HAMMERSTAD


class ImprovedLossModel(Enum):
    """Provides an enum representing HFSSPI improved loss models."""

    LEVEL_1 = pb.LEVEL_1
    LEVEL_2 = pb.LEVEL_2
    LEVEL_3 = pb.LEVEL_3


class ConductorModeling(Enum):
    """Provides an enum representing HFSSPI conductor modeling options."""

    MESH_INSIDE = pb.MESH_INSIDE
    IMPEDANCE_BOUNDARY = pb.IMPEDANCE_BOUNDARY


class ErrorTolerance(Enum):
    """Provides an enum representing HFSSPI error tolerance values."""

    ET_0_0 = pb.ET_0_0
    ET_0_02 = pb.ET_0_02
    ET_0_04 = pb.ET_0_04
    ET_0_06 = pb.ET_0_06
    ET_0_08 = pb.ET_0_08
    ET_0_1 = pb.ET_0_1
    ET_0_2 = pb.ET_0_2
    ET_0_5 = pb.ET_0_5
    ET_1_0 = pb.ET_1_0


class HFSSPISimulationSettings(SimulationSettings):
    """Represents HFSSPI simulation settings."""

    @property
    def general(self) -> HFSSPIGeneralSettings:
        """:class:`.HFSSPIGeneralSettings`: General settings for HFSSPI simulations."""
        return HFSSPIGeneralSettings(self)

    @property
    def net_processing(self) -> HFSSPINetProcessingSettings:
        """:class:`.HFSSPINetProcessingSettings`: Net processing settings for HFSSPI simulations."""
        return HFSSPINetProcessingSettings(self)

    @property
    def power_ground_nets(self) -> HFSSPIPowerGroundNetsSettings:
        """:class:`.HFSSPIPowerGroundNetsSettings`: Power/ground nets settings for HFSSPI simulations."""
        return HFSSPIPowerGroundNetsSettings(self)

    @property
    def signal_nets(self) -> HFSSPISignalNetsSettings:
        """:class:`.HFSSPISignalNetsSettings`: Signal nets settings for HFSSPI simulations."""
        return HFSSPISignalNetsSettings(self)


class HFSSPIGeneralSettings(SimulationSettingsBase):
    """Represents HFSSPI general settings."""

    __stub: HFSSPIGeneralSettingsServiceStub = StubAccessor(StubType.hfss_pi_general_sim_settings)

    @property
    def simulation_preference(self) -> HFSSPISimulationPreference:
        """:class:`.HFSSPISimulationPreference`: Simulation preference. \
            Balanced (i.e., use less memory) or Accuracy (i.e., use more memory)."""
        return HFSSPISimulationPreference(
            self.__stub.GetPISliderPos(self.msg).hfss_pi_simulation_preference
        )

    @simulation_preference.setter
    def simulation_preference(self, simulation_preference: HFSSPISimulationPreference):
        self.__stub.SetPISliderPos(
            pb.HFSSPISimulationPreferencePropertyMessage(
                target=self.msg, hfss_pi_simulation_preference=simulation_preference.value
            )
        )

    @property
    def model_type(self) -> HFSSPIModelType:
        """:class:`.HFSSPIModelType`: (General Mode Only) Model type."""
        return HFSSPIModelType(self.__stub.GetHFSSPIModelType(self.msg).hfss_pi_model_type)

    @model_type.setter
    def model_type(self, hfss_pi_model_type: HFSSPIModelType):
        self.__stub.SetHFSSPIModelType(
            pb.HFSSPIModelTypePropertyMessage(
                target=self.msg, hfss_pi_model_type=hfss_pi_model_type.value
            )
        )

    @property
    def min_plane_area_to_mesh(self) -> str:
        """:obj:`str`: (General Mode Only) The minimum plane area to mesh. \
            Ignore geometry smaller than this value."""
        return self.__stub.GetMinPlaneAreaToMesh(self.msg).value

    @min_plane_area_to_mesh.setter
    def min_plane_area_to_mesh(self, min_plane_area_to_mesh: str):
        self.__stub.SetMinPlaneAreaToMesh(
            messages.string_property_message(self, min_plane_area_to_mesh)
        )

    @property
    def min_void_area_to_mesh(self) -> str:
        """:obj:`str`: (General Mode Only) The minimum void area to mesh. Ignore voids smaller than this value."""
        return self.__stub.GetMinVoidAreaToMesh(self.msg).value

    @min_void_area_to_mesh.setter
    def min_void_area_to_mesh(self, min_void_area_to_mesh: str):
        self.__stub.SetMinVoidAreaToMesh(
            messages.string_property_message(self, min_void_area_to_mesh)
        )

    @property
    def snap_length_threshold(self) -> str:
        """:obj:`str`: (General Mode Only) The snap length threshold. \
            Snap vertices separated by less than this value."""
        return self.__stub.GetSnapLengthThreshold(self.msg).value

    @snap_length_threshold.setter
    def snap_length_threshold(self, snap_length_threshold: str):
        self.__stub.SetSnapLengthThreshold(
            messages.string_property_message(self, snap_length_threshold)
        )

    @property
    def include_enhanced_bondwire_modeling(self) -> bool:
        """:obj:`bool`: Flag indicating whether to include enhanced bondwire modeling. This can slow simulation."""
        return self.__stub.GetIncludeEnhancedBondWireModeling(self.msg).value

    @include_enhanced_bondwire_modeling.setter
    def include_enhanced_bondwire_modeling(self, include_enhanced_bondwire_modeling: bool):
        self.__stub.SetIncludeEnhancedBondWireModeling(
            messages.bool_property_message(self, include_enhanced_bondwire_modeling)
        )

    @property
    def surface_roughness_model(self) -> SurfaceRoughnessModel:
        """:class:`.SurfaceRoughnessModel`: Surface roughness model."""
        return SurfaceRoughnessModel(
            self.__stub.GetSurfaceRoughnessModel(self.msg).surface_roughness_model
        )

    @surface_roughness_model.setter
    def surface_roughness_model(self, surface_roughness_model: SurfaceRoughnessModel):
        self.__stub.SetSurfaceRoughnessModel(
            pb.SurfaceRoughnessModelPropertyMessage(
                target=self.msg, surface_roughness_model=surface_roughness_model.value
            )
        )

    @property
    def rms_surface_roughness(self) -> str:
        """:obj:`str`: RMS surface roughness."""
        return self.__stub.GetRMSSurfaceRoughness(self.msg).value

    @rms_surface_roughness.setter
    def rms_surface_roughness(self, rms_surface_roughness: str):
        self.__stub.SetRMSSurfaceRoughness(
            messages.string_property_message(self, rms_surface_roughness)
        )

    @property
    def perform_erc(self) -> bool:
        """:obj:`bool`: (General Mode Only) Flag indicating whether to \
            perform error checking while generating the solver input file."""
        return self.__stub.GetPerformERC(self.msg).value

    @perform_erc.setter
    def perform_erc(self, perform_erc: bool):
        self.__stub.SetPerformERC(messages.bool_property_message(self, perform_erc))


class HFSSPINetProcessingSettings(SimulationSettingsBase):
    """Represents HFSSPI net processing settings."""

    __stub: HFSSPINetProcessingSettingsServiceStub = StubAccessor(
        StubType.hfss_pi_net_processing_sim_settings
    )

    @property
    def auto_select_nets_for_simulation(self) -> bool:
        """:obj:`bool`: Flag indicating whether to automatically select nets for simulation."""
        return self.__stub.GetAutoSelectNetsForSimulation(self.msg).value

    @auto_select_nets_for_simulation.setter
    def auto_select_nets_for_simulation(self, auto_select_nets_for_simulation: bool):
        self.__stub.SetAutoSelectNetsForSimulation(
            messages.bool_property_message(self, auto_select_nets_for_simulation)
        )

    @property
    def ignore_dummy_nets_for_selected_nets(self) -> bool:
        """:obj:`bool`: Flag indicating whether to ignore dummy nets for selected nets."""
        return self.__stub.GetIgnoreDummyNetsForSelectedNets(self.msg).value

    @ignore_dummy_nets_for_selected_nets.setter
    def ignore_dummy_nets_for_selected_nets(self, ignore_dummy_nets_for_selected_nets: bool):
        self.__stub.SetIgnoreDummyNetsForSelectedNets(
            messages.bool_property_message(self, ignore_dummy_nets_for_selected_nets)
        )

    @property
    def include_nets(self) -> List[str]:
        """:obj:`list` of :obj:`str`: Nets to include in HFSSPI simulation."""
        return self.__stub.GetIncludeNets(self.msg).strings

    @include_nets.setter
    def include_nets(self, value: List[str]):
        self.__stub.SetIncludeNets(messages.strings_property_message(self, value))


class HFSSPIPowerGroundNetsSettings(SimulationSettingsBase):
    """Represents HFSSPI power/ground nets settings."""

    __stub: HFSSPIPowerGroundNetsServiceStub = StubAccessor(
        StubType.hfss_pi_power_ground_sim_settings
    )

    @property
    def improved_loss_model(self):
        """:class:`.ImprovedLossModel`: Improved loss model."""
        return ImprovedLossModel(self.__stub.GetImprovedLossModel(self.msg).improved_loss_model)

    @improved_loss_model.setter
    def improved_loss_model(self, improved_loss_model: ImprovedLossModel):
        self.__stub.SetImprovedLossModel(
            pb.ImprovedLossModelPropertyMessage(
                target=self.msg, improved_loss_model=improved_loss_model.value
            )
        )

    @property
    def auto_detect_ignore_small_holes_min_diameter(self) -> bool:
        """:obj:`bool`: Flag indicating whether to automatically detect a diameter \
            that holes smaller than the diameter will be ignored."""
        return self.__stub.GetAutoDetectIgnoreSmallHolesMinDiameter(self.msg).value

    @auto_detect_ignore_small_holes_min_diameter.setter
    def auto_detect_ignore_small_holes_min_diameter(
        self, auto_detect_ignore_small_holes_min_diameter: bool
    ):
        self.__stub.SetAutoDetectIgnoreSmallHolesMinDiameter(
            messages.bool_property_message(self, auto_detect_ignore_small_holes_min_diameter)
        )

    @property
    def ignore_small_holes_min_diameter(self) -> str:
        """:obj:`str`: Diameter that holes smaller than the diameter will be ignored."""
        return self.__stub.GetIgnoreSmallHolesMinDiameter(self.msg).value

    @ignore_small_holes_min_diameter.setter
    def ignore_small_holes_min_diameter(self, ignore_small_holes_min_diameter: str):
        self.__stub.SetIgnoreSmallHolesMinDiameter(
            messages.string_property_message(self, ignore_small_holes_min_diameter)
        )


class HFSSPISignalNetsSettings(SimulationSettingsBase):
    """Represents HFSSPI signal nets settings."""

    __stub: HFSSPISignalNetsSettingsServiceStub = StubAccessor(
        StubType.hfss_pi_signal_nets_sim_settings
    )

    @property
    def error_tolerance(self) -> ErrorTolerance:
        """:class:`.ErrorTolerance`: Error tolerance."""
        return ErrorTolerance(self.__stub.GetSignalNetsErrorTolerance(self.msg).error_tolerance)

    @error_tolerance.setter
    def error_tolerance(self, error_tolerance: ErrorTolerance):
        self.__stub.SetSignalNetsErrorTolerance(
            pb.ErrorTolerancePropertyMessage(target=self.msg, error_tolerance=error_tolerance.value)
        )

    @property
    def conductor_modeling(self) -> ConductorModeling:
        """:class:`.ConductorModeling`: Conductor modeling. \
            When using surface roughness, users must use IMPEDANCE_BOUNDARY."""
        return ConductorModeling(
            self.__stub.GetSignalNetsConductorModeling(self.msg).conductor_modeling
        )

    @conductor_modeling.setter
    def conductor_modeling(self, conductor_modeling: ConductorModeling):
        self.__stub.SetSignalNetsConductorModeling(
            pb.ConductorModelingPropertyMessage(
                target=self.msg, conductor_modeling=conductor_modeling.value
            )
        )

    @property
    def include_improved_loss_handling(self) -> bool:
        """:obj:`bool`: Flag indicating whether to include improved metal loss handling. \
            Enabling this option can significantly slow simulation time."""
        return self.__stub.GetSignalNetsIncludeImprovedLossHandling(self.msg).value

    @include_improved_loss_handling.setter
    def include_improved_loss_handling(self, include_improved_loss_handling: bool):
        self.__stub.SetSignalNetsIncludeImprovedLossHandling(
            messages.bool_property_message(self, include_improved_loss_handling)
        )

    @property
    def include_improved_dielectric_fill_refinement(self) -> bool:
        """:obj:`bool`: Flag indicating whether to include improved dielectric fill refinement. \
            Activating Improved Dielectric Fill Refinement in Metal Layers can significantly slow simulation time."""
        return self.__stub.GetSignalNetsIncludeImprovedDielectricFillRefinement(self.msg).value

    @include_improved_dielectric_fill_refinement.setter
    def include_improved_dielectric_fill_refinement(
        self, include_improved_dielectric_fill_refinement: bool
    ):
        self.__stub.SetSignalNetsIncludeImprovedDielectricFillRefinement(
            messages.bool_property_message(self, include_improved_dielectric_fill_refinement)
        )
