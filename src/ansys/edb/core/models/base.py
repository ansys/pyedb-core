"""Base Model."""

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage


class ObjBase:
    """Class representing a base object that all gRPC-related models extend from."""

    def __init__(self, msg):
        """Initialize object.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        self._id = msg.id

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
        return self._id

    @property
    def msg(self):
        """Return protobuf message that represents this object's ID.

        Returns
        -------
        EDBObjMessage
        """
        return EDBObjMessage(id=self.id)

    @msg.setter
    def msg(self, val):
        """Modify protobuf message that represents this object's ID. can only be used to reset ID to None.

        Parameters
        ----------
        val : EDBObjMessage
        """
        if val is None:
            self._id = 0
