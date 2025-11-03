from ansys.edb.core.database import Database
from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.session import session
from ansys.edb.core.simulation_setup.hfss_pi_simulation_settings import HFSSPIModelType
from ansys.edb.core.simulation_setup.hfss_pi_simulation_setup import HFSSPISimulationSetup

ANSYS_EM_ROOT = r"C:\View_2\build_output\64Debug"
EDB_PATH = r"C:\pyedb\Diff_Via.aedb"
with session(ANSYS_EM_ROOT, 50056):
    try:
        db = Database.open(EDB_PATH, False)
        cell: Cell = db.circuit_cells[0]
        pi_sim_setup = HFSSPISimulationSetup.create(cell, "HFSSPI1")
        pi_sim_settings = pi_sim_setup.settings
        general = pi_sim_settings.general

        print(general.model_type)
        general.model_type = HFSSPIModelType.PACKAGE
        print(general.model_type)

        print(general.use_mesh_region)
        general.use_mesh_region = True
        print(general.use_mesh_region)

        print(general.use_auto_mesh_region)
        general.use_auto_mesh_region = True
        print(general.use_auto_mesh_region)

        advanced = pi_sim_settings.advanced

        print(advanced.small_void_area)
        advanced.small_void_area = 0.05
        print(advanced.small_void_area)

        print(advanced.small_plane_area)
        advanced.small_plane_area = "0.05mm2"
        print(advanced.small_plane_area)

        print(advanced.zero_metal_layer_thickness)
        advanced.zero_metal_layer_thickness = "0.05mm"
        print(advanced.zero_metal_layer_thickness)

        solver = pi_sim_settings.solver

        print(solver.via_area_cutoff_circ_elems)
        solver.via_area_cutoff_circ_elems = "0.05mm2"
        print(solver.via_area_cutoff_circ_elems)

    except Exception as e:
        raise e
    finally:
        db.close()
