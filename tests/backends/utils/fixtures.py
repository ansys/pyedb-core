"""Fixtures for backend tests."""

import os
import pytest
from ansys.edb.core.session import launch_session
from ansys.edb.core.geometry.arc_data import ArcData

os.environ["ANSYSEM_EDB_EXE_DIR"] = r"C:\Program Files\ANSYS Inc\v262\AnsysEM"
EXE_DIR = os.environ["ANSYSEM_EDB_EXE_DIR"]


def _get_session_scope(fixture_name, config):
    """Get the scope for the session fixture from command line option."""
    return config.getoption("--session-scope", default="module")


def create_polygon(data, holes = []):
    """Create a PolygonData object based on input data type.
    
    Args:
        data: Either a list of point tuples [(x, y), ...] or a list of ArcData objects
        
    Returns:
        PolygonData: A polygon created with either points or arcs based on the input
    """
    from ansys.edb.core.geometry.polygon_data import PolygonData
    
    # Check if data contains ArcData objects
    if data and isinstance(data[0], ArcData):
        # Create polygon with arcs
        if holes and isinstance(holes[0][0], ArcData):
            return PolygonData(arcs=data, holes=[PolygonData(arcs=h) for h in holes])
        else:
            return PolygonData(arcs=data, holes=[PolygonData(h) for h in holes])
    else:
        # Create polygon with points
        if holes and isinstance(holes[0][0], ArcData):
            return PolygonData(data, holes=[PolygonData(arcs=h) for h in holes])
        else:
            return PolygonData(data, holes=[PolygonData(h) for h in holes])


@pytest.fixture(scope=_get_session_scope)
def session(request):
    """Fixture that launches a session for tests that need it.
    
    The scope can be controlled via the --session-scope command line option.
    Usage: pytest --session-scope=function
    """
    session = launch_session(EXE_DIR)
    yield session
    session.disconnect()


