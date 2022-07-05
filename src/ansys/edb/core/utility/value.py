"""Value Class."""

from ansys.api.edb.v1 import value_pb2_grpc
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage
import ansys.api.edb.v1.value_pb2 as value_msgs

from ansys.edb.core.interface.grpc import messages
from ansys.edb.core import session
from ansys.edb.core.utility import conversions

from ansys.edb.core.utility.edb_errors import handle_grpc_exception


class Value:
    """Class representing a number or an expression."""

    __stub: value_pb2_grpc.ValueServiceStub = session.StubAccessor(session.StubType.value)

    @handle_grpc_exception
    def __init__(self, val, _owner=None):
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
            temp = value_msgs.ValueTextMessage(
                text=val, variable_owner=messages.edb_obj_message(_owner)
            )
            self.msg = self.__stub.CreateValue(temp)
        elif isinstance(val, float) or isinstance(val, int):
            self.msg.constant.real = val
            self.msg.constant.imag = 0
        elif isinstance(val, complex):
            self.msg.constant.real = val.real
            self.msg.constant.imag = val.imag
        else:
            assert False, "Invalid Value"

    def __str__(self):
        """Generate a readable string for the value.

        Returns
        -------
        str
        """
        if self.is_parametric:
            return f"{self.text}"
        else:
            return f"{self._value}"

    def __eq__(self, other):
        """Compare if two values are equivalent by evaluated value.

        Parameters
        ----------
        other : Value

        Returns
        -------
        bool
        """
        try:
            other = conversions.to_value(other)
            if isinstance(other, self.__class__):
                return self.double == other.double
        except TypeError:
            return False
        return False

    def __add__(self, other):
        """Perform addition of two values.

        Parameters
        ----------
        other : ansys.edb.typing.ValueLike

        Returns
        -------
        Value
        """
        other = conversions.to_value(other)
        return self.__class__(self._value + other._value)

    def __sub__(self, other):
        """Perform subtraction of two values.

        Parameters
        ----------
        other : ansys.edb.typing.ValueLike

        Returns
        -------
        Value
        """
        other = conversions.to_value(other)
        return self.__class__(self._value - other._value)

    def __mul__(self, other):
        """Perform multiplication of two values.

        Parameters
        ----------
        other : ansys.edb.typing.ValueLike

        Returns
        -------
        Value
        """
        other = conversions.to_value(other)
        return self.__class__(self._value * other._value)

    def __truediv__(self, other):
        """Perform floating-point division of two values.

        Parameters
        ----------
        other : ansys.edb.typing.ValueLike

        Returns
        -------
        Value
        """
        other = conversions.to_value(other)
        return self.__class__(self._value / other._value)

    def __floordiv__(self, other):
        """Perform division of two values and return its floor (integer part).

        Parameters
        ----------
        other : ansys.edb.typing.ValueLike

        Returns
        -------
        Value
        """
        other = conversions.to_value(other)
        return self.__class__(self._value // other._value)

    def __pow__(self, power, modulo=None):
        """Raise a value to the power of another value.

        Parameters
        ----------
        other : ansys.edb.typing.ValueLike

        Returns
        -------
        Value
        """
        return self.__class__(self._value**power)

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
        return type(self._value) == complex

    @property
    def double(self):
        """Get double from Value object.

        Returns
        -------
        double
        """
        evaluated = self._value
        return evaluated.real if type(evaluated) == complex else evaluated

    @property
    def complex(self):
        """Get imaginary value from Value object.

        Returns
        -------
        double
        """
        return complex(self._value)

    @property
    @handle_grpc_exception
    def _value(self):
        """Get complex number from Value object.

        Returns
        -------
        complex, float
        """
        if self.is_parametric:
            evaluated = self.__stub.GetComplex(
                value_msgs.ValueTextMessage(
                    text=self.msg.text, variable_owner=self.msg.variable_owner
                )
            )
        else:
            evaluated = self.msg.constant

        if evaluated.imag == 0:
            return evaluated.real
        else:
            return complex(evaluated.real, evaluated.imag)

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

    @property
    def sqrt(self):
        """Compute square root of this value.

        Returns
        -------
        Value
        """
        return self**0.5
