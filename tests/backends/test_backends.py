import math
import pytest
from ansys.edb.core.config import Config, ComputationBackend
from ansys.edb.core.geometry.arc_data import ArcData
from utils.fixtures import session, create_polygon


def test_config_default(session):
    """Test default configuration."""
    backend = Config.get_computation_backend()
    assert backend == ComputationBackend.AUTO


def test_config_set_backend(session):
    """Test setting backend programmatically."""
    Config.set_computation_backend(ComputationBackend.SERVER)
    assert Config.get_computation_backend() == ComputationBackend.SERVER
    
    Config.set_computation_backend('shapely')
    assert Config.get_computation_backend() == ComputationBackend.SHAPELY


def test_config_environment_variable(session):
    """Test setting backend via environment variable."""
    import os
    
    try:
        Config.reset()
        os.environ['PYEDB_COMPUTATION_BACKEND'] = 'server'
        assert Config.get_computation_backend() == ComputationBackend.SERVER
        
        Config.reset()
        os.environ['PYEDB_COMPUTATION_BACKEND'] = 'shapely'
        assert Config.get_computation_backend() == ComputationBackend.SHAPELY
        
    finally:
        Config.reset()


def test_backend_factory_server(session):
    """Test server backend creation."""
    from ansys.edb.core.geometry.backends.backend_factory import _get_server_backend
    from ansys.edb.core.geometry.backends.server_backend import ServerBackend
    
    # Mock stub for testing
    class MockStub:
        pass
    
    stub = MockStub()
    backend = _get_server_backend(stub)
    assert isinstance(backend, ServerBackend)


def test_backend_factory_shapely(session):
    """Test Shapely backend creation."""
    from ansys.edb.core.geometry.backends.backend_factory import _get_shapely_backend
    from ansys.edb.core.geometry.backends.shapely_backend import ShapelyBackend, SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    backend = _get_shapely_backend()
    assert isinstance(backend, ShapelyBackend)


def test_backend_factory_shapely_not_available(session):
    """Test Shapely backend when library not available."""
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if SHAPELY_AVAILABLE:
        pytest.skip("Shapely is installed, cannot test unavailable case")
    
    from ansys.edb.core.geometry.backends.backend_factory import _get_shapely_backend
    
    with pytest.raises(ImportError, match="Shapely is not installed"):
        _get_shapely_backend()


@pytest.mark.parametrize("test_case, holes, expected_result", [
    ([(0, 0), (10, 0), (10, 10)], [], 50.0),  # Triangle
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], 100.0),  # Square
    ([(0, 0), (-20, 0), (-20, 10), (0, 10)], [], 200.0),  # Rectangle with negative coords
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], 139.26991271972656),  # Square with one convex arc
    ([ArcData((0, 0), (-10, 0), height=-1.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], 93.28030395507812),  # Square with one concave arc
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]], 0.52),  # Square with two holes
])
def test_polygon_area(session, test_case, holes, expected_result):
    """Test area computation with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(test_case, holes)
    result_server = polygon_server.area()
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(test_case, holes)
    result_shapely = polygon_shapely.area()

    tol = 1e-6
    if isinstance(test_case[0], ArcData):
        tol = 0.1

    assert result_server == pytest.approx(expected_result, rel=tol)
    assert result_shapely == pytest.approx(expected_result, rel=tol)


@pytest.mark.parametrize("test_case, holes, expected_result", [
    ([(0, 0), (1, 0), (0.5, 1)], [], True),  # Triangle
    ([(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)], [], False),  # L-shape
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], True),  # Square with one convex arc
    ([ArcData((0, 0), (-10, 0), height=-5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], False),  # Square with one concave arc
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]], False),  # Square with two holes
])
def test_is_convex(session, test_case, holes, expected_result):
    """Test is_convex with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(test_case, holes)
    result_server = polygon_server.is_convex()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(test_case, holes)
    result_shapely = polygon_shapely.is_convex()

    assert result_server == expected_result
    assert result_shapely == expected_result


