"""Fixtures for backend tests."""

import os
import pytest
from ansys.edb.core.session import launch_session

os.environ["ANSYSEM_EDB_EXE_DIR"] = r"C:\Program Files\ANSYS Inc\v262\AnsysEM"
EXE_DIR = os.environ["ANSYSEM_EDB_EXE_DIR"]


def _get_session_scope(fixture_name, config):
    """Get the scope for the session fixture from command line option."""
    return config.getoption("--session-scope", default="module")


@pytest.fixture(scope=_get_session_scope)
def session(request):
    """Fixture that launches a session for tests that need it.
    
    The scope can be controlled via the --session-scope command line option.
    Usage: pytest --session-scope=function
    """
    session = launch_session(EXE_DIR)
    yield session
    session.disconnect()
