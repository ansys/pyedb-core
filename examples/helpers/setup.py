import glob
import os
import pathlib
import shutil
import sys

import ansys.edb
from ansys.edb.core.database import Database

"""Import definition classes."""

from ansys.edb.core.definition.bondwire_def import (
    ApdBondwireDef,
    BondwireDef,
    BondwireDefType,
    Jedec4BondwireDef,
    Jedec5BondwireDef,
)
from ansys.edb.core.definition.component_def import ComponentDef
from ansys.edb.core.definition.component_model import (
    ComponentModel,
    DynamicLinkComponentModel,
    NPortComponentModel,
)
from ansys.edb.core.definition.component_pin import ComponentPin
from ansys.edb.core.definition.component_property import ComponentProperty
from ansys.edb.core.definition.dataset_def import DatasetDef
from ansys.edb.core.definition.debye_model import DebyeModel
from ansys.edb.core.definition.die_property import DieOrientation, DieProperty, DieType
from ansys.edb.core.definition.dielectric_material_model import (
    DielectricMaterialModel,
    DielectricMaterialModelType,
)
from ansys.edb.core.definition.djordjecvic_sarkar_model import DjordjecvicSarkarModel
from ansys.edb.core.definition.ic_component_property import ICComponentProperty
from ansys.edb.core.definition.io_component_property import IOComponentProperty
from ansys.edb.core.definition.material_def import MaterialDef, MaterialProperty
from ansys.edb.core.definition.material_property_thermal_modifier import (
    MaterialPropertyThermalModifier,
)
from ansys.edb.core.definition.multipole_debye_model import MultipoleDebyeModel
from ansys.edb.core.definition.package_def import PackageDef
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.definition.padstack_def_data import (
    PadGeometryType,
    PadstackDefData,
    PadstackHoleRange,
    PadType,
    SolderballPlacement,
    SolderballShape,
)
from ansys.edb.core.definition.port_property import PortProperty
from ansys.edb.core.definition.rlc_component_property import RLCComponentProperty
from ansys.edb.core.definition.solder_ball_property import SolderBallProperty
from ansys.edb.core.edb_defs import DefinitionObjType

"""Import geometry classes."""

from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.geometry.point3d_data import Point3DData
from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import ExtentType, PolygonData, PolygonSenseType
from ansys.edb.core.geometry.r_tree import RTree
from ansys.edb.core.geometry.triangle3d_data import Triangle3DData

"""Import hierarchy classes."""

from ansys.edb.core.hierarchy.cell_instance import CellInstance
from ansys.edb.core.hierarchy.component_group import ComponentGroup, ComponentType
from ansys.edb.core.hierarchy.group import Group
from ansys.edb.core.hierarchy.inst_array import InstArray
from ansys.edb.core.hierarchy.model import Model
from ansys.edb.core.hierarchy.netlist_model import NetlistModel
from ansys.edb.core.hierarchy.pin_group import PinGroup
from ansys.edb.core.hierarchy.pin_pair_model import PinPairModel
from ansys.edb.core.hierarchy.sparameter_model import SParameterModel
from ansys.edb.core.hierarchy.spice_model import SPICEModel
from ansys.edb.core.hierarchy.structure3d import MeshClosure, Structure3D
from ansys.edb.core.hierarchy.via_group import ViaGroup

"""Import layer classes."""

from ansys.edb.core.layer.layer import (
    DrawOverride,
    Layer,
    LayerType,
    LayerVisibility,
    TopBottomAssociation,
)
from ansys.edb.core.layer.layer_collection import (
    DielectricMergingMethod,
    LayerCollection,
    LayerCollectionMode,
    LayerTypeSet,
)
from ansys.edb.core.layer.stackup_layer import DCThicknessType, RoughnessRegion, StackupLayer
from ansys.edb.core.layer.via_layer import ViaLayer

"""Import layout classes."""

from ansys.edb.core.layout.cell import Cell, CellType, DesignMode
from ansys.edb.core.layout.layout import Layout
from ansys.edb.core.layout.mcad_model import McadModel
from ansys.edb.core.layout.voltage_regulator import PowerModule, VoltageRegulator

"""Import layout instance classes."""

from ansys.edb.core.layout_instance.layout_instance import LayoutInstance
from ansys.edb.core.layout_instance.layout_instance_context import LayoutInstanceContext
from ansys.edb.core.layout_instance.layout_obj_instance import LayoutObjInstance
from ansys.edb.core.layout_instance.layout_obj_instance_2d_geometry import (
    LayoutObjInstance2DGeometry,
)
from ansys.edb.core.layout_instance.layout_obj_instance_3d_geometry import (
    LayoutObjInstance3DGeometry,
)
from ansys.edb.core.layout_instance.layout_obj_instance_geometry import LayoutObjInstanceGeometry

"""Import net classes."""

from ansys.edb.core.net.differential_pair import DifferentialPair
from ansys.edb.core.net.extended_net import ExtendedNet
from ansys.edb.core.net.net import Net
from ansys.edb.core.net.net_class import NetClass

"""Import primitive classes."""

