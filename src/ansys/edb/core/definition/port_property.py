"""Port property."""

from ansys.api.edb.v1.port_property_pb2_grpc import PortPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class PortProperty(ObjBase):
    """Represents a port property."""

    __stub: PortPropertyServiceStub = StubAccessor(StubType.port_property)

    @classmethod
    def create(cls):
        """
        Create a port property.

        Returns
        -------
        PortProperty
            Port property created.
        """
        return PortProperty(cls.__stub.Create(empty_pb2.Empty()))

    def clone(self):
        """
        Clone a port property.

        Returns
        -------
        PortProperty
            Port property cloned.
        """
        return PortProperty(self.__stub.Clone(messages.edb_obj_message(self)))

    @property
    def reference_height(self):
        """:class:`.Value`: Reference height of the port property.

        This property can be set with :term:`ValueLike`.
        """
        return Value(self.__stub.GetReferenceHeight(messages.edb_obj_message(self)))

    @reference_height.setter
    def reference_height(self, height):
        self.__stub.SetReferenceHeight(
            messages.value_property_message(self, messages.value_message(height))
        )

    @property
    def reference_size_auto(self):
        """:obj:`bool`: Flag indicating if the reference size is automatic."""
        return self.__stub.GetReferenceSizeAuto(messages.edb_obj_message(self)).value

    @reference_size_auto.setter
    def reference_size_auto(self, auto):
        self.__stub.SetReferenceSizeAuto(messages.bool_property_message(self, auto))

    def get_reference_size(self):
        r"""Get the X and Y reference sizes for the port property.

        Returns
        -------
        tuple[:class:`.Value`, :class:`.Value`]
        """
        value_pair_message = self.__stub.GetReferenceSize(messages.edb_obj_message(self))
        return Value(value_pair_message.val1), Value(value_pair_message.val2)

    def set_reference_size(self, ref_x, ref_y):
        """Set the X and Y reference sizes for the port property.

        Parameters
        ----------
        ref_x : :term:`ValueLike`
            X reference size.
        ref_y : :term:`ValueLike`
            Y reference size.
        """
        self.__stub.SetReferenceSize(messages.value_pair_property_message(self, ref_x, ref_y))
