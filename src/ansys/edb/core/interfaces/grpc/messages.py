"""Protobuf interface for message creation."""

from typing import List, Tuple

from ansys.api.edb.v1.adaptive_settings_pb2 import AdaptiveFrequencyDataMessage
from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage, ValueMessage
from ansys.api.edb.v1.material_def_pb2 import MaterialDefPropertiesMessage
from ansys.api.edb.v1.point_data_pb2 import (
    SENSE_CCW,
    PathPointsMessage,
    PointMessage,
    PointsMessage,
)
from ansys.api.edb.v1.refs_pb2 import LayerRefMessage, NetRefMessage
from ansys.api.edb.v1.simulation_settings_pb2 import (
    MeshOperationMessage,
    MeshOpNetLayerInfoMessage,
    SkinDepthMeshOperationMessage,
)
from ansys.api.edb.v1.simulation_setup_info_pb2 import SweepDataMessage
from google.protobuf.wrappers_pb2 import BoolValue, Int64Value, StringValue


def optional(params, key, value, func):
    """Evaluate a function is the value is present."""
    if value is not None:
        params[key] = func(value)


def str_message(s: str):
    """Convert to StringValue."""
    return StringValue(value=s) if s is not None else None


def bool_message(b: bool):
    """Convert to BoolValue."""
    return BoolValue(value=b) if b is not None else None


def int64_message(i: int):
    """Convert to Int64Value."""
    return Int64Value(value=i) if i is not None else None


def points_message(points):
    """Convert to PointsMessage."""
    if points is None:
        return None
    elif isinstance(points, list) or isinstance(points, tuple):
        return PointsMessage(points_data=points_data_message(points))
    else:
        return PointsMessage(polygon_data=edb_obj_message(points.msg))


def points_data_message(points):
    """Convert to PathPointsMessage."""
    is_tuple = isinstance(points, tuple)
    points_data = points[0] if is_tuple else points
    closed = points[1] if is_tuple and len(points) > 1 and points[1] is not None else True
    sense = points[2] if is_tuple and len(points) > 2 and points[2] is not None else SENSE_CCW
    data = [point_message(p) for p in points_data]
    return PathPointsMessage(data=data, closed=closed, sense=sense)


def point_message(point):
    """Convert to PointMessage."""
    if point is None:
        return None
    else:
        return PointMessage(x=value_message(point[0]), y=value_message(point[1]))


def value_message(value):
    """Convert to ValueMessage."""
    return ValueMessage(value=value)


def edb_obj_message(obj):
    """Extract EDB impl ptr."""
    if obj is None:
        return None
    elif isinstance(obj, EDBObjMessage):
        return obj
    else:
        raise RuntimeError("EDB Object has invalid ID.")


def material_properties_message(**kwargs):
    """Convert to MaterialDefPropertiesMessage."""
    params = {
        key: value_message(value)
        for key, value in kwargs.items()
        if key
        in {
            "permittivity",
            "permeability",
            "conductivity",
            "dielectric_loss_tangent",
            "magnetic_loss_tangent",
            "thermal_conductivity",
            "mass_density",
            "specific_heat",
            "youngs_modulus",
            "poissons_ratio",
            "thermal_expansion_coefficient",
        }
    }
    return MaterialDefPropertiesMessage(**params)


def layer_ref_message(layer):
    """Convert to LayerRefMessage."""
    if layer is None:
        return None
    elif type(layer) == str:
        return LayerRefMessage(name=str_message(layer))
    else:
        return LayerRefMessage(id=edb_obj_message(layer.msg))


def net_ref_message(net):
    """Convert to NetRefMessage."""
    if net is None:
        return None
    elif type(net) == str:
        return NetRefMessage(name=str_message(net))
    else:
        return NetRefMessage(id=edb_obj_message(net.msg))


def adaptive_frequency_message(frequency: str, max_delta_s: float, max_passes: int):
    """Convert to AdaptiveFrequencyDataMessage."""
    return AdaptiveFrequencyDataMessage(
        adaptive_frequency=frequency, max_delta=str(max_delta_s), max_passes=max_passes
    )


def mesh_operation_message(
    name: str,
    net_layers: List[Tuple[str, str, bool]],
    enabled: bool = True,
    refine_inside: bool = False,
    mesh_region: str = "",
    skin_depth: str = "1um",
    surf_tri_length: str = "1mm",
    num_layers: str = "2",
    max_elem: str = "1000",
    restrict_max_elem: bool = False,
):
    """Convert to MeshOperationMessage."""
    return MeshOperationMessage(
        name=name,
        enabled=enabled,
        refine_inside=refine_inside,
        mesh_region=mesh_region,
        skin_depth_mesh_op=_mesh_op_skin_depth_message(
            skin_depth, surf_tri_length, num_layers, max_elem, restrict_max_elem
        ),
        net_layer_info=[_mesh_op_net_layer_message(*nl) for nl in net_layers],
    )


def frequency_sweep_message(name, distribution, start_f, end_f, step, fast_sweep):
    """Convert to FrequencySweepMessage."""
    return SweepDataMessage(
        name=name,
        frequency_string=distribution + " " + start_f + " " + end_f + " " + step,
        fast_sweep=fast_sweep,
    )


def _mesh_op_skin_depth_message(
    skin_depth, surf_tri_length, num_layers, max_elem, restrict_max_elem
):
    return SkinDepthMeshOperationMessage(
        skin_depth=skin_depth,
        max_surface_triangle_length=surf_tri_length,
        num_layers=num_layers,
        max_elements=max_elem,
        restrict_max_elements=restrict_max_elem,
    )


def _mesh_op_net_layer_message(net, layer, is_sheet):
    return MeshOpNetLayerInfoMessage(net=net, layer=layer, is_sheet=is_sheet)


def value_message_to_value(message):
    """Extract a value from ValueMessage."""
    if message:
        return message.value
