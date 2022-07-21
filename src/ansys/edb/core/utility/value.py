"""Value Class."""
import math

from ansys.api.edb.v1 import value_pb2, value_pb2_grpc
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage

from ansys.edb.core import session
from ansys.edb.core.core import messages
from ansys.edb.core.utility import conversions


class Value:
    """Class representing a number or an expression."""

    __stub: value_pb2_grpc.ValueServiceStub = session.StubAccessor(session.StubType.value)

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
            temp = value_pb2.ValueTextMessage(
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
            raise TypeError(f"invalid value. Received '{val}'")

    def __str__(self):
        """Generate a readable string for the value.

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

    def __eq__(self, other):
        """Compare if two values are equivalent by evaluated value.

        Parameters
        ----------
        other : Value

        Returns
        -------
        bool
        """
        return self.equals(other)

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
        return self.__class__(self.value + other.value)

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
        return self.__class__(self.value - other.value)

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
        return self.__class__(self.value * other.value)

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
        return self.__class__(self.value / other.value)

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
        return self.__class__(self.value // other.value)

    def __pow__(self, power, modulo=None):
        """Raise a value to the power of another value.

        Parameters
        ----------
        power : int, float

        Returns
        -------
        Value
        """
        return self.__class__(self.value**power)

    def __neg__(self):
        """Flip the sign.

        Returns
        -------
        Value
        """
        return self.__class__(-self.value)

    def __gt__(self, other):
        """Compare if this value is greater than another value.

        Parameters
        ----------
        other : ansys.edb.core.typing.ValueLike

        Returns
        -------
        bool
        """
        return self.value > other.value

    def __lt__(self, other):
        """Compare if this value is less than another value.

        Parameters
        ----------
        other : ansys.edb.core.typing.ValueLike

        Returns
        -------
        bool
        """
        return self.value < other.value

    def equals(self, other, tolerance=1e-9):
        """Check if two values are equivalent when evaluated.

        Parameters
        ----------
        other : ansys.edb.core.typing.ValueLike
        tolerance : float, optional

        Returns
        -------
        bool
        """
        try:
            other = conversions.to_value(other)
            diff = self.value - other.value

            if type(diff) == complex:
                return math.fabs(diff.real) <= tolerance and math.fabs(diff.imag) <= tolerance
            else:
                return math.fabs(diff) <= tolerance
        except TypeError:
            return False

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
        return type(self.value) == complex

    @property
    def double(self):
        """Get double from Value object.

        Returns
        -------
        double
        """
        evaluated = self.value
        return evaluated.real if type(evaluated) == complex else evaluated

    @property
    def complex(self):
        """Get imaginary value from Value object.

        Returns
        -------
        double
        """
        return complex(self.value)

    @property
    def value(self):
        """Evaluate parametric value, if any, and return as number.

        Returns
        -------
        complex, float
        """
        if self.is_parametric:
            evaluated = self.__stub.GetComplex(
                value_pb2.ValueTextMessage(
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
    def sqrt(self):
        """Compute square root of this value.

        Returns
        -------
        Value
        """
        return self**0.5
