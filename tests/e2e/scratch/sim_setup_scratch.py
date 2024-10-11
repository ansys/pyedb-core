# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import settings

from ansys.edb.core.database import Database
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.session import session
from ansys.edb.core.simulation_setup.adaptive_solutions import (
    BroadbandAdaptiveSolution,
    MultiFrequencyAdaptiveSolution,
    SingleFrequencyAdaptiveSolution,
)
from ansys.edb.core.simulation_setup.hfss_simulation_settings import (
    AdaptType,
    BasisFunctionOrder,
    HFSSAdvancedMeshingSettings,
    HFSSAdvancedSettings,
    HFSSDCRSettings,
    HFSSGeneralSettings,
    HFSSSettingsOptions,
    HFSSSimulationSettings,
    HFSSSolverSettings,
    SolverType,
)
from ansys.edb.core.simulation_setup.hfss_simulation_setup import HfssSimulationSetup
from ansys.edb.core.simulation_setup.mesh_operation import (
    LengthMeshOperation,
    SkinDepthMeshOperation,
)
from ansys.edb.core.simulation_setup.simulation_settings import ViaStyle
from ansys.edb.core.simulation_setup.simulation_setup import SweepData


def do_hfss_sim_setup_test(hfss_sim_setup):
    og_name = hfss_sim_setup.name
    hfss_sim_setup.name = "new_name"
    new_name = hfss_sim_setup.name

    og_pos = hfss_sim_setup.position
    hfss_sim_setup.position = 1
    new_pos = hfss_sim_setup.position

    og_sweep_data = hfss_sim_setup.sweep_data
    hfss_sim_setup.sweep_data = [SweepData("sweep_1", "LIN", "1GHz", "10GHz", "1GHz")]
    new_sweep_data = hfss_sim_setup.sweep_data

    og_mesh_ops = hfss_sim_setup.mesh_operations
    sk_op = SkinDepthMeshOperation(
        name="sk_op", mesh_region="mes_region", net_layer_info=[("net", "lyr", True)]
    )
    l_op = LengthMeshOperation(
        name="l_op", mesh_region="mes_region", net_layer_info=[("net", "lyr", True)]
    )
    hfss_sim_setup.mesh_operations = [sk_op, l_op]
    new_mesh_ops = hfss_sim_setup.mesh_operations

    print("done")


def do_general_test(settings: HFSSGeneralSettings):
    og_sas = settings.single_frequency_adaptive_solution
    single_sol = SingleFrequencyAdaptiveSolution(use_mx_conv_data=True)
    mx_data = single_sol.mx_conv_data
    mx_data.add_entry("port0", "port1", 1.0, 2.0)
    mx_data.add_entry("port0", "port1", 1.0, 3.0)
    single_sol.mx_conv_data = mx_data
    settings.single_frequency_adaptive_solution = single_sol
    new_sas = settings.single_frequency_adaptive_solution

    og_m = settings.multi_frequency_adaptive_solution
    settings.multi_frequency_adaptive_solution = MultiFrequencyAdaptiveSolution()
    new_m = settings.multi_frequency_adaptive_solution

    og_b = settings.broadband_adaptive_solution
    settings.broadband_adaptive_solution = BroadbandAdaptiveSolution()
    new_b = settings.broadband_adaptive_solution

    og_save_fields = settings.save_fields
    settings.save_fields = not og_save_fields
    new_save_fields = settings.save_fields

    og_save_rad_fields = settings.save_rad_fields_only
    settings.save_rad_fields_only = not og_save_rad_fields
    new_save_rad_fields = settings.save_rad_fields_only

    og_adapt_type = settings.adaptive_solution_type
    settings.adaptive_solution_type = AdaptType.BROADBAND
    new_adapt_type = settings.adaptive_solution_type

    og_use_mesh_Region = settings.use_mesh_region
    settings.use_mesh_region = not og_use_mesh_Region
    new_use_mesh_region = settings.use_mesh_region

    og_mesh_region_name = settings.mesh_region_name
    settings.mesh_region_name = "new_name"
    new_mesh_region_name = settings.mesh_region_name

    og_use_parellel_refinement = settings.use_parallel_refinement
    settings.use_parallel_refinement = not og_use_parellel_refinement
    new_use_parallel_refinement = settings.use_parallel_refinement

    print("done")


