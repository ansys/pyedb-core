"""Fixtures for backend tests."""

import os

import pytest

from ansys.edb.core.geometry.arc_data import ArcData
from ansys.edb.core.session import launch_session

os.environ["ANSYSEM_EDB_EXE_DIR"] = r"C:\Program Files\ANSYS Inc\v262\AnsysEM"
EXE_DIR = os.environ["ANSYSEM_EDB_EXE_DIR"]


def _get_session_scope(fixture_name, config):
    """Get the scope for the session fixture from command line option."""
    return config.getoption("--session-scope", default="module")


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
    if isinstance(geometry["data"][0], ArcData):
        params["arcs"] = geometry["data"]
    else:
        params["points"] = geometry["data"]

    if "holes" in geometry:
        holes = []
        for hole in geometry["holes"]:
            if isinstance(hole[0], ArcData):
                holes.append(PolygonData(arcs=hole))
            else:
                holes.append(PolygonData(points=hole))
        params["holes"] = holes

    return PolygonData(**params)


@pytest.fixture(scope=_get_session_scope)
def session(request):
    """Fixture that launches a session for tests that need it.

    The scope can be controlled via the --session-scope command line option.
    Usage: pytest --session-scope=function
    """
    session = launch_session(EXE_DIR)
    yield session
    session.disconnect()
