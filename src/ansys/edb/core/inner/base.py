"""Base model."""

from ansys.api.edb.v1.caching_pb2 import FutureMessage
from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage

from ansys.edb.core.utility.io_manager import get_buffer, get_cache


class ObjBase:
    """Provides the base object that all gRPC-related models extend from."""

    def __init__(self, msg):
        """Initialize the base object.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        self.msg = msg

    @property
    def is_null(self):
        """:obj:`bool`: Flag indicating if the object exists in the database.

        This property is read-only.
        """
        return self.id == 0

    def id(self, evaluate_future=True):
        """:obj:`int`: Unique ID of the EDB object.

        A ``0`` indicates an invalid object.

        This property is read-only.
        """
        if self._is_future and evaluate_future and (buffer := get_buffer()) is not None:
            buffer.flush()
        return self._id

    @property
    def msg(self):
        """:obj:`EDBObjMessage`: Protobuf message that represents the object's ID.

        This property can only be set to ``None``.
        """
        return EDBObjMessage(id=self.id())

    @msg.setter
    def msg(self, msg):
        if msg is None:
            self._id = 0
            return
        self._id = msg.id
        if isinstance(msg, FutureMessage):
            self._is_future = True
            if (buffer := get_buffer()) is not None:
                buffer.add_future_ref(self)
        else:
            self._is_future = False
            if (cache := get_cache()) is not None:
                cache.add_from_cache_msg(msg.cache)


class TypeField(object):
    """Provides a descriptor for a type field that can be overridden by subclasses.

    You can have an optional ``@property def _type(self)`` in the same class as a fallback method to
    fetch the type from the server in case the static type is unknown.

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
        """Get the static type if possible. Otherwise, fetch and return the instance type."""
        if self._type is not None:
            # return static type
            return self._type
        if instance is not None and hasattr(instance, "_type"):
            # fetch type
            return instance._type  # noqa
        else:
            # no type info available
            return None