def do_advanced_test(settings: HFSSAdvancedSettings):
    og_union_polys = settings.union_polygons
    settings.union_polygons = not og_union_polys
    new_union_polys = settings.union_polygons

    og_remove_floating_geometry = settings.remove_floating_geometry
    settings.remove_floating_geometry = not og_remove_floating_geometry
    new_remove_floating_geometry = settings.remove_floating_geometry

    og_small_void_area = settings.small_void_area
    settings.small_void_area = og_small_void_area + 1e-3
    new_small_void_area = settings.small_void_area

    og_use_defeature = settings.use_defeature
    settings.use_defeature = not og_use_defeature
    new_use_defeature = settings.use_defeature

    og_use_defeature_absolute_length = settings.use_defeature_absolute_length
    settings.use_defeature_absolute_length = not og_use_defeature_absolute_length
    new_use_defeature_absolute_length = settings.use_defeature_absolute_length

    og_defeature_absolute_length = settings.defeature_absolute_length
    settings.defeature_absolute_length = "1mm"
    new_defeature_absolute_length = settings.defeature_absolute_length

    og_defeature_ratio = settings.defeature_ratio
    settings.defeature_ratio = og_defeature_ratio + 1
    new_defeature_ratio = settings.defeature_ratio

    og_via_model_type = settings.via_model_type
    settings.via_model_type = ViaStyle.RIBBON
    new_via_model_type = settings.via_model_type

    og_num_via_density = settings.num_via_density
    settings.num_via_density = og_num_via_density + 1
    new_num_via_density = settings.num_via_density

    og_via_material = settings.via_material
    settings.via_material = "new_via_material"
    new_via_material = settings.via_material

    og_ic_mode_auto_resolution = settings.ic_mode_auto_resolution
    settings.ic_mode_auto_resolution = not og_ic_mode_auto_resolution
    new_ic_mode_auto_resolution = settings.ic_mode_auto_resolution

    og_ic_mode_length = settings.ic_mode_length
    settings.ic_mode_length = "1mm"
    new_ic_mode_length = settings.ic_mode_length

    print("done")


def do_advanced_meshing_test(settings: HFSSAdvancedMeshingSettings):
    og_arc_step_size = settings.arc_step_size
    settings.arc_step_size = "1deg"
    new_arc_step_size = settings.arc_step_size

    og_circle_start_azimuth = settings.circle_start_azimuth
    settings.circle_start_azimuth = "1deg"
    new_circle_start_azimuth = settings.circle_start_azimuth

    og_max_num_arc_points = settings.max_num_arc_points
    settings.max_num_arc_points = 20
    new_max_num_arc_points = settings.max_num_arc_points

    og_use_arc_chord_error_approx = settings.use_arc_chord_error_approx
    settings.use_arc_chord_error_approx = not og_use_arc_chord_error_approx
    new_use_arc_chord_error_approx = settings.use_arc_chord_error_approx

    og_arc_to_chord_error = settings.arc_to_chord_error
    settings.arc_to_chord_error = "1mm"
    new_arc_to_chord_error = settings.arc_to_chord_error

    og_layer_snap_tol = settings.layer_snap_tol
    settings.layer_snap_tol = "1mm"
    new_layer_snap_tol = settings.layer_snap_tol

    print("done")


def do_solver_test(settings: HFSSSolverSettings):
    og_thin_signal_layer_threshold = settings.thin_signal_layer_threshold
    settings.thin_signal_layer_threshold = "1mm"
    new_thin_signal_layer_threshold = settings.thin_signal_layer_threshold

    og_thin_dielectric_layer_threshold = settings.thin_dielectric_layer_threshold
    settings.thin_dielectric_layer_threshold = "2mm"
    new_thin_dielectric_layer_threshold = settings.thin_dielectric_layer_threshold

    og_max_delta_z0 = settings.max_delta_z0
    settings.max_delta_z0 = og_max_delta_z0 + 1e-3
    new_max_delta_z0 = settings.max_delta_z0

    og_set_triangles_for_wave_port = settings.set_triangles_for_wave_port
    settings.set_triangles_for_wave_port = not og_set_triangles_for_wave_port
    new_set_triangles_for_wave_port = settings.set_triangles_for_wave_port

    og_min_triangles_for_wave_port = settings.min_triangles_for_wave_port
    settings.min_triangles_for_wave_port = og_min_triangles_for_wave_port + 1
    new_min_triangles_for_wave_port = settings.min_triangles_for_wave_port

    og_max_triangles_for_wave_port = settings.max_triangles_for_wave_port
    settings.max_triangles_for_wave_port = og_max_triangles_for_wave_port + 1
    new_max_triangles_for_wave_port = settings.max_triangles_for_wave_port

    og_enable_intra_plane_coupling = settings.enable_intra_plane_coupling
    settings.enable_intra_plane_coupling = not og_enable_intra_plane_coupling
    new_enable_intra_plane_coupling = settings.enable_intra_plane_coupling

    print("done")


