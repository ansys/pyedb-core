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

"""Component property."""

from ansys.api.edb.v1.component_property_pb2_grpc import ComponentPropertyServiceStub
import ansys.api.edb.v1.model_pb2 as model_pb2

from ansys.edb.core.definition import package_def
from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class ComponentProperty(ObjBase):
    """Represents a component property."""

    __stub: ComponentPropertyServiceStub = StubAccessor(StubType.component_property)

    def clone(self):
        """Clone the component property.

        Returns
        -------
        ComponentProperty
            Component property cloned.
        """
        return ComponentProperty(self.__stub.Clone(messages.edb_obj_message(self)))

    @property
    def package_mounting_offset(self):
        """:class:`.Value`: Mounting offset of the package definition object.

        This property can be set with :term:`ValueLike`.
        """
        return Value(self.__stub.GetPackageMountingOffset(messages.edb_obj_message(self)))

    @package_mounting_offset.setter
    def package_mounting_offset(self, offset):
        self.__stub.SetPackageMountingOffset(
            messages.value_property_message(self, messages.value_message(offset))
        )

    @property
    def package_def(self):
        """:obj:`PackageDef`: Package definition object."""
        return package_def.PackageDef(self.__stub.GetPackageDef(messages.edb_obj_message(self)))

    @package_def.setter
    def package_def(self, value):
        self.__stub.SetPackageDef(messages.pointer_property_message(target=self, value=value))

    @property
    def model(self):
        """:class:`.Model`: Model object.

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
    def model(self, value):
        self.__stub.SetModel(messages.pointer_property_message(target=self, value=value))
