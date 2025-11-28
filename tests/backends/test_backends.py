import math
import pytest
from ansys.edb.core.config import Config, ComputationBackend
from ansys.edb.core.geometry.arc_data import ArcData
from utils.fixtures import session


def test_config_default(session):
    """Test default configuration."""
    Config.reset()
    backend = Config.get_computation_backend()
    assert backend == ComputationBackend.AUTO


def test_config_set_backend(session):
    """Test setting backend programmatically."""
    Config.set_computation_backend(ComputationBackend.SERVER)
    assert Config.get_computation_backend() == ComputationBackend.SERVER
    
    Config.set_computation_backend('shapely')
    assert Config.get_computation_backend() == ComputationBackend.SHAPELY
    
    Config.reset()


def test_config_environment_variable(session):
    """Test setting backend via environment variable."""
    import os
    
    # Save original value
    original = os.environ.get('PYEDB_COMPUTATION_BACKEND')
    
    try:
        os.environ['PYEDB_COMPUTATION_BACKEND'] = 'server'
        Config.reset()
        assert Config.get_computation_backend() == ComputationBackend.SERVER
        
        os.environ['PYEDB_COMPUTATION_BACKEND'] = 'shapely'
        Config.reset()
        assert Config.get_computation_backend() == ComputationBackend.SHAPELY
        
    finally:
        # Restore original value
        if original is not None:
            os.environ['PYEDB_COMPUTATION_BACKEND'] = original
        elif 'PYEDB_COMPUTATION_BACKEND' in os.environ:
            del os.environ['PYEDB_COMPUTATION_BACKEND']
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


@pytest.mark.parametrize("test_case, expected_result", [
    ([(0, 0), (10, 0), (10, 10)], 50.0),  # Triangle
])
def test_polygon_area_server_backend(session, test_case, expected_result):
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()

    polygon = PolygonData(test_case)
    area = polygon.area()
    assert area == pytest.approx(expected_result)


@pytest.mark.parametrize("test_case, expected_result", [
    ([(0, 0), (10, 0), (10, 10)], 50.0),  # Triangle
])
def test_polygon_area_shapely_backend(session, test_case, expected_result):
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
     
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    polygon = PolygonData(test_case)
    area = polygon.area()
    assert area == pytest.approx(expected_result)


@pytest.mark.parametrize("test_case", [
    ([(0, 0), (10, 0), (10, 10)]),  # Triangle
])
def test_polygon_backends_match(session, test_case):
    '''Test that server and Shapely backends give same results.'''
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Get result from server
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    polygon1 = PolygonData(test_case)
    server_area = polygon1.area()
    
    # Get result from Shapely
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    polygon2 = PolygonData(test_case)
    shapely_area = polygon2.area()
    
    # Should match within floating point tolerance
    assert server_area == pytest.approx(shapely_area, rel=1e-9)


@pytest.mark.parametrize("test_case, expected_result", [
    ([(0, 0), (1, 0), (0.5, 1)], True),  # Triangle
    ([(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)], False),  # L-shape
])
def test_is_convex_server_backend(session, test_case, expected_result):
    """Test is_convex with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()

    polygon = PolygonData(test_case)
    assert polygon.is_convex() == expected_result


@pytest.mark.parametrize("test_case, expected_result", [
    ([(0, 0), (1, 0), (0.5, 1)], True),  # Triangle
    ([(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)], False),  # L-shape
])
def test_is_convex_shapely_backend(session, test_case, expected_result):
    """Test is_convex with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    convex_polygon = PolygonData(test_case)
    assert convex_polygon.is_convex() == expected_result


