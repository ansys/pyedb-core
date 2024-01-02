"""Value Class."""
import math

from ansys.api.edb.v1 import value_pb2, value_pb2_grpc
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage

from ansys.edb.core import session
from ansys.edb.core.inner.messages import edb_obj_message
from ansys.edb.core.utility.conversions import to_value


class Value:
    r"""Represents a number or an expression.

    Attributes
    ----------
    val : :term:`ValueLike`
        The value assigned to the new Value
    _owner :    None, :class:`Database <ansys.edb.core.database.Database>`, :class:`Cell <ansys.edb.core.layout.Cell>`,
                :class:`Layout <ansys.edb.core.layout.Layout>`, \
                :class:`ComponentDef <ansys.edb.core.definition.ComponentDef>`

    Notes
    -----
    Values can be either constant (e.g. 1, 2.35, 7+0.3i, 23mm) or parametric (e.g. w1 + w2)

    if the Value is parametric, it needs _owner set to the object that hosts the variables used. If the owner is
    Cell or Layout, the expression can reference both Database variables and Cell variables. A better way to create
    parametric values is to call obj_with_variables.create_value(str) which will automatically set the _owner to
    the correct object.

    Values can be used in expressions with the following operators:

    .. list-table:: Mathematical operators supported by Values
       :widths: 25 25 25
       :header-rows: 1

       * - Operator
         - Operation
         - Return Value
       * - \+
         - addition
         - Value
       * - \-
         - subtraction or negation
         - Value
       * - \*
         - multiplication
         - Value
       * - /
         - division
         - Value
       * - //
         - floor division
         - integer
       * - \*\*
         - power
         - Value
       * - ==
         - equality
         - bool
       * - \<
         - less than
         - bool
       * - >
         - greater than
         - bool

    The Value will be evaluated to a constant (if it is parametric) before applying the operators.
    """

    __stub: value_pb2_grpc.ValueServiceStub = session.StubAccessor(session.StubType.value)

    def __init__(self, val, _owner=None):
        """Construct a Value object."""
        self.msg = ValueMessage()
        if isinstance(val, ValueMessage):
            self.msg = val
        elif isinstance(val, Value):
            self.msg = val.msg
        elif isinstance(val, str):
            temp = value_pb2.ValueTextMessage(text=val, variable_owner=edb_obj_message(_owner))
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
            Value that will be compared to self

        Returns
        -------
        bool
        """
        return self.equals(other)

    def __add__(self, other):
        """Perform addition of two values.

        Parameters
        ----------
        other : str, int, float, complex, Value

        Returns
        -------
        Value
            this is a constant Value wrapping either real or complex number
        """
        other = to_value(other)
        return self.__class__(self.value + other.value)

    def __sub__(self, other):
        """Perform subtraction of two values.

        Parameters
        ----------
        other : str, int, float, complex, Value

        Returns
        -------
        Value
            this is a constant Value wrapping either real or complex number
        """
        other = to_value(other)
        return self.__class__(self.value - other.value)

    def __mul__(self, other):
        """Perform multiplication of two values.

        Parameters
        ----------
        other : str, int, float, complex, Value

        Returns
        -------
        Value
            this is a constant Value wrapping either real or complex number
        """
        other = to_value(other)
        return self.__class__(self.value * other.value)

    def __truediv__(self, other):
        """Perform floating-point division of two values.

        Parameters
        ----------
        other : str, int, float, complex, Value

        Returns
        -------
        Value
            this is a constant Value wrapping either real or complex number
        """
        other = to_value(other)
        return self.__class__(self.value / other.value)

    def __floordiv__(self, other):
        """Perform division of two values and return its floor (integer part).

        Parameters
        ----------
        other : str, int, float, complex, Value

        Returns
        -------
        Value
            this is a constant Value wrapping an integer number
        """
        other = to_value(other)
        return self.__class__(self.value // other.value)

    def __pow__(self, power, modulo=None):
        """Raise a value to the power of another value.

        Parameters
        ----------
        power : int, float
            the exponent applied to this Value.

        Returns
        -------
        Value
            this is a constant Value wrapping either real or complex number
        """
        return self.__class__(self.value**power)

    def __neg__(self):
        """Flip the sign.

        Returns
        -------
        Value
            this is a constant Value wrapping either real or complex number
        """
        return self.__class__(-self.value)

    def __gt__(self, other):
        """Compare if this value is greater than another value.

        Parameters
        ----------
        other : str, int, float, complex, Value

        Returns
        -------
        bool
        """
        return self.value > other.value

    def __lt__(self, other):
        """Compare if this value is less than another value.

        Parameters
        ----------
        other : str, int, float, complex, Value

        Returns
        -------
        bool
        """
        return self.value < other.value

    def equals(self, other, tolerance=1e-9):
        """Check if two values are equivalent when evaluated.

        Parameters
        ----------
        other : str, int, float, complex, Value
        tolerance : float, optional

        Returns
        -------
        bool
        """
        try:
            other = to_value(other)
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
        """Is Value a complex number (has a non-zero imaginary part).

        Returns
        -------
        bool
        """
        return type(self.value) == complex

    @property
    def double(self):
        """Get float from Value object.

        Returns
        -------
        float
            If number is complex, this returns real part.
        """
        evaluated = self.value
        return evaluated.real if type(evaluated) == complex else evaluated

    @property
    def complex(self):
        """Get complex value from Value object.

        Returns
        -------
        complex
            If number is real, the imaginary part will be 0.
        """
        return complex(self.value)

    @property
    def value(self):
        """Evaluate to a constant and return as a float or complex.

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
        """Compute square root of this value as a constant Value.

        Returns
        -------
        Value
        """
        return self**0.5