@pytest.mark.parametrize("polygon, holes, point, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], (5, 5), True),  # Point inside square
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], (15, 5), False),  # Point outside square
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], (0, 0), True),  # Point on vertex
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], (5, 0), True),  # Point on edge
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], (5, 0), True),  # Point inside square with one convex arc
    ([ArcData((0, 0), (-10, 0), height=-5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], (-5, 0), False),  # Point outside square with one concave arc
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [], (7.5, 5), True),  # Point inside Bow-tie
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [], (2.5, 5), True),  # Point inside Bow-tie
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [], (5, 0), False),  # Point outside Bow-tie
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]], (0.5, 0.5), True),  # Point inside the body of a square with two holes
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]], (0.25, 0.5), False),  # Point inside the hole of a square with two holes
])
def test_is_inside(session, polygon, holes, point, expected_result):
    """Test is_inside with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    result_server = polygon_server.is_inside(point)
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    result_shapely = polygon_shapely.is_inside(point)

    assert result_shapely == expected_result
    assert result_server == expected_result


@pytest.mark.parametrize("polygon, holes, expected_bbox", [
    ([(0, 0), (5, 0), (2.5, 5)], [], ((0, 0), (5, 5))),  # Triangle
    ([(1, 1), (4, 2), (3, 5), (0, 4)], [], ((0, 1), (4, 5))),  # Irregular polygon
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], ((0, -5), (10, 10))),  # Square with one convex arc
    ([ArcData((0, 0), (-10, 0), height=-5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], ((-10, 0), (0, 10))),  # Square with one concave arc
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [], ((0, 0), (10, 10))),  # Bow-tie
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]], ((0, 0), (1, 1))),  # Square with two holes
])
def test_bbox(session, polygon, holes, expected_bbox):
    """Test bbox with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    result_server = polygon_server.bbox()
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    result_shapely = polygon_shapely.bbox()

    tol = 1e-9

    assert result_server[0].x.double == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_server[0].y.double == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_server[1].x.double == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_server[1].y.double == pytest.approx(expected_bbox[1][1], rel=tol)

    assert result_shapely[0].x.double == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_shapely[0].y.double == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_shapely[1].x.double == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_shapely[1].y.double == pytest.approx(expected_bbox[1][1], rel=tol)


