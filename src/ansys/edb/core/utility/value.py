"""Value Class."""

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage, ValueMessage
import ansys.api.edb.v1.value_pb2 as value_msgs

from ansys.edb.core.session import get_value_stub
from ansys.edb.core.utility.edb_errors import handle_grpc_exception


class Value:
    """Class representing a number or an expression."""

    @handle_grpc_exception
    def __init__(self, val):
        """Initialize Value object.

        Parameters
        ----------
        val : str, int, float, complex, ValueMessage
        """
        self.msg = ValueMessage()
        if isinstance(val, ValueMessage):
            self.msg = val
        elif isinstance(val, Value):
            self.msg = val.msg
        elif isinstance(val, str):
            temp = value_msgs.ValueTextMessage(text=val, variable_owner=EDBObjMessage(id=0))
            self.msg = get_value_stub().CreateValue(temp)
        elif isinstance(val, float) or isinstance(val, int):
            self.msg.constant.real = val
            self.msg.constant.imag = 0
        elif isinstance(val, complex):
            self.msg.constant.real = val.real
            self.msg.constant.imag = val.imag
        else:
            assert False, "Invalid Value"

    @property
    def is_parametric(self):
        """Is Value object parametric (dependent on variables).

        Returns
        -------
        bool
        """
        return not self.msg.HasField("constant")

    @property
    def is_complex(self):
        """Is Value a complex number.

        Returns
        -------
        bool
        """
        c = self.complex
        return c.imag != 0

    @property
    @handle_grpc_exception
    def double(self):
        """Get double from Value object.

        A complex number will return the real part

        Returns
        -------
        double
        """
        if self.msg.HasField("constant"):
            return self.msg.constant.real
        else:
            temp = value_msgs.ValueTextMessage(
                text=self.msg.text, variable_owner=self.msg.variable_owner
            )
            return get_value_stub().GetDouble(temp)

    @property
    @handle_grpc_exception
    def complex(self):
        """Get complex number from Value object.

        Returns
        -------
        complex
        """
        if self.msg.HasField("constant"):
            return complex(self.msg.constant.real, self.msg.constant.imag)
        else:
            temp = value_msgs.ValueTextMessage(
                text=self.msg.text, variable_owner=self.msg.variable_owner
            )
            msg = get_value_stub().GetComplex(temp)
            return complex(msg.real, msg.imag)

    @property
    def text(self):
        """Get text from Value object.

        Returns
        -------
        str
        """
        if self.msg.text:
            return self.msg.text
        elif self.msg.constant.imag == 0:
            return str(self.msg.constant.real)
        else:
            return str(complex(self.msg.constant.real, self.msg.constant.imag))
