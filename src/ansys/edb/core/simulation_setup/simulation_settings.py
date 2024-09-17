"""Simulation Settings."""
from enum import Enum

import ansys.api.edb.v1.simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import (
    AdvancedMeshingSettingsServiceStub,
    AdvancedSettingsServiceStub,
    SettingsOptionsServiceStub,
    SimulationSettingsServiceStub,
    SolverSettingsServiceStub,
    StubAccessor,
    StubType,
)


class ViaStyle(Enum):
    """Enum representing via modeling styles."""

    WIREBOND = pb.WIREBOND
    RIBBON = pb.RIBBON
    MESH = pb.MESH
    FIELD = pb.FIELD
    NUM_VIA_STYLE = pb.NUM_VIA_STYLE


class ModelType(Enum):
    """Enum representing defeature model types."""

    GENERAL_MODEL = pb.GENERAL_MODEL
    IC_MODEL = pb.IC_MODEL


class SimulationSettingsBase:
    """Internal base class for simulation settings."""

    def __init__(self, sim_setup):
        """Create a SimulationSettingsBase object."""
        self._sim_setup = sim_setup

    @property
    def msg(self):
        """:obj:`EDBObjMessage`: Protobuf message that represents this object's ID.

        This property is read-only.
        """
        return self._sim_setup.msg


class SimulationSettings(SimulationSettingsBase):
    """Class representing base simulation settings."""

    __stub: SimulationSettingsServiceStub = StubAccessor(StubType.sim_settings)

    @property
    def enabled(self):
        """:obj:`bool`: Flag indicating if the simulation setup is enabled."""
        return self.__stub.GetEnabled(self.msg).value

    @enabled.setter
    def enabled(self, enabled):
        self.__stub.SetEnabled(messages.bool_property_message(self, enabled))


class SettingsOptions(SimulationSettingsBase):
    """Class representing options for base simulation settings."""

    __stub: SettingsOptionsServiceStub = StubAccessor(StubType.sim_settings_options)

    @property
    def do_lamda_refine(self):
        """:obj:`bool`: Flag indicating if lambda refinement is used during meshing."""
        return self.__stub.GetDoLamdaRefineFlag(self.msg).value

    @do_lamda_refine.setter
    def do_lamda_refine(self, do_lamda_refine):
        self.__stub.SetDoLamdaRefineFlag(messages.bool_property_message(self, do_lamda_refine))

    @property
    def lamda_target(self):
        """:obj:`float`: Target lambda value for lambda refinement."""
        return self.__stub.GetLamdaTarget(self.msg).value

    @lamda_target.setter
    def lamda_target(self, lamda_target):
        self.__stub.SetLamdaTarget(messages.double_property_message(self, lamda_target))

    @property
    def mesh_size_factor(self):
        """:obj:`float`: Mesh size factor used for lambda refinement."""
        return self.__stub.GetMeshSizefactor(self.msg).value

    @mesh_size_factor.setter
    def mesh_size_factor(self, mesh_size_factor):
        self.__stub.SetMeshSizefactor(messages.double_property_message(self, mesh_size_factor))

    @property
    def use_default_lamda_value(self):
        """:obj:`bool`: Flag indicating if the default lambda target value is used."""
        return self.__stub.GetLamdaTarget(self.msg).value

    @use_default_lamda_value.setter
    def use_default_lamda_value(self, use_default_value):
        self.__stub.SetDoLamdaRefineFlag(messages.bool_property_message(self, use_default_value))


