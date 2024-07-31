"""Protobuf interface for message creatia."""

from ansys.api.edb.v1 import arc_data_pb2
from ansys.api.edb.v1.cell_instance_pb2 import (
    CellInstanceCreationMessage,
    CellInstanceParameterOverride,
)
from ansys.api.edb.v1.cell_pb2 import (
    CellCutOutMessage,
    CellFindMessage,
    CellSetTemperatureSettingsMessage,
)
from ansys.api.edb.v1.component_def_pb2 import ComponentDefCreateMessage
from ansys.api.edb.v1.component_group_pb2 import (
    ComponentGroupCreateMessage,
    SetComponentGroupTypeMessage,
)
from ansys.api.edb.v1.die_property_pb2 import (
    DieOrientationMessage,
    DieOrientationPropertyMessage,
    DieTypeMessage,
    DieTypePropertyMessage,
)
from ansys.api.edb.v1.differential_pair_pb2 import (
    DifferentialPairCreationMessage,
    DifferentialPairNetRefsMessage,
)
from ansys.api.edb.v1.edb_messages_pb2 import (
    BoolPropertyMessage,
    ComponentTypeMessage,
    DesignModePropertyMessage,
    DoublePropertyMessage,
    DoublesMessage,
    DoublesPropertyMessage,
    EDBInternalIdMessage,
    EDBObjCollectionMessage,
    EDBObjMessage,
    EDBObjNameMessage,
    EDBObjPairMessage,
    GetProductPropertyIdsMessage,
    GetProductPropertyMessage,
    HfssExtentInfoMessage,
    HfssExtentMessage,
    IntPropertyMessage,
    PointerPropertyMessage,
    ProductPropertyIdMessage,
    SetProductPropertyMessage,
    StringPairMessage,
    StringPairPropertyMessage,
    StringPropertyMessage,
    StringsMessage,
    StringsPropertyMessage,
    TemperatureSettingsMessage,
    UInt64PropertyMessage,
    ValueMessage,
    ValuePairMessage,
    ValuePairPropertyMessage,
    ValuePropertyMessage,
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
from ansys.api.edb.v1.group_pb2 import GroupModifyMemberMessage
from ansys.api.edb.v1.hfss_simulation_settings_pb2 import (
    AdaptiveFrequencyDataMessage,
    AdaptiveMultiFrequencyDataMessage,
    BroadbandFrequencyAdaptiveSolutionMessage,
    MatrixConvergenceDataMessage,
    MultiFrequencyAdaptiveSolutionMessage,
    SingleFrequencyAdaptiveSolutionMessage,
)
from ansys.api.edb.v1.hfss_simulation_setup_pb2 import (
    LengthMeshOperationMessage,
    MeshOperationMessage,
    MeshOpNetLayerInfoMessage,
    SkinDepthMeshOperationMessage,
)
from ansys.api.edb.v1.hierarchy_obj_pb2 import ObjectNameInLayoutMessage
from ansys.api.edb.v1.inst_array_pb2 import InstArrayCreationMessage
from ansys.api.edb.v1.layout_pb2 import (
    LayoutConvertP2VMessage,
    LayoutExpandedExtentMessage,
    LayoutGetItemsMessage,
)
from ansys.api.edb.v1.material_def_pb2 import MaterialDefPropertiesMessage
from ansys.api.edb.v1.mcad_model_pb2 import *  # noqa
from ansys.api.edb.v1.net_pb2 import NetGetLayoutObjMessage
from ansys.api.edb.v1.package_def_pb2 import HeatSinkMessage, SetHeatSinkMessage
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
from ansys.api.edb.v1.pin_pair_model_pb2 import PinPairModelRlcPropertyMessage
from ansys.api.edb.v1.point_3d_data_pb2 import *  # noqa
from ansys.api.edb.v1.point_data_pb2 import *  # noqa
from ansys.api.edb.v1.point_term_pb2 import (
    PointTermCreationMessage,
    PointTermParamsMessage,
    PointTermSetParamsMessage,
)
from ansys.api.edb.v1.polygon_data_pb2 import *  # noqa
from ansys.api.edb.v1.port_post_processing_prop_pb2 import PortPostProcessingPropMessage
from ansys.api.edb.v1.refs_pb2 import LayerRefMessage, LayerRefPropertyMessage, NetRefMessage
from ansys.api.edb.v1.rlc_pb2 import RlcMessage
from ansys.api.edb.v1.simulation_setup_pb2 import MatrixConvergenceEntryMessage
from ansys.api.edb.v1.sparameter_model_pb2 import SParameterModelMessage
from ansys.api.edb.v1.spice_model_pb2 import SpiceModelMessage, SpiceModelNewTerminalPinMessage
from ansys.api.edb.v1.structure3d_pb2 import ClosureMessage, SetClosureMessage
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
from ansys.api.edb.v1.via_group_pb2 import (
    ViaGroupCreateWithOutlineMessage,
    ViaGroupCreateWithPrimitivesMessage,
)
from ansys.api.edb.v1.voltage_regulator_pb2 import PowerModuleMessage
from google.protobuf.empty_pb2 import Empty
from google.protobuf.wrappers_pb2 import BoolValue, DoubleValue, FloatValue, Int64Value, StringValue

from ansys.edb.core.simulation_setup.mesh_operation import (
    LengthMeshOperation,
    SkinDepthMeshOperation,
)
from ansys.edb.core.utility import conversions, value


def str_message(s: str):
    """Convert to a ``StringValue`` message."""
    return StringValue(value=s) if s is not None else None


def bool_message(b: bool):
    """Convert to a ``BoolValue`` message."""
    return BoolValue(value=b) if b is not None else None


def int64_message(i: int):
    """Convert to an ``Int64Value`` message."""
    return Int64Value(value=i) if i is not None else None


def float_message(v: float):
    """Convert to a ``FloatValue`` message."""
    return FloatValue(value=v)


def double_message(v: float):
    """Convert to a ``DoubleValue`` message."""
    return DoubleValue(value=v)


def empty_message():
    """Get an empty message."""
    return Empty()


def str_pair_message(pair):
    """Convert to a ``StringPairMessage`` object."""
    return StringPairMessage(first=pair[0], second=pair[1])


def point_message(point):
    """Convert to a ``PointMessage`` object."""
    point = conversions.to_point(point)
    return PointMessage(x=value_message(point.x), y=value_message(point.y))


def point_property_message(target, point):
    """Convert to a ``PointPropertyMessage`` object."""
    return PointPropertyMessage(target=target.msg, point=point_message(point))


def point_data_rotate_message(point, center, angle):
    """Convert to a ``PointRotateMessage`` object."""
    return PointDataRotateMessage(
        point=point_message(point), rotation_center=point_message(center), angle=angle
    )


def point_data_with_line_message(point, line_start, line_end):
    """Convert to a ``PointDataWithLineMessage`` object."""
    return PointDataWithLineMessage(
        point=point_message(point),
        line_start=point_message(line_start),
        line_end=point_message(line_end),
    )


def box_message(ll, ur):
    """Convert to a ``BoxMessage`` object."""
    return BoxMessage(lower_left=point_message(ll), upper_right=point_message(ur))


def circle_message(center, radius):
    """Convert to a ``CircleMessage`` object."""
    return CircleMessage(center=point_message(center), radius=value_message(radius))


def polygon_data_message(pd):
    """Convert to a ``PolygonDataMessage`` object."""
    return PolygonDataMessage(
        points=[point_message(pt) for pt in pd.points],
        closed=pd.is_closed,
        sense=pd.sense.value,
        holes=[polygon_data_message(h) for h in pd.holes],
    )


def polygon_data_list_message(pds):
    """Convert to a ``PolygonDataListMessage`` object."""
    pds = _as_array(pds)
    return PolygonDataListMessage(polygons=[polygon_data_message(pd) for pd in pds])


def polygon_data_with_tol_message(pd, tol):
    """Convert to a ``PolygonDataWithToleranceMessage`` object."""
    return PolygonDataWithToleranceMessage(polygon=polygon_data_message(pd), tol=tol)


def polygon_data_pair_message(pds1, pds2):
    """Convert to a ``PolygonDataPairMessage`` object."""
    return PolygonDataPairMessage(
        first=polygon_data_list_message(pds1), second=polygon_data_list_message(pds2)
    )


def polygon_data_pair_with_tolerance_message(pd1, pd2, tol):
    """Convert to a ``PolygonDataPairWithToleranceMessage`` object."""
    return PolygonDataPairWithToleranceMessage(
        first=polygon_data_message(pd1), second=polygon_data_message(pd2), tol=tol
    )


def _polygon_data_transform_message_point_value(point, value):
    """Convert to a ``PolygonDataTransformMessage`` object."""
    return PolygonDataTransformMessage.PointValueMessage(point=point_message(point), value=value)


def polygon_data_transform_message(op, pd, *args):
    """Convert to a ``PolygonDataTransformMessage`` object."""
    payload = {}
    if op == "move":
        payload["move"] = point_message(args[0])
    elif op == "rotate":
        payload["rotate"] = _polygon_data_transform_message_point_value(*args)
    elif op == "scale":
        payload["scale"] = _polygon_data_transform_message_point_value(*args)
    elif op == "mirror_x":
        payload["mirror_x"] = args[0]

    return PolygonDataTransformMessage(polygon=polygon_data_message(pd), **payload)


def polygon_data_remove_arc_message(pd, max_chord_error, max_arc_angle, max_points):
    """Convert to a ``PolygonDataRemoveArcMessage`` object."""
    return PolygonDataRemoveArcMessage(
        polygon=polygon_data_message(pd),
        max_chord_error=max_chord_error,
        max_arc_angle=max_arc_angle,
        max_points=max_points,
    )


def polygon_data_with_circle_message(pd, center, radius):
    """Convert to a ``PolygonDataWithCircleMessage`` object."""
    return PolygonDataWithCircleMessage(
        polygon=polygon_data_message(pd), circle=circle_message(center, radius)
    )


def polygon_data_with_point_message(pd, point):
    """Convert to a ``PolygonDataWithPointMessage`` object."""
    return PolygonDataWithPointMessage(polygon=polygon_data_message(pd), point=point_message(point))


def polygon_data_with_points_message(pd, point=None, polygon=None):
    """Convert to a ``PolygonDataWithPointsMessage`` object."""
    payload = {}
    if point is not None:
        payload["point"] = point_message(point)
    elif polygon is not None:
        payload["polygon"] = polygon_data_message(polygon)

    return PolygonDataWithPointsMessage(polygon=polygon_data_message(pd), **payload)


def polygon_data_expand_message(pd, offset, tol, round_corner, max_corner_expansion):
    """Convert to a ``PolygonDataExpandMessage`` object."""
    return PolygonDataExpandMessage(
        polygon=polygon_data_message(pd),
        offset=offset,
        tol=tol,
        round_corner=round_corner,
        max_corner_extension=max_corner_expansion,
    )


def polygon_data_get_alpha_shape_message(pd, alpha):
    """Convert to a ``PolygonDataGetAlphaShapeMessage`` object."""
    return PolygonDataGetAlphaShapeMessage(polygon=polygon_data_message(pd), alpha=alpha)


def _arc_rotation_dir(dir):
    if dir.value == "cw":
        return arc_data_pb2.ROTATION_DIRECTION_CW
    elif dir.value == "ccw":
        return arc_data_pb2.ROTATION_DIRECTION_CCW
    elif dir.value == "colinear":
        return arc_data_pb2.ROTATION_DIRECTION_COLINEAR


def arc_message(arc):
    """Convert to an ``ArcMessage`` object."""
    message = arc_data_pb2.ArcMessage(start=point_message(arc.start), end=point_message(arc.end))
    h, opts = arc._height, arc._height_options  # noqa
    if h is not None:
        message.height.value = h
    elif "radius" in opts and "direction" in opts and "is_big" in opts:
        message.radius.radius = opts["radius"]
        message.radius.dir = _arc_rotation_dir(opts["direction"])
        message.radius.is_big = opts["is_big"]
    elif "center" in opts and "direction" in opts:
        message.center.point.CopyFrom(point_message(opts["center"]))
        message.center.dir = _arc_rotation_dir(opts["direction"])
    elif "thru" in opts:
        message.thru.CopyFrom(point_message(opts["thru"]))
    else:
        raise TypeError(
            "`ArcData` instance was not initialized with correct parameters to compute height."
            f"Received '{opts}'"
        )

    return message


def arc_data_two_points(arc1, arc2):
    """Convert to an ``ArcDataTwoArcsMessage`` object."""
    return arc_data_pb2.ArcDataTwoArcsMessage(arc1=arc_message(arc1), arc2=arc_message(arc2))


def int_property_message(target, value):
    """Convert to an ``IntPropertyMessage`` object."""
    return IntPropertyMessage(target=target.msg, value=value)


def uint64_property_message(target, value):
    """Convert to a ``UInt64PropertyMessage`` object."""
    return UInt64PropertyMessage(target=target.msg, value=value)


def bool_property_message(target, value):
    """Convert to a ``BoolPropertyMessage`` object."""
    return BoolPropertyMessage(target=target.msg, value=value)


def string_property_message(target, value):
    """Convert to a ``StringPropertyMessage`` object."""
    return StringPropertyMessage(target=target.msg, value=value)


def string_pair_property_message(target, pair):
    """Convert to a ``StringPairPropertyMessage`` object."""
    return StringPairPropertyMessage(target=target.msg, values=str_pair_message(pair))


def value_property_message(target, value):
    """Convert to a ``ValuePropertyMessage`` object."""
    return ValuePropertyMessage(target=edb_obj_message(target), value=value_message(value))


def pointer_property_message(target, value):
    """Convert to a ``PointerPropertyMessage`` object."""
    return PointerPropertyMessage(target=target.msg, value=value.msg)


def edb_obj_name_message(obj, name):
    """Convert to an ``EDBObjNameMessage`` object."""
    return EDBObjNameMessage(target=edb_obj_message(obj), name=name)


def object_name_in_layout_message(layout, name):
    """Convert to an ``ObjectNameInLayoutMessage`` object."""
    return ObjectNameInLayoutMessage(layout=layout.msg, name=name)


def group_modify_member_message(target, member):
    """Convert to a ``GroupModifyMemberMessage`` object."""
    return GroupModifyMemberMessage(target=target.msg, member=member.msg)


def via_group_create_with_primitives_message(layout, primitives, is_persistent):
    """Convert to a ``ViaGroupCreateWithPrimitivesMessage`` object."""
    return ViaGroupCreateWithPrimitivesMessage(
        layout=layout.msg,
        primitives=edb_obj_collection_message(primitives),
        is_persistent=is_persistent,
    )


def via_group_create_with_outline_message(layout, outline, conductivity_ratio, layer, net=None):
    """Convert to a ``ViaGroupCreateWithOutlineMessage`` object."""
    return ViaGroupCreateWithOutlineMessage(
        layout=layout.msg,
        points=polygon_data_message(outline),
        conductivity_ratio=conductivity_ratio,
        layer=layer_ref_message(layer),
        net=net_ref_message(net),
    )


def cell_instance_creation_message(layout, name, ref):
    """Convert to a ``CellInstanceCreationMessage`` object."""
    return CellInstanceCreationMessage(
        target=object_name_in_layout_message(layout, name), ref=edb_obj_message(ref)
    )


def cell_instance_parameter_override_message(target, param_name, param_value):
    """Convert to a ``CellInstanceParameterOverrideMessage`` object."""
    return CellInstanceParameterOverride(
        target=edb_obj_message(target),
        pname=param_name,
        pval=value_message(param_value),
    )


def inst_array_creation_message(layout, name, ref, orig, xaxis, yaxis, xcount, ycount):
    """Convert to an ``InstArrayCreationMessage`` object."""
    return InstArrayCreationMessage(
        layout=string_property_message(layout, name),
        ref=edb_obj_message(ref),
        orig=point_message(orig),
        xaxis=point_message(xaxis),
        yaxis=point_message(yaxis),
        xcount=value_message(xcount),
        ycount=value_message(ycount),
    )


def component_def_creation_message(db, comp_name, fp):
    """Convert to a ``ComponentDefCreateMessage`` object."""
    if fp is None:
        return ComponentDefCreateMessage(db=db.msg, comp_name=comp_name, fp=None)
    else:
        return ComponentDefCreateMessage(db=db.msg, comp_name=comp_name, fp=fp.msg)


def transform_message(transform):
    """Convert to a ``TransformMessage`` object."""
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
    """Convert to a ``TransformPropertyMessage`` object."""
    return TransformPropertyMessage(target=target.msg, transf=transform_message(transform))


def point3d_message(point3d):
    """Convert to a ``Point3DMessage`` object."""
    if point3d is None:
        return None
    else:
        x, y, z = point3d.x, point3d.y, point3d.z
        return Point3DMessage(x=value_message(x), y=value_message(y), z=value_message(z))


def point_3d_property_message(target, value):
    """Convert to a ``Point3DPropertyMessage`` object."""
    return Point3DPropertyMessage(target=edb_obj_message(target), origin=point3d_message(value))


def layout_get_items_message(layout, item_type):
    """Convert to a ``LayoutGetItemsMessage`` object."""
    return LayoutGetItemsMessage(layout=layout.msg, obj_type=item_type.value)


def layout_expanded_extent_message(
    layout, nets, extent, exp, exp_unitless, use_round_corner, num_increments
):
    """Convert to a ``LayoutExpandedExtentMessage`` object."""
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
    """Convert to a ``LayoutConvertP2VMessage`` message."""
    return LayoutConvertP2VMessage(
        layout=layout.msg, primitives=edb_obj_collection_message(primitives), is_pins=is_pins
    )


def temperature_settings_message(settings):
    """Convert to a ``TemperatureSettingsMessage`` object."""
    return TemperatureSettingsMessage(
        temperature=value_message(settings.temperature),
        include_temp_dependence=settings.include_temp_dependence,
        enable_thermal_feedback=settings.enable_thermal_feedback,
    )


def hfss_extent_message(val):
    """Convert to an ``ExtentMessage`` object."""
    if type(val) == float or type(val) == int:
        value = val
        absolute = False
    else:
        value, absolute = val
    return HfssExtentMessage(value=value, absolute=absolute)


def hfss_extent_info_message(hfss_info):
    """Convert to an ``HfssExtentInfoMessage`` object."""
    return HfssExtentInfoMessage(
        use_open_region=hfss_info.use_open_region,
        extent_type=hfss_info.extent_type.value,
        open_region_type=hfss_info.open_region_type.value,
        base_polygon=edb_obj_message(hfss_info.base_polygon),
        dielectric_extent_type=hfss_info.dielectric_extent_type.value,
        dielectric_base_polygon=edb_obj_message(hfss_info.dielectric_base_polygon),
        dielectric=hfss_extent_message(hfss_info.dielectric),
        honor_user_dielectric=hfss_info.honor_user_dielectric,
        airbox_truncate_at_ground=hfss_info.airbox_truncate_at_ground,
        airbox_horizontal=hfss_extent_message(hfss_info.airbox_horizontal),
        airbox_vertical_positive=hfss_extent_message(hfss_info.airbox_vertical_positive),
        airbox_vertical_negative=hfss_extent_message(hfss_info.airbox_vertical_negative),
        sync_airbox_vertical_extent=hfss_info.sync_airbox_vertical_extent,
        is_pml_visible=hfss_info.is_pml_visible,
        operating_frequency=value_message(hfss_info.operating_frequency),
        radiation_level=value_message(hfss_info.radiation_level),
        user_xy_data_extent_for_vertical_expansion=hfss_info.user_xy_data_extent_for_vertical_expansion,
    )


def design_mode_property_message(target, mode):
    """Convert to a ``DesignModePropertyMessage`` object."""
    return DesignModePropertyMessage(target=target.msg, mode=mode.value)


def cell_find_message(database, cell_type, cell_name=None, cell_id=None):
    """Convert to a ``CellFindMessage`` object."""
    if cell_name is not None:
        return CellFindMessage(database=database.msg, type=cell_type.value, name=cell_name)
    elif cell_id is not None:
        return CellFindMessage(database=database.msg, type=cell_type.value, id=cell_id)
    else:
        assert False, "Either name or ID must be provided to find a cell."


def cell_cutout_message(cell, included_nets, clipped_nets, clipping_polygon, clean_clipping):
    """Convert to a ``CellCutOutMessage`` object."""
    return CellCutOutMessage(
        cell=cell.msg,
        included_nets=edb_obj_collection_message(included_nets),
        clipped_nets=edb_obj_collection_message(clipped_nets),
        clipping_polygon=polygon_data_message(clipping_polygon),
        clean_clipping=clean_clipping,
    )


def cell_set_temperature_settings_message(cell, temp_settings):
    """Convert to a ``CellSetTemperatureSettingsMessage`` object."""
    return CellSetTemperatureSettingsMessage(
        cell=cell.msg, temp_settings=temperature_settings_message(temp_settings)
    )


def point_term_params_message(layer, point):
    """Convert to a ``PointTermParamMessage`` object."""
    return PointTermParamsMessage(point=point_message(point), layer=layer_ref_message(layer))


def point_term_set_params_message(term, layer, point):
    """Convert to a ``PointTermSetParamsMessage`` object."""
    return PointTermSetParamsMessage(term=term.msg, params=point_term_params_message(layer, point))


def point_term_creation_message(layout, net, layer, name, point):
    """Convert to a ``PointTermCreationMessage`` object."""
    return PointTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net),
        name=name,
        params=point_term_params_message(layer, point),
    )


