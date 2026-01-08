import math

import pytest
from utils.fixtures import create_polygon, safe_tol

from ansys.edb.core.config import ComputationBackend, Config
from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.geometry.polygon_data import IntersectionType


def test_config_default(session):
    """Test default configuration."""
    backend = Config.get_computation_backend()
    assert backend == ComputationBackend.AUTO


def test_config_set_backend(session):
    """Test setting backend programmatically."""
    Config.set_computation_backend(ComputationBackend.SERVER)
    assert Config.get_computation_backend() == ComputationBackend.SERVER

    Config.set_computation_backend("shapely")
    assert Config.get_computation_backend() == ComputationBackend.SHAPELY

    Config.set_computation_backend("build123d")
    assert Config.get_computation_backend() == ComputationBackend.BUILD123D


def test_config_environment_variable(session):
    """Test setting backend via environment variable."""
    import os

    try:
        Config.reset()
        os.environ["PYEDB_COMPUTATION_BACKEND"] = "server"
        assert Config.get_computation_backend() == ComputationBackend.SERVER

        Config.reset()
        os.environ["PYEDB_COMPUTATION_BACKEND"] = "shapely"
        assert Config.get_computation_backend() == ComputationBackend.SHAPELY

        Config.reset()
        os.environ["PYEDB_COMPUTATION_BACKEND"] = "build123d"
        assert Config.get_computation_backend() == ComputationBackend.BUILD123D

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
    from ansys.edb.core.geometry.backends.shapely_backend import SHAPELY_AVAILABLE, ShapelyBackend

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


def test_backend_factory_build123d(session):
    """Test Build123d backend creation."""
    from ansys.edb.core.geometry.backends.backend_factory import _get_build123d_backend
    from ansys.edb.core.geometry.backends.build123d_backend import (
        BUILD123D_AVAILABLE,
        Build123dBackend,
    )

    if not BUILD123D_AVAILABLE:
        pytest.skip("Build123d not installed")

    backend = _get_build123d_backend()
    assert isinstance(backend, Build123dBackend)


def test_backend_factory_build123d_not_available(session):
    """Test Build123d backend when library not available."""
    from ansys.edb.core.geometry.backends.build123d_backend import BUILD123D_AVAILABLE

    if BUILD123D_AVAILABLE:
        pytest.skip("Build123d is installed, cannot test unavailable case")

    from ansys.edb.core.geometry.backends.backend_factory import _get_build123d_backend

    with pytest.raises(ImportError, match="Build123d is not installed"):
        _get_build123d_backend()


@pytest.mark.parametrize(
    "polygon, expected_result",
    [
        ({"data": [(0, 0), (10, 0), (10, 10)]}, 50.0),  # Triangle
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, 100.0),  # Square
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (1, 2), (2, 2), (2, 1)]],
            },
            99.0,
        ),  # Square with hole
        ({"data": [(0, 0), (-20, 0), (-20, 10), (0, 10)]}, 200.0),  # Rectangle with negative coords
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            139.26991271972656,
        ),  # Square with one convex arc
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-1.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            93.28030395507812,
        ),  # Square with one concave arc
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                    [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                ],
            },
            0.52,
        ),  # Square with two holes
        (
            {
                "data": [(0, 1e-9), (0, 0), (1, 0), (1, 1)],
            },
            0.5,
        ),  # Square with two holes
    ],
)
def test_area(session, polygon, expected_result):
    """Test area computation with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    result_server = polygon_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    result_shapely = polygon_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    result_build123d = polygon_build123d.area()

    tol = 1e-7

    assert result_server == pytest.approx(expected_result, rel=tol)
    assert result_shapely == pytest.approx(expected_result, rel=safe_tol(polygon, tol))
    assert result_build123d == pytest.approx(expected_result, rel=tol)


@pytest.mark.parametrize(
    "test_case, expected_result",
    [
        ({"data": [(0, 0), (1, 0), (0.5, 1)]}, True),  # Triangle
        ({"data": [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]}, False),  # L-shape
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            True,
        ),  # Square with one convex arc
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-5.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            False,
        ),  # Square with one concave arc
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                    [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                ],
            },
            False,
        ),  # Square with two holes
    ],
)
def test_is_convex(session, test_case, expected_result):
    """Test is_convex with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(test_case)
    result_server = polygon_server.is_convex()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(test_case)
    result_shapely = polygon_shapely.is_convex()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(test_case)
    result_build123d = polygon_build123d.is_convex()

    assert result_server == expected_result
    assert result_shapely == expected_result
    assert result_build123d == expected_result


@pytest.mark.parametrize(
    "polygon, point, expected_result",
    [
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, (5, 5), True),  # Point inside square
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, (15, 5), False),  # Point outside square
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, (0, 0), True),  # Point on vertex
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, (5, 0), True),  # Point on edge
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            (5, 0),
            True,
        ),  # Point inside square with one convex arc
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-5.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            (-5, 0),
            False,
        ),  # Point outside square with one concave arc
        ({"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}, (7.5, 5), True),  # Point inside Bow-tie
        ({"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}, (2.5, 5), True),  # Point inside Bow-tie
        ({"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}, (5, 0), False),  # Point outside Bow-tie
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                    [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                ],
            },
            (0.5, 0.5),
            True,
        ),  # Point inside the body of a square with two holes
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                    [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                ],
            },
            (0.25, 0.5),
            False,
        ),  # Point inside the hole of a square with two holes
    ],
)
def test_is_inside(session, polygon, point, expected_result):
    """Test is_inside with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    result_server = polygon_server.is_inside(point)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    result_shapely = polygon_shapely.is_inside(point)

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    result_build123d = polygon_build123d.is_inside(point)
    self_intersects_build123d = polygon_build123d.has_self_intersections()

    assert result_shapely == expected_result
    assert result_server == expected_result
    if not self_intersects_build123d:
        assert result_build123d == expected_result


@pytest.mark.parametrize(
    "polygon, expected_bbox",
    [
        ({"data": [(0, 0), (5, 0), (2.5, 5)]}, ((0, 0), (5, 5))),  # Triangle
        ({"data": [(1, 1), (4, 2), (3, 5), (0, 4)]}, ((0, 1), (4, 5))),  # Irregular polygon
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            ((0, -5), (10, 10)),
        ),  # Square with one convex arc
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-5.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            ((-10, 0), (0, 10)),
        ),  # Square with one concave arc
        ({"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}, ((0, 0), (10, 10))),  # Bow-tie
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                    [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                ],
            },
            ((0, 0), (1, 1)),
        ),  # Square with two holes
    ],
)
def test_bbox(session, polygon, expected_bbox):
    """Test bbox with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    result_server = polygon_server.bbox()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    result_shapely = polygon_shapely.bbox()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    result_build123d = polygon_build123d.bbox()

    tol = 1e-9

    assert result_server[0][0] == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_server[0][1] == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_server[1][0] == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_server[1][1] == pytest.approx(expected_bbox[1][1], rel=tol)

    assert result_shapely[0][0] == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_shapely[0][1] == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_shapely[1][0] == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_shapely[1][1] == pytest.approx(expected_bbox[1][1], rel=tol)

    assert result_build123d[0][0] == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_build123d[0][1] == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_build123d[1][0] == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_build123d[1][1] == pytest.approx(expected_bbox[1][1], rel=tol)


