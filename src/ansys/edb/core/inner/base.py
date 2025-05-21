"""Base model."""

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage

from ansys.edb.core.utility.io_manager import get_buffer, get_cache, get_io_manager


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
        if (buffer := get_buffer()) is not None:
            buffer.flush()
        return self.id == 0

    @property
    def id(self):
        """:obj:`int`: Unique ID of the EDB object.

        A ``0`` indicates an invalid object.

        This property is read-only.
        """
        return self._id

    @property
    def msg(self):
        """:obj:`EDBObjMessage`: Protobuf message that represents the object's ID.

        This property can only be set to :obj:`None`.
        """
        msg = EDBObjMessage(id=self.id)
        io_mgr = get_io_manager()
        if io_mgr.is_enabled:
            if self._is_future:
                msg.is_future = True
            io_mgr.active_request_edb_obj_msg_mgr.add_active_request_edb_obj_msg(msg)
        return msg

    @msg.setter
    def msg(self, msg):
        if msg is None:
            self._id = 0
            return
        self._id = msg.id
        self._is_future = msg.is_future
        if self._is_future:
            if (buffer := get_buffer()) is not None:
                buffer.add_future_ref(self)
        else:
            if (cache := get_cache()) is not None:
                cache.add_from_cache_msg(msg)


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
