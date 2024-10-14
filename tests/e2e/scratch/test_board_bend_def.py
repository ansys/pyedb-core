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
from ansys.edb.core.layer.layer import Layer, LayerType
from ansys.edb.core.layer.layer_collection import LayerCollection, LayerCollectionMode
from ansys.edb.core.layout.cell import Cell, CellType
from ansys.edb.core.primitive.primitive import BoardBendDef, Rectangle, RectangleRepresentationType
from ansys.edb.core.session import session
from ansys.edb.core.utility.value import Value


def do_test():
    db = Database.create("test.aedb")
    lyt = Cell.create(db, CellType.CIRCUIT_CELL, "test_cell").layout

    lc_col = LayerCollection.create(LayerCollectionMode.MULTIZONE)
    lc_col.add_layers([Layer.create("Outline", LayerType.OUTLINE_LAYER)])
    zone_id = lc_col.insert_zone(0)
    lyt.layer_collection = lc_col

    fixed_rect_props = (-1e-3, -1.0e-3, 0.0, 1e-3, 0.0, 0.0)
    rect_props = (0.0, -1.0e-3, 1e-2, 1e-3, 0.0, 0.0)
    #                 x1   ,  y1,  x2/w, y2/h, rad, rot

    fixed_zone_prim = Rectangle.create(
        lyt, "Outline", None, RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT, *fixed_rect_props
    )
    non_fixed_zone_prim = Rectangle.create(
        lyt, "Outline", None, RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT, *rect_props
    )

    lyt.synchronize_bend_manager()

    fixed_zone_prim.make_zone_primitive(0)
    non_fixed_zone_prim.make_zone_primitive(0)

    board_bend_def_props = ((5.0e-3, -1.0e-3), (5.0e-3, 1.0e-3)), Value("1mm"), Value("90deg")

    board_bend_def = BoardBendDef.create(lyt, non_fixed_zone_prim, *board_bend_def_props)

    lyt.synchronize_bend_manager()

    angle = board_bend_def.angle
    board_bend_def.angle = "95deg"
    new_angle = board_bend_def.angle

    radius = board_bend_def.radius
    board_bend_def.radius = "2mm"
    new_radius = board_bend_def.radius

    boundary_prim = board_bend_def.boundary_primitive

    bend_middle = board_bend_def.bend_middle
    board_bend_def.bend_middle = ((5.5e-3, -0.5e-3), (5.5e-3, 0.5e-3))
    new_bend_middle = board_bend_def.bend_middle

    bent_regions = board_bend_def.bent_regions

    print("done")


def test_board_bend_def():
    with session(settings.server_exe_dir(), 50051):
        do_test()
