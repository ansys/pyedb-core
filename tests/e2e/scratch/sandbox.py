from ansys.edb.core.database import Database
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.primitive.rectangle import Rectangle
from ansys.edb.core.session import session
from ansys.edb.core.utility.io_manager import IOMangementType, enable_io_manager

db_name = "io_performance_test.aedb"
lyr_name = "signal_1"
net_name = "net_1"
db = None
lyt: Layout = None

with session("path_to_ansysem_dir_in_aedt"):
    db = Database.create(db_name)
    cell = Cell.create(db, CellType.CIRCUIT_CELL, "EMDesign1")
    lyt = cell.layout
    lyt.layer_collection.add_layers(
        [StackupLayer.create(lyr_name, LayerType.SIGNAL_LAYER, 1e-3, 0, "copper")]
    )
    Net.create(lyt, net_name)

    with enable_io_manager(IOMangementType.READ_AND_WRITE):
        rect = Rectangle.create()
