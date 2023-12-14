import settings

from ansys.edb.core.database import Database
from ansys.edb.core.layer.layer import LayerType
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.primitive import Circle
from ansys.edb.core.session import launch_session
from ansys.edb.core.utility.value import Value


def test_value():
    session = launch_session(settings.configs.get("RPC_SERVER_ROOT"), 50051)

    db = Database.create(settings.configs.get("RPC_SERVER_TEMP"))
    db.add_variable("$green", 0.5)

    print(db.get_all_variable_names())

    cell = Cell.create(db, CellType.CIRCUIT_CELL, "my_cell")
    layout = cell.layout
    net = Net.create(layout, "net_1")
    lc = layout.layer_collection
    layer = StackupLayer.create("layer_1", LayerType.SIGNAL_LAYER, 0.0001, 0, "copper")
    lc.add_layers([layer])
    layer2 = lc.find_by_name("layer_1")

    layout.layer_collection = lc

    param = Value(33.1)
    cell.add_variable("blue1", param)
    cell.add_variable("blue2", "25mm")
    vv = cell.create_value("blue1 + blue2")
    print(vv.double)

    layout.add_variable("c_blue", param)

    print(cell.get_all_variable_names())

    vv = cell.create_value("c_blue + 10mm")
    print("vv = " + str(vv))
    print("value of vv is ", vv.double)
    print("complex of vv is ", vv.complex)

    print("start circle parameter testing")
    circ = Circle.create(layout, layer2, net, 1.335, "2.7mm", "c_blue+$green")

    params = circ.get_parameters()
    print(
        "After creation: params[0] = "
        + str(params[0])
        + " params[1] = "
        + str(params[1])
        + " params[2] = "
        + str(params[2])
    )
    print(
        "Same, but doubles: params[0] = "
        + str(params[0].double)
        + " params[1] = "
        + str(params[1].double)
        + " params[2] = "
        + str(params[2].double)
    )
    print(
        "Same, but is_parametric: params[0] = "
        + str(params[0].is_parametric)
        + " params[1] = "
        + str(params[1].is_parametric)
        + " params[2] = "
        + str(params[2].is_parametric)
    )

    circ.set_parameters(4, "0.355MHz", "c_blue-0.009")

    params = circ.get_parameters()
    print(
        "After setting: params[0] = "
        + str(params[0])
        + " params[1] = "
        + str(params[1])
        + " params[2] = "
        + str(params[2])
    )
    print(
        "Same, but doubles: params[0] = "
        + str(params[0].double)
        + " params[1] = "
        + str(params[1].double)
        + " params[2] = "
        + str(params[2].double)
    )

    session.disconnect()


if __name__ == "__main__":
    test_value()
