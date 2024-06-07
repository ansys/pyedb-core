"""Layout object instance."""

from ansys.edb.core.inner import ObjBase, factory, parser, utils
from ansys.edb.core.inner.messages import bool_property_message, layer_ref_property_message
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.layout_instance import layout_instance_context
from ansys.edb.core.layout_instance.layout_obj_instance_2d_geometry import (
    LayoutObjInstance2DGeometry,
)
from ansys.edb.core.layout_instance.layout_obj_instance_3d_geometry import (
    LayoutObjInstance3DGeometry,
)
from ansys.edb.core.session import LayoutObjInstanceServiceStub, StubAccessor, StubType


def _parse_layout_obj_instance_geometry_message(lyt_obj_inst_geom_msg):
    if lyt_obj_inst_geom_msg.type == -1:
        raise TypeError("Encountered an unknown geometry type for the layout object instance.")
    geom_type = (
        LayoutObjInstance2DGeometry
        if lyt_obj_inst_geom_msg.type == 0
        else LayoutObjInstance3DGeometry
    )
    geom_msg = lyt_obj_inst_geom_msg.geometry
    return geom_type(geom_msg.geometry, geom_msg.owning_drawing, geom_msg.placement_layer)


class LayoutObjInstance(ObjBase):
    """Represents a layout object instance."""

    __stub: LayoutObjInstanceServiceStub = StubAccessor(StubType.layout_obj_instance)

    @property
    def layers(self):
        """:obj:`list` of :class:`.Layer`: All layer instances.

        This list contains the layer` instances that the layout object instance has geometry on.
        """
        return [Layer(msg).cast() for msg in self.__stub.GetLayers(self.msg).items]

    def get_geometries(self, layer):
        """Get the geometry that exists on a given layer.

        Parameters
        ----------
        layer : :class:`.Layer` or str
           Layer.

        Returns
        -------
        list[LayoutObjInstance2DGeometry or LayoutObjInstance3DGeometry]
        """
        geoms = self.__stub.GetGeometries(layer_ref_property_message(self, layer))
        return utils.map_list(geoms.geometries, _parse_layout_obj_instance_geometry_message)

    @property
    def context(self):
        r""":obj:`list`\[:obj:`str`\]: All strings representing the context of the layout object instance.

        This list of strings is a list of :class:`.CellInstance`
        names representing the hierarchy level this layout obj instance's :class:`context <.LayoutInstanceContext>`
        resides on. The first entry represents the top-level context and the last entry represents
        the context that the layout object instance exists in.

        This property is read-only.
        """
        return utils.map_list(self.__stub.GetContext(self.msg).strings)

    @property
    def layout_instance_context(self):
        """:class:`LayoutInstanceContext`: Context that the layout object instance exists in.

        This property is read-only.
        """
        return layout_instance_context.LayoutInstanceContext(
            self.__stub.GetLayoutInstanceContext(self.msg)
        )

    @property
    def layout_obj(self):
        """:term:`Connectable <Connectable>`: Definition layout object that the layout object \
        instance is an instance of.

        This property is read-only.
        """
        return factory.create_conn_obj(self.__stub.GetLayoutObj(self.msg))

    @parser.to_polygon_data
    def get_bbox(self, local=False):
        """Get the bounding box of the layout object instance.

        Parameters
        ----------
        local : bool
            Whether to return the bounding box in the local :class:`context <.LayoutInstanceContext>`.
            If ``False``, the bounding box is returned in the global context.

        Returns
        -------
        :class:`.PolygonData`
            Bounding box of the layout object instance.
        """
        return self.__stub.GetBBox(bool_property_message(self, local))
