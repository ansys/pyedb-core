"""Tests for arc computation backends.

This module contains tests for arc backend implementations including
server, Shapely, and Build123d backends.
"""

import math

import pytest
from utils.fixtures import safe_tol

from ansys.edb.core.config import ComputationBackend, Config
from ansys.edb.core.geometry.arc_data import ArcData


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
    from ansys.edb.core.geometry.backends.arc_backend_factory import _get_server_backend
    from ansys.edb.core.geometry.backends.arc_server_backend import ArcServerBackend

    # Mock stub for testing
    class MockStub:
        pass

    stub = MockStub()
    backend = _get_server_backend(stub)
    assert isinstance(backend, ArcServerBackend)


def test_backend_factory_shapely(session):
    """Test Shapely backend creation."""
    from ansys.edb.core.geometry.backends.arc_backend_factory import _get_shapely_backend
    from ansys.edb.core.geometry.backends.arc_shapely_backend import (
        SHAPELY_AVAILABLE,
        ArcShapelyBackend,
    )

    if not SHAPELY_AVAILABLE:
        pytest.skip("Shapely not installed")

    backend = _get_shapely_backend()
    assert isinstance(backend, ArcShapelyBackend)


def test_backend_factory_shapely_not_available(session):
    """Test Shapely backend when library not available."""
    from ansys.edb.core.geometry.backends.arc_shapely_backend import SHAPELY_AVAILABLE

    if SHAPELY_AVAILABLE:
        pytest.skip("Shapely is installed, cannot test unavailable case")

    from ansys.edb.core.geometry.backends.arc_backend_factory import _get_shapely_backend

    with pytest.raises(ImportError, match="Shapely is required"):
        _get_shapely_backend()


def test_backend_factory_build123d(session):
    """Test Build123d backend creation."""
    from ansys.edb.core.geometry.backends.arc_backend_factory import _get_build123d_backend
    from ansys.edb.core.geometry.backends.arc_build123d_backend import (
        BUILD123D_AVAILABLE,
        ArcBuild123dBackend,
    )

    if not BUILD123D_AVAILABLE:
        pytest.skip("Build123d not installed")

    backend = _get_build123d_backend()
    assert isinstance(backend, ArcBuild123dBackend)


def test_backend_factory_build123d_not_available(session):
    """Test Build123d backend when library not available."""
    from ansys.edb.core.geometry.backends.arc_build123d_backend import BUILD123D_AVAILABLE

    if BUILD123D_AVAILABLE:
        pytest.skip("Build123d is installed, cannot test unavailable case")

    from ansys.edb.core.geometry.backends.arc_backend_factory import _get_build123d_backend

    with pytest.raises(ImportError, match="Build123d is required"):
        _get_build123d_backend()