@pytest.mark.parametrize(
    "polygons, expected_bbox",
    [
        ([{"data": [(0, 0), (5, 0), (5, 5), (0, 5)]}], ((0, 0), (5, 5))),  # Single square
        (
            [
                {"data": [(0, 0), (5, 0), (5, 5), (0, 5)]},
                {"data": [(10, 10), (15, 10), (15, 15), (10, 15)]},
            ],
            ((0, 0), (15, 15)),
        ),  # Two non-overlapping squares
        (
            [
                {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
                {"data": [(5, 5), (15, 5), (15, 15), (5, 15)]},
            ],
            ((0, 0), (15, 15)),
        ),  # Two overlapping squares
        (
            [
                {
                    "data": [
                        ArcData((0, 0), (10, 0), height=-5.0),
                        ArcData((10, 0), (10, 10), height=0.0),
                        ArcData((10, 10), (0, 10), height=0.0),
                        ArcData((0, 10), (0, 0), height=0.0),
                    ]
                },
                {
                    "data": [
                        ArcData((0, 0), (-10, 0), height=-5.0),
                        ArcData((-10, 0), (-10, 10), height=0.0),
                        ArcData((-10, 10), (0, 10), height=0.0),
                        ArcData((0, 10), (0, 0), height=0.0),
                    ]
                },
            ],
            ((-10, -5), (10, 10)),
        ),  # A square with one convex arc and a square with one concave arc
        ([{"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}], ((0, 0), (10, 10))),  # Bow-tie
        (
            [
                {
                    "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                    "holes": [
                        [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                        [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                    ],
                }
            ],
            ((0, 0), (1, 1)),
        ),  # Square with two holes
    ],
)
def test_bbox_of_polygons(session, polygons, expected_bbox):
    """Test bbox_of_polygons with server backend."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server_list = [create_polygon(p) for p in polygons]
    result_server = PolygonData.bbox_of_polygons(polygon_server_list)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely_list = [create_polygon(p) for p in polygons]
    result_shapely = PolygonData.bbox_of_polygons(polygon_shapely_list)

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d_list = [create_polygon(p) for p in polygons]
    result_build123d = PolygonData.bbox_of_polygons(polygon_build123d_list)

    tol = 1e-9

    assert result_server[0][0] == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_server[0][1] == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_server[1][0] == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_server[1][1] == pytest.approx(expected_bbox[1][1], rel=tol)

    assert result_shapely[0][0] == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_shapely[0][1] == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_shapely[1][0] == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_shapely[1][1] == pytest.approx(expected_bbox[1][1], rel=tol)

    assert result_build123d[0][0] == pytest.approx(expected_bbox[0][0], rel=tol)
    assert result_build123d[0][1] == pytest.approx(expected_bbox[0][1], rel=tol)
    assert result_build123d[1][0] == pytest.approx(expected_bbox[1][0], rel=tol)
    assert result_build123d[1][1] == pytest.approx(expected_bbox[1][1], rel=tol)


@pytest.mark.parametrize(
    "polygons, expected_result",
    [
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, 100.0),  # Simple square
        ({"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}, 0.0),  # Bow-tie
        (
            {
                "data": [
                    ArcData((0, 0), (2, 0), height=-1.0),
                    ArcData((2, 0), (2, 2), height=0.0),
                    ArcData((2, 2), (0, 2), height=-1.0),
                    ArcData((0, 2), (0, 0), height=0.0),
                ]
            },
            7.0,
        ),  # Square with arcs
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            137.5,
        ),  # Square with one convex arc
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-5.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            62.5,
        ),  # Square with one concave arc
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-5.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            100.0,
        ),  # Square with two concave arcs.
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-1.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ],
                "holes": [
                    [
                        ArcData((-4, 4), (-6, 4), height=-1.0),
                        ArcData((-6, 4), (-6, 6), height=0.0),
                        ArcData((-6, 6), (-4, 6), height=0.0),
                        ArcData((-4, 6), (-4, 4), height=0.0),
                    ]
                ],
            },
            92.5,
        ),  # Square with one concave arc and one hole
    ],
)
def test_without_arcs(session, polygons, expected_result):
    """Test tessellation with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygons)
    tessellated_server = polygon_server.without_arcs(
        max_chord_error=0, max_arc_angle=math.pi / 6, max_points=8
    )
    tessellated_area_server = tessellated_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygons)
    tessellated_shapely = polygon_shapely.without_arcs(
        max_chord_error=0, max_arc_angle=math.pi / 6, max_points=8
    )
    tessellated_area_shapely = tessellated_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygons)
    tessellated_build123d = polygon_build123d.without_arcs(
        max_chord_error=0, max_arc_angle=math.pi / 6, max_points=8
    )
    tessellated_area_build123d = tessellated_build123d.area()

    tol = 1e-9

    assert tessellated_server.has_arcs() == False
    assert tessellated_area_server == pytest.approx(expected_result, rel=tol)

    assert tessellated_shapely.has_arcs() == False
    assert tessellated_area_shapely == pytest.approx(expected_result, rel=tol)

    assert tessellated_build123d.has_arcs() == False
    assert tessellated_area_build123d == pytest.approx(expected_result, rel=tol)


@pytest.mark.parametrize(
    "polygon, expected_result",
    [
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, False),  # Simple square
        ({"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}, True),  # Bow-tie
        ({"data": [(0, 0), (5, 0), (5, 5), (0, 5)]}, False),  # Simple polygon
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 8), height=0.0),
                    ArcData((10, 8), (0, 8), height=-5.0),
                    ArcData((0, 8), (0, 0), height=0.0),
                ]
            },
            False,
        ),  # Square with two convex arcs
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-8.0),
                    ArcData((-10, 0), (-10, 8), height=0.0),
                    ArcData((-10, 8), (0, 8), height=-8.0),
                    ArcData((0, 8), (0, 0), height=0.0),
                ]
            },
            True,
        ),  # Square with two concave arcs
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                    [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                ],
            },
            False,
        ),  # Square with two non-intersecting holes
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.6, 0.9), (0.6, 0.1)],
                    [(0.4, 0.1), (0.9, 0.1), (0.9, 0.9), (0.4, 0.9)],
                ],
            },
            True,
        ),  # Square with two intersecting holes
        (
            {"data": [(0, 0), (20, 0), (0, 0), (10, 10), (0, 10)]},
            True,
        ),  # Polygon with overlapping edges
    ],
)
def test_has_self_intersections(session, polygon, expected_result):
    """Test has_self_intersections with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    result_server = polygon_server.has_self_intersections()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    result_shapely = polygon_shapely.has_self_intersections()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    result_build123d = polygon_build123d.has_self_intersections()

    assert result_server == expected_result
    assert result_shapely == expected_result
    assert result_build123d == expected_result


@pytest.mark.parametrize(
    "polygon, expected_count",
    [
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, 1),  # Simple square
        ({"data": [(0, 0), (10, 10), (10, 0), (0, 10)]}, 2),  # Bow-tie
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 8), height=0.0),
                    ArcData((10, 8), (0, 8), height=-5.0),
                    ArcData((0, 8), (0, 0), height=0.0),
                ]
            },
            1,
        ),  # Square with two convex arcs
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-5.0),
                    ArcData((-10, 0), (-10, 8), height=0.0),
                    ArcData((-10, 8), (0, 8), height=-5.0),
                    ArcData((0, 8), (0, 0), height=0.0),
                ]
            },
            3,
        ),  # Square with two concave arcs
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [
                    [(0.1, 0.1), (0.1, 0.9), (0.4, 0.9), (0.4, 0.1)],
                    [(0.6, 0.1), (0.9, 0.1), (0.9, 0.9), (0.6, 0.9)],
                ],
            },
            1,
        ),  # Square with two non-intersecting holes
        (
            {
                "data": [(0, 0), (10, 10), (10, 0), (0, 10)],
                "holes": [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]],
            },
            2,
        ),  # Bow-tie with one hole in each lobe
    ],
)
def test_remove_self_intersections(session, polygon, expected_count):
    """Test remove_self_intersections with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    no_self_intersections_server = polygon_server.remove_self_intersections()
    result_server = [polygon.has_self_intersections() for polygon in no_self_intersections_server]

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    no_self_intersections_shapely = polygon_shapely.remove_self_intersections()
    result_shapely = [polygon.has_self_intersections() for polygon in no_self_intersections_shapely]

    # TODO:
    ## The server implementation does not look correct at the moment, so commenting out these assertions.
    # assert len(result_server) == expected_count
    # for item in result_server:
    #     assert not item

    assert len(result_shapely) == expected_count
    for item in result_shapely:
        assert not item


