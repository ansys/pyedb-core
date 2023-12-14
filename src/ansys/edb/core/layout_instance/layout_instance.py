"""Layout Instance."""
import ansys.api.edb.v1.layout_instance_pb2 as layout_instance_pb2

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.inner.base import ObjBase
from ansys.edb.core.inner.messages import (
    layer_ref_message,
    net_ref_message,
    point_message,
    polygon_data_message,
    strings_message,
)
from ansys.edb.core.inner.utils import map_list
from ansys.edb.core.layout_instance.layout_obj_instance import LayoutObjInstance
from ansys.edb.core.session import LayoutInstanceServiceStub, StubAccessor, StubType


class LayoutInstance(ObjBase):
    """Class representing layout instance object."""

    __stub: LayoutInstanceServiceStub = StubAccessor(StubType.layout_instance)

    def refresh(self):
        """Refresh the layout instance so it contains up to date geometry."""
        self.__stub.Refresh(self.msg)

    def query_layout_obj_instances(self, layer_filter=None, net_filter=None, spatial_filter=None):
        """Query :class:`layout object instances <LayoutObjInstance>` using the provided filters.

        Parameters
        ----------
        layer_filter : list[:class:`Layer <ansys.edb.core.layer.Layer>` or str or None], optional
            Specifies which layers to query. If :obj:`None`, all layers will be queried.
        net_filter : list[:class:`Net <ansys.edb.core.net.Net>` or str or None], optional
            Specifies which nets to query. If :obj:`None`, all nets will be queried.
        spatial_filter : :class:`PolygonData <ansys.edb.core.geometry.PolygonData>` or \
         :class:`PointData <ansys.edb.core.geometry.PointData>` or None, optional
            Specifies which area of the design to query. If :obj:`None`, the entire spatial domain of the design will \
            be queried.

        Returns
        -------
        list[LayoutObjInstance] or tuple[list[LayoutObjInstance], list[LayoutObjInstance]]
            If a polygonal spatial filter is specified, a tuple of lists of hits is returned of the
            format [<hits_completely_enclosed_in_polygon_region>, <hits_partially_enclosed_in_polygon_region>].
            Otherwise, a list containing all hits is returned.
        """

        def to_msg_filter_list(client_filter, ref_msg_type):
            return map_list(client_filter, ref_msg_type) if client_filter is not None else None

        msg_params = {
            "layout_inst": self.msg,
            "layer_filter": to_msg_filter_list(layer_filter, layer_ref_message),
            "net_filter": to_msg_filter_list(net_filter, net_ref_message),
        }
        if spatial_filter is not None:
            is_point_filter = isinstance(spatial_filter, PointData)
            spatial_filter_field = "point_filter" if is_point_filter else "region_filter"
            spatial_filter_msg = (
                point_message(spatial_filter)
                if is_point_filter
                else polygon_data_message(spatial_filter)
            )
            msg_params[spatial_filter_field] = spatial_filter_msg

        hits = self.__stub.QueryLayoutObjInstances(
            layout_instance_pb2.LayoutObjInstancesQueryMessage(**msg_params)
        )

        if hits.HasField("full_partial_hits"):
            full_partial_hits = hits.full_partial_hits
            return map_list(full_partial_hits.full.items, LayoutObjInstance), utils.map_list(
                full_partial_hits.partial.items, LayoutObjInstance
            )
        else:
            return map_list(hits.hits.items, LayoutObjInstance)

    def get_layout_obj_instance_in_context(self, layout_obj, context):
        """Get the :class:`layout object instance <LayoutObjInstance>` of the given :term:`Connectable <Connectable>` \
        in the provided context.

        Parameters
        ----------
        layout_obj : :term:`Connectable <Connectable>`
            Layout object whose instances will be searched for.
        context : list[str]
            list of strings specifying the :class:`context <LayoutInstanceContext>` that the instance of \
            layout_obj will be retrieved from.

            .. seealso:: :func:`LayoutObjInstance.context`

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
        """Get the :class:`layout object instances <LayoutObjInstance>` connected to the origin \
        layout object instance.

        Parameters
        ----------
        origin_layout_obj_inst : LayoutObjInstance
            :class:`layout object instance <LayoutObjInstance>` that will act as the origin to get connected objects \
            from.
        touching_only : bool
            If touching_only is true, only :class:`layout object instances <LayoutObjInstance>` touching \
            origin_layout_obj_inst on the placement :class:`layer <ansys.edb.core.layer.Layer>` of \
            origin_layout_obj_inst will be returned. Otherwise, all layout object instances across all layers that \
            are electrically connected to origin_layout_obj_inst will be returned.

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
        return map_list(hits.items, LayoutObjInstance)