@pytest.mark.parametrize(
    "arc, expected_result",
    [
        (ArcData((0, 0), (10, 0), height=0.0), (math.nan, math.nan)),
        (ArcData((10, 2), (10, 2), height=5.0), (12.5, 2.0)),
        (ArcData((10, 0), (10, 0), height=0.0), (10.0, 0.0)),
        (ArcData((0, 0), (10, 0), height=-5.0), (5.0, 0.0)),
        (ArcData((0, 0), (10, 0), height=5.0), (5.0, 0.0)),
        (ArcData((0, 0), (10, 0), height=1.0), (5.0, -12.0)),
        (ArcData((0, 0), (10, 0), height=-2.0), (5.0, 5.25)),
        (ArcData((5, -5), (5, 5), height=6.5), (3.6730769230769234, 0.0)),
        (ArcData((5, -5), (5, 5), height=-10.0), (8.75, 0.0)),
        (ArcData((2, 3), (30, 6), height=3.0), (19.360232274630782, -26.862167896553974)),
        (ArcData((2, 3), (30, 6), height=-4.0), (13.573042277206895, 27.15160541273565)),
        (ArcData((-1, -2), (-10, -20), height=9.0), (-6.506230589874905, -10.496884705062547)),
    ],
)
def test_center(session, arc, expected_result):
    """Test center computation with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    result_server = arc.center

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    result_shapely = arc.center

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    result_build123d = arc.center

    tol = 1e-9

    assert (result_server.x.double, result_server.y.double) == pytest.approx(
        expected_result, rel=tol, nan_ok=True
    )
    assert (result_shapely.x.double, result_shapely.y.double) == pytest.approx(
        expected_result, rel=tol, nan_ok=True
    )
    assert (result_build123d.x.double, result_build123d.y.double) == pytest.approx(
        expected_result, rel=tol, nan_ok=True
    )


@pytest.mark.parametrize(
    "arc, expected_result",
    [
        (ArcData((0, 0), (10, 0), height=0.0), (5.0, 0.0)),
        # (ArcData((10, 2), (10, 2), height=5.0), (10.0, 2.0)),  # The server returns an incorrect result in this case.
        (ArcData((10, 0), (10, 0), height=0.0), (10.0, 0.0)),
        (ArcData((0, 0), (10, 0), height=-5.0), (5.0, -5.0)),
        (ArcData((0, 0), (10, 0), height=5.0), (5.0, 5.0)),
        (ArcData((0, 0), (10, 0), height=1.0), (5.0, 1.0)),
        (ArcData((0, 0), (10, 0), height=-2.0), (5.0, -2.0)),
        (ArcData((5, -5), (5, 5), height=6.5), (-1.5, 0.0)),
        (ArcData((5, -5), (5, 5), height=-10.0), (15.0, 0.0)),
        (ArcData((2, 3), (30, 6), height=3.0), (15.680400629097205, 7.482927461759427)),
        (ArcData((2, 3), (30, 6), height=-4.0), (16.42613249453706, 0.522763384320764)),
        (ArcData((-1, -2), (-10, -20), height=9.0), (2.5498447189992426, -15.024922359499621)),
    ],
)
def test_midpoint(session, arc, expected_result):
    """Test midpoint computation with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    result_server = arc.midpoint

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    result_shapely = arc.midpoint

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    result_build123d = arc.midpoint

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
    "arc, expected_result",
    [
        (ArcData((0, 0), (10, 0), height=0.0), math.inf),
        (ArcData((10, 2), (10, 2), height=5.0), 2.5),
        (ArcData((10, 0), (10, 0), height=0.0), 0.0),
        (ArcData((0, 0), (10, 0), height=-5.0), 5.0),
        (ArcData((0, 0), (10, 0), height=5.0), 5.0),
        (ArcData((0, 0), (10, 0), height=1.0), 13.0),
        (ArcData((0, 0), (10, 0), height=-2.0), 7.25),
        (ArcData((5, -5), (5, 5), height=-10.0), 6.25),
        (ArcData((2, 3), (30, 6), height=-4.0), 26.78125),
        (ArcData((-1, -2), (-10, -20), height=9.0), 10.125),
    ],
)
def test_radius(session, arc, expected_result):
    """Test radius computation with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    result_server = arc.radius

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    result_shapely = arc.radius

    Config.set_computation_backend(ComputationBackend.BUILD123D)
    result_build123d = arc.radius

    tol = 1e-9

    assert result_server == pytest.approx(expected_result, rel=tol)
    assert result_shapely == pytest.approx(expected_result, rel=tol)
    assert result_build123d == pytest.approx(expected_result, rel=tol)


@pytest.mark.parametrize(
    "arc, expected_result",
    [
        (ArcData((0, 0), (10, 0), height=0.0), [(0.0, 0.0), (10.0, 0.0)]),
        (ArcData((10, 2), (10, 2), height=5.0), [(10.0, -0.5), (15.0, 4.5)]),
        (ArcData((10, 0), (10, 0), height=0.0), [(10.0, 0.0), (10.0, 0.0)]),
        (ArcData((0, 0), (10, 0), height=-5.0), [(0.0, -5.0), (10.0, 0.0)]),
        (ArcData((0, 0), (10, 0), height=5.0), [(0.0, 0.0), (10.0, 5.0)]),
        (ArcData((0, 0), (10, 0), height=1.0), [(0.0, 0.0), (10.0, 1.0)]),
        (ArcData((0, 0), (10, 0), height=-2.0), [(0.0, -2.0), (10.0, 0.0)]),
        (ArcData((5, -5), (5, 5), height=-10.0), [(5.0, -6.25), (15.0, 6.25)]),
        (ArcData((2, 3), (30, 6), height=-4.0), [(2.0, 0.3703554127356483), (30.0, 6.0)]),
        (
            ArcData((-1, -2), (-10, -20), height=9.0),
            [(-10.0, -20.62188470506255), (3.618769410125095, -2.0)],
        ),
    ],
)
def test_bbox(session, arc, expected_result):
    """Test bounding box computation with server backend."""

    Config.set_computation_backend(ComputationBackend.SERVER)
    arc_server = arc.bbox
    result_server = [
        (min(p.x.double for p in arc_server.points), min(p.y.double for p in arc_server.points)),
        (max(p.x.double for p in arc_server.points), max(p.y.double for p in arc_server.points)),
    ]

    Config.set_computation_backend(ComputationBackend.SHAPELY)
    Config.set_backend_parameters(max_chord_error=0.0, max_arc_angle=math.pi / 128, max_points=128)
    arc_shapely = arc.bbox
    result_shapely = [
        (min(p.x.double for p in arc_shapely.points), min(p.y.double for p in arc_shapely.points)),
        (max(p.x.double for p in arc_shapely.points), max(p.y.double for p in arc_shapely.points)),
    ]

    print(result_server, result_shapely)

    # Config.set_computation_backend(ComputationBackend.BUILD123D)
    # result_build123d = arc.bbox

    tol = 1e-9

    for point_server, point_shapely, point_result in zip(
        result_server, result_shapely, expected_result
    ):
        assert point_server == pytest.approx(point_result, rel=tol, abs=tol)
        assert point_shapely == pytest.approx(point_result, rel=tol, abs=10 * safe_tol(arc, tol))