def padstack_inst_term_params_message(padstack_instance, layer):
    """Convert to a ``PadstackInstTermParamsMessage`` object."""
    return PadstackInstTermParamsMessage(
        padstack_instance=padstack_instance.msg, layer=layer_ref_message(layer)
    )


def padstack_inst_term_creation_message(layout, name, padstack_instance, layer, net, is_ref):
    """Convert to a ``PadstackInstTermCreationMessage`` object."""
    return PadstackInstTermCreationsMessage(
        layout=layout.msg,
        name=name,
        params=padstack_inst_term_params_message(padstack_instance, layer),
        net=net_ref_message(net),
        is_ref=is_ref,
    )


def padstack_inst_term_set_params_message(term, padstack_instance, layer):
    """Convert to a ``PadstackInstTermSetParamsMessage`` object."""
    return PadstackInstTermSetParamsMessage(
        term=term.msg, params=padstack_inst_term_params_message(padstack_instance, layer)
    )


def pin_group_creation_message(layout, name, padstack_instances):
    """Convert to a ``PinGroupCreationMessage`` object."""
    return PinGroupCreationMessage(
        layout=layout.msg, name=name, pins=[pi.msg for pi in padstack_instances]
    )


def pin_group_lookup_message(layout, name):
    """Convert to a ``PinGroupLookupMessage`` object."""
    return PinGroupLookupMessage(layout=layout.msg, name=name)