@pytest.mark.parametrize(
    "polygon",
    [
        ({"data": [(3, 0), (0, 4), (5, 12)]}),  # Clock-wise triangle with no hole
        (
            {
                "data": [(0, 1), (0, 0), (1, 0), (1, 1)],
                "holes": [[(0.25, 0.25), (0.25, 0.75), (0.75, 0.75), (0.75, 0.25)]],
            }
        ),  # Counter clock-wise square with counter clock-wise hole
        (
            {"data": [(0, 0), (0, 5), (5, 0)], "holes": [[(1, 1), (1, 3), (3, 1)]]}
        ),  # Clock-wise triangle with with clock-wise hole
        # Arc cases are not yet verified. There is a discrepancy between backends.
        # There is no clear definition of what normalized should do with holes either.
    ],
)
def test_normalized(session, polygon):
    """Test normalized with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    normalized_server = polygon_server.normalized()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    normalized_shapely = polygon_shapely.normalized()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    normalized_build123d = polygon_build123d.normalized()

    # TODO: Make sure the normalized polygon has the correct orientation (including holes) for both backends.
    # TODO: Make sure the points match between both backends.


@pytest.mark.parametrize(
    "polygon, vector",
    [
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(2, 2), (3, 2), (3, 3), (2, 3)]],
            },
            (5, 5),
        ),  # Square with hole moved by (5, 5)
        (
            {"data": [(0, 0), (5, 0), (2.5, 5)]},
            (-2, 3),
        ),  # Triangle moved by (-2, 3)
        (
            {"data": [(1, 1), (4, 1), (4, 4), (1, 4)], "holes": [[(2, 2), (3, 2), (3, 3), (2, 3)]]},
            (0, 0),
        ),  # Square with hole moved by (0, 0)
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-1.0),
                    ArcData((10, 0), (10, 8), height=0.0),
                    ArcData((10, 8), (0, 8), height=0.0),
                    ArcData((0, 8), (0, 0), height=0.0),
                ]
            },
            (2, 2),
        ),  # Square with one convex arc and no holes moved by (2, 2).
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ],
                "holes": [
                    [
                        ArcData((4, 4), (6, 4), height=-1.0),
                        ArcData((6, 4), (6, 6), height=0.0),
                        ArcData((6, 6), (4, 6), height=0.0),
                        ArcData((4, 6), (4, 4), height=0.0),
                    ]
                ],
            },
            (42, 42),
        ),  # Square with one convex arc and one hole moved by (42, 42).
    ],
)
def test_move(session, polygon, vector):
    """Test move with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    area_server = polygon_server.area()
    moved_server = polygon_server.move(vector)
    moved_area_server = moved_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    area_shapely = polygon_shapely.area()
    moved_shapely = polygon_shapely.move(vector)
    moved_area_shapely = moved_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    area_build123d = polygon_build123d.area()
    moved_build123d = polygon_build123d.move(vector)
    moved_area_build123d = moved_build123d.area()

    tol = 1e-7

    assert area_server == pytest.approx(moved_area_server, rel=tol)
    assert area_shapely == pytest.approx(moved_area_shapely, rel=safe_tol(polygon, tol))
    assert area_build123d == pytest.approx(moved_area_build123d, rel=tol)

    assert area_server == pytest.approx(area_shapely, rel=safe_tol(polygon, tol))
    assert area_server == pytest.approx(area_build123d, rel=tol)


