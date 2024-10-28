# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Material property thermal modifier."""

from ansys.api.edb.v1 import material_property_thermal_modifier_pb2_grpc
import ansys.api.edb.v1.material_property_thermal_modifier_pb2 as pb

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.material_property_thermal_modifier_params import (
    AdvancedQuadraticParams,
    BasicQuadraticParams,
)
from ansys.edb.core.utility.value import Value


class MaterialPropertyThermalModifier(ObjBase):
    """Representing material property thermal modifiers."""

    __stub: material_property_thermal_modifier_pb2_grpc.MaterialPropertyThermalModifierServiceStub = StubAccessor(
        StubType.material_property_thermal_modifier
    )

    @classmethod
    def create(cls, basic_quadratic_params=None, advanced_quadratic_params=None):
        """Create a material property thermal modifier.

        Parameters
        ----------
        basic_quadratic_params : :class:`.BasicQuadraticParams`, default: None
            Basic parameters needed for the thermal modifier.
        advanced_quadratic_params : :class:`.AdvancedQuadraticParams`, default: None
            Advanced parameeteres needed for the thermal modifier.

        Returns
        -------
        MaterialPropertyThermalModifier
            Material property thermal modifier created.
        """
        if basic_quadratic_params is None:
            basic_quadratic_params = BasicQuadraticParams()
        if advanced_quadratic_params is None:
            advanced_quadratic_params = AdvancedQuadraticParams()
        return MaterialPropertyThermalModifier(
            cls.__stub.Create(
                pb.MaterialPropertyThermalModifierParamsMessage(
                    temp_ref=messages.value_message(basic_quadratic_params.temp_ref_val),
                    c1=messages.value_message(basic_quadratic_params.c1_val),
                    c2=messages.value_message(basic_quadratic_params.c2_val),
                    temp_lower_limit=messages.value_message(
                        advanced_quadratic_params.temp_lower_limit_val
                    ),
                    temp_upper_limit=messages.value_message(
                        advanced_quadratic_params.temp_upper_limit_val
                    ),
                    auto_calc_constant_thermal_modifier=(
                        advanced_quadratic_params.auto_calc_constant_thermal_modifier_vals
                    ),
                    lower_const_therm_mod=messages.value_message(
                        advanced_quadratic_params.lower_constant_thermal_modifier_val
                    ),
                    upper_const_therm_mod=messages.value_message(
                        advanced_quadratic_params.upper_constant_thermal_modifier_val
                    ),
                )
            )
        )

    @property
    def quadratic_model_params(self):
        """:class:`.BasicQuadraticParams`, :class:`.AdvancedQuadraticParams`: \
        Quadratic model parameters of the thermal modifier.

        The quadratic model is in this form: \
        PropVal(Temp) = PropValRef[1 + C1(Temp - TempRef) + C2(Temp - TempRef)^2]
        where PropValRef = The original property value without the thermal modifier applied

        This property is read-only.
        """
        msg = self.__stub.GetQuadraticModelParams(messages.edb_obj_message(self))
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
        """:class:`.Value`: Expression value representing the thermal modifier.

        This property is read-only.
        """
        return Value(self.__stub.GetThermalModifierExpression(messages.edb_obj_message(self)))