class AdvancedSettings(SimulationSettingsBase):
    """Class representing base advanced simulation settings."""

    __stub: AdvancedSettingsServiceStub = StubAccessor(StubType.advanced_sim_settings)

    @property
    def union_polygons(self):
        """:obj:`bool`: Flag indicating if polygons are unioned before meshing."""
        return self.__stub.GetUnionPolygons(self.msg).value

    @union_polygons.setter
    def union_polygons(self, union_polygons):
        self.__stub.SetUnionPolygons(messages.bool_property_message(self, union_polygons))

    @property
    def use_defeature(self):
        """:obj:`bool`: Flag indicating if polygon defeaturing is performed."""
        return self.__stub.GetUseDefeature(self.msg).value

    @use_defeature.setter
    def use_defeature(self, use_defeature):
        self.__stub.SetUseDefeature(messages.bool_property_message(self, use_defeature))

    @property
    def use_defeature_absolute_length(self):
        """:obj:`bool`: Flag indicating if absolute length or extent ratio is used when defeaturing polygons."""
        return self.__stub.GetUseDefeatureAbsoluteLength(self.msg).value

    @use_defeature_absolute_length.setter
    def use_defeature_absolute_length(self, use_defeature_absolute_length):
        self.__stub.SetUseDefeatureAbsoluteLength(
            messages.bool_property_message(self, use_defeature_absolute_length)
        )

    @property
    def remove_floating_geometry(self):
        """:obj:`bool`: Flag indicating if a geometry not connected to any other geometry is removed."""
        return self.__stub.GetRemoveFloatingGeometry(self.msg).value

    @remove_floating_geometry.setter
    def remove_floating_geometry(self, remove_floating_geometry):
        self.__stub.SetRemoveFloatingGeometry(
            messages.bool_property_message(self, remove_floating_geometry)
        )

    @property
    def healing_option(self):
        """:obj:`int`: Enable/disable healing of mis-aligned points and edges."""
        return self.__stub.GetHealingOption(self.msg).value

    @healing_option.setter
    def healing_option(self, healing_option):
        self.__stub.SetHealingOption(messages.int_property_message(self, healing_option))

    @property
    def defeature_absolute_length(self):
        """:obj:`str`: Absolute length used as tolerance when defeaturing polygons."""
        return self.__stub.GetDefeatureAbsoluteLength(self.msg).value

    @defeature_absolute_length.setter
    def defeature_absolute_length(self, defeature_absolute_length):
        self.__stub.SetDefeatureAbsoluteLength(
            messages.string_property_message(self, defeature_absolute_length)
        )

    @property
    def defeature_ratio(self):
        """:obj:`float`: Extent ratio used as tolerance when defeaturing polygons."""
        return self.__stub.GetDefeatureRatio(self.msg).value

    @defeature_ratio.setter
    def defeature_ratio(self, defeature_ratio):
        self.__stub.SetDefeatureRatio(messages.double_property_message(self, defeature_ratio))

    @property
    def small_void_area(self):
        """:obj:`float`: Voids with an area smaller than this value are ignored during simulation."""
        return self.__stub.GetSmallVoidArea(self.msg).value

    @small_void_area.setter
    def small_void_area(self, small_void_area):
        self.__stub.SetSmallVoidArea(messages.double_property_message(self, small_void_area))

    @property
    def via_model_type(self):
        """:class:`.ViaStyle`: Via model type."""
        return ViaStyle(self.__stub.GetViaModelType(self.msg).via_model_type)

    @via_model_type.setter
    def via_model_type(self, via_model_type):
        self.__stub.SetViaModelType(
            pb.ViaModelTypePropertyMessage(target=self.msg, via_model_type=via_model_type.value)
        )

    @property
    def num_via_sides(self):
        """:obj:`int`: Number of sides a via is considered to have."""
        return self.__stub.GetNumViaSides(self.msg).value

    @num_via_sides.setter
    def num_via_sides(self, num_via_sides):
        self.__stub.SetNumViaSides(messages.uint64_property_message(self, num_via_sides))

    @property
    def num_via_density(self):
        """:obj:`float`: Spacing between vias."""
        return self.__stub.GetViaDensity(self.msg).value

    @num_via_density.setter
    def num_via_density(self, num_via_density):
        self.__stub.SetViaDensity(messages.double_property_message(self, num_via_density))

    @property
    def via_material(self):
        """:obj:`str`: Default via material."""
        return self.__stub.GetViaMaterial(self.msg).value

    @via_material.setter
    def via_material(self, via_material):
        self.__stub.SetViaMaterial(messages.string_property_message(self, via_material))

    @property
    def model_type(self):
        """:class:`.ModelType`: model type."""
        return ModelType(self.__stub.GetModelType(self.msg).defeature_model_type)

    @model_type.setter
    def model_type(self, model_type):
        self.__stub.SetModelType(
            pb.DefeatureModelTypePropertyMessage(
                target=self.msg, defeature_model_type=model_type.value
            )
        )