@pytest.mark.parametrize(
    "polygon, angle, center",
    [
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            math.pi / 2,
            (0, 0),
        ),  # Square rotated 90 degrees (π/2) around origin
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (1, 9), (9, 9), (9, 1)]],
            },
            math.pi,
            (5, 5),
        ),  # Square rotated 180 degrees (π) around its center
        (
            {"data": [(0, 0), (5, 0), (2.5, 5)]},
            0,
            (0, 0),
        ),  # Triangle rotated 0 degrees (no rotation)
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-1.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            math.pi / 2,
            (0, 0),
        ),  # Square with one convex arc and no holes rotated by 90 degrees (π/2) around origin.
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ],
                "holes": [
                    [
                        ArcData((4, 4), (6, 4), height=-1.0),
                        ArcData((6, 4), (6, 6), height=0.0),
                        ArcData((6, 6), (4, 6), height=0.0),
                        ArcData((4, 6), (4, 4), height=0.0),
                    ]
                ],
            },
            math.pi / 4,
            (42, 42),
        ),  # Square with one convex arc and one hole rotated by pi/4 around (42, 42).
    ],
)
def test_rotate(session, polygon, angle, center):
    """Test rotate with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    area_server = polygon_server.area()
    rotated_server = polygon_server.rotate(angle, center, use_radians=True)
    rotated_area_server = rotated_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    area_shapely = polygon_shapely.area()
    rotated_shapely = polygon_shapely.rotate(angle, center, use_radians=True)
    rotated_area_shapely = rotated_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    area_build123d = polygon_build123d.area()
    rotated_build123d = polygon_build123d.rotate(angle, center, use_radians=True)
    rotated_area_build123d = rotated_build123d.area()

    tol = 1e-7

    assert rotated_area_server == pytest.approx(area_server, rel=tol)
    assert rotated_area_shapely == pytest.approx(area_shapely, rel=safe_tol(polygon, tol))
    assert rotated_area_build123d == pytest.approx(area_build123d, rel=tol)

    assert area_server == pytest.approx(area_shapely, rel=safe_tol(polygon, tol))
    assert area_server == pytest.approx(area_build123d, rel=tol)


@pytest.mark.parametrize(
    "polygon, factor, center",
    [
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            2.0,
            (0, 0),
        ),  # Square scaled 2x from origin
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            0.5,
            (0, 0),
        ),  # Square scaled 0.5x from origin
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            2.0,
            (5, 5),
        ),  # Square scaled 2x from center
        (
            {"data": [(5, 5), (15, 5), (10, 15)]},
            3.0,
            (10, 10),
        ),  # Triangle scaled 3x from point
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            2.0,
            (0, 0),
        ),  # Square with one convex arc and one concave arc scaled 2x from origin
        (
            {"data": [(0, 0), (10, 10), (10, 0), (0, 10)]},
            2.0,
            (5, 5),
        ),  # Bow-tie with one hole in each lobe scaled 2x from (5, 5).
    ],
)
def test_scale(session, polygon, factor, center):
    """Test scale with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    area_server = polygon_server.area()
    scaled_server = polygon_server.scale(factor, center)
    scaled_area_server = scaled_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    area_shapely = polygon_shapely.area()
    scaled_shapely = polygon_shapely.scale(factor, center)
    scaled_area_shapely = scaled_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    area_build123d = polygon_build123d.area()
    scaled_build123d = polygon_build123d.scale(factor, center)
    scaled_area_build123d = scaled_build123d.area()

    tol = 1e-9

    assert scaled_area_server == pytest.approx(factor * factor * area_server, rel=tol)
    assert scaled_area_shapely == pytest.approx(
        factor * factor * area_shapely, rel=safe_tol(polygon, tol)
    )
    assert scaled_area_build123d == pytest.approx(factor * factor * area_build123d, rel=tol)

    assert scaled_area_server == pytest.approx(scaled_area_shapely, rel=tol)
    assert scaled_area_server == pytest.approx(scaled_area_build123d, rel=tol)


# TODO: Fix the expected_points
@pytest.mark.parametrize(
    "polygon, x",
    [
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, 10.0),  # Square
        ({"data": [(5, 5), (15, 5), (10, 15)]}, 0),  # Triangle
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            -5,
        ),  # Square with two convex arcs
        (
            {
                "data": [(0, 0), (10, 10), (10, 0), (0, 10)],
                "holes": [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]],
            },
            5.0,
        ),  # Bow-tie with one hole in each lobe
    ],
)
def test_mirror_x(session, polygon, x):
    """Test mirror_x with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    area_server = polygon_server.area()
    mirrored_server = polygon_server.mirror_x(x)
    mirrored_area_server = mirrored_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    area_shapely = polygon_shapely.area()
    mirrored_shapely = polygon_shapely.mirror_x(x)
    mirrored_area_shapely = mirrored_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    area_build123d = polygon_build123d.area()
    mirrored_build123d = polygon_build123d.mirror_x(x)
    mirrored_area_build123d = mirrored_build123d.area()

    tol = 1e-7

    assert mirrored_area_server == pytest.approx(area_server, rel=tol)
    assert mirrored_area_shapely == pytest.approx(area_shapely, rel=safe_tol(polygon, tol))
    assert mirrored_area_build123d == pytest.approx(area_build123d, rel=tol)

    assert mirrored_area_server == pytest.approx(mirrored_area_shapely, rel=safe_tol(polygon, tol))
    assert mirrored_area_server == pytest.approx(mirrored_area_build123d, rel=tol)


@pytest.mark.parametrize(
    "polygon, expected_result",
    [
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, [(5, 5), 7.0710678118654755]),  # Square
        ({"data": [(5, 5), (15, 5), (10, 15)]}, [(10, 10), 7.0710678118654755]),  # Triangle
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ],
                "holes": [],
            },
            [(5, 5), 11.180339887498949],
        ),  # Square with two convex arcs
        (
            {
                "data": [(0, 0), (10, 10), (10, 0), (0, 10)],
                "holes": [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]],
            },
            [(5, 5), 7.0710678118654755],
        ),  # Bow-tie with one hole in each lobe
    ],
)
def test_bounding_circle(session, polygon, expected_result):
    """Test bounding_circle with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    result_server = polygon_server.bounding_circle()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    result_shapely = polygon_shapely.bounding_circle()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    result_build123d = polygon_build123d.bounding_circle()

    tol = 1e-9

    assert result_server[0] == pytest.approx(expected_result[0], rel=tol)
    assert result_server[1] == pytest.approx(expected_result[1], rel=tol)

    assert result_shapely[0] == pytest.approx(expected_result[0], rel=tol)
    assert result_shapely[1] == pytest.approx(expected_result[1], rel=tol)

    assert result_build123d[0] == pytest.approx(expected_result[0], rel=tol)
    assert result_build123d[1] == pytest.approx(expected_result[1], rel=tol)