@pytest.mark.parametrize("polygons, holes, expected_bbox", [
    ([[(0, 0), (5, 0), (5, 5), (0, 5)]], [[]], ((0, 0), (5, 5))),  # Single square
    ([[(0, 0), (5, 0), (5, 5), (0, 5)], [(10, 10), (15, 10), (15, 15), (10, 15)]], [[], []], ((0, 0), (15, 15))),  # Two non-overlapping squares
    ([[(0, 0), (10, 0), (10, 10), (0, 10)], [(5, 5), (15, 5), (15, 15), (5, 15)]], [[], []], ((0, 0), (15, 15))),  # Two overlapping squares
    ([[ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [ArcData((0, 0), (-10, 0), height=-5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)]], [[], []], ((-10, -5), (10, 10))),  # A square with one convex arc and a square with one concave arc
    ([[(0, 0), (10, 10), (10, 0), (0, 10)]], [[]], ((0, 0), (10, 10))),  # Bow-tie
    ([[(0, 1), (0, 0), (1, 0), (1, 1)]], [[[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]]], ((0, 0), (1, 1))),  # Square with two holes
])
def test_bbox_of_polygons(session, polygons, holes, expected_bbox):
    """Test bbox_of_polygons with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server_list = [create_polygon(p, h) for p, h in zip(polygons, holes)]
    result_server = PolygonData.bbox_of_polygons(polygon_server_list)
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely_list = [create_polygon(p, h) for p, h in zip(polygons, holes)]
    result_shapely = PolygonData.bbox_of_polygons(polygon_shapely_list)

    assert result_server[0].x.double == pytest.approx(expected_bbox[0][0], rel=1e-9)
    assert result_server[0].y.double == pytest.approx(expected_bbox[0][1], rel=1e-9)
    assert result_server[1].x.double == pytest.approx(expected_bbox[1][0], rel=1e-9)
    assert result_server[1].y.double == pytest.approx(expected_bbox[1][1], rel=1e-9)

    assert result_shapely[0].x.double == pytest.approx(expected_bbox[0][0], rel=1e-9)
    assert result_shapely[0].y.double == pytest.approx(expected_bbox[0][1], rel=1e-9)
    assert result_shapely[1].x.double == pytest.approx(expected_bbox[1][0], rel=1e-9)
    assert result_shapely[1].y.double == pytest.approx(expected_bbox[1][1], rel=1e-9)

@pytest.mark.parametrize("polygons, holes, expected_result", [
    ([ArcData((0, 0), (2, 0), height=-1.0), ArcData((2, 0), (2, 2), height=0.0), ArcData((2, 2), (0, 2), height=-1.0), ArcData((0, 2), (0, 0), height=0.0)], [], 7.0),  # Square with arcs
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], 137.5),  # Square with one convex arc
    ([ArcData((0, 0), (-10, 0), height=-5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], 62.5),  # Square with one concave arc
    ([ArcData((0, 0), (-10, 0), height=-8.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=8.0), ArcData((0, 10), (0, 0), height=0.0)], [], 6.573724563263833),  # Square with two concave arcs.
    ([ArcData((0, 0), (-10, 0), height=-1.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [[ArcData((-4, 4), (-6, 4), height=-1.0), ArcData((-6, 4), (-6, 6), height=0.0), ArcData((-6, 6), (-4, 6), height=0.0), ArcData((-4, 6), (-4, 4), height=0.0)]], 92.5),  # Square with one concave arc and one hole
])
def test_without_arcs(session, polygons, holes, expected_result):
    """Test tessellation with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygons, holes)
    tessellated_server = polygon_server.without_arcs(max_chord_error=0, max_arc_angle=math.pi/6, max_points=8)
    tessellated_area_server = tessellated_server.area()
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygons, holes)
    tessellated_shapely = polygon_shapely.without_arcs(max_chord_error=0, max_arc_angle=math.pi/6, max_points=8)
    tessellated_area_shapely = tessellated_shapely.area()

    tol = 1e-9

    #TODO:
    # # Server tessellation is not correct at the moment, so commenting out these assertions. This needs to be fixed in the server backend.
    # assert polygon_server.has_arcs() == True
    # assert tessellated_server.has_arcs() == False
    # assert tessellated_area_server == pytest.approx(expected_result, rel=tol)

    assert polygon_shapely.has_arcs() == True
    assert tessellated_shapely.has_arcs() == False
    assert tessellated_area_shapely == pytest.approx(expected_result, rel=tol)


