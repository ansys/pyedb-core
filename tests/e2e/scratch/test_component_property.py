import settings

from ansys.edb.core.database import Database
from ansys.edb.core.definition import (
    ComponentDef,
    DieOrientation,
    DieProperty,
    DieType,
    ICComponentProperty,
    IOComponentProperty,
    PackageDef,
    PortProperty,
    RLCComponentProperty,
    SolderBallProperty,
    SolderballShape,
)
from ansys.edb.core.hierarchy import ComponentGroup, ComponentType, PinPairModel
from ansys.edb.core.layout import Cell, CellType
from ansys.edb.core.session import session
from ansys.edb.core.utility import Rlc


def do_test():
    db = Database.create(settings.configs.get("RPC_SERVER_TEMP"))
    cell = Cell.create(db, CellType.CIRCUIT_CELL, "my_cell")
    layout = cell.layout

    print("Create Component group")
    fp = Cell.create(db, CellType.FOOTPRINT_CELL, "test-fp-cell")
    comp_def = ComponentDef.create(db, "test-comp-def", fp)
    comp_grp = ComponentGroup.create_with_component(layout, "test-cmp-grp", "test-comp-def")

    print("Create pin pair model")
    ppm = PinPairModel.create()
    rlc = Rlc(1, True)
    ppm.set_rlc(("test-pin-1", "test-pin-2"), rlc)

    print("Create rlc component property")
    rlc_cp = RLCComponentProperty.create()
    rlc_cp.enabled = False
    rlc_cp.package_mounting_offset = 0.5
    rlc_cp.package_def = PackageDef.create(db, "test-package-def")
    rlc_cp.model = ppm

    print("Change component group property")
    old_type = comp_grp.component_type
    comp_grp.component_type = ComponentType.RESISTOR
    comp_grp.component_property = rlc_cp

    print("------------RLC------------------")
    print("Previous component type was: " + str(old_type))
    print("New component type is: " + str(comp_grp.component_type))
    print("Is component property enabled: " + str(comp_grp.component_property.enabled))
    print("Package mounting offset is: " + str(comp_grp.component_property.package_mounting_offset))
    print("Package def is: " + str(comp_grp.component_property.package_def.name))
    print("---------------------------------\n")

    print("Create Solder ball property")
    sold_prop = SolderBallProperty.create()
    sold_prop.shape = SolderballShape.SOLDERBALL_CYLINDER
    sold_prop.height = 0.2
    sold_prop.set_diameter(0.1, 0.2)

    print("Create Die property")
    die_prop = DieProperty.create()
    die_prop.die_type = DieType.FLIPCHIP
    die_prop.die_orientation = DieOrientation.CHIP_DOWN

    print("Create Port property")
    port_prop = PortProperty.create()
    port_prop.reference_size_auto = True

    print("Create ic component property")
    ic_cp = ICComponentProperty.create()
    ic_cp.port_property = port_prop
    ic_cp.die_property = die_prop
    ic_cp.solder_ball_property = sold_prop

    print("Change component group property")
    old_type = comp_grp.component_type
    comp_grp.component_type = ComponentType.IC
    comp_grp.component_property = ic_cp

    print("-------------IC------------------")
    print("Previous component type was: " + str(old_type))
    print("New component type is: " + str(comp_grp.component_type))
    print("Package mounting offset is: " + str(comp_grp.component_property.package_mounting_offset))
    print(
        "Solder Property shape is: " + str(comp_grp.component_property.solder_ball_property.shape)
    )
    print(
        "Port Property height is: "
        + str(comp_grp.component_property.port_property.reference_height)
    )
    print(
        "Die Property orientation is: "
        + str(comp_grp.component_property.die_property.die_orientation)
    )
    print("---------------------------------\n")

    print("Create io component property")
    io_cp = IOComponentProperty.create()
    new_port_prop = port_prop.clone()
    new_port_prop.reference_height = 0.3
    new_solder_prop = sold_prop.clone()
    new_solder_prop.shape = SolderballShape.SOLDERBALL_SPHEROID
    io_cp.port_property = new_port_prop
    io_cp.solder_ball_property = new_solder_prop
    rlc_cp.package_mounting_offset = 0.7

    print("Change component group property")
    old_type = comp_grp.component_type
    comp_grp.component_type = ComponentType.IO
    comp_grp.component_property = io_cp

    print("-------------IO------------------")
    print("Previous component type was: " + str(old_type))
    print("New component type is: " + str(comp_grp.component_type))
    print("Package mounting offset is: " + str(comp_grp.component_property.package_mounting_offset))
    print(
        "Solder Property shape is: " + str(comp_grp.component_property.solder_ball_property.shape)
    )
    print(
        "Port Property height is: "
        + str(comp_grp.component_property.port_property.reference_height)
    )
    print("---------------------------------\n")

    comp_grp.delete()


def test_component_property():
    with session(settings.configs.get("RPC_SERVER_ROOT"), 50051):
        do_test()