from ansys.edb.core.primitive.board_bend_def import BoardBendDef
from ansys.edb.core.primitive.bondwire import Bondwire, BondwireCrossSectionType, BondwireType
from ansys.edb.core.primitive.circle import Circle
from ansys.edb.core.primitive.padstack_instance import BackDrillType, PadstackInstance
from ansys.edb.core.primitive.path import Path, PathCornerType, PathEndCapType
from ansys.edb.core.primitive.polygon import Polygon
from ansys.edb.core.primitive.primitive import Primitive, PrimitiveType
from ansys.edb.core.primitive.rectangle import Rectangle, RectangleRepresentationType
from ansys.edb.core.primitive.text import Text

"""Import simulation setup classes."""

from ansys.edb.core.simulation_setup.adaptive_solutions import (
    AdaptiveFrequency,
    BroadbandAdaptiveSolution,
    MatrixConvergenceData,
    MatrixConvergenceDataEntry,
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
    MeshOperation,
    SkinDepthMeshOperation,
)
from ansys.edb.core.simulation_setup.raptor_x_simulation_settings import (
    RaptorXAdvancedSettings,
    RaptorXGeneralSettings,
    RaptorXSimulationSettings,
)
from ansys.edb.core.simulation_setup.raptor_x_simulation_setup import RaptorXSimulationSetup
from ansys.edb.core.simulation_setup.simulation_settings import (
    AdvancedMeshingSettings,
    AdvancedSettings,
    SettingsOptions,
    SimulationSettings,
    SolverSettings,
    ViaStyle,
)
from ansys.edb.core.simulation_setup.simulation_setup import (
    FreqSweepType,
    HFSSRegionComputeResource,
    InterpolatingSweepData,
    SimulationSetup,
    SimulationSetupType,
    SweepData,
)
from ansys.edb.core.simulation_setup.siwave_dcir_simulation_settings import (
    SIWaveDCIRSimulationSettings,
)
from ansys.edb.core.simulation_setup.siwave_dcir_simulation_setup import SIWaveDCIRSimulationSetup
from ansys.edb.core.simulation_setup.siwave_simulation_settings import (
    SIWaveAdvancedSettings,
    SIWaveDCAdvancedSettings,
    SIWaveDCSettings,
    SIWaveGeneralSettings,
    SIWaveSimulationSettings,
    SIWaveSParameterSettings,
    SParamDCBehavior,
    SParamExtrapolation,
    SParamInterpolation,
)
from ansys.edb.core.simulation_setup.siwave_simulation_setup import SIWaveSimulationSetup

"""Import terminal classes."""

from ansys.edb.core.terminal.bundle_terminal import BundleTerminal
from ansys.edb.core.terminal.edge_terminal import (
    Edge,
    EdgeTerminal,
    EdgeType,
    PadEdge,
    PrimitiveEdge,
)
from ansys.edb.core.terminal.padstack_instance_terminal import PadstackInstanceTerminal
from ansys.edb.core.terminal.pin_group_terminal import PinGroupTerminal
from ansys.edb.core.terminal.point_terminal import PointTerminal
from ansys.edb.core.terminal.terminal import (
    BoundaryType,
    HfssPIType,
    SourceTermToGroundType,
    Terminal,
    TerminalType,
)
from ansys.edb.core.terminal.terminal_instance import TerminalInstance
from ansys.edb.core.terminal.terminal_instance_terminal import TerminalInstanceTerminal

"""Import utility classes."""

from ansys.edb.core.session import launch_session
from ansys.edb.core.utility.heat_sink import HeatSink
from ansys.edb.core.utility.hfss_extent_info import HfssExtentInfo
from ansys.edb.core.utility.material_property_thermal_modifier_params import (
    AdvancedQuadraticParams,
    BasicQuadraticParams,
)
from ansys.edb.core.utility.port_post_processing_prop import PortPostProcessingProp
from ansys.edb.core.utility.rlc import PinPair, PinPairRlc, Rlc
from ansys.edb.core.utility.temperature_settings import TemperatureSettings
from ansys.edb.core.utility.transform3d import Transform3D
from ansys.edb.core.utility.transform import Transform
from ansys.edb.core.utility.value import Value


def get_example_name(script_path: str = None) -> str:
    return os.path.splitext(os.path.basename(script_path))[0]


def get_project_root() -> str:
    helpers_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.dirname(helpers_dir)
    project_root = os.path.dirname(examples_dir)
    return project_root


# def get_helpers_path(filename: str) -> str:
#     helpers_dir = os.path.join(get_project_root(), "examples", "helpers")
#     return os.path.join(helpers_dir, filename)


def get_fixture_file(script_path: str = None) -> str:
    example_name = get_example_name(script_path)
    return os.path.join(
        get_project_root(), "examples", "fixtures", f"{example_name}", f"{example_name}.a3dcomp"
    )


def get_input_dir(script_path: str = None) -> str:
    example_name = get_example_name(script_path)
    return os.path.join(get_project_root(), "examples", f"{example_name}.aedb")


def get_output_dir(script_path: str = None):
    example_name = get_example_name(script_path)
    return os.path.join(get_project_root(), "examples", "results", f"{example_name}.aedb")


