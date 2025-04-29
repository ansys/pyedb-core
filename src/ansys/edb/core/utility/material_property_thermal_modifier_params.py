"""Class representing parameters for the material property thermal modifier."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike

from ansys.edb.core.utility.value import Value


class BasicQuadraticParams:
    """Represents basic quadratic parameters.

    Attributes
    ----------
    temp_ref_val : :term:`ValueLike`
        Temperature reference value in the quadratic model.
    c1_val : :term:`ValueLike`
        C1 value in the quadratic model.
    c2_val : :term:`ValueLike`
        C2 value in the quadratic model.
    """

    def __init__(
        self,
        temp_ref_val: ValueLike = "22cel",
        c1_val: Value = Value(0),
        c2_val: Value = Value(0),
    ):
        """Initialize a basic quadratic parameters object using given values.

        Parameters
        ----------
        temp_ref_val : :term:`ValueLike`, default: ``"22cel"``
            Temperature reference value in the quadratic model.
        c1_val : :term:`ValueLike`
            C1 value in the quadratic model.
        c2_val : :term:`ValueLike`
            C2 value in the quadratic model.
        """
        self.temp_ref_val = Value(temp_ref_val)
        self.c1_val = c1_val
        self.c2_val = c2_val


class AdvancedQuadraticParams:
    """Represents advanced quadratic parameters.

    Attributes
    ----------
    temp_lower_limit_val : :term:`ValueLike`
        Lower temperature limit where the quadratic model is valid.
    temp_upper_limit_val : :term:`ValueLike`
        Upper temperature limit where the quadratic model is valid.
    auto_calc_constant_thermal_modifier_vals : bool
        Flag indicating if the values for the lower and upper constant thermal modifieries
        are to be automatically calculated.
    lower_constant_thermal_modifier_val : :term:`ValueLike`
        Constant thermal modifier value for temperatures less than the lower constant
        thermal modifier value.
    upper_constant_thermal_modifier_val : :term:`ValueLike`
        Constant thermal modifier value for temperatures greater than the upper
        constant thermal modifier value.
    """

    def __init__(
        self,
        temp_lower_limit_val: ValueLike = "-273.15cel",
        temp_upper_limit_val: ValueLike = "1000cel",
        auto_calc_constant_thermal_modifier_vals: bool = True,
        lower_constant_thermal_modifier_val: ValueLike = 1,
        upper_constant_thermal_modifier_val: ValueLike = 1,
    ):
        """Initialize an advanced quadratic parameters object using given values.

        Parameters
        ----------
        temp_lower_limit_val : :term:`ValueLike`, default: ``"-273.15cel"``
            Lower temperature limit where the quadratic model is valid.
        temp_upper_limit_val : :term:`ValueLike`, default: ``"1000cel"``
            Upper temperature limit where the quadratic model is valid.
        auto_calc_constant_thermal_modifier_vals : bool, default: ``True``
            Flag indicating if the values for the lower and upper constant thermal modifieries
            are to be automatically calculated.
        lower_constant_thermal_modifier_val : :term:`ValueLike`, default: 1
            Constant thermal modifier value for temperatures less than the lower constant
            thermal modifier value.
        upper_constant_thermal_modifier_val : :term:`ValueLike`, default: 1
            Constant thermal modifier value for temperatures greater than the upper
            constant thermal modifier value.
        """
        self.temp_lower_limit_val = Value(temp_lower_limit_val)
        self.temp_upper_limit_val = Value(temp_upper_limit_val)
        self.auto_calc_constant_thermal_modifier_vals = auto_calc_constant_thermal_modifier_vals
        self.lower_constant_thermal_modifier_val = lower_constant_thermal_modifier_val
        self.upper_constant_thermal_modifier_val = upper_constant_thermal_modifier_val
