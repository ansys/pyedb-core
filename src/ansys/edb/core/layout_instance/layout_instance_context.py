"""Layout instance context."""

from ansys.edb.core.inner import ObjBase, parser
from ansys.edb.core.inner.messages import bool_property_message
from ansys.edb.core.layout import layout
from ansys.edb.core.session import LayoutInstanceContextServiceStub, StubAccessor, StubType


class LayoutInstanceContext(ObjBase):
    """Represents the layout instance context object."""

    __stub: LayoutInstanceContextServiceStub = StubAccessor(StubType.layout_instance_context)

    @property
    def layout(self):
        """:class:`.Layout`: Layout of the context.

        This property is read-only.
        """
        return layout.Layout(self.__stub.GetLayout(self.msg))

    @parser.to_polygon_data
    def get_bbox(self, local):
        """Get the bounding box of the context.

        Parameters
        ----------
        local : bool
            Whether to return the bounding box in the local :class:`context <LayoutInstanceContext>`.
            If ``False``, the bounding-box in the global context is returned.

        Returns
        -------
        :class:`.PolygonData`
            Bounding box of the context.
        """
        return self.__stub.GetBBox(bool_property_message(self, local))

    @property
    def is_top_or_black_box(self):
        """:obj:`bool`: Flag indicating if this is a top-level or blackbox context.

        This property is read-only.
        """
        return self.__stub.IsTopOrBlackBox(self.msg).value

    @property
    def top_or_black_box(self):
        """:class:`LayoutInstanceContext`: Top-level or blackbox :class:`context <LayoutInstanceContext>` instance.

        This property is read-only.
        """
        return LayoutInstanceContext(self.__stub.GetTopOrBlackBox(self.msg))

    @property
    def placement_elevation(self):
        """:obj:`float`: Placement elevation of the context.

        This parameter only applies if the context does not have 3D placement enabled.
        If the context has 3D placement enabled, ``None`` is returned because the
        placement of the context is dictated by the underlying 3D transformation.
        Otherwise, the placement elevation of the context is returned.

        This property is read-only.
        """
        return (
            self.__stub.GetPlacementElevation(self.msg).value
            if not self.get_is_3d_placement(False)
            else None
        )

    def get_is_3d_placement(self, local):
        """Determine if the context has 3D placement enabled.

        Parameters
        ----------
        local : bool
            Whether 3D placement is enabled only in the local :class:`context <LayoutInstanceContext>`.
            If ``False``, a check is run to see if 3D placement is enabled anywhere higher in the
            hierarchy.

        Returns
        -------
        bool
            ``True`` if 3D placement is enabled in the local context.
        """
        return self.__stub.Is3DPlacement(bool_property_message(self, local)).value
