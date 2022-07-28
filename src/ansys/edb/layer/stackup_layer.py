"""Stackup Layer."""

from enum import Enum

import ansys.api.edb.v1.stackup_layer_pb2 as stackup_layer_pb2

from ansys.edb.core import messages
from ansys.edb.layer import Layer
from ansys.edb.session import get_stackup_layer_stub
from ansys.edb.utility import Value


class DCThicknessType(Enum):
    """Enum representing DC thickness types of StackupLayers."""

    EFFECTIVE = stackup_layer_pb2.HFSSSolverPropertiesMessage.EFFECTIVE
    LAYER = stackup_layer_pb2.HFSSSolverPropertiesMessage.LAYER
    MANUAL = stackup_layer_pb2.HFSSSolverPropertiesMessage.MANUAL


class RoughnessRegion(Enum):
    """Enum representing regions for roughness models of StackupLayers."""

    TOP = stackup_layer_pb2.LayerRoughnessRegionMessage.RoughnessRegion.TOP
    BOTTOM = stackup_layer_pb2.LayerRoughnessRegionMessage.RoughnessRegion.BOTTOM
    SIDE = stackup_layer_pb2.LayerRoughnessRegionMessage.RoughnessRegion.SIDE


def _set_layer_material_name_message(layer, mat_name):
    """Convert to SetLayerMaterialNameMessage."""
    return stackup_layer_pb2.SetLayerMaterialMessage(layer=layer.msg, material=mat_name)


def _get_layer_material_name_message(layer, evaluated):
    """Convert to GetLayerMaterialNameMessage."""
    return stackup_layer_pb2.GetLayerMaterialMessage(layer=layer.msg, evaluated=evaluated)


def _stackup_layer_value_message(layer, value):
    """Convert to StackupLayerValueMessage."""
    return stackup_layer_pb2.StackupLayerValueMessage(
        layer=layer.msg, value=messages.value_message(value)
    )


def _layer_roughness_region_message(layer, region):
    """Convert to LayerRoughnessRegionMessage."""
    return stackup_layer_pb2.LayerRoughnessRegionMessage(
        layer=layer.msg, roughness_region=region.value
    )


