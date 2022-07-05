"""Protobuf interface for message creation."""

from typing import List, Tuple

from ansys.api.edb.v1.adaptive_settings_pb2 import AdaptiveFrequencyDataMessage
from ansys.api.edb.v1.arc_data_pb2 import ArcMessage
from ansys.api.edb.v1.database_pb2 import (
    GetProductPropertyIdsMessage,
    GetProductPropertyMessage,
    ProductPropertyIdMessage,
    SetProductPropertyMessage,
)
from ansys.api.edb.v1.edb_messages_pb2 import (
    BoolPropertyMessage,
    EDBObjCollectionMessage,
    EDBObjMessage,
    EDBObjNameMessage,
    IntPropertyMessage,
    PointerPropertyMessage,
    StringPropertyMessage,
    ValueMessage,
)
from ansys.api.edb.v1.edge_term_pb2 import (
    EdgeCreationMessage,
    EdgeParamsMessage,
    EdgeTermCreationMessage,
    EdgeTermSetEdgesMessage,
    EdgeType,
    PadEdgeParamsMessage,
    PrimitiveEdgeParamsMessage,
)
from ansys.api.edb.v1.layout_pb2 import (
    LayoutConvertP2VMessage,
    LayoutExpandedExtentMessage,
    LayoutGetItemsMessage,
)
from ansys.api.edb.v1.material_def_pb2 import MaterialDefPropertiesMessage
from ansys.api.edb.v1.padstack_inst_term_pb2 import (
    PadstackInstTermCreationsMessage,
    PadstackInstTermParamsMessage,
    PadstackInstTermSetParamsMessage,
)
from ansys.api.edb.v1.pin_group_pb2 import (
    PinGroupCreationMessage,
    PinGroupGetUniqueNameMessage,
    PinGroupLookupMessage,
    PinGroupPinsModifyMessage,
)
from ansys.api.edb.v1.pin_group_term_pb2 import (
    PinGroupTermCreationMessage,
    PinGroupTermSetLayerMessage,
    PinGroupTermSetPinGroupMessage,
)
from ansys.api.edb.v1.point_data_pb2 import (
    SENSE_CCW,
    PathPointsMessage,
    PointMessage,
    PointPropertyMessage,
    PointsMessage,
)
from ansys.api.edb.v1.point_term_pb2 import (
    PointTermCreationMessage,
    PointTermParamsMessage,
    PointTermSetParamsMessage,
)
from ansys.api.edb.v1.port_post_processing_prop_pb2 import PortPostProcessingPropMessage
from ansys.api.edb.v1.refs_pb2 import LayerRefMessage, NetRefMessage
from ansys.api.edb.v1.rlc_pb2 import RlcMessage
from ansys.api.edb.v1.simulation_settings_pb2 import (
    MeshOperationMessage,
    MeshOpNetLayerInfoMessage,
    SkinDepthMeshOperationMessage,
)
from ansys.api.edb.v1.simulation_setup_info_pb2 import SweepDataMessage
from ansys.api.edb.v1.term_inst_pb2 import TermInstCreationMessage
from ansys.api.edb.v1.term_inst_term_pb2 import (
    TermInstTermCreationMessage,
    TermInstTermSetInstanceMessage,
)
from ansys.api.edb.v1.term_pb2 import (
    TermFindByNameMessage,
    TermGetProductSolversMessage,
    TermSetLayerMessage,
    TermSetParamsMessage,
    TermSetRefMessage,
    TermSetSolverOptionMessage,
)
from ansys.api.edb.v1.transform_pb2 import TransformMessage, TransformPropertyMessage
from google.protobuf.wrappers_pb2 import BoolValue, Int64Value, StringValue

from ansys.edb.core.utility.value import Value


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


def point_property_message(target, point):
    """Convert to PointPropertyMessage."""
    return PointPropertyMessage(target=target.msg, point=point_message(point))


def arc_message(arc):
    """Convert to ArcMessage."""
    if isinstance(arc, tuple) and len(arc) == 2:
        return ArcMessage(start=point_message(arc[0]), end=point_message(arc[1]))
    raise RuntimeError("arc must be of a tuple containing start and end point.")


def transform_message(transform):
    """Convert to TransformMessage."""
    if transform is None:
        return None
    else:
        return TransformMessage(
            scale=value_message(transform.scale),
            angle=value_message(transform.angle),
            mirror=transform.mirror,
            offset_x=value_message(transform.offset_x),
            offset_y=value_message(transform.offset_y),
        )


