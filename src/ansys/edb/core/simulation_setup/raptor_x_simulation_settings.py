"""RaptorX simulation settings."""

import ansys.api.edb.v1.raptor_x_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import (
    RaptorXAdvancedSettingsServiceStub,
    RaptorXGeneralSettingsServiceStub,
    StubAccessor,
    StubType,
)
from ansys.edb.core.simulation_setup.simulation_settings import (
    SimulationSettings,
    SimulationSettingsBase,
)


def _translate_options_dictionary(dictionary):
    return {
        key: messages.strings_message([val for val in vals]) for (key, vals) in dictionary.items()
    }


def _to_options_dict(msg):
    return {key: [val for val in vals.strings] for (key, vals) in msg.options.items()}


def _to_raptor_x_sim_settings_options_property_msg(obj, options):
    return pb.RaptorXSimSettingsOptionsPropertyMessage(
        target=obj.msg,
        value=pb.RaptorXSimSettingsOptionsMessage(
            options={
                key: messages.strings_message([val for val in vals])
                for (key, vals) in options.items()
            }
        ),
    )


class RaptorXSimulationSettings(SimulationSettings):
    """Represents SIWave simulation settings."""

    @property
    def general(self):
        """:class:`.RaptorXGeneralSettings`: General settings for RaptorX simulations."""
        return RaptorXGeneralSettings(self._sim_setup)

    @property
    def advanced(self):
        """:class:`.RaptorXAdvancedSettings`: Advanced settings for RaptorX simulations."""
        return RaptorXAdvancedSettings(self._sim_setup)


class RaptorXGeneralSettings(SimulationSettingsBase):
    """Represents general settings for RaptorX simulations."""

    __stub: RaptorXGeneralSettingsServiceStub = StubAccessor(StubType.raptor_x_general_sim_settings)

    @property
    def use_gold_em_solver(self):
        """:obj:`bool`: Flag indicating if the gold em solver is used. If ``False``, \
        the fast em solver is used."""
        return self.__stub.GetUseGoldEMSolver(self.msg).value

    @use_gold_em_solver.setter
    def use_gold_em_solver(self, use_gold_em_solver):
        self.__stub.SetUseGoldEMSolver(messages.bool_property_message(self, use_gold_em_solver))

    @property
    def max_frequency(self):
        """:obj:`str`: Maximum frequency value, which controls the tightness of the model mesh."""
        return self.__stub.GetMaxFrequency(self.msg).value

    @max_frequency.setter
    def max_frequency(self, max_frequency):
        self.__stub.SetMaxFrequency(messages.string_property_message(self, max_frequency))

    @property
    def global_temperature(self):
        """:obj:`float`: Simulation temperature in degrees Celsius."""
        return self.__stub.GetGlobalTemperature(self.msg).value

    @global_temperature.setter
    def global_temperature(self, global_temperature):
        self.__stub.SetGlobalTemperature(messages.double_property_message(self, global_temperature))

    @property
    def save_netlist(self):
        """:obj:`bool`: Flag indicating if the netlist output is saved."""
        return self.__stub.GetSaveNetlist(self.msg).value

    @save_netlist.setter
    def save_netlist(self, save_netlist):
        self.__stub.SetSaveNetlist(messages.bool_property_message(self, save_netlist))

    @property
    def netlist_export_spectre(self):
        """:obj:`bool`: Flag indicating if the netlist is exported in Spectre format."""
        return self.__stub.GetNetlistExportSpectre(self.msg).value

    @netlist_export_spectre.setter
    def netlist_export_spectre(self, netlist_export_spectre):
        self.__stub.SetNetlistExportSpectre(
            messages.bool_property_message(self, netlist_export_spectre)
        )

    @property
    def save_rfm(self):
        """:obj:`bool`: Flag indicating if an RFM file is exported."""
        return self.__stub.GetSaveRFM(self.msg).value

    @save_rfm.setter
    def save_rfm(self, save_rfm):
        self.__stub.SetSaveRFM(messages.bool_property_message(self, save_rfm))