def pin_group_get_unique_name_message(layout, prefix):
    """Convert to a ``PinGroupGetUniqueNameMessage`` object."""
    return PinGroupGetUniqueNameMessage(layout=layout.msg, prefix=prefix)


def pin_group_pins_modify_message(pin_group, padstack_instances):
    """Convert to a ``PinGroupPinsModifyMessage`` object."""
    return PinGroupPinsModifyMessage(
        pin_group=pin_group.msg, pins=[pi.msg for pi in padstack_instances]
    )


def pin_group_term_creation_message(layout, net_ref, name, pin_group, is_ref):
    """Convert to a ``PinGroupTermCreationMessage`` object."""
    return PinGroupTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net_ref),
        name=name,
        pin_group=pin_group.msg,
        is_ref=is_ref,
    )


def pin_group_term_set_pin_group_message(term, pin_group):
    """Convert to a ``PinGroupTermSetPinGroupMessage`` object."""
    return PinGroupTermSetPinGroupMessage(term=term.msg, pin_group=pin_group.msg)


def pin_group_term_set_layer_message(term, layer_ref):
    """Convert to a ``PinGroupTermSetLayerMessage`` object."""
    return PinGroupTermSetLayerMessage(term=term.msg, layer=layer_ref_message(layer_ref))


def edge_creation_message(edge_type, **params):
    """Convert to an ``EdgeCreationMessage`` object."""
    return EdgeCreationMessage(edge_type=edge_type, params=edge_params_message(edge_type, **params))