class AdvancedMeshingSettings(SimulationSettingsBase):
    """Class representing base advanced meshing simulation settings."""

    __stub: AdvancedMeshingSettingsServiceStub = StubAccessor(StubType.advanced_mesh_sim_settings)

    @property
    def arc_step_size(self):
        """:obj:`str`: Arc step size used when approximating arcs."""
        return self.__stub.GetArcStepSize(self.msg).value

    @arc_step_size.setter
    def arc_step_size(self, arc_step_size):
        self.__stub.SetArcStepSize(messages.string_property_message(self, arc_step_size))

    @property
    def circle_start_azimuth(self):
        """:obj:`str`: Starting azimuth used when approximating arcs."""
        return self.__stub.GetCircleStartAzimuth(self.msg).value

    @circle_start_azimuth.setter
    def circle_start_azimuth(self, circle_start_azimuth):
        self.__stub.SetCircleStartAzimuth(
            messages.string_property_message(self, circle_start_azimuth)
        )

    @property
    def max_num_arc_points(self):
        """:obj:`str`: Maximum number of points used to approximate arcs."""
        return self.__stub.GetMaxNumArcPoints(self.msg).value

    @max_num_arc_points.setter
    def max_num_arc_points(self, max_num_arc_points):
        self.__stub.SetMaxNumArcPoints(messages.int_property_message(self, max_num_arc_points))

    @property
    def use_arc_chord_error_approx(self):
        """:obj:`bool`: Flag indicating if arc chord error approximation is used."""
        return self.__stub.GetUseArcChordErrorApprox(self.msg).value

    @use_arc_chord_error_approx.setter
    def use_arc_chord_error_approx(self, use_arc_chord_error_approx):
        self.__stub.SetUseArcChordErrorApprox(
            messages.bool_property_message(self, use_arc_chord_error_approx)
        )

    @property
    def arc_to_chord_error(self):
        """:obj:`str`: Maximum allowable arc to chord error."""
        return self.__stub.GetArcChordErrorApprox(self.msg).value

    @arc_to_chord_error.setter
    def arc_to_chord_error(self, arc_to_chord_error):
        self.__stub.SetArcChordErrorApprox(
            messages.string_property_message(self, arc_to_chord_error)
        )


class SolverSettings(SimulationSettingsBase):
    """Class representing base solver simulation settings."""

    __stub: SolverSettingsServiceStub = StubAccessor(StubType.solver_sim_settings)

    @property
    def thin_signal_layer_threshold(self):
        """:obj:`str`: Value below which signal layers are considered to have zero thickness."""
        return self.__stub.GetThinSignalLayerThreshold(self.msg).value

    @thin_signal_layer_threshold.setter
    def thin_signal_layer_threshold(self, thin_signal_layer_threshold):
        self.__stub.SetThinSignalLayerThreshold(
            messages.string_property_message(self, thin_signal_layer_threshold)
        )

    @property
    def thin_dielectric_layer_threshold(self):
        """:obj:`str`: Value below which dielectric layers are merged with adjacent dielectric layers."""
        return self.__stub.GetThinDielectricLayerThreshold(self.msg).value

    @thin_dielectric_layer_threshold.setter
    def thin_dielectric_layer_threshold(self, thin_dielectric_layer_threshold):
        self.__stub.SetThinDielectricLayerThreshold(
            messages.string_property_message(self, thin_dielectric_layer_threshold)
        )
