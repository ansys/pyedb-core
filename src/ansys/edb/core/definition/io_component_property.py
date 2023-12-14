"""IO Component Property."""

from ansys.api.edb.v1.io_component_property_pb2_grpc import IOComponentPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition.component_property import ComponentProperty
from ansys.edb.core.definition.port_property import PortProperty
from ansys.edb.core.definition.solder_ball_property import SolderBallProperty
from ansys.edb.core.inner.messages import edb_obj_message, pointer_property_message
from ansys.edb.core.session import StubAccessor, StubType


class IOComponentProperty(ComponentProperty):
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
        return SolderBallProperty(self.__stub.GetSolderBallProperty(edb_obj_message(self)))

    @solder_ball_property.setter
    def solder_ball_property(self, value):
        self.__stub.SetSolderBallProperty(pointer_property_message(target=self, value=value))

    @property
    def port_property(self):
        """:obj:`PortProperty` : Port property.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return PortProperty(self.__stub.GetPortProperty(edb_obj_message(self)))

    @port_property.setter
    def port_property(self, value):
        self.__stub.SetPortProperty(pointer_property_message(target=self, value=value))