@pytest.mark.parametrize("test_case, expected_result", [
    ([(0, 0), (1, 0), (1, 1), (0, 1)], True),  # Square
    ([(0, 0), (3, 0), (3, 2), (2, 1), (0, 2)], False),  # Concave pentagon
])
def test_is_convex_backends_match(session, test_case, expected_result):
    """Test that server and Shapely backends give same is_convex results."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Get result from server
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    polygon1 = PolygonData(test_case)
    server_result = polygon1.is_convex()
    
    # Get result from Shapely
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    polygon2 = PolygonData(test_case)
    shapely_result = polygon2.is_convex()
    
    # Both should match
    assert server_result == shapely_result
    assert server_result == expected_result


@pytest.mark.parametrize("polygon, point, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 5), True),  # Point inside square
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (15, 5), False),  # Point outside square
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (0, 0), True),  # Point on vertex
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 0), True),  # Point on edge
])
def test_is_inside_server_backend(session, polygon, point, expected_result):
    """Test is_inside with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()

    poly = PolygonData(polygon)
    assert poly.is_inside(point) == expected_result


@pytest.mark.parametrize("polygon, point, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 5), True),  # Point inside square
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (15, 5), False),  # Point outside square
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (0, 0), True),  # Point on vertex
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 0), True),  # Point on edge
])
def test_is_inside_shapely_backend(session, polygon, point, expected_result):
    """Test is_inside with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly = PolygonData(polygon)
    assert poly.is_inside(point) == expected_result


@pytest.mark.parametrize("polygon, point, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 5), True),  # Point inside square
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (15, 5), False),  # Point outside square
    ([(0, 0), (10, 0), (5, 10)], (5, 5), True),  # Point inside triangle
    ([(0, 0), (10, 0), (5, 10)], (0, 5), False),  # Point outside triangle
])
def test_is_inside_backends_match(session, polygon, point, expected_result):
    """Test that server and Shapely backends give same is_inside results."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Get result from server
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    polygon1 = PolygonData(polygon)
    server_result = polygon1.is_inside(point)
    
    # Get result from Shapely
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    polygon2 = PolygonData(polygon)
    shapely_result = polygon2.is_inside(point)
    
    # Both should match
    assert server_result == shapely_result
    assert server_result == expected_result


@pytest.mark.parametrize("polygon, expected_bbox", [
    ([(0, 0), (5, 0), (2.5, 5)], ((0, 0), (5, 5))),  # Triangle
    ([(1, 1), (4, 2), (3, 5), (0, 4)], ((0, 1), (4, 5))),  # Irregular polygon
])
def test_bbox_server_backend(session, polygon, expected_bbox):
    """Test bbox with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()

    poly = PolygonData(polygon)
    bbox = poly.bbox()
    
    # Verify the bounding box coordinates
    assert bbox[0].x.double == pytest.approx(expected_bbox[0][0])
    assert bbox[0].y.double == pytest.approx(expected_bbox[0][1])
    assert bbox[1].x.double == pytest.approx(expected_bbox[1][0])
    assert bbox[1].y.double == pytest.approx(expected_bbox[1][1])


@pytest.mark.parametrize("polygon, expected_bbox", [
    ([(0, 0), (5, 0), (2.5, 5)], ((0, 0), (5, 5))),  # Triangle
    ([(1, 1), (4, 2), (3, 5), (0, 4)], ((0, 1), (4, 5))),  # Irregular polygon
])
def test_bbox_shapely_backend(session, polygon, expected_bbox):
    """Test bbox with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly = PolygonData(polygon)
    bbox = poly.bbox()
    
    # Verify the bounding box coordinates
    assert bbox[0].x.double == pytest.approx(expected_bbox[0][0])
    assert bbox[0].y.double == pytest.approx(expected_bbox[0][1])
    assert bbox[1].x.double == pytest.approx(expected_bbox[1][0])
    assert bbox[1].y.double == pytest.approx(expected_bbox[1][1])