class RaptorXAdvancedSettings(SimulationSettingsBase):
    """Represents advanced settings for RaptorX simulations."""

    __stub: RaptorXAdvancedSettingsServiceStub = StubAccessor(StubType.raptor_x_adv_sim_settings)

    @property
    def use_mesh_frequency(self):
        """:obj:`bool`: Flag indicating if the default meshing frequency is overridden."""
        return self.__stub.GetUseMeshFrequency(self.msg).value

    @use_mesh_frequency.setter
    def use_mesh_frequency(self, use_mesh_frequency):
        self.__stub.SetUseMeshFrequency(messages.bool_property_message(self, use_mesh_frequency))

    @property
    def mesh_frequency(self):
        """:obj:`str`: Mesh frequency override."""
        return self.__stub.GetMeshFrequency(self.msg).value

    @mesh_frequency.setter
    def mesh_frequency(self, mesh_frequency):
        self.__stub.SetMeshFrequency(messages.string_property_message(self, mesh_frequency))

    @property
    def use_edge_mesh(self):
        """:obj:`bool`: Flag indicating if the edge mesh is used."""
        return self.__stub.GetUseEdgeMesh(self.msg).value

    @use_edge_mesh.setter
    def use_edge_mesh(self, use_edge_mesh):
        self.__stub.SetUseEdgeMesh(messages.bool_property_message(self, use_edge_mesh))

    @property
    def edge_mesh(self):
        """:obj:`str`: Thickness and width of the exterior conductor filament."""
        return self.__stub.GetEdgeMesh(self.msg).value

    @edge_mesh.setter
    def edge_mesh(self, edge_mesh):
        self.__stub.SetEdgeMesh(messages.string_property_message(self, edge_mesh))

    @property
    def use_cells_per_wavelength(self):
        """:obj:`bool`: Flag indicating if cells per wavelength are used."""
        return self.__stub.GetUseCellsPerWavelength(self.msg).value

    @use_cells_per_wavelength.setter
    def use_cells_per_wavelength(self, use_cells_per_wavelength):
        self.__stub.SetUseCellsPerWavelength(
            messages.bool_property_message(self, use_cells_per_wavelength)
        )

    @property
    def cells_per_wavelength(self):
        """:obj:`int`: Number of cells that fit under each wavelength."""
        return self.__stub.GetCellsPerWavelength(self.msg).value

    @cells_per_wavelength.setter
    def cells_per_wavelength(self, cells_per_wavelength):
        self.__stub.SetCellsPerWavelength(messages.int_property_message(self, cells_per_wavelength))

    @property
    def use_plane_projection_factor(self):
        """:obj:`bool`: Flag indicating if the plane projection factor is used."""
        return self.__stub.GetUsePlaneProjectionFactor(self.msg).value

    @use_plane_projection_factor.setter
    def use_plane_projection_factor(self, use_plane_projection_factor):
        self.__stub.SetUsePlaneProjectionFactor(
            messages.bool_property_message(self, use_plane_projection_factor)
        )

    @property
    def plane_projection_factor(self):
        """:obj:`float`: Plane projection factor for reducing the mesh complexity of large metal planes."""
        return self.__stub.GetPlaneProjectionFactor(self.msg).value

    @plane_projection_factor.setter
    def plane_projection_factor(self, plane_projection_factor):
        self.__stub.SetPlaneProjectionFactor(
            messages.double_property_message(self, plane_projection_factor)
        )

    @property
    def use_relaxed_z_axis(self):
        """:obj:`bool`: Flag indicating if simplified meshing is used along the z axis."""
        return self.__stub.GetUseRelaxedZAxis(self.msg).value

    @use_relaxed_z_axis.setter
    def use_relaxed_z_axis(self, use_relaxed_z_axis):
        self.__stub.SetUseRelaxedZAxis(messages.bool_property_message(self, use_relaxed_z_axis))

    @property
    def use_eliminate_slit_per_holes(self):
        """:obj:`bool`: Flag indicating if strain relief or thermal relief slits and holes are removed."""
        return self.__stub.GetUseEliminateSlitPerHoles(self.msg).value

    @use_eliminate_slit_per_holes.setter
    def use_eliminate_slit_per_holes(self, use_eliminate_slit_per_holes):
        self.__stub.SetUseEliminateSlitPerHoles(
            messages.bool_property_message(self, use_eliminate_slit_per_holes)
        )

    @property
    def eliminate_slit_per_holes(self):
        """:obj:`float`: Threshold for strain or thermal relief slits and hole polygon areas."""
        return self.__stub.GetEliminateSlitPerHoles(self.msg).value

    @eliminate_slit_per_holes.setter
    def eliminate_slit_per_holes(self, eliminate_slit_per_holes):
        self.__stub.SetEliminateSlitPerHoles(
            messages.double_property_message(self, eliminate_slit_per_holes)
        )

    @property
    def use_auto_removal_sliver_poly(self):
        """:obj:`bool`: Flag indicating if slight misaligned overlapping polygons are to be automatically aligned."""
        return self.__stub.GetUseAutoRemovalSliverPoly(self.msg).value

    @use_auto_removal_sliver_poly.setter
    def use_auto_removal_sliver_poly(self, use_auto_removal_sliver_poly):
        self.__stub.SetUseAutoRemovalSliverPoly(
            messages.bool_property_message(self, use_auto_removal_sliver_poly)
        )

    @property
    def auto_removal_sliver_poly(self):
        """:obj:`float`: Automatic sliver polygon removal tolerance."""
        return self.__stub.GetAutoRemovalSliverPoly(self.msg).value

    @auto_removal_sliver_poly.setter
    def auto_removal_sliver_poly(self, auto_removal_sliver_poly):
        self.__stub.SetAutoRemovalSliverPoly(
            messages.double_property_message(self, auto_removal_sliver_poly)
        )

    @property
    def use_accelerate_via_extraction(self):
        """:obj:`bool`: Flag indicating if neighboring vias are simplified/merged."""
        return self.__stub.GetUseAccelerateViaExtraction(self.msg).value

    @use_accelerate_via_extraction.setter
    def use_accelerate_via_extraction(self, use_accelerate_via_extraction):
        self.__stub.SetUseAccelerateViaExtraction(
            messages.bool_property_message(self, use_accelerate_via_extraction)
        )

    @property
    def use_enable_substrate_network_extraction(self):
        """:obj:`bool`: Flag indicating if modeling of substrate coupling effects \
        is enabled using equivalent distributed RC networks."""
        return self.__stub.GetUseEnableSubstrateNetworkExtraction(self.msg).value

    @use_enable_substrate_network_extraction.setter
    def use_enable_substrate_network_extraction(self, use_enable_substrate_network_extraction):
        self.__stub.SetUseEnableSubstrateNetworkExtraction(
            messages.bool_property_message(self, use_enable_substrate_network_extraction)
        )

    @property
    def use_lde(self):
        """:obj:`bool`: Flag indicating if variations in resistivity are taken into account."""
        return self.__stub.GetUseLDE(self.msg).value

    @use_lde.setter
    def use_lde(self, use_lde):
        self.__stub.SetUseLDE(messages.bool_property_message(self, use_lde))

    @property
    def use_extract_floating_metals_dummy(self):
        """:obj:`bool`: Flag indicating if floating metals are modeled as dummy fills."""
        return self.__stub.GetUseExtractFloatingMetalsDummy(self.msg).value

    @use_extract_floating_metals_dummy.setter
    def use_extract_floating_metals_dummy(self, use_extract_floating_metals_dummy):
        self.__stub.SetUseExtractFloatingMetalsDummy(
            messages.bool_property_message(self, use_extract_floating_metals_dummy)
        )

    @property
    def use_extract_floating_metals_floating(self):
        """:obj:`bool`: Flag indicating if floating metals are modeled as floating nets."""
        return self.__stub.GetUseExtractFloatingMetalsFloating(self.msg).value

    @use_extract_floating_metals_floating.setter
    def use_extract_floating_metals_floating(self, use_extract_floating_metals_floating):
        self.__stub.SetUseExtractFloatingMetalsFloating(
            messages.bool_property_message(self, use_extract_floating_metals_floating)
        )

    @property
    def use_enable_etch_transform(self):
        """:obj:`bool`: Flag indicating if layout is "pre-distorted" based on foundry rules."""
        return self.__stub.GetUseEnableEtchTransform(self.msg).value

    @use_enable_etch_transform.setter
    def use_enable_etch_transform(self, use_enable_etch_transform):
        self.__stub.SetUseEnableEtchTransform(
            messages.bool_property_message(self, use_enable_etch_transform)
        )

    @property
    def use_enable_hybrid_extraction(self):
        """:obj:`bool`: Flag indicating if the modeler is to split the layout into \
        two parts in an attempt to decrease the complexity."""
        return self.__stub.GetUseEnableHybridExtraction(self.msg).value

    @use_enable_hybrid_extraction.setter
    def use_enable_hybrid_extraction(self, use_enable_hybrid_extraction):
        self.__stub.SetUseEnableHybridExtraction(
            messages.bool_property_message(self, use_enable_hybrid_extraction)
        )

    @property
    def use_enable_advanced_cap_effects(self):
        """:obj:`bool`: Flag indicating if capacitance-related effects such as conformal dielectrics are applied."""
        return self.__stub.GetUseEnableAdvancedCapEffects(self.msg).value

    @use_enable_advanced_cap_effects.setter
    def use_enable_advanced_cap_effects(self, use_enable_advanced_cap_effects):
        self.__stub.SetUseEnableAdvancedCapEffects(
            messages.bool_property_message(self, use_enable_advanced_cap_effects)
        )

    @property
    def use_override_shrink_factor(self):
        """:obj:`bool`: Flag indicating if shrink factor is overridden."""
        return self.__stub.GetUseOverrideShrinkFac(self.msg).value

    @use_override_shrink_factor.setter
    def use_override_shrink_factor(self, use_override_shrink_factor):
        self.__stub.SetUseOverrideShrinkFac(
            messages.bool_property_message(self, use_override_shrink_factor)
        )

    @property
    def override_shrink_factor(self):
        """:obj:`float`: Shrink factor override value."""
        return self.__stub.GetOverrideShrinkFac(self.msg).value

    @override_shrink_factor.setter
    def override_shrink_factor(self, override_shrink_factor):
        self.__stub.SetOverrideShrinkFac(
            messages.double_property_message(self, override_shrink_factor)
        )

    @property
    def advanced_options(self):
        """:obj:`dict` { :obj:`str` : :obj:`list`[:obj:`str`] }: Advanced options."""
        return _to_options_dict(self.__stub.GetAdvancedOptions(self.msg))

    @advanced_options.setter
    def advanced_options(self, advanced_options):
        self.__stub.SetAdvancedOptions(
            _to_raptor_x_sim_settings_options_property_msg(self, advanced_options)
        )

    @property
    def net_settings_options(self):
        """:obj:`dict` { :obj:`str` : :obj:`list`[:obj:`str`] }: Options for net settings."""
        return _to_options_dict(self.__stub.GetNetSettingsOptions(self.msg))

    @net_settings_options.setter
    def net_settings_options(self, net_settings_options):
        self.__stub.SetNetSettingsOptions(
            _to_raptor_x_sim_settings_options_property_msg(self, net_settings_options)
        )
