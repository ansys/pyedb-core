"""This module parses messages back to client data types."""

import functools

from ansys.edb.core.simulation_setup.adaptive_solutions import (
    AdaptiveFrequency,
    BroadbandAdaptiveSolution,
    MatrixConvergenceData,
    MultiFrequencyAdaptiveSolution,
    SingleFrequencyAdaptiveSolution,
)
from ansys.edb.core.simulation_setup.mesh_operation import (
    LengthMeshOperation,
    SkinDepthMeshOperation,
)


def to_point_data(fn):
    """Decorate a function that returns a message to return it as a ``PointData`` object."""
    return _wraps(fn, _to_point_data)


def to_point_data_list(fn):
    """Decorate a function that returns a message to return it as a list of ``PointData`` objects."""
    return _wraps(fn, _to_point_data_list)


def to_point3d_data(fn):
    """Decorate a function that returns a message to return it as a ``Point3DData`` object."""
    return _wraps(fn, _to_point3d_data)


def to_point_data_pair(fn):
    """Decorate a function that returns a message to return it as a ``[PointData, PointData]`` tuple."""
    return _wraps(fn, _to_point_data_pair)


def to_3_point3d_data(fn):
    """Decorate a function that returns a message to return it as a list of ``Point3DData`` objects."""
    return _wraps(fn, _to_3_point3d_data)


def to_polygon_data(fn):
    """Decorate a function that returns a message to return it as a ``PolygonData`` object."""
    return _wraps(fn, _to_polygon_data)


def to_polygon_data_list(fn):
    """Decorate a function that returns a message to return it as a list of ``PolygonData`` objects."""
    return _wraps(fn, _to_polygon_data_list)


def to_rlc(fn):
    """Decorate a function that returns a message to return it as an RLC."""
    return _wraps(fn, _to_rlc)


def to_box(fn):
    """Decorate a function that returns a message to return it as ``(lower_left, upper_right)``."""
    return _wraps(fn, _to_box)


def to_circle(fn):
    """Decorate a function that returns a message to return it as ``(center, radius)``."""
    return _wraps(fn, _to_circle)


def to_base_adaptive_frequency_solution(fn):
    """Decorate a function that returns a message to return it as a ``[`str`, `str`]`` tuple."""
    return _wraps(fn, _to_base_adaptive_frequency_solution)


def to_single_frequency_adaptive_solution(fn):
    """Decorate a function that returns a message to return it as a ``SingleFrequencyAdaptiveSolution`` object."""
    return _wraps(fn, _to_single_frequency_adaptive_solution)


def to_multi_adaptive_freq(fn):
    """Decorate a function that returns a message to return it as an ``AdaptiveFrequency`` object."""
    return _wraps(fn, _to_multi_adaptive_freq)


def to_multi_frequency_adaptive_solution(fn):
    """Decorate a function that returns a message to return it as a ``MultiFrequencyAdaptiveSolution`` object."""
    return _wraps(fn, _to_multi_frequency_adaptive_solution)


def to_broadband_adaptive_solution(fn):
    """Decorate a function that returns a message to return it as a ``BroadbandAdaptiveSolution`` object."""
    return _wraps(fn, _to_broadband_adaptive_solution)


def to_mesh_op(fn):
    """Decorate a function that returns a message to return it as a ``MeshOperation`` object."""
    return _wraps(fn, _to_mesh_op)


def _wraps(fn, wrapper_fn):
    if callable(fn):

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return wrapper_fn(fn(*args, **kwargs))

        return wrapper
    else:
        return wrapper_fn(fn)


def _to_point_data(message):
    """Convert a ``PointMessage`` object to a ``PointData`` object.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.PointMessage

    Returns
    -------
    :class:`.PointData`
    """
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.utility.value import Value

    return PointData([Value(message.x), Value(message.y)])


def _to_point_data_pair(message):
    """Convert a ``PointPairMessage`` object to a ``[PointData, PointData]`` tuple.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.PointPairMessage

    Returns
    -------
    tuple[:class:`.PointData`, :class:`.PointData`]
    """
    return _to_point_data(message.point_0), _to_point_data(message.point_1)


def _to_point_data_list(message):
    """Convert a message to list of ``PointData`` objects.

    Parameters
    ----------
    message : list[ansys.api.edb.v1.point_data_pb2.PointMessage]

    Returns
    -------
    list[:class:`.PointData`]
    """
    return [_to_point_data(m) for m in message]