@pytest.mark.parametrize("polygon, expected_bbox", [
    ([(0, 0), (5, 0), (2.5, 5)], ((0, 0), (5, 5))),  # Triangle
    ([(1, 1), (4, 2), (3, 5), (0, 4)], ((0, 1), (4, 5))),  # Irregular polygon
])
def test_bbox_backends_match(session, polygon, expected_bbox):
    """Test that server and Shapely backends give same bbox results."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Get result from server
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    polygon1 = PolygonData(polygon)
    server_bbox = polygon1.bbox()
    
    # Get result from Shapely
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    polygon2 = PolygonData(polygon)
    shapely_bbox = polygon2.bbox()
    
    # Both should match
    assert server_bbox[0].x.double == pytest.approx(shapely_bbox[0].x.double, rel=1e-9)
    assert server_bbox[0].y.double == pytest.approx(shapely_bbox[0].y.double, rel=1e-9)
    assert server_bbox[1].x.double == pytest.approx(shapely_bbox[1].x.double, rel=1e-9)
    assert server_bbox[1].y.double == pytest.approx(shapely_bbox[1].y.double, rel=1e-9)
    
    # And match expected values
    assert server_bbox[0].x.double == pytest.approx(expected_bbox[0][0])
    assert server_bbox[0].y.double == pytest.approx(expected_bbox[0][1])
    assert server_bbox[1].x.double == pytest.approx(expected_bbox[1][0])
    assert server_bbox[1].y.double == pytest.approx(expected_bbox[1][1])


@pytest.mark.parametrize("polygons, expected_bbox", [
    ([[(0, 0), (5, 0), (5, 5), (0, 5)]], ((0, 0), (5, 5))),  # Single square
    ([[(0, 0), (5, 0), (5, 5), (0, 5)], [(10, 10), (15, 10), (15, 15), (10, 15)]], ((0, 0), (15, 15))),  # Two non-overlapping squares
    ([[(0, 0), (10, 0), (10, 10), (0, 10)], [(5, 5), (15, 5), (15, 15), (5, 15)]], ((0, 0), (15, 15))),  # Two overlapping squares
])
def test_bbox_of_polygons_server_backend(session, polygons, expected_bbox):
    """Test bbox_of_polygons with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()

    poly_list = [PolygonData(p) for p in polygons]
    bbox = PolygonData.bbox_of_polygons(poly_list)
    
    # Verify the bounding box coordinates
    assert bbox[0].x.double == pytest.approx(expected_bbox[0][0])
    assert bbox[0].y.double == pytest.approx(expected_bbox[0][1])
    assert bbox[1].x.double == pytest.approx(expected_bbox[1][0])
    assert bbox[1].y.double == pytest.approx(expected_bbox[1][1])


@pytest.mark.parametrize("polygons, expected_bbox", [
    ([[(0, 0), (5, 0), (5, 5), (0, 5)]], ((0, 0), (5, 5))),  # Single square
    ([[(0, 0), (5, 0), (5, 5), (0, 5)], [(10, 10), (15, 10), (15, 15), (10, 15)]], ((0, 0), (15, 15))),  # Two non-overlapping squares
    ([[(0, 0), (10, 0), (10, 10), (0, 10)], [(5, 5), (15, 5), (15, 15), (5, 15)]], ((0, 0), (15, 15))),  # Two overlapping squares
])
def test_bbox_of_polygons_shapely_backend(session, polygons, expected_bbox):
    """Test bbox_of_polygons with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly_list = [PolygonData(p) for p in polygons]
    bbox = PolygonData.bbox_of_polygons(poly_list)
    
    # Verify the bounding box coordinates
    assert bbox[0].x.double == pytest.approx(expected_bbox[0][0])
    assert bbox[0].y.double == pytest.approx(expected_bbox[0][1])
    assert bbox[1].x.double == pytest.approx(expected_bbox[1][0])
    assert bbox[1].y.double == pytest.approx(expected_bbox[1][1])


@pytest.mark.parametrize("polygons, expected_bbox", [
    ([[(0, 0), (10, 0), (10, 10), (0, 10)]], ((0, 0), (10, 10))),  # Single square
    ([[(0, 0), (5, 0), (2.5, 5)], [(10, 0), (15, 0), (12.5, 8)]], ((0, 0), (15, 8))),  # Two triangles
])
def test_bbox_of_polygons_backends_match(session, polygons, expected_bbox):
    """Test that server and Shapely backends give same bbox_of_polygons results."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Get result from server
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    poly_list_1 = [PolygonData(p) for p in polygons]
    server_bbox = PolygonData.bbox_of_polygons(poly_list_1)
    
    # Get result from Shapely
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    poly_list_2 = [PolygonData(p) for p in polygons]
    shapely_bbox = PolygonData.bbox_of_polygons(poly_list_2)
    
    # Both should match
    assert server_bbox[0].x.double == pytest.approx(shapely_bbox[0].x.double, rel=1e-9)
    assert server_bbox[0].y.double == pytest.approx(shapely_bbox[0].y.double, rel=1e-9)
    assert server_bbox[1].x.double == pytest.approx(shapely_bbox[1].x.double, rel=1e-9)
    assert server_bbox[1].y.double == pytest.approx(shapely_bbox[1].y.double, rel=1e-9)
    
    # And match expected values
    assert server_bbox[0].x.double == pytest.approx(expected_bbox[0][0])
    assert server_bbox[0].y.double == pytest.approx(expected_bbox[0][1])
    assert server_bbox[1].x.double == pytest.approx(expected_bbox[1][0])
    assert server_bbox[1].y.double == pytest.approx(expected_bbox[1][1])

