"""Base Model."""


class ObjBase:
    """Class representing a base object that all gRPC-related models extend from."""

    def __init__(self, msg):
        """Initialize object.

        Parameters
        ----------
        msg : EdbObjMessage
        """
        self._msg = msg

    def is_null(self):
        """Determine whether this object exists in EDB."""
        return len(self.id) == 0

    @property
    def id(self):
        """Return unique ID of an EDB object.

        Returns
        -------
        str
        """
        if self._msg is None:
            return ""

        return self._msg.id

    @property
    def msg(self):
        """Return protobuf message that represents this object's ID.

        Returns
        -------
        EDBObjMessage
        """
        return self._msg

    @msg.setter
    def msg(self, val):
        if self._msg is None or val is None:
            self._msg = val
