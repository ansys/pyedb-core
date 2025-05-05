import os
import platform
import tempfile

import settings

from ansys.edb.core.database import Database
from ansys.edb.core.definition.material_def import MaterialDef, MaterialProperty
from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.hierarchy.via_group import ViaGroup
from ansys.edb.core.layer.layer import LayerType
from ansys.edb.core.layer.layer_collection import LayerCollection, LayerCollectionMode
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.layer.via_layer import ViaLayer
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.primitive import (
    Path,
    PathCornerType,
    PathEndCapType,
    Polygon,
    Rectangle,
    RectangleRepresentationType,
)
from ansys.edb.core.session import session
from ansys.edb.core.simulation_setup.adaptive_solutions import SingleFrequencyAdaptiveSolution
from ansys.edb.core.simulation_setup.hfss_simulation_setup import HfssSimulationSetup
from ansys.edb.core.simulation_setup.mesh_operation import SkinDepthMeshOperation
from ansys.edb.core.simulation_setup.simulation_setup import Distribution, FrequencyData, SweepData
from ansys.edb.core.terminal.point_terminal import PointTerminal

# Wrapper class over Database
# This will ensure clean entry and exit from database
from ansys.edb.core.utility.hfss_extent_info import HfssExtentInfo


class TDatabase:
    def __init__(self, path: str):
        rootdir = tempfile.gettempdir()
        rootdir = os.path.join(rootdir, "pyedb")
        rootdir = os.path.join(rootdir, platform.python_version())
        path = os.path.join(rootdir, path)
        print("deleting old database at", path)
        Database.delete(path)

        print("creating database at", path)
        self.db = Database.create(path)

    def __enter__(self):
        print("__enter__")
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")
        self.db.save()
        self.db.close()

    def database(self):
        return self.db


class BaseExample:
    def database(self, path: str) -> TDatabase:
        db = TDatabase(path)
        self.db = db.database()
        print("creating default cell")
        self.cell = Cell.create(self.db, CellType.CIRCUIT_CELL, "EMDesign1")
        print("assigning default layout")
        self.layout = self.cell.layout
        return db

    def __init__(self):
        self.db = None
        self.cell = None
        self.layout = None
        self.nets = {}

    def run(self):
        pass

    def create_material(self, name, properties):
        mat = MaterialDef.create(self.db, name)
        for key, value in properties.items():
            MaterialDef.set_property(mat, key, value)
        return mat

    def net(self, name):
        if name not in self.nets:
            self.nets[name] = Net.create(self.layout, name)

        return self.nets[name]

    def create_rectangle(self, layer_name, net_name, llx, lly, urx, ury):
        return Rectangle.create(
            self.layout,
            layer_name,
            self.net(net_name),
            RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT,
            llx,
            lly,
            urx,
            ury,
            0.0,
            0.0,
        )

    def create_polygon(self, layer_name, net_name, vertices, holes=[]):
        polygon_data = PolygonData(vertices, closed=True)
        polygon = Polygon.create(self.layout, layer_name, self.net(net_name), polygon_data)
        if len(holes):
            hole_polygon = self.create_polygon(layer_name, net_name, holes)
            polygon.add_void(hole_polygon)

        return polygon

    def create_path(self, layer_name, net_name, width, vertices):
        polygon_data = PolygonData(vertices, closed=True)
        return Path.create(
            self.layout,
            layer_name,
            self.net(net_name),
            width,
            PathEndCapType.FLAT,
            PathEndCapType.FLAT,
            PathCornerType.SHARP,
            polygon_data,
        )

    def create_point_terminal(self, net_name, name, point, layer_name):
        return PointTerminal.create(self.layout, self.net(net_name), layer_name, name, point)

    def set_hfss_extents(self, extents):
        self.cell.set_hfss_extent_info(extents)


def um(val, val2=None):
    if val2:
        return um(val), um(val2)
    else:
        return val * 1e-6


materials = [
    ("IMD1", (0, 3.56, 1, 0)),
    ("IMD7", (0, 4.299, 1, 0)),
    ("IMD9", (0, 4.285, 1, 0)),
    ("MetalRDL", (33300000, 1, 1, 0)),
    ("MetalU", (53475900, 1, 1, 0)),
    ("Metalx", (24690000, 1, 1, 0)),
    ("MetalZ", (55586400, 1, 1, 0)),
    ("My_Sub1", (10, 11.8, 1, 0)),
    ("Passivation", (0, 4.472, 1, 0)),
    ("SolderMask", (0, 3.1, 1, 0.035)),
    ("Underfill", (0, 3.7, 1, 0)),
    ("vacuum", (0, 1, 1, 0)),
    ("VIAuz", (3222000, 1, 1, 0)),
    ("VIAx-CO", (854198, 1, 1, 0)),
    ("VIAz", (3358800, 1, 1, 0)),
    ("copper", (5.8e8, 1, 0.999991, 0)),
]