@pytest.mark.parametrize("arc_config, expected_result", [
    ([ArcData((0, 0), (2, 0), height=-1.0), ArcData((2, 0), (2, 2), height=0.0), 
      ArcData((2, 2), (0, 2), height=-1.0), ArcData((0, 2), (0, 0), height=0.0)], 7.0),
])
def test_tessellation_server_backend(session, arc_config, expected_result):
    """Test tessellation with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.arc_data import ArcData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    
    # Create a polygon with arcs
    poly = PolygonData(arcs=arc_config)
    
    # Verify polygon has arcs
    assert poly.has_arcs() == True
    
    # Tessellate the polygon
    tessellated = poly.without_arcs(max_chord_error=0, max_arc_angle=math.pi/6, max_points=8)
    
    # Verify tessellation removed arcs
    assert tessellated.has_arcs() == False
    
    # Verify tessellated polygon has more points than arcs
    assert len(tessellated.points) > len(poly.points)
    
    # Verify area is approximately correct
    tessellated_area = tessellated.area()
    assert tessellated_area == pytest.approx(expected_result, rel=1e-9)


@pytest.mark.parametrize("arc_config, expected_result", [
    ([ArcData((0, 0), (2, 0), height=-1.0), ArcData((2, 0), (2, 2), height=0.0), 
      ArcData((2, 2), (0, 2), height=-1.0), ArcData((0, 2), (0, 0), height=0.0)], 7.0),
])
def test_tessellation_shapely_backend(session, arc_config, expected_result):
    """Test tessellation with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    # Create a polygon with arcs
    poly = PolygonData(arcs=arc_config)
    
    # Verify polygon has arcs
    assert poly.has_arcs() == True
    
    # Tessellate the polygon
    tessellated = poly.without_arcs(max_chord_error=0, max_arc_angle=math.pi/6, max_points=8)
    
    # Verify tessellation removed arcs
    assert tessellated.has_arcs() == False
    
    # Verify tessellated polygon has more points than arcs
    assert len(tessellated.points) > len(poly.points)
    
    # Verify area is approximately correct
    original_area = poly.area()  # Unlike server backend, in Shapely backend, area() performs tessellation internally. As a result, in shapely backend, area() before and after tessellation should match. In server backend, area() before tessellation will be larger than after.
    tessellated_area = tessellated.area()
    assert tessellated_area == pytest.approx(expected_result, rel=1e-9)
    assert tessellated_area == pytest.approx(original_area, rel=1e-9)


