"""Class representing Material Property Thermal Modifier Parameters."""

from ansys.edb.utility.value import Value


class BasicQuadraticParams:
    """Class representing BasicQuadraticParams.

    Attributes
    ----------
    temp_ref_val : str, int, float, complex, Value
        The TempRef value in the quadratic model.
    c1_val : str, int, float, complex, Value
        The C1 value in the quadratic model.
    c2_val : str, int, float, complex, Value
        The C2 value in the quadratic model.
    """

    def __init__(
        self,
        temp_ref_val=Value("22cel"),
        c1_val=Value(0),
        c2_val=Value(0),
    ):
        """Construct a BasicQuadraticParams object using given values.

        Parameters
        ----------
        temp_ref_val : str, int, float, complex, Value
            The TempRef value in the quadratic model.
        c1_val : str, int, float, complex, Value
            The C1 value in the quadratic model.
        c2_val : str, int, float, complex, Value
            The C2 value in the quadratic model.
        """
        self.temp_ref_val = temp_ref_val
        self.c1_val = c1_val
        self.c2_val = c2_val


class AdvancedQuadraticParams:
    """Class representing AdvancedQuadraticParams.

    Attributes
    ----------
    temp_lower_limit_val : str, int, float, complex, Value
        The lower temperature limit where the quadratic model is valid.
    temp_upper_limit_val : str, int, float, complex, Value
        The upper temperature limit where the quadratic model is valid.
    auto_calc_constant_thermal_modifier_vals : str, int, float, complex, Value
        The flag indicating if the lower_constant_thermal_modifier_val and \
        upper_constant_thermal_modifier_val values should be auto calculated.
    lower_constant_thermal_modifier_val : str, int, float, complex, Value
        The constant thermal modifier value for temperatures lower than lower_constant_thermal_modifier_val.
    upper_constant_thermal_modifier_val : str, int, float, complex, Value
        The constant thermal modifier value for temperatures greater than upper_constant_thermal_modifier_val.
    """

    def __init__(
        self,
        temp_lower_limit_val=Value("-273.15cel"),
        temp_upper_limit_val=Value("1000cel"),
        auto_calc_constant_thermal_modifier_vals=True,
        lower_constant_thermal_modifier_val=1,
        upper_constant_thermal_modifier_val=1,
    ):
        """Construct an AdvancedQuadraticParams object using given values.

        Parameters
        ----------
        temp_lower_limit_val : str, int, float, complex, Value
            The lower temperature limit where the quadratic model is valid.
        temp_upper_limit_val : str, int, float, complex, Value
            The upper temperature limit where the quadratic model is valid.
        auto_calc_constant_thermal_modifier_vals : str, int, float, complex, Value
            The flag indicating if the lower_constant_thermal_modifier_val and \
            upper_constant_thermal_modifier_val values should be auto calculated.
        lower_constant_thermal_modifier_val : str, int, float, complex, Value
            The constant thermal modifier value for temperatures lower than lower_constant_thermal_modifier_val.
        upper_constant_thermal_modifier_val : str, int, float, complex, Value
            The constant thermal modifier value for temperatures greater than upper_constant_thermal_modifier_val.
        """
        self.temp_lower_limit_val = temp_lower_limit_val
        self.temp_upper_limit_val = temp_upper_limit_val
        self.auto_calc_constant_thermal_modifier_vals = auto_calc_constant_thermal_modifier_vals
        self.lower_constant_thermal_modifier_val = lower_constant_thermal_modifier_val
        self.upper_constant_thermal_modifier_val = upper_constant_thermal_modifier_val