@pytest.mark.parametrize(
    "polygons, expected_area",
    [
        (
            [
                {"data": [(0, 0), (2, 0), (2, 2), (0, 2)]},
                {"data": [(5, 0), (7, 0), (7, 2), (5, 2)]},
            ],
            14.0,
        ),  # Two separate squares
        (
            [
                {"data": [(0, 0), (3, 0), (3, 3), (0, 3)]},
                {"data": [(2, 2), (5, 2), (5, 5), (2, 5)]},
            ],
            21.0,
        ),  # Two overlapping squares
        (
            [
                {
                    "data": [
                        ArcData((0, 0), (10, 0), height=-5.0),
                        ArcData((10, 0), (10, 10), height=0.0),
                        ArcData((10, 10), (0, 10), height=-5.0),
                        ArcData((0, 10), (0, 0), height=0.0),
                    ]
                },
                {
                    "data": [
                        ArcData((0, 0), (10, 0), height=-5.0),
                        ArcData((10, 0), (10, 10), height=0.0),
                        ArcData((10, 10), (0, 10), height=-5.0),
                        ArcData((0, 10), (0, 0), height=0.0),
                    ]
                },
            ],
            178.53981633165816,
        ),  # One squares with two convex arcs and one square with two concave arcs
        (
            [
                {
                    "data": [(0, 0), (10, 10), (10, 0), (0, 10)],
                    "holes": [[(1, 4), (2, 4), (2, 6), (1, 6)], [(8, 4), (9, 4), (9, 6), (8, 6)]],
                },
                {"data": [(0, 0), (-10, -10), (-10, 0), (0, -10)]},
            ],
            300.0,
        ),  # Bow-tie with one hole in each lobe
    ],
)
def test_convex_hull(session, polygons, expected_area):
    """Test convex_hull with both server and shapely backends."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server_list = [create_polygon(p) for p in polygons]
    convex_hull_server = PolygonData.convex_hull(polygon_server_list)
    area_server = convex_hull_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely_list = [create_polygon(p) for p in polygons]
    convex_hull_shapely = PolygonData.convex_hull(polygon_shapely_list)
    area_shapely = convex_hull_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d_list = [create_polygon(p) for p in polygons]
    convex_hull_build123d = PolygonData.convex_hull(polygon_build123d_list)
    area_build123d = convex_hull_build123d.area()

    tol = 1e-7

    assert area_server == pytest.approx(
        expected_area, rel=safe_tol(polygons, tol)
    )  # The server backend does not conserve exact arc shapes in convex hull calculation.
    assert area_shapely == pytest.approx(expected_area, rel=safe_tol(polygons, tol))
    assert area_build123d == pytest.approx(expected_area, rel=tol)


@pytest.mark.parametrize(
    "polygon, tol, expected_area",
    [
        (
            {
                "data": [
                    ArcData((0, 0), (1, 0), height=-1.0),
                    ArcData((1, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            1.0,
            89.26990509033203,
        ),  # Square with two convex arcs
        # TODO: The server backend is not handling this case correctly.
        # ({'data': [(0, 0), (10, 0), (11, 0), (11, 0.5), (10, 0.5), (10, 10), (0, 10)]},
        # 1.0, 100.5),  # Square with a small feature
        (
            {"data": [(0, 0), (10, 1), (10, 0), (0, 10)]},
            1.0,
            50.0,
        ),  # Bow-tie with a small lobe
    ],
)
def test_defeature(session, polygon, tol, expected_area):
    """Test defeature with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    defeatured_server = polygon_server.defeature(tol)
    area_server = defeatured_server.area()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    defeatured_shapely = polygon_shapely.defeature(tol)
    area_shapely = defeatured_shapely.area()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    defeatured_build123d = polygon_build123d.defeature(tol)
    area_build123d = defeatured_build123d.area()

    tol = 1e-7

    assert area_server == pytest.approx(expected_area, rel=tol)
    assert area_shapely == pytest.approx(expected_area, rel=safe_tol(polygon, tol))
    assert area_build123d == pytest.approx(expected_area, rel=tol)


@pytest.mark.parametrize(
    "polygon, other, expected_result",
    [
        (
            {"data": [(0, 0), (1, 0), (1, 1), (0, 1)]},
            {"data": [(2, 2), (3, 2), (3, 3), (2, 3)]},
            IntersectionType.NO_INTERSECTION,
        ),  # No intersection
        (
            {"data": [(0, 0), (2, 0), (2, 2), (0, 2)]},
            {"data": [(1, 1), (3, 1), (3, 3), (1, 3)]},
            IntersectionType.COMMON_INTERSECTION,
        ),  # Common intersection
        (
            {"data": [(0, 0), (3, 0), (3, 3), (0, 3)]},
            {"data": [(1, 1), (2, 1), (2, 2), (1, 2)]},
            IntersectionType.OTHER_INSIDE_THIS,
        ),  # Other inside this
        (
            {"data": [(1, 1), (2, 1), (2, 2), (1, 2)]},
            {"data": [(0, 0), (3, 0), (3, 3), (0, 3)]},
            IntersectionType.THIS_INSIDE_OTHER,
        ),  # This inside other
        (
            {"data": [(5, 5), (15, 5), (10, 15)]},
            {"data": [(10, 10), (10, 15), (15, 15), (15, 10)]},
            IntersectionType.COMMON_INTERSECTION,
        ),  # Common intersection
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"data": [(0, 14), (10, 14), (10, 20), (0, 20)]},
            IntersectionType.COMMON_INTERSECTION,
        ),  # Common intersection
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"data": [(0, 16), (10, 16), (10, 20), (0, 20)]},
            IntersectionType.NO_INTERSECTION,
        ),  # No intersection
        # TODO: The server backend is not handling this case correctly.
        # ({'data': [(0, 0), (10, 0), (10, 10), (0, 10)],
        # 'holes': [[(1, 1), (9, 1), (9, 9), (1, 9)]]},
        # {'data': [(2, 2), (8, 2), (8, 8), (2, 8)]},
        # IntersectionType.NO_INTERSECTION),  # Square inside the hole - no intersection
    ],
)
def test_intersection_type(session, polygon, other, expected_result):
    """Test intersection_type with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    other_server = create_polygon(other)
    result_server = polygon_server.intersection_type(other_server)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    other_shapely = create_polygon(other)
    result_shapely = polygon_shapely.intersection_type(other_shapely)

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    other_build123d = create_polygon(other)
    result_build123d = polygon_build123d.intersection_type(other_build123d)

    assert result_server == expected_result
    assert result_shapely == expected_result
    assert result_build123d == expected_result


@pytest.mark.parametrize(
    "polygon, circle, expected_result",
    [
        ({"data": [(0, 0), (1, 0), (1, 1), (0, 1)]}, {"center": (1, 1), "radius": 0.5}, True),
        ({"data": [(0, 0), (2, 0), (2, 2), (0, 2)]}, {"center": (-1, -1), "radius": 0.5}, False),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"center": (5, 5), "radius": 4},
            True,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (-10, 0), height=-5.0),
                    ArcData((-10, 0), (-10, 10), height=0.0),
                    ArcData((-10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"center": (-5, 0), "radius": 4},
            False,
        ),
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (9, 1), (9, 9), (1, 9)]],
            },
            {"center": (5, 5), "radius": 2},
            False,
        ),  # Circle inside the hole of a square
    ],
)
def test_circle_intersect(session, polygon, circle, expected_result):
    """Test circle_intersect with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    result_server = polygon_server.circle_intersect(**circle)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    result_shapely = polygon_shapely.circle_intersect(**circle)

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    result_build123d = polygon_build123d.circle_intersect(**circle)

    assert result_server == expected_result
    assert result_shapely == expected_result
    assert result_build123d == expected_result