@pytest.mark.parametrize("arc_config", [
    ([ArcData((0, 0), (2, 0), height=-1.0), ArcData((2, 0), (2, 2), height=0.0), 
      ArcData((2, 2), (0, 2), height=-1.0), ArcData((0, 2), (0, 0), height=0.0)]),
])
def test_tessellation_backends_match(session, arc_config):
    """Test that server and Shapely backends produce consistent tessellation results."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Test with server backend
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    rounded_poly_server = PolygonData(arcs=arc_config)
    tessellated_server = rounded_poly_server.without_arcs(max_chord_error=0, max_arc_angle=math.pi/6, max_points=8)
    server_area = tessellated_server.area()
    
    # Test with Shapely backend
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    rounded_poly_shapely = PolygonData(arcs=arc_config)
    tessellated_shapely = rounded_poly_shapely.without_arcs(max_chord_error=0, max_arc_angle=math.pi/6, max_points=8)
    shapely_area = tessellated_shapely.area()
    
    # Both tessellations should produce similar areas
    assert server_area == pytest.approx(shapely_area, rel=1e-9)
    
    # Both should have no arcs after tessellation
    assert tessellated_server.has_arcs() == False
    assert tessellated_shapely.has_arcs() == False


@pytest.mark.parametrize("arc_config, expected_has_more_points", [
    # Simple arc
    ([ArcData((0, 0), (10, 0), height=2.0), ArcData((10, 0), (10, 10), height=0.0), 
      ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], True),
    # Multiple arcs
    ([ArcData((0, 0), (5, 0), height=1.0), ArcData((5, 0), (5, 5), height=1.0), 
      ArcData((5, 5), (0, 5), height=1.0), ArcData((0, 5), (0, 0), height=1.0)], True),
    # No arcs (all straight edges)
    ([ArcData((0, 0), (5, 0), height=0.0), ArcData((5, 0), (5, 5), height=0.0), 
      ArcData((5, 5), (0, 5), height=0.0), ArcData((0, 5), (0, 0), height=0.0)], False),
])
def test_tessellation_point_count_server(session, arc_config, expected_has_more_points):
    """Test that tessellation produces expected number of points with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    
    poly = PolygonData(arcs=arc_config)
    original_point_count = len(poly.points)
    
    tessellated = poly.without_arcs(max_chord_error=0.01, max_arc_angle=0.5, max_points=8)
    tessellated_point_count = len(tessellated.points)
    
    if expected_has_more_points:
        assert tessellated_point_count > original_point_count
    else:
        # For polygons with no arcs, point count should be similar
        assert ((tessellated_point_count + 1 == original_point_count) or (tessellated_point_count == original_point_count))  # May close differently


@pytest.mark.parametrize("arc_config, expected_has_more_points", [
    # Simple arc
    ([ArcData((0, 0), (10, 0), height=2.0), ArcData((10, 0), (10, 10), height=0.0), 
      ArcData((10, 10), (0, 10), height=0.0), ArcData((0, 10), (0, 0), height=0.0)], True),
    # Multiple arcs
    ([ArcData((0, 0), (5, 0), height=1.0), ArcData((5, 0), (5, 5), height=1.0), 
      ArcData((5, 5), (0, 5), height=1.0), ArcData((0, 5), (0, 0), height=1.0)], True),
    # No arcs (all straight edges)
    ([ArcData((0, 0), (5, 0), height=0.0), ArcData((5, 0), (5, 5), height=0.0), 
      ArcData((5, 5), (0, 5), height=0.0), ArcData((0, 5), (0, 0), height=0.0)], False),
])
def test_tessellation_point_count_shapely(session, arc_config, expected_has_more_points):
    """Test that tessellation produces expected number of points with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly = PolygonData(arcs=arc_config)
    original_point_count = len(poly.points)
    
    tessellated = poly.without_arcs(max_chord_error=0.01, max_arc_angle=0.5, max_points=8)
    tessellated_point_count = len(tessellated.points)
    
    if expected_has_more_points:
        assert tessellated_point_count > original_point_count
    else:
        # For polygons with no arcs, point count should be similar
        assert ((tessellated_point_count + 1 == original_point_count) or (tessellated_point_count == original_point_count))  # May close differently


@pytest.mark.parametrize("arc_config", [
    ([ArcData((0, 0), (2, 0), height=-1.0), ArcData((2, 0), (2, 2), height=0.0), 
      ArcData((2, 2), (0, 2), height=-1.0), ArcData((0, 2), (0, 0), height=0.0)]),
])
def test_tessellation_operations_on_arc_polygon_server(session, arc_config):
    """Test that geometry operations work on arc polygons with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.arc_data import ArcData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    
    # Create a polygon with arcs
    rounded_poly = PolygonData(arcs=arc_config)
    
    # Test that operations work
    area = rounded_poly.area()
    assert area > 0
    
    is_convex = rounded_poly.is_convex()
    assert isinstance(is_convex, bool)
    
    is_inside = rounded_poly.is_inside((1, 1))
    assert is_inside == True
    
    bbox = rounded_poly.bbox()
    assert bbox is not None


