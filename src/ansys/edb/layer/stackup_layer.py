"""Stackup Layer."""

from enum import Enum

import ansys.api.edb.v1.stackup_layer_pb2 as stackup_layer_pb2

from ansys.edb.core import messages
from ansys.edb.layer import Layer
from ansys.edb.session import get_stackup_layer_stub
from ansys.edb.utility import Value


class DCThicknessType(Enum):
    """Enum representing DC thickness types of StackupLayers.

    - EFFECTIVE
    - LAYER
    - MANUAL
    """

    EFFECTIVE = stackup_layer_pb2.HFSSSolverPropertiesMessage.EFFECTIVE
    LAYER = stackup_layer_pb2.HFSSSolverPropertiesMessage.LAYER
    MANUAL = stackup_layer_pb2.HFSSSolverPropertiesMessage.MANUAL


class RoughnessRegion(Enum):
    """Enum representing regions for roughness models of StackupLayers.

    - TOP
    - BOTTOM
    - SIDE
    """

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
        ----------
        name : str
        layer_type : LayerType
        thickness : float
        elevation : float
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
        """:obj:`bool`: Flag indicating if the layer is a negative layer."""
        return get_stackup_layer_stub().GetNegative(self.msg).value

    @negative.setter
    def negative(self, is_negative):
        get_stackup_layer_stub().SetNegative(
            stackup_layer_pb2.SetNegativeMessage(layer=self.msg, is_negative=is_negative)
        )

    @property
    def thickness(self):
        """:class:`Value <ansys.edb.utility.Value>`: Thickness value of the layer."""
        return Value(get_stackup_layer_stub().GetThickness(self.msg))

    @thickness.setter
    def thickness(self, thickness):
        get_stackup_layer_stub().SetThickness(_stackup_layer_value_message(self, thickness))

    @property
    def lower_elevation(self):
        """:class:`Value <ansys.edb.utility.Value>`: Lower elevation value of the layer."""
        return Value(get_stackup_layer_stub().GetLowerElevation(self.msg))

    @lower_elevation.setter
    def lower_elevation(self, lower_elevation):
        get_stackup_layer_stub().SetLowerElevation(
            _stackup_layer_value_message(self, lower_elevation)
        )

    @property
    def upper_elevation(self):
        """:class:`Value <ansys.edb.utility.Value>`: Upper elevation value of the layer."""
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
        """Get the name of the fill material of the layer.

        Parameters
        ----------
        evaluated : bool
            If true and the material name is parameterized, the material name will be evaluated.

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
        """:obj:`bool`: Flag indicating if roughness models are used by the layer."""
        return get_stackup_layer_stub().IsRoughnessEnabled(self.msg).value

    @roughness_enabled.setter
    def roughness_enabled(self, enable_roughness):
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
        RoughnessModel
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
        roughness_model : :term:`RoughnessModel`
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
        """:obj:`bool`: Flag indicating if etch factor is used by the layer."""
        return get_stackup_layer_stub().IsEtchFactorEnabled(self.msg).value

    @etch_factor_enabled.setter
    def etch_factor_enabled(self, enable_etch_factor):
        get_stackup_layer_stub().SetEtchFactorEnabled(
            stackup_layer_pb2.SetLayerPropEnabledMessage(layer=self.msg, enabled=enable_etch_factor)
        )

    @property
    def etch_factor(self):
        """:class:`Value <ansys.edb.utility.Value>`: Etch factor of the layer."""
        return Value(get_stackup_layer_stub().GetEtchFactor(self.msg))

    @etch_factor.setter
    def etch_factor(self, etch_factor):
        get_stackup_layer_stub().SetEtchFactor(_stackup_layer_value_message(self, etch_factor))

    @property
    def use_solver_properties(self):
        """:obj:`bool`: Flag indicating if solver properties are used by the layer."""
        return get_stackup_layer_stub().IsEtchFactorEnabled(self.msg).value

    @use_solver_properties.setter
    def use_solver_properties(self, use_solver_properties):

        get_stackup_layer_stub().SetUseSolverProperties(
            stackup_layer_pb2.SetLayerPropEnabledMessage(
                layer=self.msg, enabled=use_solver_properties
            )
        )

    @property
    def hfss_solver_properties(self):
        """:term:`HFSSSolverProperties`: The HFSS solver properties of the layer."""
        response = get_stackup_layer_stub().GetHFSSSolverProperties(self.msg)
        return (
            DCThicknessType(response.dc_thickness_type),
            Value(response.dc_thickness),
            response.solve_inside,
        )

    @hfss_solver_properties.setter
    def hfss_solver_properties(self, hfss_solver_props):
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
        r""":obj:`list`\[:obj:`int`\]: Retrieve the layer ids of all via layers referencing the layer.

        Read-Only.
        """
        return [
            via_lyr_id
            for via_lyr_id in get_stackup_layer_stub()
            .GetReferencingViaLayerIds(self.msg)
            .ref_layer_ids
        ]
