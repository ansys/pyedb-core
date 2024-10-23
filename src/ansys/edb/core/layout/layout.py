"""Layout."""

from ansys.api.edb.v1 import layout_pb2
from ansys.api.edb.v1.layout_pb2_grpc import LayoutServiceStub

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.hierarchy import cell_instance, group, pin_group
from ansys.edb.core.inner import ObjBase, messages, parser, utils, variable_server
from ansys.edb.core.layer.layer_collection import LayerCollection
from ansys.edb.core.layout import voltage_regulator
from ansys.edb.core.layout.mcad_model import McadModel
from ansys.edb.core.layout_instance import layout_instance
from ansys.edb.core.net.differential_pair import DifferentialPair
from ansys.edb.core.net.extended_net import ExtendedNet
from ansys.edb.core.net.net import Net
from ansys.edb.core.net.net_class import NetClass
from ansys.edb.core.primitive.primitive import BoardBendDef, PadstackInstance, Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.terminal.terminals import Terminal


def _geometry_simplifications_settings_msg(layout, layer, tol):
    """Create a GeometrySimplificationSettingsMessage."""
    return layout_pb2.GeometrySimplificationSettingsMessage(
        layout_layer=messages.layer_ref_property_message(layout, layer),
        tolerance=messages.value_message(tol),
    )


def _geometry_simplifications_settings_with_option_msg(layout, layer, tol, option):
    """Create a GeometrySimplificationSettingsWithOptionMessage."""
    return layout_pb2.GeometrySimplificationSettingsWithOptionMessage(
        geom_simplification_settings=_geometry_simplifications_settings_msg(layout, layer, tol),
        option=option,
    )


def _via_simplifications_settings_with_option_msg(
    layout, layer, tol, option, simplification_method
):
    """Create a ViaSimplificationSettingsMessage."""
    return layout_pb2.ViaSimplificationSettingsMessage(
        geom_simplification_settings_with_option=_geometry_simplifications_settings_with_option_msg(
            layout, layer, tol, option
        ),
        simplification_method=simplification_method,
    )