@pytest.mark.parametrize("arc_config", [
    ([ArcData((0, 0), (2, 0), height=-1.0), ArcData((2, 0), (2, 2), height=0.0), 
      ArcData((2, 2), (0, 2), height=-1.0), ArcData((0, 2), (0, 0), height=0.0)]),
])
def test_tessellation_operations_on_arc_polygon_shapely(session, arc_config):
    """Test that geometry operations work on arc polygons with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.arc_data import ArcData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    # Create a polygon with arcs
    rounded_poly = PolygonData(arcs=arc_config)
    
    # Test that operations work (Shapely backend should tessellate internally)
    area = rounded_poly.area()
    assert area > 0
    
    is_convex = rounded_poly.is_convex()
    assert isinstance(is_convex, bool)
    
    is_inside = rounded_poly.is_inside((1, 1))
    assert is_inside == True
    
    bbox = rounded_poly.bbox()
    assert bbox is not None


@pytest.mark.parametrize("polygon, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], False),  # Simple square - no self-intersections
    ([(0, 0), (10, 10), (10, 0), (0, 10)], True),   # Bow-tie - has self-intersections
    ([(0, 0), (5, 0), (5, 5), (0, 5)], False),      # Another simple polygon - no self-intersections
])
def test_has_self_intersections_server_backend(session, polygon, expected_result):
    """Test has_self_intersections with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    
    result = poly.has_self_intersections()
    assert result == expected_result


@pytest.mark.parametrize("polygon, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], False),  # Simple square - no self-intersections
    ([(0, 0), (10, 10), (10, 0), (0, 10)], True),   # Bow-tie - has self-intersections
    ([(0, 0), (5, 0), (5, 5), (0, 5)], False),      # Another simple polygon - no self-intersections
])
def test_has_self_intersections_shapely_backend(session, polygon, expected_result):
    """Test has_self_intersections with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    
    result = poly.has_self_intersections()
    assert result == expected_result


@pytest.mark.parametrize("polygon, expected_result", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], False),  # Simple square - no self-intersections
    ([(0, 0), (10, 10), (10, 0), (0, 10)], True),   # Bow-tie - has self-intersections
])
def test_has_self_intersections_backends_match(session, polygon, expected_result):
    """Test that both backends give the same result for has_self_intersections."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Test with server backend
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    poly_server = PolygonData(points=polygon)
    result_server = poly_server.has_self_intersections()
    
    # Test with Shapely backend
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    poly_shapely = PolygonData(points=polygon)
    result_shapely = poly_shapely.has_self_intersections()
    
    # Both backends should give the same result
    assert result_server == result_shapely == expected_result


@pytest.mark.parametrize("polygon, expected_count", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], 1),  # Simple square - should return 1 polygon
    # ([(0, 0), (10, 10), (10, 0), (0, 10)], 2),  # Bow-tie - should split into 2 polygons. However, the server implementation is returning 1 which is incorrect. This needs to be fixed in the server backend.
])
def test_remove_self_intersections_server_backend(session, polygon, expected_count):
    """Test remove_self_intersections with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    result = poly.remove_self_intersections()
    
    # Check that we get the expected number of polygons
    assert len(result) == expected_count
    
    # All resulting polygons should have no self-intersections
    for p in result:
        assert not p.has_self_intersections()


@pytest.mark.parametrize("polygon, expected_count", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], 1),  # Simple square - should return 1 polygon
    ([(0, 0), (10, 10), (10, 0), (0, 10)], 2),  # Bow-tie - should split into 2 polygons
])
def test_remove_self_intersections_shapely_backend(session, polygon, expected_count):
    """Test remove_self_intersections with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    result = poly.remove_self_intersections()
    
    # Check that we get the expected number of polygons
    assert len(result) == expected_count
    
    # All resulting polygons should have no self-intersections
    for p in result:
        assert not p.has_self_intersections()