def get_output_files(script_path: str = None) -> str:
    example_name = get_example_name(script_path)
    return os.path.join(get_project_root(), "examples", "results", f"{example_name}.*")


def copy_input_dir(script_path: str = None) -> str:
    if os.path.exists(get_output_dir(script_path)):
        shutil.rmtree(get_output_dir(script_path))
    shutil.copytree(get_input_dir(script_path), get_output_dir(script_path))
    return get_output_dir(script_path)


def initialize_edb(script_path: str = None):
    # Launch EDB session
    os.environ["ANSYSEM_EDB_EXE_DIR"] = r"C:\Program Files\ANSYS Inc\v262\AnsysEM"
    EXE_DIR = os.environ["ANSYSEM_EDB_EXE_DIR"]
    # session = launch_session(EXE_DIR, 50052)
    session = launch_session(EXE_DIR)

    # Prepare output directory
    if not pathlib.Path(get_output_dir(script_path)).is_dir():
        os.makedirs(get_output_dir(script_path))

    # Clean up previous output files
    for f in glob.glob(get_output_files(script_path)):
        if pathlib.Path(f).is_dir():
            shutil.rmtree(f)
        else:
            os.remove(f)

    # Open existing design or create a new one
    if pathlib.Path(get_input_dir(script_path)).is_dir():
        db = Database.open(copy_input_dir(script_path), False)
        cell = db.circuit_cells[0]
        layout = cell.layout
        print("db, cell, layout variables set to the default from edb design.")
    else:
        db = Database.create(get_output_dir(script_path))
        cell = Cell.create(db, CellType.CIRCUIT_CELL, "Example")
        layout = cell.layout
        gnd_net = Net.create(layout, "GND")
        print("clean design created with default db, cell, layout, gnd_net variables.")

    return db, cell, layout, gnd_net


import math
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def plot_poly(ax, p, color, label=None, linetype='solid'):
    pts = p.points
    if len(pts) == 0:
        return

    xss = []
    yss = []
    arcs = []
    xs = [pts[0].x.value]
    ys = [pts[0].y.value]

    i = 1
    while i < len(pts):
        if pts[i].is_arc:
            if len(xs) > 1:
                # flush current line segment
                xss.append(xs)
                yss.append(ys)
            xs = []
            ys = []

            start = pts[i - 1]
            end = pts[(i + 1) % len(pts)]
            arc = ArcData(start, end, height=pts[i].arc_height.value)
            center = arc.center
            center_pt = [center.x.value, center.y.value]
            theta1 = math.atan2((start - center).y.value, (start - center).x.value)
            theta2 = math.atan2((end - center).y.value, (end - center).x.value)
            
            # Swap angles if arc_height is positive to draw on the left side
            if pts[i].arc_height.value > 0:
                theta1, theta2 = theta2, theta1
            
            diameter = arc.radius * 2
            arcs.append(
                mpatches.Arc(
                    center_pt,
                    height=diameter,
                    width=diameter,
                    theta1=math.degrees(theta1),
                    theta2=math.degrees(theta2),
                    color=color,
                    lw=1.5,
                )
            )
        else:
            xs.append(pts[i].x.value)
            ys.append(pts[i].y.value)
        i += 1

    if not pts[-1].is_arc:
        # close the loop
        xs.append(pts[0].x.value)
        ys.append(pts[0].y.value)

    if len(xs) > 0:
        xss.append(xs)
        yss.append(ys)

    for a in arcs:
        ax.add_patch(a)

    for i in range(0, len(xss)):
        ax.plot(xss[i], yss[i], color=color, linestyle=linetype)

    ax.plot(xss[0][0], yss[0][0], color=color, label=label, linestyle=linetype)


def plot_polys(ax, ps, title, labels=[]):
    try:
        if len(ps) == 0:
            return
    except TypeError:
        ps = [p]

    ax.set_title(title)

    # Count total number of polygons and holes
    total_holes = sum(len(p.holes) for p in ps)
    total_items = len(ps) + total_holes
    
    # Generate different colors for all polygons and holes
    colors = plt.cm.tab10(range(total_items))
    
    # Define line styles for holes
    line_styles = ['dashed', 'dotted', 'dashdot', (0, (3, 1, 1, 1)), (0, (5, 2, 1, 2))]

    clean_labels = []
    for i, _ in enumerate(ps):
        label = labels[i] if labels is not None and i < len(labels) else None
        clean_labels.append(label)

    # plot contours
    color_index = 0
    for i, p in enumerate(ps):
        plot_poly(ax, p, color=colors[color_index], label=clean_labels[i])
        color_index += 1

    # plot holes with unique colors and line styles
    hole_index = 0
    for p in ps:
        for h in p.holes:
            linestyle = line_styles[hole_index % len(line_styles)]
            plot_poly(ax, h, color=colors[color_index], label=f'Hole in {clean_labels[color_index%len(ps)]}', linetype=linestyle)
            color_index += 1
            hole_index += 1

    if labels is not None:
        ax.legend()

    # ax.set_aspect('equal')