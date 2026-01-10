"""Tests for point computation backends.

This module contains tests for point backend implementations including
server, Shapely, and Build123d backends.
"""

import pytest

from ansys.edb.core.config import ComputationBackend, Config
from ansys.edb.core.geometry.point_data import PointData


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
    from ansys.edb.core.geometry.backends.point_backend_factory import _get_server_backend
    from ansys.edb.core.geometry.backends.point_server_backend import PointServerBackend

    # Mock stub for testing
    class MockStub:
        pass

    stub = MockStub()
    backend = _get_server_backend(stub)
    assert isinstance(backend, PointServerBackend)


def test_backend_factory_shapely(session):
    """Test Shapely backend creation."""
    from ansys.edb.core.geometry.backends.point_backend_factory import _get_shapely_backend
    from ansys.edb.core.geometry.backends.point_shapely_backend import (
        SHAPELY_AVAILABLE,
        PointShapelyBackend,
    )

    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")

    backend = _get_shapely_backend()
    assert isinstance(backend, PointShapelyBackend)


def test_backend_factory_shapely_not_available(session):
    """Test Shapely backend when library not available."""
    from ansys.edb.core.geometry.backends.point_shapely_backend import SHAPELY_AVAILABLE

    if SHAPELY_AVAILABLE:
        pytest.skip("Shapely is installed, cannot test unavailable case")

    from ansys.edb.core.geometry.backends.point_backend_factory import _get_shapely_backend

    with pytest.raises(ImportError, match="Shapely is required"):
        _get_shapely_backend()


def test_backend_factory_build123d(session):
    """Test Build123d backend creation."""
    from ansys.edb.core.geometry.backends.point_backend_factory import _get_build123d_backend
    from ansys.edb.core.geometry.backends.point_build123d_backend import (
        BUILD123D_AVAILABLE,
        PointBuild123dBackend,
    )

    if not BUILD123D_AVAILABLE:
        pytest.skip("Build123d not installed")

    backend = _get_build123d_backend()
    assert isinstance(backend, PointBuild123dBackend)


def test_backend_factory_build123d_not_available(session):
    """Test Build123d backend when library not available."""
    from ansys.edb.core.geometry.backends.point_build123d_backend import BUILD123D_AVAILABLE

    if BUILD123D_AVAILABLE:
        pytest.skip("Build123d is installed, cannot test unavailable case")

    from ansys.edb.core.geometry.backends.point_backend_factory import _get_build123d_backend

    with pytest.raises(ImportError, match="Build123d is not installed"):
        _get_build123d_backend()


