"""HFSS simulation settings."""

from enum import Enum

import ansys.api.edb.v1.hfss_pi_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import (
    HFSSPIAdvancedSettingsServiceStub,
    HFSSPIGeneralSettingsServiceStub,
    HFSSPISolverSettingsServiceStub,
    StubAccessor,
    StubType,
)
from ansys.edb.core.simulation_setup.simulation_settings import (
    AdvancedMeshingSettingsServiceStub,
    AdvancedSettingsServiceStub,
    SimulationSettings,
    SimulationSettingsBase,
)


class HFSSPIModelType(Enum):
    """Provides an enum representing HFSS adaptive solution types."""

    PCB = pb.HFSSPI_PCB
    PACKAGE = pb.HFSSPI_PACKAGE
    RDL = pb.HFSSPI_RDL


class HFSSPISimulationSettings(SimulationSettings):
    """Represents HFSSPI simulation settings."""

    @property
    def general(self):
        """:class:`.HFSSPIGeneralSettings`: General settings for HFSSPI simulations."""
        return HFSSPIGeneralSettings(self)

    @property
    def advanced(self):
        """:class:`.HFSSPIAdvancedSettings`: Advanced settings for HFSSPI simulations."""
        return HFSSPIAdvancedSettings(self)

    @property
    def solver(self):
        """:class:`.HFSSPISolverSettings`: Solver settings for HFSSPI simulations."""
        return HFSSPISolverSettings(self)


class HFSSPIGeneralSettings(SimulationSettingsBase):
    """Represents general settings for HFSSPI simulations."""

    __stub: HFSSPIGeneralSettingsServiceStub = StubAccessor(StubType.hfss_pi_general_sim_settings)

    @property
    def model_type(self):
        """:class:`.HFSSPIModelType`: Model type."""
        return HFSSPIModelType(self.__stub.GetHFSSPIModelType(self.msg).hfss_pi_model_type)

    @model_type.setter
    def model_type(self, hfss_pi_model_type):
        self.__stub.SetHFSSPIModelType(
            pb.HFSSPIModelTypePropertyMessage(
                target=self.msg, hfss_pi_model_type=hfss_pi_model_type.value
            )
        )

    @property
    def use_auto_mesh_region(self):
        """:obj:`bool`: Flag indicating if auto mesh regions are used."""
        return self.__stub.GetUseAutoMeshRegion(self.msg).value

    @use_auto_mesh_region.setter
    def use_auto_mesh_region(self, use_auto_mesh_region):
        self.__stub.SetUseAutoMeshRegion(messages.bool_property_message(self, use_auto_mesh_region))

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


class HFSSPISolverSettings(SimulationSettingsBase):
    """Representis solver settings for HFSSPI simulations."""

    __stub: HFSSPISolverSettingsServiceStub = StubAccessor(StubType.hfss_pi_solver_sim_settings)

    @property
    def enhanced_low_frequency_accuracy(self):
        """:obj:`bool`: Flag indicating if enhanced low-frequency accuracy is enabled during simulation."""
        return self.__stub.GetEnhancedLowFrequencyAccuracy(self.msg).value

    @enhanced_low_frequency_accuracy.setter
    def enhanced_low_frequency_accuracy(self, enhanced_low_frequency_accuracy):
        self.__stub.SetEnhancedLowFrequencyAccuracy(
            messages.bool_property_message(self, enhanced_low_frequency_accuracy)
        )

    @property
    def via_area_cutoff_circ_elems(self) -> str:
        """:obj:`str`: Pwr/Gnd vias with an area smaller than this value are simplified during simulation."""
        return self.__stub.GetViaAreaCutoffCircElems(self.msg).value

    @via_area_cutoff_circ_elems.setter
    def via_area_cutoff_circ_elems(self, via_area_cutoff_circ_elems):
        self.__stub.SetViaAreaCutoffCircElems(
            messages.string_property_message(self, via_area_cutoff_circ_elems)
        )