def edge_params_message(edge_type, **params):
    """Convert to an ``EdgeParamsMessage`` object."""
    if edge_type == EdgeType.PRIMITIVE_EDGE:
        return EdgeParamsMessage(primitve_params=primitive_edge_params_message(**params))
    elif edge_type == EdgeType.PAD_EDGE:
        return EdgeParamsMessage(pad_params=pad_edge_params_message(**params))
    else:
        raise RuntimeError(f"Edge type {edge_type} is not valid.")


def primitive_edge_params_message(primitive, point):
    """Convert to a ``PrimitiveEdgeParamsMessage`` object."""
    return PrimitiveEdgeParamsMessage(primitive=primitive.msg, point=point_message(point))


def pad_edge_params_message(padstack_instance, layer, arc):
    """Convert to a ``PadEdgeParamsMessage`` object."""
    return PadEdgeParamsMessage(
        padstack_instance=padstack_instance.msg,
        layer=layer_ref_message(layer),
        arc=arc_message(arc),
    )


def edge_term_creation_message(layout, net, name, edges, is_ref):
    """Convert to an ``EdgeTermCreationMessage`` object."""
    return EdgeTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net),
        name=name,
        edges=[edge.msg for edge in edges],
        is_ref=is_ref,
    )


def edge_term_set_edges_message(terminal, edges):
    """Convert to an ``EdgeTermSetEdgesMessage`` object."""
    return EdgeTermSetEdgesMessage(term=terminal.msg, edges=[edge.msg for edge in edges])