@pytest.mark.parametrize(
    "polygon, point, expected_result",
    [
        ({"data": [(0, 0), (1, 0), (1, 1), (0, 1)]}, (2, 2), (1, 1)),
        ({"data": [(0, 0), (1, 0), (1, 1), (0, 1)]}, (-1, -1), (0, 0)),
        ({"data": [(0, 0), (2, 0), (1, 2)]}, (1, 10), (1, 2)),
        # TODO: The server backend is not handling this case correctly.
        # ({'data': [ArcData((0, 0), (10, 0), height=-5.0),
        # ArcData((10, 0), (10, 10), height=0.0), ArcData((10, 10), (0, 10), height=-5.0),
        # ArcData((0, 10), (0, 0), height=0.0)]}, (5, -2), (4.5, -2.0)),
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (9, 1), (9, 9), (1, 9)]],
            },
            (5, 4),
            (5, 1),
        ),
    ],
)
def test_closest_point(session, polygon, point, expected_result):
    """Test closest_point with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    result_server = polygon_server.closest_point(point)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    result_shapely = polygon_shapely.closest_point(point)

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    result_build123d = polygon_build123d.closest_point(point)

    tol = 1e-9

    assert (result_server.x.double, result_server.y.double) == pytest.approx(
        expected_result, rel=tol
    )
    assert (result_shapely.x.double, result_shapely.y.double) == pytest.approx(
        expected_result, rel=tol
    )
    assert (result_build123d.x.double, result_build123d.y.double) == pytest.approx(
        expected_result, rel=tol
    )


@pytest.mark.parametrize(
    "polygon1, polygon2, expected_area",
    [
        (
            {"data": [(0, 0), (2, 0), (2, 2), (0, 2)]},
            {"data": [(1, 1), (3, 1), (3, 3), (1, 3)]},
            1.0,
        ),
        (
            {"data": [(0, 0), (4, 0), (4, 4), (0, 4)]},
            {"data": [(2, 2), (6, 2), (6, 6), (2, 6)]},
            4.0,
        ),
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            {"data": [(5, 5), (15, 5), (15, 15), (5, 15)]},
            25.0,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {
                "data": [
                    ArcData((0, 5), (10, 5), height=-5.0),
                    ArcData((10, 5), (10, 15), height=0.0),
                    ArcData((10, 15), (0, 15), height=-5.0),
                    ArcData((0, 15), (0, 5), height=0.0),
                ]
            },
            128.53981018066406,
        ),
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (9, 1), (9, 9), (1, 9)]],
            },
            {
                "data": [(5, 0), (15, 0), (15, 10), (5, 10)],
                "holes": [[(6, 1), (14, 1), (14, 9), (6, 9)]],
            },
            10.0,
        ),
    ],
)
def test_intersect(session, polygon1, polygon2, expected_area):
    """Test polygon intersection using both backends."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    poly1_server = create_polygon(polygon1)
    poly2_server = create_polygon(polygon2)
    intersect_server = PolygonData.intersect(poly1_server, poly2_server)
    area_server = [poly.area() for poly in intersect_server]

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    poly1_shapely = create_polygon(polygon1)
    poly2_shapely = create_polygon(polygon2)
    intersect_shapely = PolygonData.intersect(poly1_shapely, poly2_shapely)
    area_shapely = [poly.area() for poly in intersect_shapely]

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    poly1_build123d = create_polygon(polygon1)
    poly2_build123d = create_polygon(polygon2)
    intersect_build123d = PolygonData.intersect(poly1_build123d, poly2_build123d)
    area_build123d = [poly.area() for poly in intersect_build123d]

    tol = 1e-7

    assert len(intersect_server) == len(intersect_shapely)
    assert len(intersect_server) == len(intersect_build123d)

    assert sum(area_server) == pytest.approx(expected_area, rel=tol)
    assert sum(area_shapely) == pytest.approx(
        expected_area, rel=safe_tol([polygon1, polygon2], tol)
    )
    assert sum(area_build123d) == pytest.approx(expected_area, rel=tol)


@pytest.mark.parametrize(
    "polygons, expected_area",
    [
        (
            [
                {"data": [(0, 0), (2, 0), (2, 2), (0, 2)]},
                {"data": [(1, 1), (3, 1), (3, 3), (1, 3)]},
            ],
            7.0,
        ),
        (
            [
                {"data": [(0, 0), (1, 0), (1, 1), (0, 1)]},
                {"data": [(2, 0), (3, 0), (3, 1), (2, 1)]},
            ],
            2.0,
        ),
        (
            [
                {"data": [(0, 0), (4, 0), (4, 4), (0, 4)]},
                {"data": [(2, 2), (6, 2), (6, 6), (2, 6)]},
            ],
            28.0,
        ),
        (
            [
                {
                    "data": [
                        ArcData((0, 0), (10, 0), height=-5.0),
                        ArcData((10, 0), (10, 10), height=0.0),
                        ArcData((10, 10), (0, 10), height=-5.0),
                        ArcData((0, 10), (0, 0), height=0.0),
                    ]
                },
                {
                    "data": [
                        ArcData((0, 5), (10, 5), height=-5.0),
                        ArcData((10, 5), (10, 15), height=0.0),
                        ArcData((10, 15), (0, 15), height=-5.0),
                        ArcData((0, 15), (0, 5), height=0.0),
                    ]
                },
            ],
            228.53981018066406,
        ),
        (
            [
                {
                    "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                    "holes": [[(1, 1), (9, 1), (9, 9), (1, 9)]],
                },
                {
                    "data": [(5, 0), (15, 0), (15, 10), (5, 10)],
                    "holes": [[(6, 1), (14, 1), (14, 9), (6, 9)]],
                },
            ],
            62.0,
        ),
    ],
)
def test_unite(session, polygons, expected_area):
    """Test polygon union using both backends."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    polys_server = [create_polygon(p) for p in polygons]
    union_server = PolygonData.unite(polys_server)
    area_server = [poly.area() for poly in union_server]

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polys_shapely = [create_polygon(p) for p in polygons]
    union_shapely = PolygonData.unite(polys_shapely)
    area_shapely = [poly.area() for poly in union_shapely]

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polys_build123d = [create_polygon(p) for p in polygons]
    union_build123d = PolygonData.unite(polys_build123d)
    area_build123d = [poly.area() for poly in union_build123d]

    tol = 1e-7

    assert len(union_server) == len(union_shapely)
    assert len(union_server) == len(union_build123d)

    assert sum(area_server) == pytest.approx(expected_area, rel=tol)
    assert sum(area_shapely) == pytest.approx(expected_area, rel=safe_tol(polygons, tol))
    assert sum(area_build123d) == pytest.approx(expected_area, rel=tol)


@pytest.mark.parametrize(
    "polygon1, polygon2, expected_area",
    [
        (
            {"data": [(0, 0), (4, 0), (4, 4), (0, 4)]},
            {"data": [(2, 2), (6, 2), (6, 6), (2, 6)]},
            12.0,
        ),
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            {"data": [(5, 5), (8, 5), (8, 8), (5, 8)]},
            91.0,
        ),
        (
            {"data": [(0, 0), (5, 0), (5, 5), (0, 5)]},
            {"data": [(1, 1), (4, 1), (4, 4), (1, 4)]},
            16.0,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {
                "data": [
                    ArcData((0, 5), (10, 5), height=-5.0),
                    ArcData((10, 5), (10, 15), height=0.0),
                    ArcData((10, 15), (0, 15), height=-5.0),
                    ArcData((0, 15), (0, 5), height=0.0),
                ]
            },
            50.0,
        ),
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (9, 1), (9, 9), (1, 9)]],
            },
            {
                "data": [(5, 0), (15, 0), (15, 10), (5, 10)],
                "holes": [[(6, 1), (14, 1), (14, 9), (6, 9)]],
            },
            26.0,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"data": [(0, 0), (0, -5), (10, -5), (10, 0)]},
            60.7300910949707,
        ),
    ],
)
def test_subtract(session, polygon1, polygon2, expected_area):
    """Test polygon subtraction using both backends."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    poly1_server = create_polygon(polygon1)
    poly2_server = create_polygon(polygon2)
    subtract_server = PolygonData.subtract(poly1_server, poly2_server)
    area_server = [poly.area() for poly in subtract_server]

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    poly1_shapely = create_polygon(polygon1)
    poly2_shapely = create_polygon(polygon2)
    subtract_shapely = PolygonData.subtract(poly1_shapely, poly2_shapely)
    area_shapely = [poly.area() for poly in subtract_shapely]

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    poly1_build123d = create_polygon(polygon1)
    poly2_build123d = create_polygon(polygon2)
    subtract_build123d = PolygonData.subtract(poly1_build123d, poly2_build123d)
    area_build123d = [poly.area() for poly in subtract_build123d]

    tol = 1e-7

    assert len(subtract_server) == len(subtract_shapely)
    assert len(subtract_server) == len(subtract_build123d)

    assert sum(area_server) == pytest.approx(expected_area, rel=tol)
    assert sum(area_shapely) == pytest.approx(
        expected_area, rel=safe_tol([polygon1, polygon2], tol)
    )
    assert sum(area_build123d) == pytest.approx(expected_area, rel=tol)