class Layout(ObjBase, variable_server.VariableServer):
    """Represents a layout."""

    __stub: LayoutServiceStub = StubAccessor(StubType.layout)

    def __init__(self, msg):
        """Initialize a new layout.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        variable_server.VariableServer.__init__(self, msg)

    @property
    def cell(self):
        """:class:`.Cell`: Owning cell for the layout.

        This property is read-only.
        """
        from ansys.edb.core.layout.cell import Cell

        return Cell(self.__stub.GetCell(self.msg))

    @property
    def layer_collection(self):
        """:class:`.LayerCollection`: \
        Layer collection of the layout."""
        return LayerCollection(self.__stub.GetLayerCollection(self.msg))

    @layer_collection.setter
    def layer_collection(self, layer_collection):
        self.__stub.SetLayerCollection(
            layout_pb2.SetLayerCollectionMessage(
                layout=self.msg, layer_collection=layer_collection.msg
            )
        )

    def _get_items(self, obj_type, lyt_obj_type_enum, do_cast=False):
        """Get a list of layout objects."""
        items = utils.map_list(
            self.__stub.GetItems(messages.layout_get_items_message(self, lyt_obj_type_enum)).items,
            obj_type,
        )
        return items if not do_cast else [item.cast() for item in items]

    @property
    def primitives(self):
        """:obj:`list` of :class:`.Primitive`: List of all \
            primitives in the layout.

        This property is read-only.
        """
        return self._get_items(Primitive, LayoutObjType.PRIMITIVE, True)

    @property
    def padstack_instances(self):
        """:obj:`list` of :class:`.PadstackInstance`: List of \
            all padstack instances in the layout.

        This property is read-only.
        """
        return self._get_items(PadstackInstance, LayoutObjType.PADSTACK_INSTANCE)

    @property
    def terminals(self):
        """:obj:`list` of :class:`.Terminal`: \
        List of all terminals in the layout.

        This property is read-only.
        """
        return self._get_items(Terminal, LayoutObjType.TERMINAL, True)

    @property
    def cell_instances(self):
        """:obj:`list` of :class:`CellInstances <.CellInstance>`: \
        List of all cell instances in the layout.

        This property is read-only.
        """
        return self._get_items(cell_instance.CellInstance, LayoutObjType.CELL_INSTANCE)

    @property
    def nets(self):
        """:obj:`list` of :class:`.Net`: List of all nets \
        in the layout.

        This property is read-only.
        """
        return self._get_items(Net, LayoutObjType.NET)

    @property
    def groups(self):
        """:obj:`list` of :class:`.Group`: List of all groups \
        in the layout.

        This property is read-only.
        """
        return self._get_items(group.Group, LayoutObjType.GROUP, True)

    @property
    def net_classes(self):
        """:obj:`list` of :class:`.NetClass`: List of all \
        net classes in the layout.

        This property is read-only.
        """
        return self._get_items(NetClass, LayoutObjType.NET_CLASS)

    @property
    def differential_pairs(self):
        """:obj:`list` of :class:`.DifferentialPair`: \
        List of all differential pairs in the layout.

        This property is read-only.
        """
        return self._get_items(DifferentialPair, LayoutObjType.DIFFERENTIAL_PAIR)

    @property
    def pin_groups(self):
        """:obj:`list` of :class:`.PinGroup` : List of all \
        pin groups in the layout.

        This property is read-only.
        """
        return self._get_items(pin_group.PinGroup, LayoutObjType.PIN_GROUP)

    @property
    def voltage_regulators(self):
        """:obj:`list` of :class:`.VoltageRegulator`: \
        List of all voltage regulators in the layout.

        This property is read-only.
        """
        return self._get_items(voltage_regulator.VoltageRegulator, LayoutObjType.VOLTAGE_REGULATOR)

    @property
    def extended_nets(self):
        """:obj:`list` of :class:`.ExtendedNet`: \
        List of all extended nets in the layout.

        This property is read-only.
        """
        return self._get_items(ExtendedNet, LayoutObjType.EXTENDED_NET)

    @parser.to_polygon_data
    def expanded_extent(
        self, nets, extent, expansion_factor, expansion_unitless, use_round_corner, num_increments
    ):
        """Get an expanded polygon for a list of nets.

        Parameters
        ----------
        nets : list[:class:`.Net`]
            List of nets.
        extent : :class:`.ExtentType`
            Geometry extent type for expansion.
        expansion_factor : float
            Expansion factor for the polygon union. No expansion occurs if the value
            for this parameter is less than or equal to 0.
        expansion_unitless : bool
            When unitless, the distance by which the extent expands is the factor
            multiplied by the longer dimension (X or Y distance) of the expanded
            object/net.
        use_round_corner : bool
            Whether to use round corners or sharp corners. For round corners, this
            returns a bounding box if its area is within 10% of the rounded expansion's
            area.
        num_increments : int
            Number of iterations desired to reach the full expansion.

        Returns
        -------
        :class:`.PolygonData`

        Notes
        -----
        This method returns the expansion of the contour, so any voids within expanded
        objects are ignored.
        """
        return self.__stub.GetExpandedExtentFromNets(
            messages.layout_expanded_extent_message(
                self,
                nets,
                extent,
                expansion_factor,
                expansion_unitless,
                use_round_corner,
                num_increments,
            )
        )

    def convert_primitives_to_vias(self, primitives, is_pins=False):
        """Convert a list of primitives into vias or pins.

        Parameters
        ----------
        primitives : list[:class:`.Primitive`]
            List of primitives.
        is_pins : bool, default: False
            Whether the list consists of pins. The default is ``False``, in which
            case the list consists of vias.
        """
        self.__stub.ConvertPrimitivesToVias(
            messages.layout_convert_p2v_message(self, primitives, is_pins)
        )

    @property
    def port_reference_terminals_connected(self):
        """:obj:`bool`: Flag indicating if port reference terminals are connected.

        This property applies to lumped ports and circuit ports. It is ``True`` if
        port terminals are connected, ``False`` otherwise.

        This property is read-only.
        """
        return self.__stub.ArePortReferenceTerminalsConnected(self.msg).is_connected

    @property
    def zone_primitives(self):
        """:obj:`list` of :class:`.Primitive`: List of \
        all primitives in the :term:`zones <Zone>`.

        This property is read-only.
        """
        return [Primitive(msg).cast() for msg in self.__stub.GetZonePrimitives(self.msg).items]

    @property
    def fixed_zone_primitive(self):
        """:class:`.Primitive`: Fixed :term:`zones <Zone>` primitive."""
        msg = self.__stub.GetFixedZonePrimitive(self.msg)
        return None if msg is None else Primitive(msg).cast()

    @fixed_zone_primitive.setter
    def fixed_zone_primitive(self, value):
        self.__stub.SetFixedZonePrimitives(messages.pointer_property_message(self, value))

    @property
    def board_bend_defs(self):
        """:obj:`list` of :class:`.BoardBendDef`: List of all \
        board bend definitions in the layout.

        This property is read-only.
        """
        return [BoardBendDef(msg) for msg in self.__stub.GetBoardBendDefs(self.msg)]

    def synchronize_bend_manager(self):
        """Synchronize the bend manager."""
        self.__stub.SynchronizeBendManager(self.msg)

    @property
    def layout_instance(self):
        """:class:`.LayoutInstance`: \
        Instance of the layout.

        This property is read-only.
        """
        return layout_instance.LayoutInstance(self.__stub.GetLayoutInstance(self.msg))

    def reconstruct_arcs(self, layer, tolerance):
        """Reconstruct arcs of polygons on a layer.

        Parameters
        ----------
        layer : str or :class:`.Layer`
            Layer to reconstruct arcs on.
        tolerance : :class:`.Value`
            Tolerance.
        """
        self.__stub.ReconstructArcs(_geometry_simplifications_settings_msg(self, layer, tolerance))

    def unite_primitives(self, layer):
        """Unite primitives on a layer.

        Parameters
        ----------
        layer : str or :class:`.Layer`
            Layer to unite primitives on.
        """
        self.__stub.UnitePrimitives(messages.layer_ref_property_message(self, layer))

    def create_stride(self, filename):
        """Create a Stride model from an MCAD file.

        Parameters
        ----------
        filename : str
            Absolute path of the MCAD file.

        Returns
        -------
        McadModel
           Stride model created.
        """
        return McadModel.create_stride(layout=self, filename=filename)

    def create_hfss(self, filename, design):
        """Create an HFSS model from an MCAD file.

        Parameters
        ----------
        filename : str
            Absolute path of the MCAD file.
        design : str
            Design name.

        Returns
        -------
        McadModel
            HFSS model created.
        """
        return McadModel.create_hfss(connectable=self, filename=filename, design=design)

    def create_3d_comp(self, filename):
        """Create a 3D composite model from an MCAD file.

        Parameters
        ----------
        filename : str
            Absolute path of the MCAD file.

        Returns
        -------
        McadModel
           3D composite model created.
        """
        return McadModel.create_3d_comp(layout=self, filename=filename)

    def group_vias(
        self,
        layer,
        max_grouping_distance="100um",
        persistent_vias=False,
        group_by_proximity=True,
        check_containment=True,
    ):
        """Create via groups from the primitives on the specified layer.

        Parameters
        ----------
        layer : str or :class:`.Layer`
            Layer containing the primitives to be grouped.
        max_grouping_distance : :term:`ValueLike`
            Maximum distance between vias in a via group .
        persistent_vias : bool
            Whether to preserve primitives during via group creation. If ``False``
            primitives are deleted during via group creation.
        group_by_proximity : bool
            If ``True``, vias are grouped by proximity (relative position to each other).
            If ``False``, vias are grouped by range (any vias within the specified maximum
            grouping distance of each other are grouped)
        check_containment : boo
            If ``True``, the connectivity of via groups is checked and enforced to prevent
            short circuits in geometry connecting to the via group. If false, vias are
            grouped regardless of the connectivity of touching geometry.
        """
        self.__stub.GroupVias(
            layout_pb2.ViaGroupingSettingsMessage(
                via_simplification_settings=_via_simplifications_settings_with_option_msg(
                    self, layer, max_grouping_distance, check_containment, group_by_proximity
                ),
                persistent=persistent_vias,
            )
        )

    def snap_vias(
        self,
        layer,
        via_snapping_tol=3,
        prim_snapping_tol="0.05um",
        snap_by_area_factor=True,
        remove_dangling_vias=True,
    ):
        """Snap vias on the specified layer to touching geometry.

        Parameters
        ----------
        layer : str or :class:`.Layer`
            Layer containing the vias to be snapped.
        via_snapping_tol : :term:`ValueLike`
            Tolerance for snapping vias. If snap_by_area_factor is ``True``, this
            value should not have a unit.
        prim_snapping_tol : :term:`ValueLike`
            Tolerance for snapping primitives.
        snap_by_area_factor : bool
            If ``True``, the via snapping tolerance is a factor of the surface area of the via.
            If ``False``, the via snapping tolerance is treated as an absolute distance.
        remove_dangling_vias : bool
            If ``True``, vias not connected to any geometry are removed.
        """
        self.__stub.SnapVias(
            layout_pb2.ViaSnappingSettingsMessage(
                via_simplification_settings=_via_simplifications_settings_with_option_msg(
                    self, layer, via_snapping_tol, remove_dangling_vias, snap_by_area_factor
                ),
                prim_snapping_tol=messages.value_message(prim_snapping_tol),
            )
        )

    def snap_primitives(self, layer, tol="0.05um", check_connectivity=True):
        """Snap primitives on the specified layer to touching geometry.

        Parameters
        ----------
        layer : str or :class:`.Layer`
            Layer containing the primitives to be snapped.
        tol : :term:`ValueLike`
            Tolerance for snapping primitives.
        check_connectivity : bool
            If ``True``, the connectivity of primitives is checked and enforced to prevent
            short circuits in geometry connecting to the primitives. If false, primitives are
            grouped regardless of the connectivity of touching geometry.
        """
        self.__stub.SnapPrimitives(
            _geometry_simplifications_settings_with_option_msg(self, layer, tol, check_connectivity)
        )

    def create_mesh_region(
        self,
        xy_exp,
        pos_z_exp,
        neg_z_exp,
        use_active_nets,
        incl_ref,
        ext,
        num_x_partitions,
        num_y_partitions,
    ):
        """Designate a mesh region in a design and create partitions for simulation.

        Parameters
        ----------
        xy_exp: :class:`.Value`
            Horizontal padding on both sides of the new mesh.
        pos_z_exp: :class:`.Value`
            Vertical padding above the new mesh region.
        neg_z_exp: :class:`.Value`
            Vertical padding below the new mesh region.
        use_active_nets: bool
            True will create a new mesh region defined by the active nets in the design.
            False will create a new mesh region defined by the dielectric extents in the design.
        incl_ref: bool
            True will include bot positive nets and reference nets in the definition of the new mesh region.
            False will not include bot positive nets and reference nets.
        ext: :class:`.ExtentType`
            Geometry extent type.
        num_x_partitions: int
            Number of partitions to create on x axis in the new mesh region.
        num_y_partitions: int
            Number of partitions to create on y axis in the new mesh region.
        """
        self.__stub.CreateMeshRegion(
            layout_pb2.CreateMeshRegionMessage(
                layout=self.msg,
                xy_exp=messages.value_message(xy_exp),
                pos_z_exp=messages.value_message(pos_z_exp),
                neg_z_exp=messages.value_message(neg_z_exp),
                use_active_nets=use_active_nets,
                incl_ref=incl_ref,
                ext=ext.value,
                num_x_partitions=num_x_partitions,
                num_y_partitions=num_y_partitions,
            )
        )