@pytest.mark.parametrize("polygon", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)]),  # Simple square
    # ([(0, 0), (10, 10), (10, 0), (0, 10)]),  # Bow-tie. The server implementation is returning 1 which is incorrect. It should return 2. This needs to be fixed in the server backend.
])
def test_remove_self_intersections_backends_match(session, polygon):
    """Test that both backends produce consistent results for remove_self_intersections."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Test with server backend
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    poly_server = PolygonData(points=polygon)
    result_server = poly_server.remove_self_intersections()
    
    # Test with Shapely backend
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    poly_shapely = PolygonData(points=polygon)
    result_shapely = poly_shapely.remove_self_intersections()
    
    # Both backends should give the same number of resulting polygons
    assert len(result_server) == len(result_shapely)
    
    # All resulting polygons from both backends should have no self-intersections
    for p in result_server:
        assert not p.has_self_intersections()
    for p in result_shapely:
        assert not p.has_self_intersections()


@pytest.mark.parametrize("polygon, expected_normalized", [
    ([(3, 0), (0, 4), (5, 12)], [(1.0, 0.0), (0.0, 1.0), (5/13, 12/13)]),  # Triangle
    ([(1, 0), (0, 1), (1, 1)], [(1.0, 0.0), (0.0, 1.0), (1/math.sqrt(2), 1/math.sqrt(2))]),  # Triangle
    ([(0, 0), (5, 0), (0, 5)], [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]),  # Triangle with origin point
])
def test_normalized_server_backend(session, polygon, expected_normalized):
    """Test normalized with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    normalized = poly.normalized()
    
    # Check that we get the expected number of points
    assert len(normalized) == len(expected_normalized)
    
    # Verify each normalized point
    for i, (actual_point, expected_coords) in enumerate(zip(normalized, expected_normalized)):
        assert actual_point.x.double == pytest.approx(expected_coords[0], abs=1e-9)
        assert actual_point.y.double == pytest.approx(expected_coords[1], abs=1e-9)


@pytest.mark.parametrize("polygon, expected_normalized", [
    ([(3, 0), (0, 4), (5, 12)], [(1.0, 0.0), (0.0, 1.0), (5/13, 12/13)]),  # Triangle
    ([(1, 0), (0, 1), (1, 1)], [(1.0, 0.0), (0.0, 1.0), (1/math.sqrt(2), 1/math.sqrt(2))]),  # Triangle
    ([(0, 0), (5, 0), (0, 5)], [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]),  # Triangle with origin point
])
def test_normalized_shapely_backend(session, polygon, expected_normalized):
    """Test normalized with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    normalized = poly.normalized()
    
    # Check that we get the expected number of points
    assert len(normalized) == len(expected_normalized)
    
    # Verify each normalized point
    for i, (actual_point, expected_coords) in enumerate(zip(normalized, expected_normalized)):
        assert actual_point.x.double == pytest.approx(expected_coords[0], abs=1e-9)
        assert actual_point.y.double == pytest.approx(expected_coords[1], abs=1e-9)


@pytest.mark.parametrize("polygon", [
    ([(3, 0), (0, 4), (5, 12)]),  # Triangle
    ([(1, 0), (0, 1), (1, 1)]),  # Triangle with diagonal point
    ([(10, 0), (0, 10), (10, 10), (5, 5)]),  # Square
    ([(0, 0), (5, 0), (0, 5)]),  # Triangle with origin point
])
def test_normalized_backends_match(session, polygon):
    """Test that both backends give the same result for normalized."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")
    
    # Test with server backend
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    poly_server = PolygonData(points=polygon)
    result_server = poly_server.normalized()
    
    # Test with Shapely backend
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    poly_shapely = PolygonData(points=polygon)
    result_shapely = poly_shapely.normalized()
    
    # Both backends should give the same number of points
    assert len(result_server) == len(result_shapely)
    
    # All normalized points should match between backends
    for server_point, shapely_point in zip(result_server, result_shapely):
        assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-9)
        assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-9)