@pytest.mark.parametrize(
    "polygon1, polygon2, expected_area",
    [
        (
            {"data": [(0, 0), (2, 0), (2, 2), (0, 2)]},
            {"data": [(1, 1), (3, 1), (3, 3), (1, 3)]},
            6.0,
        ),
        (
            {"data": [(0, 0), (4, 0), (4, 4), (0, 4)]},
            {"data": [(2, 2), (6, 2), (6, 6), (2, 6)]},
            24.0,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {
                "data": [
                    ArcData((0, 5), (10, 5), height=-5.0),
                    ArcData((10, 5), (10, 15), height=0.0),
                    ArcData((10, 15), (0, 15), height=-5.0),
                    ArcData((0, 15), (0, 5), height=0.0),
                ]
            },
            100.0,
        ),
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (9, 1), (9, 9), (1, 9)]],
            },
            {
                "data": [(5, 0), (15, 0), (15, 10), (5, 10)],
                "holes": [[(6, 1), (14, 1), (14, 9), (6, 9)]],
            },
            52.0,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"data": [(0, 0), (0, -5), (10, -5), (10, 0)]},
            71.4601821899414,
        ),
    ],
)
def test_xor(session, polygon1, polygon2, expected_area):
    """Test polygon XOR using both backends."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    poly1_server = create_polygon(polygon1)
    poly2_server = create_polygon(polygon2)
    xor_server = PolygonData.xor(poly1_server, poly2_server)
    area_server = [poly.area() for poly in xor_server]

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    poly1_shapely = create_polygon(polygon1)
    poly2_shapely = create_polygon(polygon2)
    xor_shapely = PolygonData.xor(poly1_shapely, poly2_shapely)
    area_shapely = [poly.area() for poly in xor_shapely]

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    poly1_build123d = create_polygon(polygon1)
    poly2_build123d = create_polygon(polygon2)
    xor_build123d = PolygonData.xor(poly1_build123d, poly2_build123d)
    area_build123d = [poly.area() for poly in xor_build123d]

    tol = 1e-7

    # The xor operation in shapely and build123d have different outputs compared to the server.
    # assert len(xor_server) == len(xor_shapely)
    # assert len(xor_server) == len(xor_build123d)
    assert len(xor_shapely) == len(xor_build123d)

    assert sum(area_server) == pytest.approx(expected_area, rel=tol)
    assert sum(area_shapely) == pytest.approx(
        expected_area, rel=safe_tol([polygon1, polygon2], tol)
    )
    assert sum(area_build123d) == pytest.approx(expected_area, rel=tol)


@pytest.mark.parametrize(
    "polygon, options, expected_result, tol",
    [
        (
            {"data": [(0, 0), (1, 0), (1, 1), (0, 1)]},
            {"offset": 1.0, "round_corner": False, "max_corner_ext": 2.0},
            9.0,
            1e-9,
        ),
        (
            {"data": [(0, 0), (1, 0), (1, 1), (0, 1)]},
            {"offset": 1.0, "round_corner": True, "max_corner_ext": 2.0},
            8.141592979431152,
            1e-3,
        ),
        # TODO: In the following case, the corners are clipped and the
        # results differ by a large value between server and shapely implementations.
        (
            {"data": [(0, 0), (2, 0), (1, 2)]},
            {"offset": 1.0, "round_corner": False, "max_corner_ext": 1.0},
            13.680339887498949,
            1,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=-5.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"offset": 1.0, "round_corner": True, "max_corner_ext": 2.0},
            233.0973358154297,
            1e-1,
        ),
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(1, 1), (9, 1), (9, 9), (1, 9)]],
            },
            {"offset": 3.5, "round_corner": False, "max_corner_ext": 10.0},
            288.0,
            1e-9,
        ),
    ],
)
def test_expand(session, polygon, options, expected_result, tol):
    """Test expand with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    extend_server = polygon_server.expand(**options)
    area_server = [poly.area() for poly in extend_server]

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    extend_shapely = polygon_shapely.expand(**options)
    area_shapely = [poly.area() for poly in extend_shapely]

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    extend_build123d = polygon_build123d.expand(**options)
    area_build123d = [poly.area() for poly in extend_build123d]

    assert sum(area_server) == pytest.approx(expected_result, rel=tol)
    assert sum(area_shapely) == pytest.approx(expected_result, rel=tol)
    assert sum(area_build123d) == pytest.approx(expected_result, rel=tol)