def term_set_params_message(term, **params):
    """Convert to a ``TermSetParamsMessage`` object."""
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
    """Convert to a ``TermSetRefMessage`` object."""
    if len(term_params) and len(layer_params):
        raise RuntimeError("Can only reference either a terminal or a layer.")
    if len(term_params) == 1:
        return TermSetRefMessage(ref_term=edb_obj_message(*term_params))
    if len(layer_params):
        return TermSetRefMessage(ref_layer=term_set_layer_message(*layer_params))


def term_set_layer_message(layer_ref, contexts=None):
    """Convert to a ``TermSetLayerMessage`` object."""
    contexts = [] if contexts is None else contexts
    return TermSetLayerMessage(
        layer=layer_ref_message(layer_ref), contexts=[str_message(ctx) for ctx in contexts]
    )


def term_find_by_name_message(layout, name):
    """Convert to a ``TermFindByNameMessage`` object."""
    return TermFindByNameMessage(layout=layout.msg, name=name)


def term_get_product_solver_message(term, product_id):
    """Convert to a ``TermGetProductSolversMessage`` object."""
    return TermGetProductSolversMessage(term=term.msg, product_id=product_id.value)


def term_set_solver_option_message(term, product_id, name, option):
    """Convert to a ``TermSetSolverOptionMessage`` object."""
    return TermSetSolverOptionMessage(
        term=term.msg, product_id=product_id.value, name=name, option=option
    )


def term_inst_creation_message(layout, net_ref, cell_inst, name):
    """Convert to a ``TermInstCreationMessage`` object."""
    return TermInstCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net_ref),
        cell_inst=cell_inst.msg,
        name=name,
    )


def term_inst_term_creation_message(layout, net_ref, name, term_inst, is_ref):
    """Convert to a ``TermInstTermCreationMessage`` object."""
    return TermInstTermCreationMessage(
        layout=layout.msg,
        net=net_ref_message(net_ref),
        name=name,
        term_inst=term_inst.msg,
        is_ref=is_ref,
    )


def term_inst_term_set_instance_message(term, term_inst):
    """Convert to a ``TermInstTermSetInstanceMessage`` object."""
    return TermInstTermSetInstanceMessage(term=term.msg, term_inst=term_inst.msg)


def edb_obj_message(obj):
    """Convert to an ``EDBObjMessage`` object."""
    if obj is None:
        return None
    elif isinstance(obj, EDBObjMessage):
        return obj
    elif isinstance(obj, int):
        return EDBObjMessage(id=obj)
    else:
        return obj.msg


def edb_obj_collection_message(objs):
    """Convert to an ``EDBObjCollectionMessage``object."""
    return EDBObjCollectionMessage(items=[edb_obj_message(obj) for obj in objs])


def rlc_message(rlc):
    """Convert to an ``RlcMessage`` object."""
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
    """Convert to a ``PortPostProcessingPropMessage`` object."""
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
    """Convert to a ``MaterialDefPropertiesMessage`` object."""
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
    """Convert to a ``LayerRefMessage`` object."""
    if layer is None:
        return None
    elif type(layer) == str:
        return LayerRefMessage(name=str_message(layer))
    else:
        return LayerRefMessage(id=edb_obj_message(layer.msg))


