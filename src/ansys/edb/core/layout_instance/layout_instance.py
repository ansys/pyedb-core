"""Layout instance."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.typing import LayerLike, NetLike

import ansys.api.edb.v1.layout_instance_pb2 as layout_instance_pb2

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData
from ansys.edb.core.inner import ObjBase, utils
from ansys.edb.core.inner.messages import (
    layer_ref_message,
    net_ref_message,
    point_message,
    polygon_data_message,
    strings_message,
)
from ansys.edb.core.inner.utils import client_stream_iterator
from ansys.edb.core.layout_instance import layout_obj_instance
from ansys.edb.core.session import LayoutInstanceServiceStub, StubAccessor, StubType


class LayoutInstance(ObjBase):
    """Represents a layout instance object."""

    __stub: LayoutInstanceServiceStub = StubAccessor(StubType.layout_instance)

    def refresh(self):
        """Refresh the layout instance so it contains an up-to-date geometry."""
        self.__stub.Refresh(self.msg)

    @staticmethod
    def _query_request_iterator(requests):
        chunk_entry_creator = lambda request: request
        chunk_entries_getter = lambda chunk: chunk.queries
        return client_stream_iterator(
            requests,
            layout_instance_pb2.LayoutObjInstancesQueriesMessage,
            chunk_entry_creator,
            chunk_entries_getter,
        )

    def query_layout_obj_instances(
        self,
        layer_filter: LayerLike | list[LayerLike] = None,
        net_filter: NetLike | list[NetLike] = None,
        spatial_filter: PolygonData | PointData | None | list[PolygonData | PointData] = None,
    ):
        """Query layout object instances using the provided filters.

        Parameters
        ----------
        layer_filter : :term:`LayerLike` or list of :term:`LayerLike`, default: None
            Layers to query. The default is ``None``, in which case all layers are queried.
        net_filter : :term:`NetLike` or list of :term:`NetLike`, default: None
            Nets to query. The default is ``None``, in which case all nets are queried.
        spatial_filter : .PolygonData or .PointData or :obj:`None` or \
        list of .PolygonData or .PointData, default: None
            Area of the design to query. The default is :obj:`None`, in which case the entire
            spatial domain of the design is queried.

        Returns
        -------
        :term:`LayoutInstanceQueryResult` or list of :term:`LayoutInstanceQueryResult`
            If a single query is provided, one :term:`LayoutInstanceQueryResult` is returned. If a \
            list of spatial queries is provided, then a list of :term:`LayoutInstanceQueryResult` is \
            returned where each entry maps to the spatial query at the same index.
        """

        def to_msg_filter_list(client_filter, ref_msg_type):
            if client_filter is None:
                return None
            return utils.map_list(utils.ensure_is_list(client_filter), ref_msg_type)

        def spatial_filter_to_msg(_spatial_filter):
            is_point_filter = isinstance(_spatial_filter, PointData)
            spatial_filter_field = "point_filter" if is_point_filter else "region_filter"
            spatial_filter_msg = (
                point_message(_spatial_filter)
                if is_point_filter
                else polygon_data_message(_spatial_filter)
            )
            return layout_instance_pb2.LayoutObjInstancesQueryMessage(
                **{spatial_filter_field: spatial_filter_msg}
            )

        # Create queries
        lyt_inst_net_filter_lyr_filter_params = {
            "layout_inst": self.msg,
            "layer_filter": to_msg_filter_list(layer_filter, layer_ref_message),
            "net_filter": to_msg_filter_list(net_filter, net_ref_message),
        }
        requests = [
            layout_instance_pb2.LayoutObjInstancesQueryMessage(
                **lyt_inst_net_filter_lyr_filter_params
            )
        ]
        has_spatial_filter = spatial_filter is not None
        if has_spatial_filter:
            for sf in utils.ensure_is_list(spatial_filter):
                requests.append(spatial_filter_to_msg(sf))

        all_hits = []
        for hits_chunk in self.__stub.StreamLayoutObjInstancesQuery(
            self._query_request_iterator(requests)
        ):
            for hit in hits_chunk.query_results:
                all_hits.append(hit)

        def process_hits(_spatial_filter, hits_iter):
            full_hits = []
            partial_hits = []
            for hit in hits_iter:
                if hit.is_end_of_query_results_group:
                    break
                lyt_obj_inst = layout_obj_instance.LayoutObjInstance(hit.edb_obj)
                if hit.is_partial:
                    partial_hits.append(lyt_obj_inst)
                else:
                    full_hits.append(lyt_obj_inst)
            return (
                (full_hits, partial_hits) if isinstance(_spatial_filter, PolygonData) else full_hits
            )

        all_hits_iter = iter(all_hits)
        if not has_spatial_filter:
            return process_hits(None, all_hits_iter)
        elif len(spatial_filter) == 1:
            return process_hits(spatial_filter[1], all_hits_iter)
        else:
            return [process_hits(sf, all_hits_iter) for sf in spatial_filter]

    def get_layout_obj_instance_in_context(self, layout_obj, context):
        """Get the layout object instance of the given :term:`connectable <Connectable>` in the provided context.

        Parameters
        ----------
        layout_obj : :term:`Connectable <Connectable>`
            Layout object with the instances to search.
        context : list[str]
            List of strings specifying the :class:`context <.LayoutInstanceContext>` that the /
            layout object instance is retrieved from.

            .. seealso:: :func:`context <ansys.edb.core.layout_instance.layout_obj_instance.LayoutObjInstance.context>`

        Returns
        -------
        :class:`.LayoutObjInstance`
        """
        return layout_obj_instance.LayoutObjInstance(
            self.__stub.GetLayoutObjInstanceInContext(
                layout_instance_pb2.GetLayoutObjInstanceInContextMessage(
                    layout_inst=self.msg,
                    layout_obj=layout_obj.msg,
                    context=strings_message(context),
                )
            )
        )

    def get_connected_objects(self, origin_layout_obj_inst, touching_only):
        """Get the layout object instance connected to the origin layout object instance.

        Parameters
        ----------
        origin_layout_obj_inst : :class:`.LayoutObjInstance`
            Layout object instance that is to act as the origin to get connected objects from.
        touching_only : bool
            Whether to get only layout object instances touching the orgigin layout object instance
            on the placement layer of the origin layout object. If ``False`` all layout object
            instances across all layers that are electrically connected to the origin layout object
            instance are returned.

        Returns
        -------
        list[:class:`.LayoutObjInstance`]
           List of layout object instances connected to the origin layout object instance.
        """
        hits = self.__stub.GetConnectedObjects(
            layout_instance_pb2.GetConnectedObjectsMessage(
                layout_inst=self.msg,
                layout_obj=origin_layout_obj_inst.msg,
                touching_only=touching_only,
            )
        )
        return utils.map_list(hits.items, layout_obj_instance.LayoutObjInstance)