def _to_3_point3d_data(message):
    """Convert a ``Point3DMessage`` object to a ``PointData`` object.

    Parameters
    ----------
    message : list[ansys.api.edb.v1.point_data_pb2.CPos3DTripleMessage]

    Returns
    -------
    :class:`.Point3DData`
    """
    return [_to_point3d_data(message.x), _to_point3d_data(message.y), _to_point3d_data(message.z)]


def _to_point3d_data(message):
    """Convert a ``Point3DMessage`` object to a ``PointData`` object.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.Point3DMessage

    Returns
    -------
    :class:`.Point3DData`
    """
    from ansys.edb.core.geometry.point3d_data import Point3DData
    from ansys.edb.core.utility.value import Value

    return Point3DData(Value(message.x), Value(message.y), Value(message.z))


def _to_polygon_data(message):
    """Convert an arbitrary message to a ``PolygonData`` object if possible.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.BoxMessage or ansys.api.edb.v1.polygon_data_pb2.PolygonDataMessage

    Returns
    -------
    :class:`.PolygonData`
    """
    from ansys.api.edb.v1.point_data_pb2 import BoxMessage

    from ansys.edb.core.geometry.polygon_data import PolygonData

    if isinstance(message, BoxMessage):
        b = _to_box(message)
        return PolygonData(lower_left=b[0], upper_right=b[1])
    else:
        return PolygonData(
            points=_to_point_data_list(message.points),
            holes=_to_polygon_data_list(message.holes),
            sense=message.sense,
            closed=message.closed,
        )


def _to_polygon_data_list(message):
    """Convert arbitrary messages to list of ``PolygonData`` objects if possible.

    Returns
    -------
    list[:class:`.PolygonData`]
    """
    if hasattr(message, "polygons"):
        return [_to_polygon_data(m) for m in message.polygons]
    elif hasattr(message, "points"):
        return [_to_polygon_data(m) for m in message.points]
    else:
        return [_to_polygon_data(m) for m in message]


def _to_box(message):
    """Convert a message to box.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.BoxMessage

    Returns
    -------
    tuple[:class:`.PointData`, :class:`.PointData`]
    """
    if hasattr(message, "lower_left") and hasattr(message, "upper_right"):
        return _to_point_data(message.lower_left), _to_point_data(message.upper_right)


def _to_circle(message):
    """Convert a message to a circle containing a center point and radius.

    Parameters
    ----------
    message : ansys.api.edb.v1.point_data_pb2.CircleMessage

    Returns
    -------
    tuple[:class:`.PointData`, :class:`.Value`]
    """
    from ansys.edb.core.utility.value import Value

    if hasattr(message, "center") and hasattr(message, "radius"):
        return _to_point_data(message.center), Value(message.radius)


def _to_rlc(message):
    """Convert a message to an RLC containing values related to resistance inductance capacitance.

    Parameters
    ----------
    message : ansys.api.edb.v1.rlc_pb2.RlcMessage

    Returns
    -------
    :class:`.Rlc`
    """
    from ansys.edb.core.utility.rlc import Rlc
    from ansys.edb.core.utility.value import Value

    return Rlc(
        Value(message.r),
        message.r_enabled.value,
        Value(message.l),
        message.l_enabled.value,
        Value(message.c),
        message.c_enabled.value,
        message.is_parallel.value,
    )


def _to_mx_convergence_data(message):
    """Convert a message to matrix convergence data.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_settings_pb2.MatrixConvergenceDataMessage

    Returns
    -------
    MatrixConvergenceData
    """
    mx_entry_msgs = message.entries
    if len(mx_entry_msgs) == 0:
        return

    mx_conv_data = MatrixConvergenceData()
    if (
        message.all_are_constant
        or message.all_diag_are_constant
        or message.all_off_diag_are_constant
    ):
        port_name_set = set()
        port_name_list = []

        def add_port_name_entry(port_name):
            if port_name not in port_name_set:
                port_name_set.add(mx_entry_msg.port_1)
                port_name_list.append(mx_entry_msg.port_1)

        for mx_entry_msg in mx_entry_msgs:
            add_port_name_entry(mx_entry_msg.port_1)
            add_port_name_entry(mx_entry_msg.port_2)

        if message.all_are_constant:
            first_msg = mx_entry_msgs[0]
            mx_conv_data.set_all_constant(
                first_msg.mag_limit, first_msg.phase_limit, port_name_list
            )

        if message.all_diag_are_constant:
            for mx_entry_msg in mx_entry_msgs:
                if mx_entry_msg.port_1 == mx_entry_msg.port_2:
                    mx_conv_data.set_all_diag_constant(
                        mx_entry_msg.mag_limit, mx_entry_msg.phase_limit, port_name_list, True
                    )
                    break

        if message.all_off_diag_are_constant:
            for mx_entry_msg in mx_entry_msgs:
                if mx_entry_msg.port_1 != mx_entry_msg.port_2:
                    mx_conv_data.set_all_off_diag_constant(
                        mx_entry_msg.mag_limit, mx_entry_msg.phase_limit, port_name_list, False
                    )
                    break
    else:
        for mx_entry_msg in mx_entry_msgs:
            mx_conv_data.add_entry(
                mx_entry_msg.port_1,
                mx_entry_msg.port_2,
                mx_entry_msg.mag_limit,
                mx_entry_msg.phase_limit,
            )

    return mx_conv_data