def net_ref_message(net):
    """Convert to a ``NetRefMessage`` object."""
    if type(net) == str:
        return NetRefMessage(name=str_message(net))
    else:
        return NetRefMessage(id=edb_obj_message(net.msg if net is not None else 0))


def adaptive_frequency_message(frequency: str, max_delta_s: float, max_passes: int):
    """Convert to an ``AdaptiveFrequencyDataMessage`` object."""
    return AdaptiveFrequencyDataMessage(
        adaptive_frequency=frequency, max_delta=str(max_delta_s), max_passes=max_passes
    )


def _length_mesh_operation_message(mesh_op):
    return LengthMeshOperationMessage(
        max_length=mesh_op.max_length,
        restrict_length=mesh_op.restrict_max_length,
        max_elements=mesh_op.max_elements,
        restrict_max_elements=mesh_op.restrict_max_elements,
    )


def _mesh_op_skin_depth_message(mesh_op):
    return SkinDepthMeshOperationMessage(
        skin_depth=mesh_op.skin_depth,
        surface_triangle_length=mesh_op.surface_triangle_length,
        num_layers=mesh_op.number_of_layers,
        max_elements=mesh_op.max_elements,
        restrict_max_elements=mesh_op.restrict_max_elements,
    )


def mesh_operation_message(mesh_op):
    """Convert to a ``MeshOperationMessage`` object."""
    mesh_op_msg = MeshOperationMessage(
        name=mesh_op.name,
        enabled=mesh_op.enabled,
        refine_inside=mesh_op.refine_inside,
        mesh_region=mesh_op.mesh_region,
        net_layer_info=[_mesh_op_net_layer_message(*nl) for nl in mesh_op.net_layer_info],
        solve_inside=mesh_op.solve_inside,
    )
    if isinstance(mesh_op, LengthMeshOperation):
        mesh_op_msg.length_mesh_op.CopyFrom(_length_mesh_operation_message(mesh_op))
    elif isinstance(mesh_op, SkinDepthMeshOperation):
        mesh_op_msg.skin_depth_mesh_op.CopyFrom(_mesh_op_skin_depth_message(mesh_op))
    return mesh_op_msg


def _mesh_op_net_layer_message(net, layer, is_sheet):
    return MeshOpNetLayerInfoMessage(net=net, layer=layer, is_sheet=is_sheet)


def value_message(val):
    """Convert data into a ``ValueMessage`` object.

    Parameters
    ----------
    val : str, int, float, complex, ansys.edb.core.utility.value.Value, ValueMessage

    Returns
    -------
    ValueMessage
    """
    if isinstance(val, value.Value):
        return val.msg
    if isinstance(val, ValueMessage):
        return val

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
        raise TypeError(f"Invalid Value. Received {val}")
    return msg


def product_property_id_message(prod_id, att_id):
    """Convert to a ``ProductPropertyIdMessage`` object."""
    return ProductPropertyIdMessage(product_id=prod_id.value, attribute_id=att_id)


def set_product_property_message(obj, prod_id, att_id, value):
    """Convert to a ``SetProductPropertyMessage`` object."""
    return SetProductPropertyMessage(
        edb_obj=obj.msg,
        product_prop_id=product_property_id_message(prod_id, att_id),
        property_value=value,
    )


def get_product_property_message(obj, prod_id, att_id):
    """Convert to a ``GetProductPropertyMessage`` object."""
    return GetProductPropertyMessage(
        edb_obj=obj.msg, product_prop_id=product_property_id_message(prod_id, att_id)
    )


def get_product_property_ids_message(obj, prod_id):
    """Convert to a ``GetProductPropertyIdsMessage`` object."""
    return GetProductPropertyIdsMessage(edb_obj=obj.msg, product_id=prod_id.value)


def edb_internal_id_message(id):
    """Convert to an ``EDBInternalIdMessage`` object."""
    return EDBInternalIdMessage(id=id)


def component_group_create_message(layout, name, comp_name):
    """Convert to a ``ComponentGroupCreateMessage`` object."""
    return ComponentGroupCreateMessage(
        target=object_name_in_layout_message(layout, name), comp=comp_name
    )


def set_component_group_type_message(obj, comp_type):
    """Convert to a ``SetComponentGroupTypeMessage`` object."""
    return SetComponentGroupTypeMessage(
        target=obj.msg, comp_type=ComponentTypeMessage(comp_type=comp_type.value)
    )


def set_closure_message(obj, closure_type):
    """Convert to a ``SetClosureMessage`` object."""
    return SetClosureMessage(
        target=obj.msg, closure_type=ClosureMessage(closure_type=closure_type.value)
    )


def strings_message(strings):
    """Convert to a ``StringsMessage`` object."""
    return StringsMessage(strings=strings)


def strings_property_message(target, value):
    """Convert to a ``StringPropertyMessage`` object."""
    return StringsPropertyMessage(edb_obj=target.msg, strings=value)


def edb_obj_pair_message(edb_obj_0, edb_obj_1):
    """Convert to an ``EDBObjPairMessage`` object."""
    return EDBObjPairMessage(edb_obj_0=edb_obj_0.msg, edb_obj_1=edb_obj_1.msg)


def layer_ref_property_message(edb_obj, layer_ref):
    """Convert to a ``LayerRefPropertyMessage`` object."""
    return LayerRefPropertyMessage(edb_obj=edb_obj.msg, layer_ref=layer_ref_message(layer_ref))


def double_property_message(edb_obj, double):
    """Convert to a ``DoublePropertyMessage`` object."""
    return DoublePropertyMessage(target=edb_obj.msg, value=double)


def net_get_layout_obj_message(obj, layout_obj_type):
    """Convert to a ``NetGetLayoutObjMessage`` object."""
    return NetGetLayoutObjMessage(net=edb_obj_message(obj), obj_type=layout_obj_type.value)