@pytest.mark.parametrize("polygon, vector, expected_points", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 5), [(5, 5), (15, 5), (15, 15), (5, 15)]),  # Square moved by (5, 5)
    ([(0, 0), (5, 0), (2.5, 5)], (-2, 3), [(-2, 3), (3, 3), (0.5, 8)]),  # Triangle moved by (-2, 3)
    ([(1, 1), (4, 1), (4, 4), (1, 4)], (0, 0), [(1, 1), (4, 1), (4, 4), (1, 4)]),  # Square moved by (0, 0)
])
def test_move_server_backend(session, polygon, vector, expected_points):
    """Test move with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    moved = poly.move(vector)
    
    # Check that we get the expected number of points
    assert len(moved.points) == len(expected_points)

    # Check area remains the same
    assert moved.area() == poly.area()
    
    # Verify each moved point
    for actual_point, expected_coords in zip(moved.points, expected_points):
        assert actual_point.x.double == pytest.approx(expected_coords[0], abs=1e-9)
        assert actual_point.y.double == pytest.approx(expected_coords[1], abs=1e-9)


@pytest.mark.parametrize("polygon, vector, expected_points", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 5), [(5, 5), (15, 5), (15, 15), (5, 15)]),  # Square moved by (5, 5)
    ([(0, 0), (5, 0), (2.5, 5)], (-2, 3), [(-2, 3), (3, 3), (0.5, 8)]),  # Triangle moved by (-2, 3)
    ([(1, 1), (4, 1), (4, 4), (1, 4)], (0, 0), [(1, 1), (4, 1), (4, 4), (1, 4)]),  # Square moved by (0, 0)
])
def test_move_shapely_backend(session, polygon, vector, expected_points):
    """Test move with Shapely backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not available")
    
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    
    poly = PolygonData(points=polygon)
    moved = poly.move(vector)
    
    # Check that we get the expected number of points
    assert len(moved.points) == len(expected_points)

    # Check area remains the same
    assert moved.area() == poly.area()
    
    # Verify each moved point
    for actual_point, expected_coords in zip(moved.points, expected_points):
        assert actual_point.x.double == pytest.approx(expected_coords[0], abs=1e-9)
        assert actual_point.y.double == pytest.approx(expected_coords[1], abs=1e-9)


@pytest.mark.parametrize("polygon, vector", [
    ([(0, 0), (10, 0), (10, 10), (0, 10)], (5, 5)),  # Square
    ([(0, 0), (5, 0), (2.5, 5)], (-2, 3)),  # Triangle
    ([(1, 1), (3, 1), (3, 3), (1, 3)], (10, -5)),  # Square
])
def test_move_backends_match(session, polygon, vector):
    """Test that server and Shapely backends produce the same result for move."""
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE
    
    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not available")
    
    # Test with server backend
    Config.set_computation_backend(ComputationBackend.SERVER)
    PolygonData.reset_backend()
    poly_server = PolygonData(points=polygon)
    result_server = poly_server.move(vector)
    
    # Test with Shapely backend
    Config.set_computation_backend(ComputationBackend.SHAPELY)
    PolygonData.reset_backend()
    poly_shapely = PolygonData(points=polygon)
    result_shapely = poly_shapely.move(vector)
    
    # Both backends should give the same number of points
    assert len(result_server.points) == len(result_shapely.points)

    # Check area remains the same
    assert result_server.area() == result_shapely.area()
    
    # All moved points should match between backends
    for server_point, shapely_point in zip(result_server.points, result_shapely.points):
        assert server_point.x.double == pytest.approx(shapely_point.x.double, abs=1e-9)
        assert server_point.y.double == pytest.approx(shapely_point.y.double, abs=1e-9)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
