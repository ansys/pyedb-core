from time import time

import settings

from ansys.edb.core.database import Database
from ansys.edb.core.layer.layer import LayerType
from ansys.edb.core.layer.stackup_layer import StackupLayer
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.layout.layout import Layout
from ansys.edb.core.net.net import Net
from ansys.edb.core.primitive.rectangle import Rectangle, RectangleRepresentationType
from ansys.edb.core.session import session
from ansys.edb.core.utility.io_manager import IOMangementType, enable_io_manager
import tests.e2e.settings as settings

db_name = "io_performance_test.aedb"
lyr_name = "signal_1"
net_name = "net_1"
db = None
lyt: Layout = None


def query_prims():
    prims = lyt.primitives
    for prim in prims:
        prim.get_hfss_prop
        prim.polygon_data
        prim.net
        prim.layer
        prim.is_void
        prim.layout
    return len(prims)


def create_prims():
    num_prims = 1000
    for i in range(num_prims):
        rect = Rectangle.create(
            lyt,
            lyr_name,
            net_name,
            RectangleRepresentationType.CENTER_WIDTH_HEIGHT,
            0,
            0,
            1e-3,
            1e-3,
            0.0,
            0.0,
        )
        rect.set_hfss_prop("copper", True)
    return num_prims


def read_test():
    read_test_start = time()
    with enable_io_manager(IOMangementType.READ):
        num_read_test_queried_prims = query_prims()
    read_test_end = time()
    print(
        f"read_test time: {read_test_end - read_test_start} seconds (queried {num_read_test_queried_prims} primitives)"
    )
    return num_read_test_queried_prims


def write_test():
    write_test_start = time()
    with enable_io_manager(IOMangementType.WRITE):
        num_write_test_created_prims = create_prims()
    write_test_end = time()
    print(
        f"write_test time: {write_test_end - write_test_start} seconds "
        f"(created {num_write_test_created_prims} primitives)"
    )
    return num_write_test_created_prims


def read_and_write_test():
    read_write_test_start = time()
    with enable_io_manager(IOMangementType.READ_AND_WRITE):
        num_read_write_test_created_prims = create_prims()
        num_read_write_test_queried_prims = query_prims()
    read_write_test_end = time()
    print(
        f"read_and_write_test time: {read_write_test_end - read_write_test_start} seconds "
        f"(created {num_read_write_test_created_prims} primitives, queried {num_read_write_test_queried_prims} "
        f"primitives)"
    )
    return num_read_write_test_created_prims, num_read_write_test_queried_prims


def setup():
    global db, lyt

    db = Database.create(db_name)
    cell = Cell.create(db, CellType.CIRCUIT_CELL, "EMDesign1")
    lyt = cell.layout
    lyt.layer_collection.add_layers(
        [StackupLayer.create(lyr_name, LayerType.SIGNAL_LAYER, 1e-3, 0, "copper")]
    )
    Net.create(lyt, net_name)


def teardown():
    db.close()
    Database.delete(db_name)


def caching_flushing_blocking_test():
    blocking_start = time()
    with enable_io_manager(
        IOMangementType.READ_AND_WRITE | IOMangementType.NO_CACHE_INVALIDATION_NO_BUFFER_FLUSHING
    ):
        for prim in lyt.primitives:
            rect: Rectangle = prim
            geom = rect.polygon_data
            ll = geom.points[3]
            ur = geom.points[1]
            scaled_geom = geom.scale(2, (((ur.x - ll.x) / 2) + ll.x, ((ur.y - ll.y) / 2) + ll.y))
            scaled_ll = scaled_geom.points[3]
            scaled_ur = scaled_geom.points[1]
            rect.set_parameters(
                RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT,
                scaled_ll.x,
                scaled_ll.y,
                scaled_ur.x,
                scaled_ur.y,
                0,
                0,
            )
    blocking_end = time()
    print(f"total blocking time: {blocking_end - blocking_start} seconds")


def read_write_test():
    rw_start = time()
    num_created_prims = write_test()
    num_queried_prims = read_test()
    prim_io_op_counts = read_and_write_test()
    rw_end = time()
    total_created_prims = num_created_prims + prim_io_op_counts[0]
    total_queried_prims = num_queried_prims + prim_io_op_counts[1]
    print(
        f"total rw time: {rw_end - rw_start} seconds (created {total_queried_prims} primitives, "
        f"queried {total_created_prims} primitives)"
    )


if __name__ == "__main__":
    with session(settings.server_exe_dir()):
        setup()
        start = time()
        read_write_test()
        caching_flushing_blocking_test()
        end = time()
        print(f"total time: {end - start} seconds")
        teardown()
