"""IO component property."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.definition.port_property import PortProperty
    from src.ansys.edb.core.definition.solder_ball_property import SolderBallProperty

from ansys.api.edb.v1.io_component_property_pb2_grpc import IOComponentPropertyServiceStub
import google.protobuf.empty_pb2 as empty_pb2

from ansys.edb.core.definition import component_property, port_property, solder_ball_property
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor, StubType


class IOComponentProperty(component_property.ComponentProperty):
    """Represents the properties of an I0 component."""

    __stub: IOComponentPropertyServiceStub = StubAccessor(StubType.io_component_property)

    @classmethod
    def create(cls) -> IOComponentProperty:
        """
        Create an IO component property.

        Returns
        -------
        .IOComponentProperty
        """
        return IOComponentProperty(cls.__stub.Create(empty_pb2.Empty()))

    @property
    def solder_ball_property(self) -> SolderBallProperty:
        """:class:`.SolderBallProperty`: Solder ball properties of the IO component.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return solder_ball_property.SolderBallProperty(
            self.__stub.GetSolderBallProperty(messages.edb_obj_message(self))
        )

    @solder_ball_property.setter
    def solder_ball_property(self, value: SolderBallProperty):
        self.__stub.SetSolderBallProperty(
            messages.pointer_property_message(target=self, value=value)
        )

    @property
    def port_property(self) -> PortProperty:
        """:class:`.PortProperty`: Port properties of the IO component.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return port_property.PortProperty(
            self.__stub.GetPortProperty(messages.edb_obj_message(self))
        )

    @port_property.setter
    def port_property(self, value: PortProperty):
        self.__stub.SetPortProperty(messages.pointer_property_message(target=self, value=value))
