"""Configuration for backend tests."""

import pytest


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--session-scope",
        action="store",
        default="module",
        choices=["function", "class", "module", "package", "session"],
        help="Set the scope for the session fixture (default: module)"
    )


@pytest.fixture(scope="session")
def session_scope(request):
    """Get the session scope from command line option."""
    return request.config.getoption("--session-scope")
