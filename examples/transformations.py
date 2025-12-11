"""Demo script to test the rotate() method implementation in both backends."""
import os
from ansys.edb.core.config import Config, ComputationBackend
from ansys.edb.core.session import launch_session
from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.geometry.point_data import PointData
from helpers.setup import *

import os
from ansys.edb.core.session import launch_session
os.environ["ANSYSEM_EDB_EXE_DIR"] = r"C:\Program Files\ANSYS Inc\v262\AnsysEM"
EXE_DIR = os.environ["ANSYSEM_EDB_EXE_DIR"]
session = launch_session(EXE_DIR)

def create_polygon(geometry: dict = None):
    """Create a PolygonData object from a geometry dictionary.
    
    Args:
        geometry: A dictionary containing polygon geometry data with:
            - 'data': Either a list of point tuples [(x, y), ...] or a list of ArcData objects
            - 'holes' (optional): A list of hole definitions, where each hole is either
                                  a list of point tuples or a list of ArcData objects
        
    Returns:
        PolygonData: A polygon created with either points or arcs, optionally with holes
    """
    from ansys.edb.core.geometry.polygon_data import PolygonData

    params = {}
    if isinstance(geometry['data'][0], ArcData):
        params['arcs'] = geometry['data']
    else:
        params['points'] = geometry['data']

    if 'holes' in geometry:
        holes = []
        for hole in geometry['holes']:
            if isinstance(hole[0], ArcData):
                holes.append(PolygonData(arcs=hole))
            else:
                holes.append(PolygonData(points=hole))
        params['holes'] = holes

    return PolygonData(**params)

def tessellation():
    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    plt.setp(axs)

    arcs = [ArcData((0, 0), (10, 0), height=1.0), ArcData((10, 0), (10, 10), height=-1.0), ArcData((10, 10), (0, 10), height=8.0), ArcData((0, 10), (0, 0), height=-8.0)]
    holes = [[(0, -10), (10, -10), (10, -15), (0, -15)]]
    polygon = PolygonData(arcs=arcs, holes=[PolygonData(hole) for hole in holes])
    Config.set_computation_backend(ComputationBackend.SERVER)
    tessellated_server = polygon.without_arcs()
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    tessellated_shapely = polygon.without_arcs()

    plot_polys(axs[0][0], [polygon, tessellated_server], title="Server tessellation", labels=['Original', 'Tessellated'])
    plot_polys(axs[0][1], [polygon, tessellated_shapely], title="Shapely tessellation", labels=['Original', 'Tessellated'])

    arcs = [ArcData((0, 0), (10, 0), height=2.0), ArcData((10, 0), (20, 0), height=-2.0), ArcData((20, 0), (30, 0), height=8.0), ArcData((30, 0), (40, 0), height=-8.0), ArcData((40, 0), (40, 10), height=0.0), ArcData((40, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)]
    holes = [[(1, 5), (5, 5), (5, 9), (1, 9)]]
    polygon = PolygonData(arcs=arcs, holes=[PolygonData(hole) for hole in holes])
    Config.set_computation_backend(ComputationBackend.SERVER)
    tessellated_server = polygon.without_arcs()
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    tessellated_shapely = polygon.without_arcs()

    plot_polys(axs[1][0], [polygon, tessellated_server], title="Server tessellation", labels=['Original', 'Tessellated'])
    plot_polys(axs[1][1], [polygon, tessellated_shapely], title="Shapely tessellation", labels=['Original', 'Tessellated'])

    plt.show()

    Config.reset()

def transformation():
    fig, axs = plt.subplots(2, 4, constrained_layout=True)
    plt.setp(axs)

    arcs = [ArcData((0, 0), (10, 0), height=1.0), ArcData((10, 0), (10, 10), height=-1.0), ArcData((10, 10), (0, 10), height=8.0), ArcData((0, 10), (0, 0), height=-8.0)]
    holes = [[(0, -10), (10, -10), (10, -15), (0, -15)]]
    polygon = PolygonData(arcs=arcs, holes=[PolygonData(hole) for hole in holes])

    Config.set_computation_backend(ComputationBackend.SERVER)
    moved_server = polygon.move((5, 5))
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    moved_shapely = polygon.move((5, 5))
    plot_polys(axs[0][0], [polygon, moved_server], title="Server moved", labels=['Original', 'Moved'])
    plot_polys(axs[0][1], [polygon, moved_shapely], title="Shapely moved", labels=['Original', 'Moved'])

    Config.set_computation_backend(ComputationBackend.SERVER)
    rotated_server = polygon.rotate(math.pi/2, (0, 0))
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    rotated_shapely = polygon.rotate(math.pi/2, (0, 0))
    plot_polys(axs[0][2], [polygon, rotated_server], title="Server rotated", labels=['Original', 'Rotated'])
    plot_polys(axs[0][3], [polygon, rotated_shapely], title="Shapely rotated", labels=['Original', 'Rotated'])

    Config.set_computation_backend(ComputationBackend.SERVER)
    scaled_server = polygon.scale(2.0, (0, 0))
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    scaled_shapely = polygon.scale(2.0, (0, 0))
    plot_polys(axs[1][0], [polygon, scaled_server], title="Server scaled", labels=['Original', 'Scaled'])
    plot_polys(axs[1][1], [polygon, scaled_shapely], title="Shapely scaled", labels=['Original', 'Scaled'])

    Config.set_computation_backend(ComputationBackend.SERVER)
    mirrored_x_server = polygon.mirror_x(-10)
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    mirrored_x_shapely = polygon.mirror_x(-10)
    plot_polys(axs[1][2], [polygon, mirrored_x_server], title="Server mirrored X", labels=['Original', 'Mirrored X'])
    plot_polys(axs[1][3], [polygon, mirrored_x_shapely], title="Shapely mirrored X", labels=['Original', 'Mirrored X'])

    plt.show()

    Config.reset()

def convex_hull():
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    plt.setp(axs)

    points, hole = [[ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0), ArcData((0, 10), (0, 0), height=0.0)], [ArcData((0, 0), (-10, 0), height=5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=5.0), ArcData((0, 10), (0, 0), height=0.0)]], [[], []]
    polygons = [PolygonData(arcs=p, holes=[PolygonData(h) for h in holes]) for p, holes in zip(points, hole)]
    Config.set_computation_backend(ComputationBackend.SERVER)
    result_server = PolygonData.convex_hull(polygons)
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    result_shapely = PolygonData.convex_hull(polygons)

    plot_polys(axs[0], [*polygons, result_server], title="Server convex hull", labels=[*['Original']*len(polygons), 'Convex Hull'])
    plot_polys(axs[1], [*polygons, result_shapely], title="Shapely convex hull", labels=[*['Original']*len(polygons), 'Convex Hull'])

    plt.show()

    Config.reset()

