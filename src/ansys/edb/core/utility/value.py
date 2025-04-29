"""Value."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike, Union
    from ansys.edb.core.database import Database
    from ansys.edb.core.layout.cell import Cell
    from ansys.edb.core.layout.layout import Layout
    from ansys.edb.core.definition.component_def import ComponentDef


import math

from ansys.api.edb.v1 import value_pb2, value_pb2_grpc
from ansys.api.edb.v1.edb_messages_pb2 import ValueMessage

from ansys.edb.core import session
from ansys.edb.core.inner import messages
from ansys.edb.core.utility import conversions


class Value:
    r"""Represents a number or an expression.

    Attributes
    ----------
    val : :term:`ValueLike`
        Value assigned to the new value.
    _owner :    None, :class:`.Database`,
                :class:`.Cell`,
                :class:`.Layout`,
                :class:`.ComponentDef`

    Notes
    -----
    A value can be either a constant (such as ``1``, ``2.35``, ``"7+0.3i"``, and ``"23mm"``) or
    parametric (such as.``w1 + w2``).

    If the value is parametric, the ``_owner`` attribute must be set to the object that hosts the
    variables used. If the owner is :class:`.Cell` or
    :class:`.Layout`, the expression can reference both database variables
    and cell variables. A better way to create a parametric values is to call the
    ``obj_with_variables.create_value(str)`` method, which automatically sets the
    ``_owner`` parameter to the correct object.

    Values can be used in expressions with the following operators:

    .. list-table:: **Mathematical operators supported by values**
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

    The value is evaluated to a constant (if it is parametric) before applying the operators.
    """

    __stub: value_pb2_grpc.ValueServiceStub = session.StubAccessor(session.StubType.value)

    def __init__(self, val: ValueLike, _owner: Union[Database, Layout, Cell, ComponentDef] = None):
        """Initialize a value object."""
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

    def __eq__(self, other: Value):
        """Compare this value to another value to determine if they are equivalent.

        Parameters
        ----------
        other : .Value
            Value to compare.

        Returns
        -------
        bool
            ``True`` if the two values are equivalent, ``False`` otherwise.
        """
        return self.equals(other)

    def __add__(self, other: ValueLike):
        """Add this value and another value.

        Parameters
        ----------
        other : :term:`ValueLike`
            Other value to add.


        Returns
        -------
        .Value
            Constant value wrapping either a real or complex number.
        """
        other = conversions.to_value(other)
        return self.__class__(self.value + other.value)

    def __sub__(self, other: ValueLike):
        """Subtract this value from another value.

        Parameters
        ----------
        other : :term:`ValueLike`
           Other value to subtract.

        Returns
        -------
        .Value
            Constant Value wrapping either a real or complex number.
        """
        other = conversions.to_value(other)
        return self.__class__(self.value - other.value)

    def __mul__(self, other: ValueLike):
        """Multiply this value and another value.

        Parameters
        ----------
        other : :term:`ValueLike`
            Other value to multiply.

        Returns
        -------
        .Value
            Constant Value wrapping either a real or complex number.
        """
        other = conversions.to_value(other)
        return self.__class__(self.value * other.value)

    def __truediv__(self, other: ValueLike):
        """Perform floating-point division of this value and another value.

        Parameters
        ----------
        other : :term:`ValueLike`
             Other value for the floating-point division.

        Returns
        -------
        .Value
            Constant value wrapping either a real or complex number.
        """
        other = conversions.to_value(other)
        return self.__class__(self.value / other.value)

    def __floordiv__(self, other: ValueLike):
        """Divide this value by another value and return its floor (integer part).

        Parameters
        ----------
        other : :term:`ValueLike`
            Other value for the division.

        Returns
        -------
        .Value
            Constant value wrapping an integer.
        """
        other = conversions.to_value(other)
        return self.__class__(self.value // other.value)

    def __pow__(self, power: Union[int, float], modulo=None):
        """Raise a value to the power of another value.

        Parameters
        ----------
        power : int, float
            Exponent to apply to the value.

        Returns
        -------
        .Value
            Constant value wrapping either a real or complex number.
        """
        return self.__class__(self.value**power)

    def __neg__(self):
        """Flip the sign.

        Returns
        -------
        .Value
            Constant value wrapping either a real or complex number.
        """
        return self.__class__(-self.value)

    def __gt__(self, other: ValueLike):
        """Compare this value to another to see if this value is greater.

        Parameters
        ----------
        other : :term:`ValueLike`
            Other value to compare to.

        Returns
        -------
        bool
            ``True`` if this value is greater than the other value.
        """
        return self.value > other.value

    def __lt__(self, other: ValueLike):
        """Compare this value to another to see if this value is less.

        Parameters
        ----------
        other : :term:`ValueLike`
            Other value to compare to.

        Returns
        -------
        bool
            ``True`` if this value is less than the other value.
        """
        return self.value < other.value

    def equals(self, other: ValueLike, tolerance: float = 1e-9):
        """Check if this value and other value are equivalent when evaluated.

        Parameters
        ----------
        other : :term:`ValueLike`
            Other value to compare to.
        tolerance : float, default: 1e-9
            Tolerance.

        Returns
        -------
        bool
            `True`` if this value and the other value are equivalent when evaluated.
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
        """:obj:`bool`: Flag indicating if the value is parametric (dependent on variables)."""
        return not self.msg.HasField("constant")

    @property
    def is_complex(self):
        """:obj:`bool`: Flag indicating if the the value is a complex number (has a non-zero imaginary part)."""
        return type(self.value) == complex

    @property
    def double(self):
        """:obj:`float`: Float from the value object.

        If the number is complex, this returns the real part.
        """
        evaluated = self.value
        return evaluated.real if type(evaluated) == complex else evaluated

    @property
    def complex(self):
        """:obj:`complex`: Complex value from the value object.

        If the number is real, the imaginary part is ``0``.
        """
        return complex(self.value)

    @property
    def value(self):
        """:obj:`complex`: Evaluation to a constant and return as a float or complex."""
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
        """:obj:`float`: Square root of this value as a constant value."""
        return self**0.5