class StackupLayer(Layer):
    """Stackup layer."""

    @staticmethod
    def create(name, layer_type, thickness, elevation, material):
        """Create a stackup layer.

        Parameters
        name : str
        layer_type : LayerType
        thickness : float
        thickness : float
        material : str

        Returns
        -------
        StackupLayer
        """
        params = {
            "name": name,
            "type": layer_type.value,
            "thickness": messages.value_message(thickness),
            "elevation": messages.value_message(elevation),
            "material": material,
        }

        stackup_layer = StackupLayer(
            get_stackup_layer_stub().Create(stackup_layer_pb2.StackupLayerCreationMessage(**params))
        )
        return stackup_layer

    @property
    def negative(self):
        """Get the negative property of the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().GetNegative(self.msg).value

    @negative.setter
    def negative(self, is_negative):
        """Set the negative property of the layer.

        Parameters
        ----------
        is_negative : bool
        """
        get_stackup_layer_stub().SetNegative(
            stackup_layer_pb2.SetNegativeMessage(layer=self.msg, is_negative=is_negative)
        )

    @property
    def thickness(self):
        """Get the thickness value of the layer.

        Returns
        -------
        Value
        """
        return Value(get_stackup_layer_stub().GetThickness(self.msg))

    @thickness.setter
    def thickness(self, thickness):
        """Set the thickness value of the layer.

        Parameters
        ----------
        thickness : Value
        """
        get_stackup_layer_stub().SetThickness(_stackup_layer_value_message(self, thickness))

    @property
    def lower_elevation(self):
        """Get the lower elevation value of the layer.

        Returns
        -------
        Value
        """
        return Value(get_stackup_layer_stub().GetLowerElevation(self.msg))

    @lower_elevation.setter
    def lower_elevation(self, lower_elevation):
        """Set the lower elevation value of the layer.

        Parameters
        ----------
        lower_elevation : Value
        """
        get_stackup_layer_stub().SetLowerElevation(
            _stackup_layer_value_message(self, lower_elevation)
        )

    @property
    def upper_elevation(self):
        """Get the upper elevation value of the layer.

        Returns
        -------
        Value
        """
        return Value(get_stackup_layer_stub().GetUpperElevation(self.msg))

    def get_material(self, evaluated=True):
        """Get the name of the material of the layer.

        Parameters
        ----------
        evaluated : bool

        Returns
        -------
        str
        """
        return get_stackup_layer_stub().GetMaterial(
            _get_layer_material_name_message(self, evaluated)
        )

    def set_material(self, material_name):
        """Set the name of the material of the layer.

        Parameters
        ----------
        material_name : str
        """
        get_stackup_layer_stub().SetMaterial(_set_layer_material_name_message(self, material_name))

    def get_fill_material(self, evaluated=True):
        """Get the name of the material of the layer.

        Parameters
        ----------
        evaluated : bool

        Returns
        -------
        str
        """
        return get_stackup_layer_stub().GetFillMaterial(
            _get_layer_material_name_message(self, evaluated)
        )

    def set_fill_material(self, fill_material_name):
        """Set the name of the fill material of the layer.

        Parameters
        ----------
        fill_material_name : str
        """
        get_stackup_layer_stub().SetFillMaterial(
            _set_layer_material_name_message(self, fill_material_name)
        )

    @property
    def roughness_enabled(self):
        """Check if roughness models are used by the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().IsRoughnessEnabled(self.msg).value

    @roughness_enabled.setter
    def roughness_enabled(self, enable_roughness):
        """Set if roughness models are used by the layer.

        Parameters
        ----------
        enable_roughness : bool
        """
        get_stackup_layer_stub().SetRoughnessEnabled(
            stackup_layer_pb2.SetLayerPropEnabledMessage(layer=self.msg, enabled=enable_roughness)
        )

    def get_roughness_model(self, region):
        """Get the roughness model used by the layer.

        Parameters
        ----------
        region : RoughnessRegion

        Returns
        -------
        Value or tuple[Value, Value]
            If a Groisse roughness model is being used by the layer, a single Value
            object is returned representing the roughness value. If a Huray roughness
            model us being used,the returned value is a tuple of the form
            [nodule_radius_value, surface_ratio_value]
        """
        request = _layer_roughness_region_message(self, region)
        response = get_stackup_layer_stub().GetRoughnessModel(request)
        roughness = Value(response.roughness)
        return (
            roughness
            if not response.HasField("huray_surface_ratio")
            else (roughness, Value(response.surface_ratio))
        )

    def set_roughness_model(self, roughness_model, region):
        """Set the roughness model used by the layer.

        Parameters
        ----------
        roughness_model : Value or tuple[Value, Value]
            If roughness_model is a single Value object, a Groisse roughness model
            with a roughness value equal to the provided value will be assigned to
            the layer. If roughness_model is a tuple of two Value objects, a Huray
            roughness model will be assigned to the layer with a nodule radius value
            equal to roughness_model[0] and a surface ratio value equal to roughness_model[1]
        region : RoughnessRegion
        """
        roughness_model_msg = stackup_layer_pb2.RoughnessModelMessage()
        is_groisse_roughness = isinstance(roughness_model, Value)
        roughness_model_msg.roughness.CopyFrom(
            messages.value_message(roughness_model if is_groisse_roughness else roughness_model[0])
        )
        if not is_groisse_roughness:
            roughness_model_msg.surface_ratio.CopyFrom(messages.value_message(roughness_model[1]))
        request = stackup_layer_pb2.SetRoughnessModelMessage(
            layer_rough_region=_layer_roughness_region_message(self, region),
            roughness_model=roughness_model_msg,
        )
        get_stackup_layer_stub().SetRoughnessModel(request)

    @property
    def etch_factor_enabled(self):
        """Check if etch factor is used by the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().IsEtchFactorEnabled(self.msg).value

    @etch_factor_enabled.setter
    def etch_factor_enabled(self, enable_etch_factor):
        """Set if etch factor is used by the layer.

        Parameters
        ----------
        enable_etch_factor : bool
        """
        get_stackup_layer_stub().SetEtchFactorEnabled(
            stackup_layer_pb2.SetLayerPropEnabledMessage(layer=self.msg, enabled=enable_etch_factor)
        )

    @property
    def etch_factor(self):
        """Get the etch factor of the layer.

        Returns
        -------
        Value
        """
        return Value(get_stackup_layer_stub().GetEtchFactor(self.msg))

    @etch_factor.setter
    def etch_factor(self, etch_factor):
        """Set the etch factor of the layer.

        Parameters
        ----------
        etch_factor : Value
        """
        get_stackup_layer_stub().SetEtchFactor(_stackup_layer_value_message(self, etch_factor))

    @property
    def use_solver_properties(self):
        """Check if solver properties are used by the layer.

        Returns
        -------
        bool
        """
        return get_stackup_layer_stub().IsEtchFactorEnabled(self.msg).value

    @use_solver_properties.setter
    def use_solver_properties(self, use_solver_properties):
        """Set if solver properties are used by the layer.

        Parameters
        ----------
        use_solver_properties : bool
        """
        get_stackup_layer_stub().SetUseSolverProperties(
            stackup_layer_pb2.SetLayerPropEnabledMessage(
                layer=self.msg, enabled=use_solver_properties
            )
        )

    @property
    def hfss_solver_properties(self):
        """Get the solver properties of the layer.

        Returns
        -------
        tuple[DCThicknessType, Value, bool]
            Returns tuple of the form [dc_thickness_type, dc_thickness_value, solve_inside_enabled]
        """
        response = get_stackup_layer_stub().GetHFSSSolverProperties(self.msg)
        return (
            DCThicknessType(response.dc_thickness_type),
            Value(response.dc_thickness),
            response.solve_inside,
        )

    @hfss_solver_properties.setter
    def hfss_solver_properties(self, hfss_solver_props):
        """Set the solver properties of the layer.

        Parameters
        ----------
        tuple[DCThicknessType, Value, bool]
            Tuple is of the form [dc_thickness_type, dc_thickness_value, solve_inside_enabled]
        """
        hfss_solver_props_msg = stackup_layer_pb2.HFSSSolverPropertiesMessage(
            dc_thickness_type=hfss_solver_props[0].value,
            dc_thickness=messages.value_message(hfss_solver_props[1]),
            solve_inside=hfss_solver_props[2],
        )
        request = stackup_layer_pb2.SetHFSSSolverPropertiesMessage(
            layer=self.msg, hfss_solver_props=hfss_solver_props_msg
        )

        get_stackup_layer_stub().SetHFSSSolverProperties(request)

    @property
    def referencing_via_layer_ids(self):
        """Retrieve the layer ids of all via layers referencing the layer.

        Returns
        -------
        list[int]
        """
        return [
            via_lyr_id
            for via_lyr_id in get_stackup_layer_stub()
            .GetReferencingViaLayerIds(self.msg)
            .ref_layer_ids
        ]
