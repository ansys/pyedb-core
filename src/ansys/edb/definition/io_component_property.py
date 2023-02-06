"""IO Component Property."""

from ansys.api.edb.v1.io_component_property_pb2_grpc import IOComponentPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core import messages
from ansys.edb.definition import component_property, port_property, solder_ball_property
from ansys.edb.session import StubAccessor, StubType


class IOComponentProperty(component_property.ComponentProperty):
    """Class representing a I0Component Property."""

    __stub: IOComponentPropertyServiceStub = StubAccessor(StubType.io_component_property)

    @classmethod
    def create(cls):
        """
        Create IO Component Property.

        Returns
        -------
        IOComponentProperty
            IO component property created.
        """
        return IOComponentProperty(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def solder_ball_property(self):
        """:obj:`SolderBallProperty` : Solder ball property.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return solder_ball_property.SolderBallProperty(
            self.__stub.GetSolderBallProperty(messages.edb_obj_message(self))
        )

    @solder_ball_property.setter
    def solder_ball_property(self, value):
        self.__stub.SetSolderBallProperty(
            messages.pointer_property_message(target=self, value=value)
        )

    @property
    def port_property(self):
        """:obj:`PortProperty` : Port property.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return port_property.PortProperty(
            self.__stub.GetPortProperty(messages.edb_obj_message(self))
        )

    @port_property.setter
    def port_property(self, value):
        self.__stub.SetPortProperty(messages.pointer_property_message(target=self, value=value))