class HFSSPIAdvancedSettings(SimulationSettingsBase):
    """Represents advanced settings for HFSSPI simulations."""

    __hfss_pi_stub: HFSSPIAdvancedSettingsServiceStub = StubAccessor(
        StubType.hfss_pi_advanced_sim_settings
    )
    __advanced_sim_settings_stub: AdvancedSettingsServiceStub = StubAccessor(
        StubType.advanced_sim_settings
    )
    __advanced_mesh_sim_settings_stub: AdvancedMeshingSettingsServiceStub = StubAccessor(
        StubType.advanced_mesh_sim_settings
    )

    @property
    def small_void_area(self):
        """:obj:`float`: Voids with an area smaller than this value are ignored during simulation."""
        return self.__advanced_sim_settings_stub.GetSmallVoidArea(self.msg).value

    @small_void_area.setter
    def small_void_area(self, small_void_area):
        self.__advanced_sim_settings_stub.SetSmallVoidArea(
            messages.double_property_message(self, small_void_area)
        )

    @property
    def small_plane_area(self) -> str:
        """:obj:`str`: Planes with an area smaller than this value are ignored during simulation."""
        return self.__hfss_pi_stub.GetSmallPlaneArea(self.msg).value

    @small_plane_area.setter
    def small_plane_area(self, small_plane_area: str):
        self.__hfss_pi_stub.SetSmallPlaneArea(
            messages.string_property_message(self, small_plane_area)
        )

    @property
    def remove_floating_geometry(self):
        """:obj:`bool`: Flag indicating if a geometry not connected to any other geometry is removed."""
        return self.__advanced_sim_settings_stub.GetRemoveFloatingGeometry(self.msg).value

    @remove_floating_geometry.setter
    def remove_floating_geometry(self, remove_floating_geometry):
        self.__advanced_sim_settings_stub.SetRemoveFloatingGeometry(
            messages.bool_property_message(self, remove_floating_geometry)
        )

    @property
    def zero_metal_layer_thickness(self) -> str:
        """:obj:`str`: Pwr/Gnd layers with a thickness smaller than this value are simplified during simulation."""
        return self.__hfss_pi_stub.GetZeroMetalLayerThickness(self.msg).value

    @zero_metal_layer_thickness.setter
    def zero_metal_layer_thickness(self, zero_metal_layer_thickness):
        self.__hfss_pi_stub.SetZeroMetalLayerThickness(
            messages.string_property_message(self, zero_metal_layer_thickness)
        )

    @property
    def auto_model_resolution(self):
        """:obj:`bool`: Flag indicating if model resolution is automatically calculated."""
        return self.__hfss_pi_stub.GetICModeAutoResolution(self.msg).value

    @auto_model_resolution.setter
    def auto_model_resolution(self, auto_model_resolution):
        self.__hfss_pi_stub.SetICModeAutoResolution(
            messages.bool_property_message(self, auto_model_resolution)
        )

    @property
    def model_resolution_length(self):
        """:obj:`str`: Model resolution to use when manually setting the model resolution."""
        return self.__hfss_pi_stub.GetICModeLength(self.msg).value

    @model_resolution_length.setter
    def model_resolution_length(self, model_resolution_length):
        self.__hfss_pi_stub.SetICModeLength(
            messages.string_property_message(self, model_resolution_length)
        )

    @property
    def max_num_arc_points(self):
        """:obj:`str`: Maximum number of points used to approximate arcs."""
        return self.__advanced_mesh_sim_settings_stub.GetMaxNumArcPoints(self.msg).value

    @max_num_arc_points.setter
    def max_num_arc_points(self, max_num_arc_points):
        self.__advanced_mesh_sim_settings_stub.SetMaxNumArcPoints(
            messages.uint64_property_message(self, max_num_arc_points)
        )

    @property
    def use_arc_chord_error_approx(self):
        """:obj:`bool`: Flag indicating if arc chord error approximation is used."""
        return self.__advanced_mesh_sim_settings_stub.GetUseArcChordErrorApprox(self.msg).value

    @use_arc_chord_error_approx.setter
    def use_arc_chord_error_approx(self, use_arc_chord_error_approx):
        self.__advanced_mesh_sim_settings_stub.SetUseArcChordErrorApprox(
            messages.bool_property_message(self, use_arc_chord_error_approx)
        )

    @property
    def arc_to_chord_error(self):
        """:obj:`str`: Maximum allowable arc to chord error."""
        return self.__advanced_mesh_sim_settings_stub.GetArcChordErrorApprox(self.msg).value

    @arc_to_chord_error.setter
    def arc_to_chord_error(self, arc_to_chord_error):
        self.__advanced_mesh_sim_settings_stub.SetArcChordErrorApprox(
            messages.string_property_message(self, arc_to_chord_error)
        )

    @property
    def num_via_sides(self):
        """:obj:`int`: Number of sides a via is considered to have."""
        return self.__stub.GetNumViaSides(self.msg).value

    @num_via_sides.setter
    def num_via_sides(self, num_via_sides):
        self.__stub.SetNumViaSides(messages.uint64_property_message(self, num_via_sides))

    @property
    def mesh_for_via_plating(self):
        """:obj:`bool`: Flag indicating if meshing for via plating is enabled."""
        return self.__stub.GetMeshForViaPlating(self.msg).value

    @mesh_for_via_plating.setter
    def mesh_for_via_plating(self, mesh_for_via_plating):
        self.__stub.SetMeshForViaPlating(messages.bool_property_message(self, mesh_for_via_plating))

    @property
    def via_material(self):
        """:obj:`str`: Default via material."""
        return self.__stub.GetViaMaterial(self.msg).value

    @via_material.setter
    def via_material(self, via_material):
        self.__stub.SetViaMaterial(messages.string_property_message(self, via_material))