def differential_pair_creation_message(layout, name, pos_net, neg_net):
    """Convert to a ``DifferentialPairCreationMessage`` object."""
    return DifferentialPairCreationMessage(
        layout=edb_obj_message(layout),
        name=name,
        pos_net=net_ref_message(pos_net),
        neg_net=net_ref_message(neg_net),
    )


def differential_pair_net_refs_message(dp, pos_net, neg_net):
    """Convert to a ``DifferentialPairNetRefsMessage`` object."""
    return DifferentialPairNetRefsMessage(
        dp=edb_obj_message(dp), pos_net=net_ref_message(pos_net), neg_net=net_ref_message(neg_net)
    )


def mcad_model_creation_message(connectable, layout, filename):
    """Convert to an ``McadModelCreationMessage`` object."""
    if connectable is not None:
        param = McadModelCreationMessage.WithConnObj(obj=edb_obj_message(connectable))
        return McadModelCreationMessage(conn_obj=param)
    elif layout is not None and filename is not None and len(filename) > 0:
        param = McadModelCreationMessage.WithLayout(obj=edb_obj_message(layout), file_name=filename)
        return McadModelCreationMessage(layout=param)
    else:
        raise TypeError("Either a connectable object or layout and filename must be provided.")


def mcad_model_hfss_creation_message(connectable, layout, filename, design):
    """Convert to an ``McadModelHfssCreationMessage`` object."""
    if connectable is not None:
        param = McadModelHfssCreationMessage.WithConnObj(obj=edb_obj_message(connectable))
        return McadModelCreationMessage(conn_obj=param)
    elif layout is not None and filename is not None and len(filename) > 0 and len(design) > 0:
        param = McadModelHfssCreationMessage.WithLayout(
            obj=edb_obj_message(layout), file_name=filename, design=design
        )
        return McadModelCreationMessage(layout=param)
    else:
        raise TypeError(
            "Either a connectable object or layout, filename, and design must be provided."
        )


def mcad_model_rotation_message(axis_from, axis_to, angle):
    """Convert to an ``McadModelRotationMessage`` object."""
    return McadModelRotationMessage(
        axis_from=point3d_message(axis_from), axis_to=point3d_message(axis_to), angle=angle
    )


def mcad_model_set_rotation_message(mcad_model, axis_from, axis_to, angle):
    """Convert to an ``McadModelSetRotationMessage`` object."""
    return McadModelSetRotationMessage(
        model=edb_obj_message(mcad_model),
        rotation=mcad_model_rotation_message(axis_from, axis_to, angle),
    )


def mcad_model_bool_message(mcad_model, index, value):
    """Convert to an ``McadModelBoolMessage`` object."""
    return McadModelBoolMessage(model=edb_obj_message(mcad_model), index=index, value=value)


def mcad_model_string_message(mcad_model, index, value):
    """Convert to an ``McadModelStringMessage`` object."""
    return McadModelStringMessage(model=edb_obj_message(mcad_model), index=index, value=value)


def set_die_type_message(obj, die_type):
    """Convert to a ``DieTypePropertyMessage`` object."""
    return DieTypePropertyMessage(target=obj.msg, die_type=DieTypeMessage(die_type=die_type.value))


def set_die_orientation_message(obj, die_orientation):
    """Convert to a ``DieOrientationPropertyMessage`` object."""
    return DieOrientationPropertyMessage(
        target=obj.msg, die_orientation=DieOrientationMessage(die_orientation=die_orientation.value)
    )


def value_pair_message(val1, val2):
    """Convert to a ``ValuePairMessage`` object."""
    return ValuePairMessage(val1=value_message(val1), val2=value_message(val2))


def value_pair_property_message(target, val1, val2):
    """Convert to a ``ValuePairPropertyMessage`` object."""
    return ValuePairPropertyMessage(
        target=edb_obj_message(target), values=value_pair_message(val1, val2)
    )


def points_message(points):
    """Convert to a ``PointsMessage`` object."""
    return PointsMessage(points=[point_message(point) for point in points])


def points_property_message(target, points):
    """Convert to a ``PointsPropertyMessage`` object."""
    return PointsPropertyMessage(
        target=edb_obj_message(target), points=[point_message(point) for point in points]
    )


def polygon_data_property_message(obj, polygon):
    """Convert to a ``PolygonDataPropertyMessage`` object."""
    return PolygonDataPropertyMessage(target=obj.msg, value=polygon_data_message(polygon))


def heat_sink_message(heat_sink):
    """Convert to a ``HeatSinkMessage`` object."""
    return HeatSinkMessage(
        thickness=value_message(heat_sink.fin_thickness),
        spacing=value_message(heat_sink.fin_spacing),
        base_height=value_message(heat_sink.fin_base_height),
        height=value_message(heat_sink.fin_height),
        orientation=heat_sink.fin_orientation.value,
    )


def set_heat_sink_message(target, heat_sink):
    """Convert to a ``SetHeatSinkMessage`` object."""
    return SetHeatSinkMessage(target=edb_obj_message(target), value=heat_sink_message(heat_sink))


def pin_pair_model_rlc_message(model, pin_pair, rlc):
    """Convert to a ``PinPairModelRlcPropertyMessage`` object."""
    return PinPairModelRlcPropertyMessage(
        model=edb_obj_message(model), pins=str_pair_message(pin_pair), rlc=rlc_message(rlc)
    )


def point_pair_message(point_pair):
    """Convert to a ``PointPairMessage`` object."""
    return PointPairMessage(
        point_0=point_message(point_pair[0]), point_1=point_message(point_pair[1])
    )


def sparameter_model_message(name, ref_net):
    """Convert to a ``SParameterModelMessage`` object."""
    return SParameterModelMessage(name=name, ref_net=ref_net)


def power_module_message(power_module):
    """Convert to a ``PowerModuleMessage`` object."""
    return PowerModuleMessage(
        comp_group_name=power_module.comp_group_name,
        pos_output_terminal=power_module.pos_output_terminal,
        neg_output_terminal=power_module.neg_output_terminal,
        relative_strength=value_message(power_module.relative_strength),
        active=power_module.active,
        needs_sync=power_module.needs_sync,
    )