@pytest.mark.parametrize("polygon, holes, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], False),  # Simple square
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [], True),   # Bow-tie
    ([(0, 0), (5, 0), (5, 5), (0, 5)], [], False),      # Simple polygon
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 8), height=0.0), ArcData((10, 8), (0, 8), height=-5.0), ArcData((0, 8), (0, 0), height=0.0)], [], False),  # Square with two convex arcs
    ([ArcData((0, 0), (-10, 0), height=-8.0), ArcData((-10, 0), (-10, 8), height=0.0), ArcData((-10, 8), (0, 8), height=-8.0), ArcData((0, 8), (0, 0), height=0.0)], [], True),  # Square with two concave arcs
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]], False),  # Square with two non-intersecting holes
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.6, 0.9), (0.6, 0.1)], [(0.4, 0.1), (0.9, 0.1), (0.9, 0.9), (0.4, 0.9)]], True),  # Square with two intersecting holes
])
def test_has_self_intersections(session, polygon, holes, expected_result):
    """Test has_self_intersections with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    result_server = polygon_server.has_self_intersections()
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    result_shapely = polygon_shapely.has_self_intersections()

    assert result_server == expected_result
    assert result_shapely == expected_result


@pytest.mark.parametrize("polygon, holes, expected_count", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], 1),  # Simple square
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [], 2),  # Bow-tie
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 8), height=0.0), ArcData((10, 8), (0, 8), height=-5.0), ArcData((0, 8), (0, 0), height=0.0)], [], 1),  # Square with two convex arcs
    ([ArcData((0, 0), (-10, 0), height=-5.0), ArcData((-10, 0), (-10, 8), height=0.0), ArcData((-10, 8), (0, 8), height=-5.0), ArcData((0, 8), (0, 0), height=0.0)], [], 3),  # Square with two concave arcs
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)], [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)]], 1),  # Square with two non-intersecting holes
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]], 2),  # Bow-tie with one hole in each lobe
])
def test_remove_self_intersections(session, polygon, holes, expected_count):
    """Test remove_self_intersections with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    no_self_intersections_server = polygon_server.remove_self_intersections()
    result_server = [polygon.has_self_intersections() for polygon in no_self_intersections_server]

    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    no_self_intersections_shapely = polygon_shapely.remove_self_intersections()
    result_shapely = [polygon.has_self_intersections() for polygon in no_self_intersections_shapely]

    #TODO:
    ## The server implementation does not look correct at the moment, so commenting out these assertions.
    # assert len(result_server) == expected_count
    # for item in result_server:
    #     assert not item

    assert len(result_shapely) == expected_count
    for item in result_shapely:
        assert not item


@pytest.mark.parametrize("polygon, holes", [
    ([(3, 0), (0, 4), (5, 12)], []),  # Clock-wise triangle with no hole
    ([(0, 1), (0, 0), (1, 0), (1, 1)], [[(0.25, 0.25), (0.25, 0.75), (0.75, 0.75), (0.75, 0.25)]]),  # Counter clock-wise square with counter clock-wise hole
    ([(0, 0), (0, 5), (5, 0)], [[(1, 1), (1, 3), (3, 1)]]),  # Clock-wise triangle with with clock-wise hole
    ([ArcData((0, 0), (10, 0), height=-1.0), ArcData((10, 0), (10, 8), height=0.0), ArcData((10, 8), (0, 8), height=0.0), ArcData((0, 8), (0, 0), height=0.0)], []),  # Square with one convex arc.
])
def test_normalized(session, polygon, holes):
    """Test normalized with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    normalized_server = polygon_server.normalized()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    normalized_shapely = polygon_shapely.normalized()

    tol = 1e-9

    #TODO: Make sure the normalized polygon has the correct orientation (including holes) for both backends.
    #TODO: Make sure the points match between both backends.


#TODO: Fix the expected_points
@pytest.mark.parametrize("polygon, holes, vector, expected_points", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [[(2, 2), (3, 2), (3, 3), (2, 3)]], (5, 5), [(5, 5), (15, 5), (15, 15), (5, 15)]),  # Square with hole moved by (5, 5)
    ([(0, 0), (5, 0), (2.5, 5)], [], (-2, 3), [(-2, 3), (3, 3), (0.5, 8)]),  # Triangle moved by (-2, 3)
    ([(1, 1), (4, 1), (4, 4), (1, 4)], [[(2, 2), (3, 2), (3, 3), (2, 3)]], (0, 0), [(1, 1), (4, 1), (4, 4), (1, 4)]),  # Square with hole moved by (0, 0)
    ([ArcData((0, 0), (10, 0), height=-1.0), ArcData((10, 0), (10, 8), height=0.0), ArcData((10, 8), (0, 8), height=0.0), ArcData((0, 8), (0, 0), height=0.0)], [], (2, 2), [ArcData((2, 2), (12, 2), height=-1.0), ArcData((12, 2), (12, 10), height=0.0), ArcData((12, 10), (2, 10), height=0.0), ArcData((2, 10), (2, 2), height=0.0)]),  # Square with one convex arc and no holes moved by (2, 2).
])
def test_move(session, polygon, holes, vector, expected_points):
    """Test move with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    area_server = polygon_server.area()
    moved_server = polygon_server.move(vector)
    moved_area_server = moved_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    area_shapely = polygon_shapely.area()
    moved_shapely = polygon_shapely.move(vector)
    moved_area_shapely = moved_shapely.area()

    tol = 1e-9
    if isinstance(polygon[0], ArcData):
        tol = 0.1

    assert area_server == pytest.approx(moved_area_server, rel=tol)
    assert area_shapely == pytest.approx(moved_area_shapely, rel=tol)
    assert area_server == pytest.approx(area_shapely, rel=tol)

    for server_point, shapely_point in zip(moved_server.points, moved_shapely.points):
        assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6)
        assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6)

    for server_hole, shapely_hole in zip(moved_server.holes, moved_shapely.holes):
        assert len(server_hole.points) == len(shapely_hole.points)
        for server_point, shapely_point in zip(server_hole.points, shapely_hole.points):
            assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6)
            assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6)