def do_dcr_test(settings: HFSSDCRSettings):
    og_max_passes = settings.max_passes
    settings.max_passes = og_max_passes + 1
    new_max_passes = settings.max_passes

    og_min_passes = settings.min_passes
    settings.min_passes = og_min_passes + 2
    new_min_passes = settings.min_passes

    og_min_converged_passes = settings.min_converged_passes
    settings.min_converged_passes = og_min_converged_passes + 3
    new_min_converged_passes = settings.min_converged_passes

    og_percent_error = settings.percent_error
    settings.percent_error = og_percent_error + 0.5
    new_percent_error = settings.percent_error

    og_percent_refinement_per_pass = settings.percent_refinement_per_pass
    settings.percent_refinement_per_pass = og_percent_refinement_per_pass + 0.75
    new_percent_refinement_per_pass = settings.percent_refinement_per_pass

    print("done")


def do_options_test(settings: HFSSSettingsOptions):
    og_do_lamda_refine = settings.do_lamda_refine
    settings.do_lamda_refine = not og_do_lamda_refine
    new_do_lamda_refine = settings.do_lamda_refine

    og_lamda_target = settings.lamda_target
    settings.lamda_target = og_lamda_target + 0.75
    new_lamda_target = settings.lamda_target

    og_use_default_lamda_value = settings.use_default_lamda_value
    settings.use_default_lamda_value = not og_use_default_lamda_value
    new_use_default_lamda_value = settings.use_default_lamda_value

    og_max_refinement_per_pass = settings.max_refinement_per_pass
    settings.max_refinement_per_pass = og_max_refinement_per_pass + 1
    new_max_refinement_per_pass = settings.max_refinement_per_pass

    og_min_passes = settings.min_passes
    settings.min_passes = og_min_passes + 1
    new_min_passes = settings.min_passes

    og_min_converged_passes = settings.min_converged_passes
    settings.min_converged_passes = og_min_converged_passes + 1
    new_min_converged_passes = settings.min_converged_passes

    og_use_max_refinement = settings.use_max_refinement
    settings.use_max_refinement = not og_use_max_refinement
    new_use_max_refinement = settings.use_max_refinement

    # TODO: fix this
    og_order_basis = settings.order_basis
    settings.order_basis = BasisFunctionOrder.MIXED_ORDER
    new_order_basis = settings.order_basis

    og_order_basis_2 = settings.order_basis
    settings.order_basis = BasisFunctionOrder.ZERO_ORDER
    new_order_basis_2 = settings.order_basis

    og_solver_type = settings.solver_type
    settings.solver_type = SolverType.ITERATIVE_SOLVER
    new_solver_type = settings.solver_type

    og_relative_residual = settings.relative_residual
    settings.relative_residual = og_relative_residual + 0.75
    new_relative_residual = settings.relative_residual

    og_enhanced_low_frequency_accuracy = settings.enhanced_low_frequency_accuracy
    settings.enhanced_low_frequency_accuracy = not og_enhanced_low_frequency_accuracy
    new_enhanced_low_frequency_accuracy = settings.enhanced_low_frequency_accuracy

    print("done")


def do_hfss_sim_settings_test(settings: HFSSSimulationSettings):
    og_enabled = settings.enabled
    settings.enabled = not og_enabled
    new_enabled = settings.enabled

    do_general_test(settings.general)

    do_advanced_test(settings.advanced)

    do_advanced_meshing_test(settings.advanced_meshing)

    do_solver_test(settings.solver)

    do_dcr_test(settings.dcr)

    do_options_test(settings.options)


def do_test():
    db = Database.create("test.aedb")
    test_cell = Cell.create(db, CellType.CIRCUIT_CELL, "test_cell")

    hfss_sim_setup = HfssSimulationSetup.create(test_cell, "test_sim_setup")

    do_hfss_sim_setup_test(hfss_sim_setup)

    do_hfss_sim_settings_test(hfss_sim_setup.settings)

    print("done")


def test_sim_setup():
    with session(settings.server_exe_dir(), 50051):
        do_test()
