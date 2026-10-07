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

"""Component property."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.definition.package_def import PackageDef
    from ansys.edb.core.hierarchy.model import Model
    from ansys.edb.core.typing import ValueLike

import ansys.api.edb.v1.component_property_pb2 as component_property_pb2
from ansys.api.edb.v1.component_property_pb2_grpc import ComponentPropertyServiceStub
import ansys.api.edb.v1.model_pb2 as model_pb2

from ansys.edb.core.definition import package_def
from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.utility.value import Value


class ComponentPropertyType(Enum):
    """Provides an enum representing component property types."""

    RLC_COMPONENT_PROPERTY = component_property_pb2.RLC_COMPONENT_PROP
    IC_COMPONENT_PROPERTY = component_property_pb2.IC_COMPONENT_PROP
    IO_COMPONENT_PROPERTY = component_property_pb2.IO_COMPONENT_PROP
    INVALID_COMPONENT_PROPERTY = component_property_pb2.INVALID_COMPONENT_PROP


class ComponentProperty(ObjBase):
    """Represents the properties of a :obj:`.ComponentGroup`."""

    __stub: ComponentPropertyServiceStub = StubAccessor(StubType.component_property)

    @property
    def component_property_type(self) -> ComponentPropertyType:
        """:class:`.ComponentPropertyType`: Type of the component property.

        This property is read-only.
        """
        return ComponentPropertyType(self.__stub.GetComponentPropertyType(messages.edb_obj_message(self)).type)

    def cast(self) -> ComponentProperty:
        """Cast the component property object to the correct concrete type.

        Returns
        -------
        .ComponentProperty
        """
        from ansys.edb.core.definition.ic_component_property import ICComponentProperty
        from ansys.edb.core.definition.io_component_property import IOComponentProperty
        from ansys.edb.core.definition.rlc_component_property import RLCComponentProperty

        comp_prop_type = (
            ComponentPropertyType.INVALID_COMPONENT_PROPERTY if self.is_null else self.component_property_type
        )
        if comp_prop_type == ComponentPropertyType.RLC_COMPONENT_PROPERTY:
            return RLCComponentProperty(self.msg)
        elif comp_prop_type == ComponentPropertyType.IC_COMPONENT_PROPERTY:
            return ICComponentProperty(self.msg)
        elif comp_prop_type == ComponentPropertyType.IO_COMPONENT_PROPERTY:
            return IOComponentProperty(self.msg)
        return ComponentProperty(self.msg)

    def clone(self) -> ComponentProperty:
        """Clone the component property.

        Returns
        -------
        .ComponentProperty
        """
        return ComponentProperty(self.__stub.Clone(messages.edb_obj_message(self))).cast()

    @property
    def package_mounting_offset(self) -> Value:
        """:class:`.Value`: Package mounting offset of the component.

        This property can be set with :term:`ValueLike`.
        """
        return Value(self.__stub.GetPackageMountingOffset(messages.edb_obj_message(self)))

    @package_mounting_offset.setter
    def package_mounting_offset(self, offset: ValueLike):
        self.__stub.SetPackageMountingOffset(messages.value_property_message(self, messages.value_message(offset)))

    @property
    def package_def(self) -> PackageDef:
        """:obj:`.PackageDef`: Package definition of the component."""
        return package_def.PackageDef(self.__stub.GetPackageDef(messages.edb_obj_message(self)))

    @package_def.setter
    def package_def(self, value: PackageDef):
        self.__stub.SetPackageDef(messages.pointer_property_message(target=self, value=value))

    @property
    def model(self) -> Model:
        """:class:`.Model`: Model of the component.

        This is a copy of the model object. Use the setter for any modifications to be reflected.
        """
        comp_model_msg = self.__stub.GetModel(messages.edb_obj_message(self))

        def get_model_obj_type():
            from ansys.edb.core.hierarchy.netlist_model import NetlistModel
            from ansys.edb.core.hierarchy.pin_pair_model import PinPairModel
            from ansys.edb.core.hierarchy.sparameter_model import SParameterModel
            from ansys.edb.core.hierarchy.spice_model import SPICEModel

            if comp_model_msg.model_type == model_pb2.SPICE_MODEL_TYPE:
                return SPICEModel
            elif comp_model_msg.model_type == model_pb2.S_PARAM_MODEL_TYPE:
                return SParameterModel
            elif comp_model_msg.model_type == model_pb2.PIN_PAIR_RLC_MODEL_TYPE:
                return PinPairModel
            elif comp_model_msg.model_type == model_pb2.NETLIST_MODEL_TYPE:
                return NetlistModel
            else:
                raise TypeError("Unsupported model type.")

        return get_model_obj_type()(comp_model_msg.model)

    @model.setter
    def model(self, value: Model):
        self.__stub.SetModel(messages.pointer_property_message(target=self, value=value))
