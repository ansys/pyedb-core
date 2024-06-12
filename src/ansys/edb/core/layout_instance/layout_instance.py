"""Layout instance."""
import ansys.api.edb.v1.layout_instance_pb2 as layout_instance_pb2

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.inner import ObjBase, utils
from ansys.edb.core.inner.messages import (
    layer_ref_message,
    net_ref_message,
    point_message,
    polygon_data_message,
    strings_message,
)
from ansys.edb.core.layout_instance import layout_obj_instance
from ansys.edb.core.session import LayoutInstanceServiceStub, StubAccessor, StubType


class LayoutInstance(ObjBase):
    """Represents a layout instance object."""

    __stub: LayoutInstanceServiceStub = StubAccessor(StubType.layout_instance)

    def refresh(self):
        """Refresh the layout instance so it contains an up-to-date geometry."""
        self.__stub.Refresh(self.msg)

    def query_layout_obj_instances(self, layer_filter=None, net_filter=None, spatial_filter=None):
        """Query layout object instances using the provided filters.

        Parameters
        ----------
        layer_filter : list[:class:`.Layer` or str or None], default: None
            Layers to query. The default is ``None``, in which case all layers are queried.
        net_filter : list[:class:`.Net` or str or None], default: None
            Nets to query. The default is ``None``, in which case all nets are queried.
        spatial_filter : :class:`.PolygonData` or
         :class:`.PointData` or ``None``, default: None
            Area of the design to query. The default is ``None``, in which case the entire
            spatial domain of the design is queried.

        Returns
        -------
        list[:class:`.LayoutObjInstance`] or tuple[list[:class:`.LayoutObjInstance`], list[:class:`.LayoutObjInstance`]]
            If a polygonal spatial filter is specified, a tuple of lists of hits is returned in this
            format: ``[<hits_completely_enclosed_in_polygon_region>, <hits_partially_enclosed_in_polygon_region>]``.
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
            return utils.map_list(
                full_partial_hits.full.items, layout_obj_instance.LayoutObjInstance
            ), utils.map_list(
                full_partial_hits.partial.items, layout_obj_instance.LayoutObjInstance
            )
        else:
            return utils.map_list(hits.hits.items, layout_obj_instance.LayoutObjInstance)

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