def transform_property_message(target, transform):
    """Convert to TransformPropertyMessage."""
    return TransformPropertyMessage(target=target.msg, transf=transform_message(transform))


def layout_get_items_message(layout, item_type):
    """Convert to LayoutGetItemsMessage."""
    return LayoutGetItemsMessage(layout=layout.msg, obj_type=item_type.value)


def int_property_message(target, value):
    """Convert to IntPropertyMessage."""
    return IntPropertyMessage(target=target.msg, value=value)


def bool_property_message(target, value):
    """Convert to BoolPropertyMessage."""
    return BoolPropertyMessage(target=target.msg, value=value)


def string_property_message(target, value):
    """Convert to StringPropertyMessage."""
    return StringPropertyMessage(target=target.msg, value=value)


def pointer_property_message(target, value):
    """Convert to PointerPropertyMessage."""
    return PointerPropertyMessage(target=target.msg, value=value.msg)


def layout_expanded_extent_message(
    layout, nets, extent, exp, exp_unitless, use_round_corner, num_increments
):
    """Convert to LayoutExpandedExtentMessage."""
    return LayoutExpandedExtentMessage(
        layout=layout.msg,
        nets=edb_obj_collection_message(nets),
        etype=extent.value,
        expansion_factor=exp,
        expansion_factor_unitless=exp_unitless,
        use_round_corner=use_round_corner,
        num_increments=num_increments,
    )


def layout_convert_p2v_message(layout, primitives, is_pins):
    """Convert to LayoutConvertP2VMessage."""
    return LayoutConvertP2VMessage(
        layout=layout.msg, primitives=edb_obj_collection_message(primitives), is_pins=is_pins
    )


def point_term_params_message(layer, point):
    """Convert to PointTermParamMessage."""
    return PointTermParamsMessage(point=point_message(point), layer=layer_ref_message(layer))


def point_term_set_params_message(term, layer, point):
    """Convert to PointTermSetParamsMessage."""
    return PointTermSetParamsMessage(term=term.msg, params=point_term_params_message(layer, point))


def point_term_creation_message(layout, net, layer, name, x, y):
    """Convert to PointTermCreationMessage."""
    return PointTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net),
        name=name,
        params=point_term_params_message(layer, (x, y)),
    )


def padstack_inst_term_params_message(padstack_instance, layer):
    """Convert to PadstackInstTermParamsMessage."""
    return PadstackInstTermParamsMessage(
        padstack_instance=padstack_instance.msg, layer=layer_ref_message(layer)
    )


def padstack_inst_term_creation_message(layout, name, padstack_instance, layer, net, is_ref):
    """Convert to PadstackInstTermCreationMessage."""
    return PadstackInstTermCreationsMessage(
        layout=layout.msg,
        name=name,
        params=padstack_inst_term_params_message(padstack_instance, layer),
        net=net_ref_message(net),
        is_ref=is_ref,
    )


def padstack_inst_term_set_params_message(term, padstack_instance, layer):
    """Convert to PadstackInstTermSetParamsMessage."""
    return PadstackInstTermSetParamsMessage(
        term=term.msg, params=padstack_inst_term_params_message(padstack_instance, layer)
    )


def pin_group_creation_message(layout, name, padstack_instances):
    """Convert to PinGroupCreationMessage."""
    return PinGroupCreationMessage(
        layout=layout.msg, name=name, pins=[pi.msg for pi in padstack_instances]
    )


def pin_group_lookup_message(layout, name):
    """Convert to PinGroupLookupMessage."""
    return PinGroupLookupMessage(layout=layout.msg, name=name)


def pin_group_get_unique_name_message(layout, prefix):
    """Convert to PinGroupGetUniqueNameMessage."""
    return PinGroupGetUniqueNameMessage(layout=layout.msg, prefix=prefix)


def pin_group_pins_modify_message(pin_group, padstack_instances):
    """Convert to PinGroupPinsModifyMessage."""
    return PinGroupPinsModifyMessage(
        pin_group=pin_group.msg, pins=[pi.msg for pi in padstack_instances]
    )


def pin_group_term_creation_message(layout, net_ref, name, pin_group, is_ref):
    """Convert to PinGroupTermCreationMessage."""
    return PinGroupTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net_ref),
        name=name,
        pin_group=pin_group.msg,
        is_ref=is_ref,
    )


def pin_group_term_set_pin_group_message(term, pin_group):
    """Convert to PinGroupTermSetPinGroupMessage."""
    return PinGroupTermSetPinGroupMessage(term=term.msg, pin_group=pin_group.msg)