dielectrics = [
    ("SolderMask", "SolderMask", 15),
    ("Underfill", "Underfill", 68),
    ("Passivation", "Passivation", 4.7),
    ("IMD9", "IMD9", 4.215),
    ("IMD7", "IMD7", 3.045),
    ("IMD1", "IMD1", 1.985),
    ("Sub", "My_Sub1", 100),
]

signals = [
    ("OVERPASS", "MetalRDL", 2.8, 109.245),
    ("VOVERPASS", "MetalRDL", 0.775, 108.47),
    ("M9", "MetalU", 3.5, 104.97),
    ("M8", "MetalZ", 0.85, 103.38),
    ("M7", "MetalZ", 0.85, 101.935),
    ("M6", "Metalx", 0.09, 101.25),
    ("M5", "Metalx", 0.09, 101.075),
    ("M4", "Metalx", 0.09, 100.9),
    ("M3", "Metalx", 0.09, 100.725),
    ("M2", "Metalx", 0.09, 100.55),
    ("M1", "Metalx", 0.09, 100.375),
    ("CO", "VIAx-CO", 0.375, 100),
    ("Ground", "copper", 0, 0),
]

vias = [
    ("V8", "M9", "M8", "VIAuz"),
    ("V7", "M8", "M7", "VIAz"),
    ("V6", "M7", "M6", "VIAz"),
    ("V5", "M6", "M5", "VIAx-CO"),
    ("V4", "M5", "M4", "VIAx-CO"),
    ("V3", "M4", "M3", "VIAx-CO"),
    ("V2", "M3", "M2", "VIAx-CO"),
    ("V1", "M2", "M1", "VIAx-CO"),
]

plane_rectangle = ("Ground", "GND", um(0.0), um(0.0), um(540), um(540))

ring = [um(110, 110), um(110, 430), um(430, 430), um(430, 110)]
ring_holes = [um(120, 120), um(120, 420), um(420, 420), um(420, 120)]
rings_split = [
    um(110, 110),
    um(110, 430),
    um(430, 430),
    um(430, 110),
    um(286.7, 110),
    um(286.7, 120),
    um(420, 120),
    um(420, 420),
    um(120, 420),
    um(120, 120),
    um(254.36, 120),
    um(254.36, 110),
]
rings = [
    ("CO", "GND_RING", ring, ring_holes),
    ("M1", "GND_RING", ring, ring_holes),
    ("V1", "GND_RING", ring, ring_holes),
    ("M2", "GND_RING", ring, ring_holes),
    ("V2", "GND_RING", ring, ring_holes),
    ("M3", "GND_RING", ring, ring_holes),
    ("V3", "GND_RING", ring, ring_holes),
    ("M4", "GND_RING", ring, ring_holes),
    ("V4", "GND_RING", ring, ring_holes),
    ("M5", "GND_RING", ring, ring_holes),
    ("V5", "GND_RING", ring, ring_holes),
    ("M6", "GND_RING", ring, ring_holes),
    ("V6", "GND_RING", ring, ring_holes),
    ("M7", "GND_RING", ring, ring_holes),
    ("V7", "GND_RING", ring, ring_holes),
    ("M8", "GND_RING", ring, ring_holes),
    ("V8", "GND_RING", rings_split, []),
    ("M9", "GND_RING", rings_split, []),
]

coils = [
    um(270.1, 110),
    um(270.1, 180.98),
    um(353.115, 180.98),
    um(353.115, 359.02),
    um(187.085, 359.02),
    um(187.085, 192.99),
    um(341.105, 192.99),
    um(341.105, 347.01),
    um(199.095, 347.01),
    um(199.095, 205),
    um(329.1, 205),
    um(329.1, 335),
    um(265.1, 335),
]

terminals = [
    (("SPIRAL", "P1", um(270.1, 110), "M9"), ("SPIRAL", "P1ref", um(270.1, 110), "M8")),
    (
        ("SPIRAL", "P2", um((265.1 + 275.1) / 2, 430), "OVERPASS"),
        ("SPIRAL", "P2ref", um((265.1 + 275.1) / 2, 430), "M9"),
    ),
]


