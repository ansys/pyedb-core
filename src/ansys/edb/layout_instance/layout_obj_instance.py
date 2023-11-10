"""Layout Obj Instance."""

from ansys.edb.core import parser, utils
from ansys.edb.core.base import ObjBase
from ansys.edb.core.factory import create_conn_obj
from ansys.edb.core.messages import bool_property_message, layer_ref_property_message
from ansys.edb.layer.layer import Layer
from ansys.edb.layout_instance.layout_instance_context import LayoutInstanceContext
from ansys.edb.layout_instance.layout_obj_instance_2d_geometry import LayoutObjInstance2DGeometry
from ansys.edb.layout_instance.layout_obj_instance_3d_geometry import LayoutObjInstance3DGeometry
from ansys.edb.session import LayoutObjInstanceServiceStub, StubAccessor, StubType


def _parse_layout_obj_instance_geometry_message(lyt_obj_inst_geom_msg):
    if lyt_obj_inst_geom_msg.type == -1:
        raise TypeError("Encountered an unknown layout obj instance geometry type")
    geom_type = (
        LayoutObjInstance2DGeometry
        if lyt_obj_inst_geom_msg.type == 0
        else LayoutObjInstance3DGeometry
    )
    geom_msg = lyt_obj_inst_geom_msg.geometry
    return geom_type(geom_msg.geometry, geom_msg.owning_drawing, geom_msg.placement_layer)


class LayoutObjInstance(ObjBase):
    """Class representing layout object instance."""

    __stub: LayoutObjInstanceServiceStub = StubAccessor(StubType.layout_obj_instance)

    @property
    def layers(self):
        r""":obj:`list`\[:class:`Layer <ansys.edb.layer.Layer>`\]: Layers this layout object instance has geometry on.

        Read-Only.
        """
        return [Layer(msg).cast() for msg in self.__stub.GetLayers(self.msg).items]

    def get_geometries(self, layer):
        """Get the geometry that exists on the specified layer.

        Parameters
        ----------
        layer : :class:`Layer <ansys.edb.layer.Layer>` or str

        Returns
        -------
        list[LayoutObjInstance2DGeometry or LayoutObjInstance3DGeometry]
        """
        geoms = self.__stub.GetGeometries(layer_ref_property_message(self, layer))
        return utils.map_list(geoms.geometries, _parse_layout_obj_instance_geometry_message)

    @property
    def context(self):
        r""":obj:`list`\[:obj:`str`\]: List of strings representing the context of the layout object instance.

        The list of strings is a list of :class:`cell instance <ansys.edb.hierarchy.CellInstance>` names representing \
        the hierarchy level this layout obj instance's :class:`context <LayoutInstanceContext>` resides on. The the \
        first entry in the list represents the top level context and the last entry represents the context the layout \
        obj instance exists in.

        Read-Only
        """
        return utils.map_list(self.__stub.GetContext(self.msg).strings)

    @property
    def layout_instance_context(self):
        """:class:`LayoutInstanceContext`: The context this layout object instance exists in.

        Read-Only.
        """
        return LayoutInstanceContext(self.__stub.GetLayoutInstanceContext(self.msg))

    @property
    def layout_obj(self):
        """:term:`Connectable <Connectable>`: The definition layout object this layout object instance \
        is an instance of.

        Read-Only.
        """
        return create_conn_obj(self.__stub.GetLayoutObj(self.msg))

    @parser.to_polygon_data
    def get_bbox(self, local=False):
        """Get the bounding box of the layout object instance.

        Parameters
        ----------
        local : bool
            If true, return the bounding-box in the local :class:`context <LayoutInstanceContext>`.  Otherwise, \
            return the bounding-box in the global context.

        Returns
        -------
        :class:`PolygonData <ansys.edb.geometry.PolygonData>`
        """
        return self.__stub.GetBBox(bool_property_message(self, local))
