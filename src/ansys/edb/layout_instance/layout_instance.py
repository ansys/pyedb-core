"""Layout Instance."""
import ansys.api.edb.v1.layout_instance_pb2 as layout_instance_pb2

from ansys.edb.core import ObjBase, utils
from ansys.edb.core.messages import (
    layer_ref_message,
    net_ref_message,
    point_message,
    points_message,
    strings_message,
)
from ansys.edb.geometry import PointData
from ansys.edb.layout_instance.layout_obj_instance import LayoutObjInstance
from ansys.edb.session import LayoutInstanceServiceStub, StubAccessor, StubType


class LayoutInstance(ObjBase):
    """Class representing layout instance object."""

    __stub: LayoutInstanceServiceStub = StubAccessor(StubType.layout_instance)

    def refresh(self):
        """Refresh the layout instance so it contains up to date geometry."""
        self.__stub.Refresh(self.msg)

    def query_layout_obj_instances(self, layer_filter=None, net_filter=None, spatial_filter=None):
        """Query the layout object instances allowed by the given filters.

        Parameters
        ----------
        layer_filter : list[ansys.edb.layer.Layer or str]
        net_filter : list[ansys.edb.net.Net or str]
        spatial_filter : ansys.edb.geometry.PolygonData or PointData or
            ansys.edb.typinglist[PointLike]

        Returns
        -------
        list[LayoutObjInstance] or tuple[list[LayoutObjInstance], list[LayoutObjInstance]]
            If a polygonal spatial filter is specified, a tuple of lists of layout obj instances is returned of the
            format [<hits_completely_enclosed_in_polygon_region>, <hits_partially_enclosed_in_polygon_region>].
            Otherwise, a list containing all hits is returned.
        """

        def to_msg_filter_list(client_filter, ref_msg_type):
            return (
                utils.map_list(client_filter, ref_msg_type) if client_filter is not None else None
            )

        msg_params = {
            "layout_inst": self.msg,
            "layer_filter": to_msg_filter_list(layer_filter, layer_ref_message),
            "net_filter": to_msg_filter_list(net_filter, net_ref_message),
        }
        if spatial_filter is not None:
            is_point_filter = isinstance(spatial_filter, PointData)
            spatial_filter_field = "point_filter" if is_point_filter else "region_filter"
            spatial_filter_msg = (
                point_message(spatial_filter) if is_point_filter else points_message(spatial_filter)
            )
            msg_params[spatial_filter_field] = spatial_filter_msg

        hits = self.__stub.QueryLayoutObjInstances(
            layout_instance_pb2.LayoutObjInstancesQueryMessage(**msg_params)
        )

        if hits.HasField("full_partial_hits"):
            full_partial_hits = hits.full_partial_hits
            return utils.map_list(full_partial_hits.full.items, LayoutObjInstance), utils.map_list(
                full_partial_hits.partial.items, LayoutObjInstance
            )
        else:
            return utils.map_list(hits.hits.items, LayoutObjInstance)

    def get_layout_obj_instance_in_context(self, layout_obj, context):
        """Get the layout obj instance of the given ConnObj in the provided context.

        Parameters
        ----------
        layout_obj : ansys.edb.core.ConnObj
        context : list[str]

        Returns
        -------
        LayoutObjInstance
        """
        return LayoutObjInstance(
            self.__stub.GetLayoutObjInstanceInContext(
                layout_instance_pb2.GetLayoutObjInstanceInContextMessage(
                    layout_inst=self.msg,
                    layout_obj=layout_obj.msg,
                    context=strings_message(context),
                )
            )
        )

    def get_connected_objects(self, origin_layout_obj_inst, touching_only):
        """Get the layout obj instances connected to the origin layout obj instance.

        Parameters
        ----------
        origin_layout_obj_inst : LayoutObjInstance
        touching_only : bool
            If touching_only is true, only layout obj instances touching origin_layout_obj_inst on the placement
            lyr of origin_layout_obj_inst will be returned. Otherwise, all layout obj instances across all layers
            that are electrically connected to origin_layout_obj will be returned.
        Returns
        -------
        list[LayoutObjInstance]
        """
        hits = self.__stub.GetConnectedObjects(
            layout_instance_pb2.GetConnectedObjectsMessage(
                layout_inst=self.msg,
                layout_obj=origin_layout_obj_inst.msg,
                touching_only=touching_only,
            )
        )
        return utils.map_list(hits.items, LayoutObjInstance)
