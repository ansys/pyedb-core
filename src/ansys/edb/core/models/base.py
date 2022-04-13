"""Base Model."""


class ObjBase:
    """Class representing a base object that all gRPC-related models extend from."""

    def __init__(self, msg):
        """Initialize object."""
        self._msg = msg

    def is_null(self):
        """Determine whether this object exists in EDB."""
        return self._msg.impl_ptr_address == 0

    @property
    def id(self):
        """Getter for address of EDB object."""
        return self._msg
