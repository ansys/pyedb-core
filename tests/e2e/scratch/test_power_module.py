import settings

from ansys.edb.database import Database
from ansys.edb.layout import Cell, CellType, PowerModule, VoltageRegulator
from ansys.edb.session import launch_session


def test_power_module():
    session = launch_session(settings.configs.get("RPC_SERVER_ROOT"), 50051)

    db = Database.create(settings.configs.get("RPC_SERVER_TEMP"))

    cell = Cell.create(db, CellType.CIRCUIT_CELL, "my_cell")
    layout = cell.layout

    vr1 = VoltageRegulator.create(layout, "VR1", True, 89, "10mA", 22)
    pm1_orig = PowerModule("group1", "p1", "n1", 18, True)
    pm2_orig = PowerModule("group3", "p1", "n0", 7, False)
    print(pm1_orig.comp_group_name)

    print("Adding two power modules; only one is active")
    vr1.add_power_module(pm1_orig)
    vr1.add_power_module(pm2_orig)
    n = vr1.num_power_modules
    print("number of power modules = " + str(n))
    na = vr1.num_active_power_modules
    print("number of active power modules = " + str(na))

    print("Getting a power module")
    pm1 = vr1.get_power_module(pm1_orig.comp_group_name)
    is_same = True
    if pm1.comp_group_name != pm1_orig.comp_group_name:
        is_same = False
    elif pm1.pos_output_terminal != pm1_orig.pos_output_terminal:
        is_same = False
    elif pm1.neg_output_terminal != pm1_orig.neg_output_terminal:
        is_same = False
    elif pm1.relative_strength != pm1_orig.relative_strength:
        is_same = False
    elif pm1.active != pm1_orig.active:
        is_same = False
    print("retrieved pm is same as original" if is_same else "retrieved pm is NOT same as original")

    print("Getting all power modules")
    all_pms = vr1.get_all_power_modules()
    txt = "retrieved modules ["
    add_comma = False
    for x in all_pms:
        if add_comma:
            txt += ","
        txt += x.comp_group_name
        add_comma = True
    print(txt + "]")

    print("Removing one power module")
    vr1.remove_power_module(pm1.comp_group_name)
    n = vr1.num_power_modules
    print("number of power modules = " + str(n))

    print("Removing all power modules")
    vr1.remove_all_power_modules()
    n = vr1.num_power_modules
    print("number of power modules = " + str(n))
    session.disconnect()


if __name__ == "__main__":
    test_power_module()