class SpiralInductor(BaseExample):
    def run(self, path):
        with self.database(path):
            print("spiral inductor begin")
            self.create_stackup()
            self.create_ground()
            self.create_inductor()
            self.create_simsetup()
            print("spiral inductor end")

    def create_stackup(self):
        print("creating stackup")
        self.create_materials()
        self.create_layers()

    def create_ground(self):
        print("creating ground plane")
        self.create_rectangle(*plane_rectangle)

        print("creating ground ring")
        for layer_name, net_name, vertices, holes in rings:
            self.create_polygon(layer_name, net_name, vertices, holes)

    def create_inductor(self):
        print("creating inductor")
        self.create_coil()
        self.create_coil_feed()
        self.set_extents()

    def create_simsetup(self):
        print("creating simulation setup")
        self.create_adaptive_settings()

    def create_materials(self):
        print("creating materials")
        for name, properties in materials:
            self.create_material(
                name,
                {
                    MaterialProperty.CONDUCTIVITY: properties[0],
                    MaterialProperty.PERMITTIVITY: properties[1],
                    MaterialProperty.PERMEABILITY: properties[2],
                    MaterialProperty.DIELECTRIC_LOSS_TANGENT: properties[3],
                },
            )

    def create_layer_collection(self, layers):
        print("creating layer collection")
        lc = LayerCollection.create(LayerCollectionMode.OVERLAPPING)
        lc.add_layers(layers)
        # weighted_capacitance = 2
        # lc.simplify_dielectrics_for_phi(db, 5e-6, weighted_capacitance)
        self.layout.layer_collection = lc
        return lc

    def create_layers(self):
        print("creating layers")
        dls = self.create_dielectric_layers()
        sls = self.create_signal_layers()
        vls = self.create_via_layers()

        self.create_layer_collection(dls + sls + vls)

    def create_dielectric_layers(self):
        print("creating dielectric layers")
        layers = []
        elevation = 0.0
        for name, material_name, thickness in reversed(dielectrics):
            layer = StackupLayer.create(
                name, LayerType.DIELECTRIC_LAYER, um(thickness), um(elevation), material_name
            )
            layers.append(layer)
            elevation += thickness
        return layers

    def create_signal_layers(self):
        print("creating signal layers")
        layers = []
        for name, material_name, thickness, elevation in reversed(signals):
            layer = StackupLayer.create(
                name, LayerType.SIGNAL_LAYER, um(thickness), um(elevation), material_name
            )
            layers.append(layer)
            if name == "Ground":
                layer.negative = True

        return layers

    def create_via_layers(self):
        print("creating via layers")
        layers = []
        for name, upper_name, lower_name, material_name in vias:
            vl = ViaLayer.create(name, lower_name, upper_name, material_name)
            layers.append(vl)

        return layers

    def create_coil(self):
        print("creating coil")
        coil_path = self.create_path("M9", "SPIRAL", um(10), coils)
        self.create_material(
            "Coil_Mat",
            {
                MaterialProperty.CONDUCTIVITY: 3.7e7,
                MaterialProperty.PERMITTIVITY: 1,
                MaterialProperty.PERMEABILITY: 1,
                MaterialProperty.DIELECTRIC_LOSS_TANGENT: 0,
            },
        )
        coil_path.set_hfss_prop("Coil_Mat", True)

    def create_coil_feed(self):
        print("creating coil feed")
        self.create_rectangle("OVERPASS", "SPIRAL", um(265.1), um(330), um(275.1), um(430))
        polygon = PolygonData(
            [um(265.1, 330), um(265.1, 340), um(275.1, 340), um(275.1, 330)], closed=True
        )
        ViaGroup.create_with_outline(self.layout, polygon, 0.5, "VOVERPASS")
        self.create_point_terminals()

    def create_point_terminals(self):
        print("creating point terminals")

        for t, t_ref in terminals:
            terminal = self.create_point_terminal(*t)
            terminal_ref = self.create_point_terminal(*t_ref)
            terminal.reference_terminal = terminal_ref

    def set_extents(self):
        print("setting HFSS extents")
        hfss_info = HfssExtentInfo(
            dielectric_extent_type=HfssExtentInfo.HFSSExtentInfoType.CONFORMING,
            dielectric=(0.0, False),
            honor_user_dielectric=True,
            airbox_truncate_at_ground=True,
            airbox_horizontal=(0.15, False),
            airbox_vertical_positive=(0.5, False),
            airbox_vertical_negative=(0.15, False),
            is_pml_visible=True,
            operating_frequency=0,
        )
        self.set_hfss_extents(hfss_info)

    def create_adaptive_settings(self):
        print("creating adaptive settings")
        setup = HfssSimulationSetup.create(self.cell, "HFSS Setup 1")
        general_settings = setup.settings.general
        general_settings.single_frequency_adaptive_solution = SingleFrequencyAdaptiveSolution(
            max_delta="0.005", max_passes=20
        )
        general_settings.save_fields = True
        setup.mesh_operations = [
            SkinDepthMeshOperation(
                name="SPIRAL_M9", net_layer_info=[("SPIRAL", "M9", False)], num_layers="3"
            )
        ]
        sweep_data = SweepData(
            "Sweep 1", FrequencyData(Distribution.LIN, "0GHz", "30GHz", "0.01GHz")
        )
        sweep_data.interpolation_data.fast_sweep = True
        setup.sweep_data = [sweep_data]


def test_spiral_inductor():
    with session(settings.server_exe_dir(), 50051):
        SpiralInductor().run(r"spiral_inductor.aedb")
