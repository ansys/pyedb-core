"""Material Property Thermal Modifier."""

from ansys.api.edb.v1 import material_property_thermal_modifier_pb2_grpc
import ansys.api.edb.v1.material_def_pb2 as pb

from ansys.edb.core.inner.base import ObjBase
from ansys.edb.core.inner.messages import edb_obj_message, value_message
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.material_property_thermal_modifier_params import (
    AdvancedQuadraticParams,
    BasicQuadraticParams,
)
from ansys.edb.core.utility.value import Value


class _QueryBuilder:
    @staticmethod
    def create(basic_quadratic_params, advanced_quadratic_params):
        return pb.MaterialPropertyThermalModifierParamsMessage(
            temp_ref=value_message(basic_quadratic_params.temp_ref_val),
            c1=value_message(basic_quadratic_params.c1_val),
            c2=value_message(basic_quadratic_params.c2_val),
            temp_lower_limit=value_message(advanced_quadratic_params.temp_lower_limit_val),
            temp_upper_limit=value_message(advanced_quadratic_params.temp_upper_limit_val),
            auto_calc_constant_thermal_modifier=advanced_quadratic_params.auto_calc_constant_thermal_modifier_vals,
            lower_const_therm_mod=value_message(
                advanced_quadratic_params.lower_constant_thermal_modifier_val
            ),
            upper_const_therm_mod=value_message(
                advanced_quadratic_params.upper_constant_thermal_modifier_val
            ),
        )


class MaterialPropertyThermalModifier(ObjBase):
    """Class representing material property thermal modifiers."""

    __stub: material_property_thermal_modifier_pb2_grpc.MaterialPropertyThermalModifierServiceStub = StubAccessor(
        StubType.material_property_thermal_modifier
    )

    @classmethod
    def create(cls, basic_quadratic_params=None, advanced_quadratic_params=None):
        """Create a material property thermal modifier.

        Parameters
        ----------
        basic_quadratic_params: :class:`BasicQuadraticParams <ansys.edb.core.utility.BasicQuadraticParams>`
            Thermal Modifier basic parameters needed.
        advanced_quadratic_params : :class:`AdvancedQuadraticParams <ansys.edb.core.utility.AdvancedQuadraticParams>`
            Thermal Modifier advanced parameters.

        Returns
        -------
        MaterialPropertyThermalModifier
            The new material property thermal modifiers.
        """
        if basic_quadratic_params is None:
            basic_quadratic_params = BasicQuadraticParams()
        if advanced_quadratic_params is None:
            advanced_quadratic_params = AdvancedQuadraticParams()
        return MaterialPropertyThermalModifier(
            cls.__stub.Create(
                _QueryBuilder.create(basic_quadratic_params, advanced_quadratic_params)
            )
        )

    @property
    def quadratic_model_params(self):
        """:class:`BasicQuadraticParams <ansys.edb.core.utility.BasicQuadraticParams>`, \
        :class:`AdvancedQuadraticParams <ansys.edb.core.utility.AdvancedQuadraticParams>`: \
        Quadratic model parameters of the thermal modifier.

        The quadratic model is of the following form:
            PropVal(Temp) = PropValRef[1 + C1(Temp - TempRef) + C2(Temp - TempRef)^2]
        where PropValRef = The original property value without the thermal modifier applied

        Read-Only.
        """
        msg = self.__stub.GetQuadraticModelParams(edb_obj_message(self))
        return BasicQuadraticParams(
            Value(msg.temp_ref),
            Value(msg.c1),
            Value(msg.c2),
        ), AdvancedQuadraticParams(
            Value(msg.temp_lower_limit),
            Value(msg.temp_upper_limit),
            msg.auto_calc_constant_thermal_modifier,
            Value(msg.lower_const_therm_mod),
            Value(msg.upper_const_therm_mod),
        )

    @property
    def expression(self):
        """:class:`Value <ansys.edb.core.utility.Value>`: Expression value representing the thermal modifier.

        Read-Only.
        """
        return Value(self.__stub.GetThermalModifierExpression(edb_obj_message(self)))
