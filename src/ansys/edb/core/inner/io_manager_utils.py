"""Utility methods for IO management."""

from ansys.edb.core.utility.io_manager import get_io_manager


def get_stub(obj, stub):
    """Retrieve the stub and track active object."""
    io_mgr = get_io_manager()
    if io_mgr.is_enabled:
        io_mgr.invalidation_tracker.track_active_obj(obj)
    return stub