def boolean_operations():
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    plt.setp(axs)

    points, hole = [[ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0), ArcData((0, 10), (0, 0), height=0.0)], [ArcData((0, 5), (10, 5), height=-5.0), ArcData((10, 5), (10, 15), height=0.0), ArcData((10, 15), (0, 15), height=-5.0), ArcData((0, 15), (0, 5), height=0.0)]], [[], []]
    polygons = [PolygonData(arcs=p, holes=[PolygonData(h) for h in holes]) for p, holes in zip(points, hole)]
    Config.set_computation_backend(ComputationBackend.SERVER)
    result_server = PolygonData.subtract(*polygons)
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    result_shapely = PolygonData.subtract(*polygons)

    plot_polys(axs[0], [*polygons, *result_server], title="Server subtraction", labels=[*['Original']*len(polygons), 'Subtraction'])
    plot_polys(axs[1], [*polygons, *result_shapely], title="Shapely subtraction", labels=[*['Original']*len(polygons), 'Subtraction'])

    plt.show()

    Config.reset()

def test():
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    plt.setp(axs)

    data = {'data': [ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0), ArcData((0, 10), (0, 0), height=0.0)]}
    data = {'data': [(0, 0), (2, 0), (1, 2)]}
    data = {'data': [ArcData((0, 0), (10, 0), height=-10+8.660254037844386), ArcData((10, 0), (0, 0), height=-18.660254037844386)]}

    polygon = create_polygon(geometry=data)
    Config.set_computation_backend(ComputationBackend.SHAPELY)

    print('Yo : ', polygon.is_circle())
    print([a.is_arc for a in polygon.points])

    plot_polys(axs[0], [polygon], title="Server expansion", labels=['1'])

    plt.show()

    Config.reset()


if __name__ == "__main__":
    # tessellation()
    # transformation()
    # convex_hull()
    # boolean_operations()
    test()