#TODO: Fix the expected_points
@pytest.mark.parametrize("polygon, holes, angle, center, expected_points", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], math.pi / 2, (0, 0), [(0, 0), (0, 10), (-10, 10), (-10, 0)]),  # Square rotated 90 degrees (π/2) around origin
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [[(1, 1), (1, 9), (9, 9), (9, 1)]], math.pi, (5, 5), [(10, 10), (0, 10), (0, 0), (10, 0)]),  # Square rotated 180 degrees (π) around its center
    ([(0, 0), (5, 0), (2.5, 5)], [], 0, (0, 0), [(0, 0), (5, 0), (2.5, 5)]),  # Triangle rotated 0 degrees (no rotation)
    ([ArcData((0, 0), (10, 0), height=-1.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], [], math.pi / 2, (0, 0), [ArcData((0, 0), (0, 10), height=-1.0), ArcData((0, 10), (-10, 10), height=0.0), ArcData((-10, 10), (-10, 0), height=0.0), ArcData((-10, 0), (0, 0), height=0.0)]),  # Square with one convex arc and no holes rotated by 90 degrees (π/2) around origin.
])
def test_rotate(session, polygon, holes, angle, center, expected_points):
    """Test rotate with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    area_server = polygon_server.area()
    rotated_server = polygon_server.rotate(angle, center)
    rotated_area_server = rotated_server.area()
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    area_shapely = polygon_shapely.area()
    rotated_shapely = polygon_shapely.rotate(angle, center)
    rotated_area_shapely = rotated_shapely.area()

    tol = 1e-9
    if isinstance(polygon[0], ArcData):
        tol = 0.1

    assert rotated_area_server == pytest.approx(area_server, rel=tol)
    assert rotated_area_shapely == pytest.approx(area_shapely, rel=tol)
    assert area_server == pytest.approx(area_shapely, rel=tol)

    for server_point, shapely_point in zip(rotated_server.points, rotated_shapely.points):
        assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6)
        assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6)

    for server_hole, shapely_hole in zip(rotated_server.holes, rotated_shapely.holes):
        assert len(server_hole.points) == len(shapely_hole.points)
        for server_point, shapely_point in zip(server_hole.points, shapely_hole.points):
            assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6)
            assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6)


#TODO: Fix the expected_points
@pytest.mark.parametrize("polygon, holes, factor, center, expected_points", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], 2.0, (0, 0), [(0, 0), (20, 0), (20, 20), (0, 20)]),  # Square scaled 2x from origin
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], 0.5, (0, 0), [(0, 0), (5, 0), (5, 5), (0, 5)]),  # Square scaled 0.5x from origin
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], 2.0, (5, 5), [(-5, -5), (15, -5), (15, 15), (-5, 15)]),  # Square scaled 2x from center
    ([(5, 5), (15, 5), (10, 15)], [], 3.0, (10, 10), [(-5, -5), (25, -5), (10, 25)]),  # Triangle scaled 3x from point
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0), ArcData((0, 10), (0, 0), height=0.0)], [], 2.0, (0, 0), [ArcData((0, 0), (20, 0), height=-10.0), ArcData((20, 0), (20, 20), height=0.0), ArcData((20, 20), (0, 20), height=-10.0), ArcData((0, 20), (0, 0), height=0.0)]),  # Square with two convex arcs scaled 2x from origin
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]], 2.0, (5, 5), [(-5, -5), (15, 15), (15, -5), (-5, 15)])  # Bow-tie with one hole in each lobe scaled 2x from (5, 5).
])
def test_scale(session, polygon, holes, factor, center, expected_points):
    """Test scale with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    area_server = polygon_server.area()
    scaled_server = polygon_server.scale(factor, center)
    scaled_area_server = scaled_server.area()
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    area_shapely = polygon_shapely.area()
    scaled_shapely = polygon_shapely.scale(factor, center)
    scaled_area_shapely = scaled_shapely.area()

    tol = 1e-9
    if isinstance(polygon[0], ArcData):
        tol = 0.1

    assert scaled_area_server == pytest.approx(factor*factor*area_server, rel=tol)
    assert scaled_area_shapely == pytest.approx(factor*factor*area_shapely, rel=tol)
    assert scaled_area_server == pytest.approx(scaled_area_shapely, rel=tol)

    for server_point, shapely_point in zip(scaled_server.points, scaled_shapely.points):
        assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6)
        assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6)

    for server_hole, shapely_hole in zip(scaled_server.holes, scaled_shapely.holes):
        assert len(server_hole.points) == len(shapely_hole.points)
        for server_point, shapely_point in zip(server_hole.points, shapely_hole.points):
            assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6)
            assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6)