def pin_group_term_set_layer_message(term, layer_ref):
    """Convert to PinGroupTermSetLayerMessage."""
    return PinGroupTermSetLayerMessage(term=term.msg, layer=layer_ref_message(layer_ref))


def edge_creation_message(edge_type, **params):
    """Convert to EdgeCreationMessage."""
    return EdgeCreationMessage(edge_type=edge_type, params=edge_params_message(edge_type, **params))


def edge_params_message(edge_type, **params):
    """Convert to EdgeParamsMessage."""
    if edge_type == EdgeType.PRIMITIVE_EDGE:
        return EdgeParamsMessage(primitve_params=primitive_edge_params_message(**params))
    elif edge_type == EdgeType.PAD_EDGE:
        return EdgeParamsMessage(pad_params=pad_edge_params_message(**params))
    else:
        raise RuntimeError(f"Edge type {edge_type} is not valid.")


def primitive_edge_params_message(primitive, point):
    """Convert to PrimitiveEdgeParamsMessage."""
    return PrimitiveEdgeParamsMessage(primitive=primitive.msg, point=point_message(point))


def pad_edge_params_message(padstack_instance, layer, arc):
    """Convert to PadEdgeParamsMessage."""
    return PadEdgeParamsMessage(
        padstack_instance=padstack_instance.msg,
        layer=layer_ref_message(layer),
        arc=arc_message(arc),
    )


def edge_term_creation_message(layout, net, name, edges, is_ref):
    """Convert to EdgeTermCreationMessage."""
    return EdgeTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net),
        name=name,
        edges=[edge.msg for edge in edges],
        is_ref=is_ref,
    )


def edge_term_set_edges_message(terminal, edges):
    """Convert to EdgeTermSetEdgesMessage."""
    return EdgeTermSetEdgesMessage(term=terminal.msg, edges=[edge.msg for edge in edges])


def term_set_params_message(term, **params):
    """Convert to TermSetParamsMessage."""
    payload = {"term": term.msg}

    if "boundary_type" in params:
        payload["boundary_type"] = params.pop("boundary_type")
    if "term_to_ground" in params:
        payload["term_to_ground"] = params.pop("term_to_ground")
    if "hfss_pi_type" in params:
        payload["hfss_pi_type"] = params.pop("hfss_pi_type")
    if "ref_term" in params or "ref_layer" in params:
        ref_term = params.pop("ref_term", ())
        ref_term = ref_term if isinstance(ref_term, tuple) else (ref_term,)
        ref_layer = params.pop("ref_layer", ())
        ref_layer = ref_layer if isinstance(ref_layer, tuple) else (ref_layer,)
        payload["ref"] = term_set_ref_message(ref_term, ref_layer)
    if "is_auto_port" in params:
        payload["is_auto_port"] = bool_message(params.pop("is_auto_port"))
    if "is_circuit_port" in params:
        payload["is_circuit_port"] = bool_message(params.pop("is_circuit_port"))
    if "use_ref_from_hierarchy" in params:
        payload["use_ref_from_hierarchy"] = bool_message(params.pop("use_ref_from_hierarchy"))
    if "name" in params:
        payload["name"] = str_message(params.pop("name"))
    if "impedance" in params:
        payload["impedance"] = value_message(params.pop("impedance"))
    if "source_amplitude" in params:
        payload["source_amplitude"] = value_message(params.pop("source_amplitude"))
    if "source_phase" in params:
        payload["source_phase"] = value_message(params.pop("source_phase"))
    if "s_param_model" in params:
        payload["s_param_model"] = str_message(params.pop("s_param_model"))
    if "rlc" in params:
        payload["rlc"] = rlc_message(params.pop("rlc"))
    if "port_post_processing_prop" in params:
        payload["port_post_processing_prop"] = port_post_processing_prop_message(
            params.pop("port_post_processing_prop")
        )
    if len(params.keys()):
        raise RuntimeError("unknown parameters.")
    return TermSetParamsMessage(**payload)


def term_set_ref_message(term_params, layer_params):
    """Convert to TermSetRefMessage."""
    if len(term_params) and len(layer_params):
        raise RuntimeError("can only reference either a terminal or a layer.")
    if len(term_params) == 1:
        return TermSetRefMessage(ref_term=edb_obj_message(*term_params))
    if len(layer_params):
        return TermSetRefMessage(ref_layer=term_set_layer_message(*layer_params))