@pytest.mark.parametrize(
    "point, start, end, expected_result",
    [
        # Point projects onto the line segment
        ((5, 5), (0, 0), (10, 0), (5, 0)),  # Point above horizontal line
        ((5, -5), (0, 0), (10, 0), (5, 0)),  # Point below horizontal line
        ((5, 5), (0, 0), (0, 10), (0, 5)),  # Point beside vertical line
        ((-5, 5), (0, 0), (0, 10), (0, 5)),  # Point on other side of vertical line
        ((5, 5), (0, 0), (10, 10), (5, 5)),  # Point on diagonal line
        ((3, 5), (0, 0), (10, 10), (4, 4)),  # Point near diagonal line
        # Point projects to start of line segment
        ((-5, 0), (0, 0), (10, 0), (0, 0)),  # Point before horizontal line
        ((-5, 5), (0, 0), (10, 10), (0, 0)),  # Point before diagonal line
        ((0, -5), (0, 0), (0, 10), (0, 0)),  # Point before vertical line
        # Point projects to end of line segment
        ((15, 0), (0, 0), (10, 0), (10, 0)),  # Point after horizontal line
        ((15, 15), (0, 0), (10, 10), (10, 10)),  # Point after diagonal line
        ((0, 15), (0, 0), (0, 10), (0, 10)),  # Point after vertical line
        # Point on the line segment
        ((5, 0), (0, 0), (10, 0), (5, 0)),  # Point on horizontal line
        ((0, 5), (0, 0), (0, 10), (0, 5)),  # Point on vertical line
        ((5, 5), (0, 0), (10, 10), (5, 5)),  # Point on diagonal line
        # Endpoints
        ((0, 0), (0, 0), (10, 0), (0, 0)),  # Point at start
        ((10, 0), (0, 0), (10, 0), (10, 0)),  # Point at end
        # Negative coordinates
        ((-5, -5), (-10, -10), (0, 0), (-5, -5)),  # Point on diagonal with negative coords
        ((-3, 2), (-10, 0), (0, 0), (-3, 0)),  # Point near horizontal line with negative coords
        ((2, -3), (0, -10), (0, 0), (0, -3)),  # Point near vertical line with negative coords
        # Very close to perpendicular from line
        ((5, 0.001), (0, 0), (10, 0), (5, 0)),  # Almost on horizontal line
        ((0.001, 5), (0, 0), (0, 10), (0, 5)),  # Almost on vertical line
        # Zero-length edge case (start equals end)
        ((5, 5), (3, 3), (3, 3), (3, 3)),  # Degenerate line segment
        (PointData(2, 2), PointData(0, 0), PointData(10, 0), (2, 0)),  # Using PointData objects
        (
            PointData(5e10, 5e10),
            PointData(0, 0),
            PointData(5e20, 0),
            (5e10, 0),
        ),  # Large coordinates
        (
            PointData(5e-5, 5e-5),
            PointData(0, 0),
            PointData(10e-5, 0),
            (5e-5, 0),
        ),  # Small coordinates
    ],
)
def test_closest(session, point, start, end, expected_result):
    """Test closest point computation with all backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    point_server = PointData(point)
    result_server = point_server.closest(start, end)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    point_shapely = PointData(point)
    result_shapely = point_shapely.closest(start, end)

    # Config.set_computation_backend(ComputationBackend.BUILD123D)
    # point_build123d = PointData(point)
    # result_build123d = point_build123d.closest(start, end)

    tol = 1e-9

    assert (result_server.x.double, result_server.y.double) == pytest.approx(
        expected_result, abs=tol, rel=tol
    )
    assert (result_shapely.x.double, result_shapely.y.double) == pytest.approx(
        expected_result, abs=tol, rel=tol
    )
    # assert (result_build123d.x.double, result_build123d.y.double) == pytest.approx(expected_result, abs=tol, rel=tol)


@pytest.mark.parametrize(
    "point, start, end, expected_distance",
    [
        # Point-to-point distance (end is None)
        ((0, 0), (3, 4), None, 5.0),  # Classic 3-4-5 triangle
        ((1, 2), (4, 6), None, 5.0),  # Another 3-4-5 triangle
        ((0, 0), (0, 0), None, 0.0),  # Same point
        ((5, 5), (5, 5), None, 0.0),  # Same point, non-zero coords
        ((-3, -4), (0, 0), None, 5.0),  # Negative coordinates
        ((1e10, 0), (0, 0), None, 1e10),  # Large coordinates
        ((1e-10, 0), (0, 0), None, 1e-10),  # Small coordinates
        # Distance to horizontal line segment
        ((5, 5), (0, 0), (10, 0), 5.0),  # Point above horizontal line
        ((5, -5), (0, 0), (10, 0), 5.0),  # Point below horizontal line
        ((5, 3), (0, 0), (10, 0), 3.0),  # Point above horizontal line, closer
        # Distance to vertical line segment
        ((5, 5), (0, 0), (0, 10), 5.0),  # Point beside vertical line
        ((-5, 5), (0, 0), (0, 10), 5.0),  # Point on other side of vertical line
        ((3, 5), (0, 0), (0, 10), 3.0),  # Point beside vertical line, closer
        # Distance to diagonal line segment
        ((5, 5), (0, 0), (10, 10), 0.0),  # Point on diagonal line
        ((0, 5), (0, 0), (10, 10), 5.0 / (2**0.5)),  # Point perpendicular to diagonal
        ((5, 0), (0, 0), (10, 10), 5.0 / (2**0.5)),  # Point perpendicular to diagonal
        # Distance when point projects before line segment start
        ((-5, 0), (0, 0), (10, 0), 5.0),  # Point before horizontal line
        ((0, -5), (0, 0), (0, 10), 5.0),  # Point before vertical line
        ((-5, -5), (0, 0), (10, 10), (50.0**0.5)),  # Point before diagonal line
        # Distance when point projects after line segment end
        ((15, 0), (0, 0), (10, 0), 5.0),  # Point after horizontal line
        ((0, 15), (0, 0), (0, 10), 5.0),  # Point after vertical line
        ((15, 15), (0, 0), (10, 10), (50.0**0.5)),  # Point after diagonal line
        # Point at segment endpoints
        ((0, 0), (0, 0), (10, 0), 0.0),  # Point at start
        ((10, 0), (0, 0), (10, 0), 0.0),  # Point at end
        # Zero-length segment (start equals end)
        ((5, 5), (3, 3), (3, 3), (8.0**0.5)),  # Degenerate line segment
        ((3, 3), (3, 3), (3, 3), 0.0),  # Point equals degenerate segment
        # Negative coordinates
        ((-5, -5), (-10, -10), (0, 0), 0.0),  # Point on diagonal with negative coords
        ((-3, 2), (-10, 0), (0, 0), 2.0),  # Point near horizontal line with negative coords
        ((2, -3), (0, -10), (0, 0), 2.0),  # Point near vertical line with negative coords
        # Very small distances
        ((5, 0.001), (0, 0), (10, 0), 0.001),  # Almost on horizontal line
        ((0.001, 5), (0, 0), (0, 10), 0.001),  # Almost on vertical line
        # Using PointData objects
        (PointData(2, 2), PointData(4, 6), None, 4.47213595499958),  # Point-to-point
        (PointData(5, 5), PointData(0, 0), PointData(10, 0), 5.0),  # Point to line segment
        (PointData(5e10, 5e10), PointData(0, 0), PointData(5e20, 0), 5e10),  # Large coordinates
        (PointData(5e-5, 5e-5), PointData(0, 0), PointData(10e-5, 0), 5e-5),  # Small coordinates
    ],
)
def test_distance(session, point, start, end, expected_distance):
    """Test distance computation with all backends."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    point_server = PointData(point)
    result_server = point_server.distance(start, end)

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    point_shapely = PointData(point)
    result_shapely = point_shapely.distance(start, end)

    # Config.set_computation_backend(ComputationBackend.BUILD123D)
    # point_build123d = PointData(point)
    # result_build123d = point_build123d.distance(start, end)

    tol = 1e-7

    assert result_server == pytest.approx(expected_distance, abs=tol, rel=tol)
    assert result_shapely == pytest.approx(expected_distance, abs=tol, rel=tol)
    # assert result_build123d == pytest.approx(expected_distance, abs=tol, rel=tol)
