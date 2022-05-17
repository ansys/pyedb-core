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
        """Determine whether this object exists in EDB.

        Returns
        -------
        bool
        """
        return self.id == 0

    @property
    def id(self):
        """Return unique ID of an EDB object. 0 indicates invalid object.

        Returns
        -------
        int
        """
        if self._msg is None:
            return 0

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
        """Modify protobuf message that represents this object's ID. can only be used to reset ID to None.

        Parameters
        ----------
        val : EDBObjMessage
        """
        if val is None:
            self._msg = val
