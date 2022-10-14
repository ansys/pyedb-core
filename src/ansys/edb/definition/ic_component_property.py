"""IC Component Property."""

from ansys.api.edb.v1.ic_component_property_pb2_grpc import ICComponentPropertyServiceStub

from ansys.edb.core import messages
from ansys.edb.definition import (
    component_property,
    die_property,
    port_property,
    solder_ball_property,
)
from ansys.edb.session import StubAccessor, StubType


class RLCComponentProperty(component_property.ComponentProperty):
    """Class representing a RLCComponentProperty Property."""

    pass


class IOComponentProperty(component_property.ComponentProperty):
    """Class representing a I0Component Property."""

    pass


class ICComponentProperty(component_property.ComponentProperty):
    """Class representing a ICComponent Property."""

    __stub: ICComponentPropertyServiceStub = StubAccessor(StubType.ic_component_property)

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
    def die_property(self):
        """:obj:`DieProperty` : Die property.

        A copy is returned. Use the setter for any modifications to be reflected.
        """
        return die_property.DieProperty(self.__stub.GetDieProperty(messages.edb_obj_message(self)))

    @die_property.setter
    def die_property(self, value):
        self.__stub.SetDieProperty(messages.pointer_property_message(target=self, value=value))

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