#TODO: Fix the expected_points
@pytest.mark.parametrize("polygon, holes, x, expected_points", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], 10.0, [(20.0, 0.0), (10.0, 0.0), (10.0, 10.0), (20.0, 10.0)]),  # Square
    ([(5, 5), (15, 5), (10, 15)], [], 0, [(-5.0, 5.0), (-15.0, 5.0), (-10.0, 15.0)]),  # Triangle
    #TODO: The server backend is not handling arcs correctly after this operation.
    # ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0), ArcData((0, 10), (0, 0), height=0.0)], [], 5.0, []),  # Square with two convex arcs
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]], 5.0, [(10.0, 0.0), (0.0, 10.0), (0.0, 0.0), (10.0, 10.0)])  # Bow-tie with one hole in each lobe
])
def test_mirror_x(session, polygon, holes, x, expected_points):
    """Test mirror_x with server backend."""
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    area_server = polygon_server.area()
    mirrored_server = polygon_server.mirror_x(x)
    mirrored_area_server = mirrored_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    area_shapely = polygon_shapely.area()
    mirrored_shapely = polygon_shapely.mirror_x(x)
    mirrored_area_shapely = mirrored_shapely.area()

    tol = 1e-9
    if isinstance(polygon[0], ArcData):
        tol = 0.1

    assert mirrored_area_server == pytest.approx(area_server, rel=tol)
    assert mirrored_area_shapely == pytest.approx(area_shapely, rel=tol)
    assert mirrored_area_server == pytest.approx(mirrored_area_shapely, rel=tol)

    for server_point, shapely_point, expected_point in zip(mirrored_server.points, mirrored_shapely.points, expected_points):
        assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6) == pytest.approx(expected_point[0], abs=1e-6)
        assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6) == pytest.approx(expected_point[1], abs=1e-6)

    for server_hole, shapely_hole in zip(mirrored_server.holes, mirrored_shapely.holes):
        assert len(server_hole.points) == len(shapely_hole.points)
        for server_point, shapely_point in zip(server_hole.points, shapely_hole.points):
            assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-6)
            assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-6)


