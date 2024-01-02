"""Component property."""

from ansys.api.edb.v1.component_property_pb2_grpc import ComponentPropertyServiceStub
import ansys.api.edb.v1.model_pb2 as model_pb2

from ansys.edb.core.definition.package_def import PackageDef
from ansys.edb.core.inner.base import ObjBase
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    pointer_property_message,
    value_message,
    value_property_message,
)
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
            Clone of the component property.
        """
        return ComponentProperty(self.__stub.Clone(edb_obj_message(self)))

    @property
    def package_mounting_offset(self):
        """:class:`Value <ansys.edb.core.utility.Value>`: Offset of the package definition object.

        This attribute can be set with the :term:`ValueLike` term.
        """
        return Value(self.__stub.GetPackageMountingOffset(edb_obj_message(self)))

    @package_mounting_offset.setter
    def package_mounting_offset(self, offset):
        self.__stub.SetPackageMountingOffset(value_property_message(self, value_message(offset)))

    @property
    def package_def(self):
        """:obj:`PackageDef` : Package definition object."""
        return PackageDef(self.__stub.GetPackageDef(edb_obj_message(self)))

    @package_def.setter
    def package_def(self, value):
        self.__stub.SetPackageDef(pointer_property_message(target=self, value=value))

    @property
    def model(self):
        """:class:`Model <ansys.edb.core.hierarchy.Model>` : Model object.

        Returns
        -------
        Copy of the model object. Use the setter for any modifications to be reflected.
        """
        comp_model_msg = self.__stub.GetModel(edb_obj_message(self))

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
        self.__stub.SetModel(pointer_property_message(target=self, value=value))
