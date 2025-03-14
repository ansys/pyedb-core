"""Text."""

from ansys.api.edb.v1 import text_pb2, text_pb2_grpc

from ansys.edb.core.inner import messages
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class Text(Primitive):
    """Represents a text object."""

    __stub: text_pb2_grpc.TextServiceStub = StubAccessor(StubType.text)

    @classmethod
    def create(cls, layout, layer, center_x, center_y, text):
        """Create a text object.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the text object in.
        layer : str or Layer
            Layer to place the text object on.
        center_x : :class:`.Value`
            X value of the center point.
        center_y : :class:`.Value`
            Y value of the center point.
        text: str
            Text string.

        Returns
        -------
        Text
            Text object created.
        """
        return Text(
            cls.__stub.Create(
                text_pb2.TextCreationMessage(
                    layout=layout.msg,
                    layer=messages.layer_ref_message(layer),
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    text=text,
                )
            )
        )

    def get_text_data(self):
        """Get the data for the text object.

        Returns
        -------
        tuple[
            :class:`.Value`,
            :class:`.Value`,
            str
        ]
            Returns a tuple in this format:

            **(center_x, center_y, text)**

            **center_x** : X value of center point.

            **center_y** : Y value of center point.

            **radius** : Text object's String value.
        """
        text_data_msg = self.__stub.GetTextData(self.msg)
        return (
            Value(text_data_msg.center_x),
            Value(text_data_msg.center_y),
            text_data_msg.text,
        )

    def set_text_data(self, center_x, center_y, text):
        """Set the data for the text object.

        Parameters
        ----------
        center_x : :class:`.Value`
            X value of the center point.
        center_y : :class:`.Value`
            Y value of the center point.
        text : str
            String value for the text object.
        """
        self.__stub.SetTextData(
            text_pb2.SetTextDataMessage(
                target=self.msg,
                data=text_pb2.TextDataMessage(
                    center_x=messages.value_message(center_x),
                    center_y=messages.value_message(center_y),
                    text=text,
                ),
            )
        )