def point_pair_property_message(target, point_pair):
    """Convert to a ``PointPairPropertyMessage`` object."""
    return PointPairPropertyMessage(
        target=edb_obj_message(target), point_pair=point_pair_message(point_pair)
    )


def spice_model_message(name, path, sub_circuit):
    """Convert to a ``SpiceModelMessage`` object."""
    return SpiceModelMessage(name=name, path=path, sub_ckt=sub_circuit)


def spice_model_net_terminal_pin_message(model, terminal, pin):
    """Convert to a ``SpiceModelNewTerminalPinMessage`` object."""
    return SpiceModelNewTerminalPinMessage(
        target=edb_obj_message(model), terminal=terminal, pin=pin
    )


def doubles_message(doubles):
    """Convert to a ``DoublesMessage`` object."""
    return DoublesMessage(doubles=doubles)


def doubles_property_message(edb_obj, doubles):
    """Convert to a ``DoublesPropertyMessage`` object."""
    return DoublesPropertyMessage(edb_obj=edb_obj_message(edb_obj), doubles=doubles)


def cpos_3d_message(point3d):
    """Convert to a ``CPos3DMessage`` object."""
    if point3d is None:
        return None
    else:
        point3d_converted = conversions.to_point3d(point3d)
        x, y, z = point3d_converted.x.double, point3d_converted.y.double, point3d_converted.z.double
        return CPos3DMessage(x=x, y=y, z=z)


def cpos_3d_property_message(target, value):
    """Convert to a ``CPos3DPropertyMessage`` object."""
    return CPos3DPropertyMessage(target=edb_obj_message(target), value=cpos_3d_message(value))


def cpos_3d_pair_message(x, y):
    """Convert to a ``CPos3DPairMessage`` object."""
    return CPos3DPairMessage(x=cpos_3d_message(x), y=cpos_3d_message(y))


def cpos_3d_triple_message(x, y, z):
    """Convert to a ``CPos3DTripleMessage`` object."""
    return CPos3DTripleMessage(x=cpos_3d_message(x), y=cpos_3d_message(y), z=cpos_3d_message(z))


def cpos_3d_double_message(pos, value):
    """Convert to a ``CPos3DDoubleMessage`` object."""
    return CPos3DDoubleMessage(pos=cpos_3d_message(pos), value=value)


def mx_convergence_entry_msg_list(mx_convergence_entry_list):
    """Convert to a list ``of MatrixConvergenceEntryMessage`` objects."""
    mx_entry_msgs = []
    for mx_entry in mx_convergence_entry_list:
        mx_entry_msgs.append(
            MatrixConvergenceEntryMessage(
                port_1=mx_entry.port_1_name,
                port_2=mx_entry.port_2_name,
                mag_limit=mx_entry.mag_limit,
                phase_limit=mx_entry.phase_limit,
            )
        )
    return mx_entry_msgs


def mx_convergence_data_msg(mx_data):
    """Convert to MatrixConvergenceDataMessage."""
    return MatrixConvergenceDataMessage(
        all_are_constant=mx_data.all_constant,
        all_diag_are_constant=mx_data.all_diag_constant,
        all_off_diag_are_constant=mx_data.all_off_diag_constant,
        mag_min_threashold=mx_data.mag_min_threshold,
        entries=mx_convergence_entry_msg_list(mx_data.entry_list),
    )


def base_adaptive_frequency_solution_msg(adaptive_frequency, max_delta):
    """Convert to an ``AdaptiveFrequencyDataMessage`` object."""
    return AdaptiveFrequencyDataMessage(adaptive_frequency=adaptive_frequency, max_delta=max_delta)


def single_frequency_adaptive_solution_msg(single_freq_adapt_sol):
    """Convert to a ``SingleFrequencyAdaptiveSolutionMessage`` object."""
    return SingleFrequencyAdaptiveSolutionMessage(
        adaptive_frequency=base_adaptive_frequency_solution_msg(
            single_freq_adapt_sol.adaptive_frequency, single_freq_adapt_sol.max_delta
        ),
        max_passes=single_freq_adapt_sol.max_passes,
        matrix_conv_data=mx_convergence_data_msg(single_freq_adapt_sol.mx_conv_data),
        use_matrix_conv_data=single_freq_adapt_sol.use_mx_conv_data,
    )


def multi_adaptive_freq_to_msg(multi_adaptive_freq):
    """Convert to an ``AdaptiveMultiFrequencyDataMessage`` object."""
    return AdaptiveMultiFrequencyDataMessage(
        adaptive_frequency=base_adaptive_frequency_solution_msg(
            multi_adaptive_freq.adaptive_frequency, multi_adaptive_freq.max_delta
        ),
        output_variables=multi_adaptive_freq.output_variables,
    )


def multi_frequency_adaptive_solution_msg(multi_freq_adapt_sol):
    """Convert to a ``MultiFrequencyAdaptiveSolutionMessage`` object."""
    return MultiFrequencyAdaptiveSolutionMessage(
        adaptive_frequencies=[
            multi_adaptive_freq_to_msg(multi_adaptive_freq)
            for multi_adaptive_freq in multi_freq_adapt_sol.adaptive_frequencies
        ],
        max_passes=multi_freq_adapt_sol.max_passes,
    )


def broadband_solution_msg(broadband_adapt_sol):
    """Convert to a ``BroadbandFrequencyAdaptiveSolutionMessage`` object."""
    return BroadbandFrequencyAdaptiveSolutionMessage(
        max_delta=broadband_adapt_sol.max_delta,
        max_passes=broadband_adapt_sol.max_num_passes,
        low_frequency=broadband_adapt_sol.low_frequency,
        high_frequency=broadband_adapt_sol.high_frequency,
    )


def _as_array(array_or_item):
    try:
        iter(array_or_item)
        return array_or_item
    except TypeError:
        return [array_or_item]
