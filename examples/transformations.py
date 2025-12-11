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
    data = {'data': [ArcData((0, 0), (-10, 0), height=-5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=5.0), ArcData((0, 10), (0, 0), height=0.0)]}
    data1 = {'data': [(0.22359712320138886, 0.13552079290407354), (0.22357625878461637, 0.13552101058378618), (0.1576148561895463, 0.13689751896063965), (0.15744029395763803, 0.1369165526164289), (0.15712331910181926, 0.1369796028353996), (0.1567593423350584, 0.13713036694858077), (0.15648193078355876, 0.13731572742120518), (0.15633002850990907, 0.1374403903954682), (0.15334198419546835, 0.14042843470990893), (0.15321732122120554, 0.1405803369835583), (0.15303500283484403, 0.14085319573122612), (0.15288651225072367, 0.14120625460884637), (0.14975001173056893, 0.15612667224971177), (0.14973420839246682, 0.156226814137581), (0.14932292463393215, 0.160098233124855), (0.149317325, 0.16020394857514447), (0.149317325, 0.16089737329953932), (0.1493365860933113, 0.16109293446178002), (0.14940167603539994, 0.16142016369818152), (0.1495524401485806, 0.16178414046494108), (0.14973780062120465, 0.16206155201644057), (0.149862463595468, 0.16221345429009074), (0.1503843457099089, 0.16273533640453164), (0.15053624798355827, 0.16285999937879445), (0.15076513462154198, 0.1630129365408007), (0.15101470073432902, 0.16313369010297238), (0.1588617616377243, 0.16566677113431302), (0.158973962797113, 0.16569593504832808), (0.15913898899973616, 0.1657287608009716), (0.15928165831644442, 0.1657466139512513), (0.16801064956601286, 0.16620644015303843), (0.16806326378134887, 0.16620782500000003), (0.1790009975378114, 0.16620782500000003), (0.17906615798450604, 0.16620570036546622), (0.21902564056855967, 0.16359707323274483), (0.21915572756700483, 0.16357996419458248), (0.21945093409818078, 0.1635212439646004), (0.21981491086494165, 0.16337047985141923), (0.22009232241644128, 0.16318511937879482), (0.22024422469009097, 0.1630604564045318), (0.22979768640453216, 0.15350699469009058), (0.22992234937879574, 0.15335509241644008), (0.2301077098514197, 0.15307768086494047), (0.23025847396460003, 0.15271370409818155), (0.23032356390668868, 0.15238647486178034), (0.23034282500000003, 0.15219091369953922), (0.23034282500000003, 0.14843728597926625), (0.23034150279683913, 0.148385874937376), (0.2298519496603027, 0.13887455685609815), (0.2298340334171302, 0.13873068029609614), (0.22977759420186486, 0.13844694120028656), (0.22962683008868348, 0.13808296443352489), (0.22945179341834052, 0.13782100354401233), (0.22932713044407782, 0.1376691012703631), (0.22870811872963664, 0.13705008955592193), (0.22855621645598603, 0.13692542658165827), (0.2283239410921431, 0.13677022514542356), (0.22803049175985454, 0.1366363114907755), (0.2240854335862734, 0.13555643361197334), (0.22382023527959274, 0.13552079290407354), (0.22359712320138886, 0.13552079290407354)]}
    data2 = {'data': [(0.404495, 0.168275), (0.404495, 0.1778), (0.40389948291982186, 0.1800225), (0.40227250000000003, 0.18164948291982186), (0.40005, 0.18224500000000002), (0.3978275, 0.18164948291982186), (0.39620051708017817, 0.18002250000000003), (0.395605, 0.1778), (0.395605, 0.168275), (-0.0044450000000000045, 1.7976931348623157e+308), (0.404495, 0.168275)]}
    polygon1 = create_polygon(geometry=data1)
    print([a.is_arc for a in polygon1.points])
    polygon2 = create_polygon(geometry=data2)
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    result_server = polygon1.intersection_type(polygon2)
    print(result_server)

    plot_polys(axs[0], [polygon1, polygon2], title="Server expansion", labels=['1', '2'])

    plt.show()

    Config.reset()


if __name__ == "__main__":
    # tessellation()
    # transformation()
    # convex_hull()
    # boolean_operations()
    test()