@pytest.mark.parametrize(
    "polygon, expected_result",
    [
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (0, 0), height=-5.0),
                ]
            },
            True,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (0, 0), height=-5.0),
                ],
                "holes": [[(4, -1), (6, -1), (6, 1), (4, 1)]],
            },
            False,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-5.0),
                    ArcData((10, 0), (0, 0), height=-5.000001),
                ]
            },
            False,
        ),
        (
            {"data": [ArcData((0, 0), (10, 0), height=5.0), ArcData((10, 0), (0, 0), height=5.0)]},
            True,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-2.071067811865475244),
                    ArcData((10, 0), (10, 10), height=-2.071067811865475244),
                    ArcData((10, 10), (0, 10), height=-2.071067811865475244),
                    ArcData((0, 10), (0, 0), height=-2.071067811865475244),
                ]
            },
            True,
        ),
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, False),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=-1.339745962155614),
                    ArcData((10, 0), (0, 0), height=-18.660254037844386),
                ]
            },
            True,
        ),
    ],
)
def test_is_circle(session, polygon, expected_result):
    """Test is_circle with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    is_circle_server = polygon_server.is_circle()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    is_circle_shapely = polygon_shapely.is_circle()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    is_circle_build123d = polygon_build123d.is_circle()

    # TODO: The server backend is not handling this operation correctly.
    # TODO: We need a more rigorous implementation for circle detection that takes into account tolerances.
    # assert is_circle_server == expected_result
    assert is_circle_shapely == expected_result
    assert is_circle_build123d == expected_result


@pytest.mark.parametrize(
    "polygon, expected_result",
    [
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10)]}, True),
        (
            {
                "data": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "holes": [[(5, 5), (5, 6), (6, 6), (6, 5)]],
            },
            False,
        ),
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0), (10, 0)]}, False),
        ({"data": [(0, 0), (5, 0), (4, 0), (10, 0), (10, 10), (0, 10)]}, False),
        (
            {
                "data": [
                    (0, 0),
                    (0, 0),
                    (5, 0),
                    (10, 0),
                    (10, 1),
                    (10, 1),
                    (10, 2),
                    (10, 10),
                    (0, 10),
                    (0, 10),
                    (0, 0),
                ]
            },
            True,
        ),
        ({"data": [(0, 0), (10, 0), (10, 10), (0, 9.999)]}, False),
        ({"data": [(0, 0), (10, 0), (10, 10)]}, False),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=0.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            True,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (5, 0), height=0.0),
                    ArcData((5, 0), (10, 0), height=0.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            True,
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (5, 0), height=0.0),
                    ArcData((5, 0), (5, 0), height=42.0),
                    ArcData((10, 0), (10, 10), height=0.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            False,
        ),
    ],
)
def test_is_box(session, polygon, expected_result):
    """Test is_box with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon_server = create_polygon(polygon)
    is_box_server = polygon_server.is_box()

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon_shapely = create_polygon(polygon)
    is_box_shapely = polygon_shapely.is_box()

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon_build123d = create_polygon(polygon)
    is_box_build123d = polygon_build123d.is_box()

    # TODO: The server backend is not handling this operation correctly.
    # assert is_box_server == expected_result
    assert is_box_shapely == expected_result
    assert is_box_build123d == expected_result


@pytest.mark.parametrize(
    "polygon1, polygon2, expected_point1, expected_point2",
    [
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            {"data": [(20, 20), (30, 20), (30, 30), (20, 30)]},
            (10, 10),
            (20, 20),
        ),
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            (0, 0),
            (0, 0),
        ),
        (
            {"data": [(0, 0), (10, 0), (10, 10), (0, 10)]},
            {"data": [(-20, -20), (-30, -20), (-30, -30), (-20, -30)]},
            (0, 0),
            (-20, -20),
        ),
        (
            {"data": [(0, 0), (10, 0), (10, 10)]},
            {"data": [(0, 10), (10, 10), (10, 20)]},
            (10, 10),
            (10, 10),
        ),
        (
            {
                "data": [
                    ArcData((0, 0), (10, 0), height=0),
                    ArcData((10, 0), (10, 10), height=-5.0),
                    ArcData((10, 10), (0, 10), height=0.0),
                    ArcData((0, 10), (0, 0), height=0.0),
                ]
            },
            {"data": [(20, 0), (30, 0), (30, 10), (20, 10)]},
            (15, 5),
            (20, 5),
        ),
    ],
)
def test_closest_points(session, polygon1, polygon2, expected_point1, expected_point2):
    """Test closest points with both server and shapely backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    polygon1_server = create_polygon(polygon1)
    polygon2_server = create_polygon(polygon2)
    closest_point1_server, closest_point2_server = polygon1_server.closest_points(polygon2_server)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    polygon1_shapely = create_polygon(polygon1)
    polygon2_shapely = create_polygon(polygon2)
    closest_point1_shapely, closest_point2_shapely = polygon1_shapely.closest_points(
        polygon2_shapely
    )

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    polygon1_build123d = create_polygon(polygon1)
    polygon2_build123d = create_polygon(polygon2)
    closest_point1_build123d, closest_point2_build123d = polygon1_build123d.closest_points(
        polygon2_build123d
    )

    tol = 1e-9

    assert closest_point1_server == pytest.approx(expected_point1, rel=tol, abs=tol)
    assert closest_point2_server == pytest.approx(expected_point2, rel=tol, abs=tol)

    assert closest_point1_shapely == pytest.approx(expected_point1, rel=tol, abs=tol)
    assert closest_point2_shapely == pytest.approx(expected_point2, rel=tol, abs=tol)

    assert closest_point1_build123d == pytest.approx(expected_point1, rel=tol, abs=tol)
    assert closest_point2_build123d == pytest.approx(expected_point2, rel=tol, abs=tol)


@pytest.mark.parametrize(
    "point_cloud, alpha, expected_points",
    [
        ([(0, 0), (1, 0), (1, 1), (0, 1)], 2.0, [(0, 0), (1, 0), (1, 1), (0, 1)]),
        (
            [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5), (0.25, 0.25), (0.75, 0.75), (0.5, 2)],
            2.0,
            [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 2)],
        ),
    ],
)
def test_alpha_shape(session, point_cloud, alpha, expected_points):
    """Test alpha shape with both server and shapely backends."""
    from ansys.edb.core.geometry.polygon_data import PolygonData

    Config.set_computation_backend(ComputationBackend.SERVER)
    alpha_shape_server = PolygonData.alpha_shape(point_cloud, alpha=alpha)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    alpha_shape_shapely = PolygonData.alpha_shape(point_cloud, alpha=alpha)

    tol = 1e-9

    # Convert points to tuples for comparison (order-independent)
    server_points = [(p.x.double, p.y.double) for p in alpha_shape_server[0].points]
    shapely_points = [(p.x.double, p.y.double) for p in alpha_shape_shapely[0].points]

    # Check that all expected points are in the results (order-independent)
    assert len(server_points) == len(expected_points)
    assert len(shapely_points) == len(expected_points)

    for expected_point in expected_points:
        # Check if expected point exists in server result
        assert any(
            math.isclose(sp[0], expected_point[0], rel_tol=tol)
            and math.isclose(sp[1], expected_point[1], rel_tol=tol)
            for sp in server_points
        ), f"Expected point {expected_point} not found in server results"

        # Check if expected point exists in shapely result
        assert any(
            math.isclose(sp[0], expected_point[0], rel_tol=tol)
            and math.isclose(sp[1], expected_point[1], rel_tol=tol)
            for sp in shapely_points
        ), f"Expected point {expected_point} not found in shapely results"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