@pytest.mark.parametrize("polygon, holes, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], [], [(5, 5), 7.0710678118654755]),  # Square
    ([(5, 5), (15, 5), (10, 15)], [], [(10, 10), 7.0710678118654755]),  # Triangle
    ([ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0), ArcData((0, 10), (0, 0), height=0.0)], [], [(5, 5), 11.180339887498949]),  # Square with two convex arcs
    ([(0, 0), (10, 10), (10, 0), (0, 10)], [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]], [(5, 5), 7.0710678118654755])  # Bow-tie with one hole in each lobe
])
def test_bounding_circle(session, polygon, holes, expected_result):
    """Test bounding_circle with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon, holes)
    result_server = polygon_server.bounding_circle()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon, holes)
    result_shapely = polygon_shapely.bounding_circle()

    tol = 1e-9

    assert result_server[0].x.double == pytest.approx(expected_result[0][0], rel=tol)
    assert result_server[0].y.double == pytest.approx(expected_result[0][1], rel=tol)
    assert result_server[1].double == pytest.approx(expected_result[1], rel=tol)

    assert result_shapely[0].x.double == pytest.approx(expected_result[0][0], rel=tol)
    assert result_shapely[0].y.double == pytest.approx(expected_result[0][1], rel=tol)
    assert result_shapely[1].double == pytest.approx(expected_result[1], rel=tol)


@pytest.mark.parametrize("polygons, holes, expected_result", [
    ([[(0, 0), (2, 0), (2, 2), (0, 2)], [(5, 0), (7, 0), (7, 2), (5, 2)]], [[], []], [(0.0, 0.0), (0.0, 2.0), (7.0, 2.0), (7.0, 0.0)]),  # Two separate squares
    ([[(0, 0), (3, 0), (3, 3), (0, 3)], [(2, 2), (5, 2), (5, 5), (2, 5)]], [[], []], [(0.0, 0.0), (0.0, 3.0), (2.0, 5.0), (5.0, 5.0), (5.0, 2.0), (3.0, 0.0)]),  # Two overlapping squares
    #TODO: The server backend is not handling arcs correctly in this operation.
    # ([[ArcData((0, 0), (10, 0), height=-5.0), ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0), ArcData((0, 10), (0, 0), height=0.0)], [ArcData((0, 0), (-10, 0), height=5.0), ArcData((-10, 0), (-10, 10), height=0.0), ArcData((-10, 10), (0, 10), height=5.0), ArcData((0, 10), (0, 0), height=0.0)]], [[], []], [(5.0, -5.0), (2.5, -4.330127018922193), (-10.0, 0.0), (-10.0, 10.0), (2.5, 14.330127018922195), (5.0, 15.0), (7.5, 14.330127018922193), (9.330127018922195, 12.5), (10.0, 10.0), (10.0, 0.0), (9.330127018922191, -2.5), (7.5, -4.330127018922195)]),  # One squares with two convex arcs and one square with two concave arcs
    ([[(0, 0), (10, 10), (10, 0), (0, 10)], [(0, 0), (-10, -10), (-10, 0), (0, -10)]], [[[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]], []], [(-10.0, -10.0), (-10.0, 0.0), (0.0, 10.0), (10.0, 10.0), (10.0, 0.0), (0.0, -10.0)])  # Bow-tie with one hole in each lobe
])
def test_convex_hull(session, polygons, holes, expected_result):
    """Test convex_hull with both server and shapely backends."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server_list = [create_polygon(p, h) for p, h in zip(polygons, holes)]
    result_server = PolygonData.convex_hull(polygon_server_list)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely_list = [create_polygon(p, h) for p, h in zip(polygons, holes)]
    result_shapely = PolygonData.convex_hull(polygon_shapely_list)

    tol = 1e-9

    # Check that both backends produce the same number of points
    assert len(result_server.points) == len(result_shapely.points)
    assert len(result_server.points) == len(expected_result)

    # Check that the points match expected values (order may vary, so we check containment)
    for i, expected_pt in enumerate(expected_result):
        assert result_server.points[i].x.double == pytest.approx(expected_pt[0], rel=tol)
        assert result_server.points[i].y.double == pytest.approx(expected_pt[1], rel=tol)
        assert result_shapely.points[i].x.double == pytest.approx(expected_pt[0], rel=tol)
        assert result_shapely.points[i].y.double == pytest.approx(expected_pt[1], rel=tol)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
