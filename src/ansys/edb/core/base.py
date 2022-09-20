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
        self._id = 0 if msg is None else msg.id

    @property
    def is_null(self):
        """:obj:`bool`: Determine whether this object exists in EDB.

        Read-Only.
        """
        return self.id == 0

    @property
    def id(self):
        """:obj:`int`: The unique ID of an EDB object. 0 indicates invalid object.

        Read-Only.
        """
        return self._id

    @property
    def msg(self):
        """:obj:`EDBObjMessage` : Protobuf message that represents this object's ID.

        This property can only be set to None.
        """
        return EDBObjMessage(id=self.id)

    @msg.setter
    def msg(self, val):
        """Modify protobuf message that represents this object's ID. can only be used to reset ID to None."""
        if val is None:
            self._id = 0


class TypeField(object):
    """A descriptor for a type field that can be overridden by subclasses.

    Can have optional `@property def _type(self)` in the same class as a fallback method to
    fetch the type from server, in case static type is unknown.

    Examples
    --------
    class PrimitiveType(Enum):
        CIRCLE = 0

    class Primitive(object):
        type = TypeField(None)
        @property
        def _type(self):
            return PrimitiveType(self.__stub.GetPrimitiveType())

    class Circle(Primitive):
        type = TypeField(PrimitiveType.CIRCLE)

    Primitive(...).type # => fetch type from server.
    Primitive.type      # => None.
    Circle(...).type    # => CIRCLE.
    Circle.type         # => CIRCLE.
    """

    def __init__(self, tp):
        """Initialize a type field with static concrete type."""
        self._type = tp

    def __get__(self, instance, owner):
        """Return the static type if possible, otherwise fetch and return the instance type."""
        if self._type is not None:
            # return static type
            return self._type
        if instance is not None and hasattr(instance, "_type"):
            # fetch type
            return instance._type  # noqa
        else:
            # no type info available
            return None
