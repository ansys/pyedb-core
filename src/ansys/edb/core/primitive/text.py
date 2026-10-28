# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Text."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.layout.layout import Layout
    from ansys.edb.core.typing import LayerLike
    from ansys.edb.core.typing import ValueLike


from ansys.api.edb.v1 import text_pb2
from ansys.api.edb.v1 import text_pb2_grpc

from ansys.edb.core.inner import messages
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.utility.value import Value


class Text(Primitive):
    """Represents a text object."""

    __stub: text_pb2_grpc.TextServiceStub = StubAccessor(StubType.text)

    @classmethod
    def create(cls, layout: Layout, layer: LayerLike, center_x: ValueLike, center_y: ValueLike, text: str) -> Text:
        """Create a text object.

        Parameters
        ----------
        layout : .Layout
            Layout to create the text object in.
        layer : :term:`LayerLike`
            Layer to place the text object on.
        center_x : :term:`ValueLike`
            X value of the center point.
        center_y : :term:`ValueLike`
            Y value of the center point.
        text : str
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

    def get_text_data(self) -> tuple[Value, Value, str]:
        """Get the data for the text object.

        Returns
        -------
        tuple of (.Value, .Value, str)
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

    def set_text_data(self, center_x: ValueLike, center_y: ValueLike, text: str):
        """Set the data for the text object.

        Parameters
        ----------
        center_x : :term:`ValueLike`
            X value of the center point.
        center_y : :term:`ValueLike`
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