def _to_base_adaptive_frequency_solution(message):
    """Convert a message to adaptive frequency solution data.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_settings_pb2.AdaptiveFrequencyDataMessage

    Returns
    -------
    tuple[`str`, `str`]
    """
    return message.adaptive_frequency, message.max_delta


def _to_single_frequency_adaptive_solution(message):
    """Convert a message to single frequency adaptive solution data.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_settings_pb2.SingleFrequencyAdaptiveSolutionMessage

    Returns
    -------
    SingleFrequencyAdaptiveSolution
    """
    adaptive_freq_data = _to_base_adaptive_frequency_solution(message.adaptive_frequency)
    return SingleFrequencyAdaptiveSolution(
        adaptive_freq_data[0],
        adaptive_freq_data[1],
        message.max_passes,
        _to_mx_convergence_data(message.matrix_conv_data),
        message.use_matrix_conv_data,
    )


def _to_multi_adaptive_freq(message):
    """Convert a message to a multi-frequency adaptive solution adaptive frequency entry.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_settings_pb2.SingleFrequencyAdaptiveSolutionMessage

    Returns
    -------
    AdaptiveFrequency
    """
    adaptive_freq_data = _to_base_adaptive_frequency_solution(message.adaptive_frequency)
    return AdaptiveFrequency(
        adaptive_freq_data[0],
        adaptive_freq_data[1],
        {key: value for (key, value) in message.output_variables},
    )


def _to_multi_frequency_adaptive_solution(message):
    """Convert a message to a multi-frequency adaptive solution data.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_settings_pb2.MultiFrequencyAdaptiveSolutionMessage

    Returns
    -------
    MultiFrequencyAdaptiveSolution
    """
    return MultiFrequencyAdaptiveSolution(
        message.max_passes,
        [_to_multi_adaptive_freq(freq_msg) for freq_msg in message.adaptive_frequencies],
    )


def _to_broadband_adaptive_solution(message):
    """Convert a message to broadband adaptive solution data.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_settings_pb2.BroadbandFrequencyAdaptiveSolutionMessage

    Returns
    -------
    BroadbandAdaptiveSolution
    """
    return BroadbandAdaptiveSolution(
        message.low_frequency, message.high_frequency, message.max_passes, message.max_delta
    )


def _length_mesh_op(message):
    """Convert a message to a length mesh operation.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_setup_pb2.LengthMeshOperationMessage

    Returns
    -------
    LengthMeshOperation
    """
    return LengthMeshOperation(
        max_length=message.max_length,
        restrict_max_length=message.restrict_length,
        max_elements=message.max_elements,
        restrict_max_elements=message.restrict_max_elements,
    )


def _to_skin_depth_mesh_op(message):
    """Convert a message to a skin depth mesh operation.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_setup_pb2.SkinDepthMeshOperationMessage

    Returns
    -------
    SkinDepthMeshOperation
    """
    return SkinDepthMeshOperation(
        skin_depth=message.skin_depth,
        surface_triangle_length=message.surface_triangle_length,
        num_layers=message.num_layers,
        max_elements=message.max_elements,
        restrict_max_elements=message.restrict_max_elements,
    )


def _to_mesh_op(message):
    """Convert a message to a mesh operation.

    Parameters
    ----------
    message : ansys.api.edb.v1.hfss_simulation_setup_pb2.MeshOperationMessage

    Returns
    -------
    MeshOperation
    """
    mesh_op = None
    if message.HasField("skin_depth_mesh_op"):
        mesh_op = _to_skin_depth_mesh_op(message.skin_depth_mesh_op)
    elif message.HasField("length_mesh_op"):
        mesh_op = _length_mesh_op(message.length_mesh_op)
    mesh_op.name = message.name
    mesh_op.enabled = message.enabled
    mesh_op.mesh_region = message.mesh_region
    mesh_op.refine_inside = message.refine_inside
    mesh_op.solve_inside = message.solve_inside
    for nli in message.net_layer_info:
        mesh_op.net_layer_info.append((nli.net, nli.layer, nli.is_sheet))
    return mesh_op