def term_set_layer_message(layer_ref, contexts=None):
    """Convert to TermSetLayerMessage."""
    contexts = [] if contexts is None else contexts
    return TermSetLayerMessage(
        layer=layer_ref_message(layer_ref), contexts=[str_message(ctx) for ctx in contexts]
    )


def term_find_by_name_message(layout, name):
    """Convert to TermFindByNameMessage."""
    return TermFindByNameMessage(layout=layout.msg, name=name)


def term_get_product_solver_message(term, product_id):
    """Convert to TermGetProductSolversMessage."""
    return TermGetProductSolversMessage(term=term.msg, product_id=product_id)


def term_set_solver_option_message(term, product_id, name, option):
    """Convert to TermSetSolverOptionMessage."""
    return TermSetSolverOptionMessage(
        term=term.msg, product_id=product_id, name=name, option=option
    )


def term_inst_creation_message(layout, net_ref, cell_inst, name):
    """Convert to TermInstCreationMessage."""
    return TermInstCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net_ref),
        cell_inst=cell_inst.msg,
        name=name,
    )


def term_inst_term_creation_message(layout, net_ref, name, term_inst, is_ref):
    """Convert to TermInstTermCreationMessage."""
    return TermInstTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net_ref),
        name=name,
        term_inst=term_inst.msg,
        is_ref=is_ref,
    )


def term_inst_term_set_instance_message(term, term_inst):
    """Convert to TermInstTermSetInstanceMessage."""
    return TermInstTermSetInstanceMessage(term=term.msg, term_inst=term_inst.msg)


def edb_obj_message(obj):
    """Convert to EDBObjMessage."""
    if obj is None:
        return None
    elif isinstance(obj, EDBObjMessage):
        return obj
    else:
        return obj.msg


def edb_obj_collection_message(objs):
    """Convert to EDBObjCollectionMessage."""
    return EDBObjCollectionMessage(items=[edb_obj_message(obj) for obj in objs])


def edb_obj_name_message(obj, name):
    """Convert to EDBObjNameMessage."""
    return EDBObjNameMessage(target=edb_obj_message(obj), name=name)


def rlc_message(rlc):
    """Convert to RlcMessage."""
    return RlcMessage(
        r=value_message(rlc.r),
        l=value_message(rlc.l),
        c=value_message(rlc.c),
        r_enabled=bool_message(rlc.r_enabled),
        l_enabled=bool_message(rlc.l_enabled),
        c_enabled=bool_message(rlc.c_enabled),
        is_parallel=bool_message(rlc.is_parallel),
    )


def port_post_processing_prop_message(prop):
    """Convert to PortPostProcessingPropMessage."""
    return PortPostProcessingPropMessage(
        voltage_magnitude=value_message(prop.voltage_magnitude),
        voltage_phase=value_message(prop.voltage_phase),
        deembed_length=value_message(prop.deembed_length),
        renormalization_impedance=value_message(prop.renormalization_impedance),
        do_deembed=prop.do_deembed,
        do_deembed_gap_length=prop.do_deembed_gap_l,
        do_renormalize=prop.do_renormalize,
    )


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


def value_message(val):
    """Convert data into a ValueMessage.

    Parameters
    ----------
    val : str, int, float, complex, Value

    Returns
    -------
    ValueMessage
    """
    if isinstance(val, Value):
        return val.msg

    msg = ValueMessage()
    if isinstance(val, str):
        msg.text = val
        msg.variable_owner.id = 0
    elif isinstance(val, float) or isinstance(val, int):
        msg.constant.real = val
        msg.constant.imag = 0
    elif isinstance(val, complex):
        msg.constant.real = val.real
        msg.constant.imag = val.imag
    else:
        assert False, "Invalid Value"
    return msg


def product_property_id_message(prod_id, att_id):
    """Convert to ProductPropertyIdMessage."""
    return ProductPropertyIdMessage(product_id=prod_id.value, attribute_id=att_id)


def set_product_property_message(obj, prod_id, att_id, value):
    """Convert to SetProductPropertyMessage."""
    return SetProductPropertyMessage(
        edb_obj=obj.msg,
        product_prop_id=product_property_id_message(prod_id, att_id),
        property_value=value,
    )


def get_product_property_message(obj, prod_id, att_id):
    """Convert to GetProductPropertyMessage."""
    return GetProductPropertyMessage(
        edb_obj=obj.msg, product_prop_id=product_property_id_message(prod_id, att_id)
    )


def get_product_property_ids_message(obj, prod_id):
    """Convert to GetProductPropertyIdsMessage."""
    return GetProductPropertyIdsMessage(edb_obj=obj.msg, product_id=prod_id.value)
