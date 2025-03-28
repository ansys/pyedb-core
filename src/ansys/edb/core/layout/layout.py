"""Layout."""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import ExtentType, PolygonData
    from ansys.edb.core.layout.cell import Cell
    from ansys.edb.core.net.net import Net
    from ansys.edb.core.typing import LayerLike, ValueLike
    from ansys.edb.core.utility.value import Value

    LayerListLike = Union[LayerLike, List[LayerLike]]
    from src.ansys.edb.core.hierarchy.cell_instance import CellInstance
    from src.ansys.edb.core.hierarchy.group import Group
    from src.ansys.edb.core.hierarchy.pin_group import PinGroup
    from src.ansys.edb.core.layout.voltage_regulator import VoltageRegulator
    from src.ansys.edb.core.layout_instance.layout_instance import LayoutInstance
    from src.ansys.edb.core.net.differential_pair import DifferentialPair
    from src.ansys.edb.core.net.extended_net import ExtendedNet
    from src.ansys.edb.core.net.net_class import NetClass
    from src.ansys.edb.core.primitive.padstack_instance import PadstackInstance
    from src.ansys.edb.core.terminal.terminal import Terminal

from ansys.api.edb.v1 import layout_pb2
from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage
from ansys.api.edb.v1.layout_pb2_grpc import LayoutServiceStub

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import ObjBase, messages, parser, utils, variable_server
from ansys.edb.core.layer.layer_collection import LayerCollection
from ansys.edb.core.layout.mcad_model import McadModel
from ansys.edb.core.layout_instance import layout_instance
from ansys.edb.core.primitive.board_bend_def import BoardBendDef
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType


def _geometry_simplifications_settings_msg(layout, layer, tol):
    """Create a GeometrySimplificationSettingsMessage."""
    return layout_pb2.GeometrySimplificationSettingsMessage(
        layout_layers=messages.layer_refs_property_message(layout, layer),
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
    """Owns the geometry, nets, and stackup of an EDB design."""

    __stub: LayoutServiceStub = StubAccessor(StubType.layout)

    def __init__(self, msg: EDBObjMessage):
        """Initialize a new layout.

        Parameters
        ----------
        msg : :class:`.EDBObjMessage`
        """
        ObjBase.__init__(self, msg)
        variable_server.VariableServer.__init__(self, self)

    @property
    def cell(self) -> Cell:
        """:class:`.Cell`: Cell that owns the layout.

        This property is read-only.
        """
        from ansys.edb.core.layout.cell import Cell

        return Cell(self.__stub.GetCell(self.msg))

    @property
    def layer_collection(self) -> LayerCollection:
        """:class:`.LayerCollection`: Stackup of the layout."""
        return LayerCollection(self.__stub.GetLayerCollection(self.msg))

    @layer_collection.setter
    def layer_collection(self, layer_collection: LayerCollection):
        self.__stub.SetLayerCollection(
            layout_pb2.SetLayerCollectionMessage(
                layout=self.msg, layer_collection=layer_collection.msg
            )
        )

    def _get_items(self, lyt_obj_type_enum):
        """Get a list of layout objects."""
        return utils.query_lyt_object_collection(
            self, lyt_obj_type_enum, self.__stub.GetItems, self.__stub.StreamItems
        )

    @property
    def primitives(self) -> List[Primitive]:
        """:obj:`list` of :class:`.Primitive`: List of all primitives in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.PRIMITIVE)

    @property
    def padstack_instances(self) -> List[PadstackInstance]:
        """:obj:`list` of :class:`.PadstackInstance`: List of all padstack instances in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.PADSTACK_INSTANCE)

    @property
    def terminals(self) -> List[Terminal]:
        """:obj:`list` of :class:`.Terminal`: List of all terminals in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.TERMINAL)

    @property
    def cell_instances(self) -> List[CellInstance]:
        """:obj:`list` of :class:`.CellInstance`: List of all cell instances in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.CELL_INSTANCE)

    @property
    def nets(self) -> List[Net]:
        """:obj:`list` of :class:`.Net`: List of all nets in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.NET)

    @property
    def groups(self) -> List[Group]:
        """:obj:`list` of :class:`.Group`: List of all groups in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.GROUP)

    @property
    def net_classes(self) -> List[NetClass]:
        """:obj:`list` of :class:`.NetClass`: List of all net classes in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.NET_CLASS)

    @property
    def differential_pairs(self) -> List[DifferentialPair]:
        """:obj:`list` of :class:`.DifferentialPair`: List of all differential pairs in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.DIFFERENTIAL_PAIR)

    @property
    def pin_groups(self) -> List[PinGroup]:
        """:obj:`list` of :class:`.PinGroup`: List of all pin groups in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.PIN_GROUP)

    @property
    def voltage_regulators(self) -> List[VoltageRegulator]:
        """:obj:`list` of :class:`.VoltageRegulator`: List of all voltage regulators in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.VOLTAGE_REGULATOR)

    @property
    def extended_nets(self) -> List[ExtendedNet]:
        """:class:`list` of :class:`.ExtendedNet`: List of all extended nets in the layout.

        This property is read-only.
        """
        return self._get_items(LayoutObjType.EXTENDED_NET)

    @parser.to_polygon_data
    def expanded_extent(
        self,
        nets: List[Net],
        extent: ExtentType,
        expansion_factor: float,
        expansion_unitless: bool,
        use_round_corner: bool,
        num_increments: int,
    ) -> List[PolygonData]:
        """Get the expanded extent of the geometry on the specified nets.

        Parameters
        ----------
        nets : list of .Net
            List of nets containing the geometry.
        extent : .ExtentType
            Type of extent to be retrieved.
        expansion_factor : float
            Expansion factor applied to the extent. No expansion occurs if the value
            for this parameter is less than or equal to 0.
        expansion_unitless : bool
            When unitless, the distance by which the extent expands is the factor
            multiplied by the longer dimension (X or Y distance) of the bounding box of the extent.
        use_round_corner : bool
            Whether to use round corners or sharp corners. For round corners, this
            returns a bounding box if its area is within 10% of the rounded expansion's
            area.
        num_increments : int
            Number of iterations desired to reach the full expansion.

        Returns
        -------
        .PolygonData

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

    def convert_primitives_to_vias(self, primitives: List[Primitive], is_pins: bool = False):
        """Convert a list of primitives into vias or pins.

        Parameters
        ----------
        primitives : list of .Primitive
            List of primitives to convert.
        is_pins : bool, default: False
            Flag indicating whether to convert the provided primitives
            to pins or vias. The default is ``False``, in which
            case the primitives will be converted to vias.
        """
        self.__stub.ConvertPrimitivesToVias(
            messages.layout_convert_p2v_message(self, primitives, is_pins)
        )

    @property
    def port_reference_terminals_connected(self) -> bool:
        """:obj:`bool`: Flag indicating if port reference terminals are connected.

        This property applies to lumped ports and circuit ports. It is ``True`` if
        port terminals are connected, ``False`` otherwise.

        This property is read-only.
        """
        return self.__stub.ArePortReferenceTerminalsConnected(self.msg).is_connected

    @property
    def zone_primitives(self) -> List[Primitive]:
        """:obj:`list` of :class:`.Primitive`: List of \
        all zone primitives in the layout.

        Zone primitives denote the outline of a :term:`zones <Zone>` in the layout.

        This property is read-only.
        """
        return [Primitive(msg).cast() for msg in self.__stub.GetZonePrimitives(self.msg).items]

    @property
    def fixed_zone_primitive(self) -> Primitive:
        """:class:`.Primitive`: Fixed :term:`zone <Zone>` primitive.

        The fixed zone primitive represents the zone that all bends are applied relative to.
        """
        msg = self.__stub.GetFixedZonePrimitive(self.msg)
        return None if msg is None else Primitive(msg).cast()

    @fixed_zone_primitive.setter
    def fixed_zone_primitive(self, value: Primitive):
        self.__stub.SetFixedZonePrimitives(messages.pointer_property_message(self, value))

    @property
    def board_bend_defs(self) -> List[BoardBendDef]:
        """:obj:`list` of :class:`.BoardBendDef`: List of all board bend definitions in the layout.

        This property is read-only.
        """
        return [BoardBendDef(msg) for msg in self.__stub.GetBoardBendDefs(self.msg)]

    def synchronize_bend_manager(self):
        """Synchronize the bend manager.

        Notes
        -----
        Most operations related to bends require this to be called first. If changes are made to the geometry
        in the design, it may be necessary to call this method again to ensure all bend related data is
        synchronized correctly.
        """
        self.__stub.SynchronizeBendManager(self.msg)

    @property
    def layout_instance(self) -> LayoutInstance:
        """:class:`.LayoutInstance`: Instance of the layout.

        This property is read-only.
        """
        return layout_instance.LayoutInstance(self.__stub.GetLayoutInstance(self.msg))

    def reconstruct_arcs(self, layer: LayerListLike, tolerance: Value):
        """Reconstruct arcs of polygons on a layer.

        Parameters
        ----------
        layer : :term:`LayerLike` or list of :term:`LayerLike`
            Layers to reconstruct arcs on.
        tolerance : .Value
            Tolerance.
        """
        self.__stub.ReconstructArcs(_geometry_simplifications_settings_msg(self, layer, tolerance))

    def unite_primitives(self, layer: LayerListLike):
        """Unite primitives on a layer.

        Parameters
        ----------
        layer : :term:`LayerLike` or list of :term:`LayerLike`
            Layers to unite primitives on.
        """
        self.__stub.UnitePrimitives(messages.layer_refs_property_message(self, layer))

    def create_stride(self, filename: str) -> McadModel:
        """Create a Stride model from an MCAD file.

        Parameters
        ----------
        filename : str
            Absolute path of the MCAD file.

        Returns
        -------
        .McadModel
           Stride model created.
        """
        return McadModel.create_stride(layout=self, filename=filename)

    def create_hfss(self, filename: str, design: str) -> McadModel:
        """Create an HFSS model from an MCAD file.

        Parameters
        ----------
        filename : str
            Absolute path of the MCAD file.
        design : str
            Design name.

        Returns
        -------
        .McadModel
            HFSS model created.
        """
        return McadModel.create_hfss(connectable=self, filename=filename, design=design)

    def create_3d_comp(self, filename: str) -> McadModel:
        """Create a 3D composite model from an MCAD file.

        Parameters
        ----------
        filename : str
            Absolute path of the MCAD file.

        Returns
        -------
        .McadModel
           3D composite model created.
        """
        return McadModel.create_3d_comp(layout=self, filename=filename)

    def group_vias(
        self,
        layer: LayerListLike,
        max_grouping_distance: ValueLike = "100um",
        persistent_vias: bool = False,
        group_by_proximity: bool = True,
        check_containment: bool = True,
    ):
        """Create via groups from the primitives on the specified layers.

        Parameters
        ----------
        layer : :term:`LayerLike` or list of :term:`LayerLike`
            Layers containing the primitives to be grouped.
        max_grouping_distance : :term:`ValueLike`
            Maximum distance between via primitives in a via group .
        persistent_vias : bool
            Whether to preserve primitives during via group creation. If ``False``
            primitives are deleted during via group creation.
        group_by_proximity : bool
            If ``True``, via primitives are grouped by proximity (relative position to each other).
            If ``False``, via primitives are grouped by range (any via primitives within the specified maximum
            grouping distance of each other are grouped)
        check_containment : bool
            If ``True``, the connectivity of via groups is checked and enforced to prevent
            short circuits in geometry connecting to the via group. If false, via primitives are
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
        layer: LayerListLike,
        via_snapping_tol: ValueLike = 3,
        prim_snapping_tol: ValueLike = "0.05um",
        snap_by_area_factor: bool = True,
        remove_dangling_vias: bool = True,
    ):
        """Snap vias on the specified layers to touching geometry.

        Parameters
        ----------
        layer : :term:`LayerLike` or list of :term:`LayerLike`
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

    def snap_primitives(
        self, layer: LayerListLike, tol: ValueLike = "0.05um", check_connectivity: bool = True
    ):
        """Snap primitives on the specified layer to touching geometry.

        Parameters
        ----------
        layer : str or list of str or .Layer or list of .Layer
            Layers containing the primitives to be snapped.
        tol : :term:`ValueLike`
            Tolerance for snapping primitives.
        check_connectivity : bool
            If ``True``, the connectivity of primitives is checked and enforced to prevent
            short circuits in geometry connecting to the primitives. If false, primitives are
            snapped regardless of the connectivity of touching geometry.
        """
        self.__stub.SnapPrimitives(
            _geometry_simplifications_settings_with_option_msg(self, layer, tol, check_connectivity)
        )

    def create_mesh_region(
        self,
        xy_exp: Value,
        pos_z_exp: Value,
        neg_z_exp: Value,
        use_active_nets: bool,
        incl_ref: bool,
        ext: ExtentType,
        num_x_partitions: int,
        num_y_partitions: int,
    ):
        """Designate a mesh region in a design and create partitions for meshing.

        Parameters
        ----------
        xy_exp : .Value
            Horizontal padding of the new mesh region (applied to both x and y directions).
        pos_z_exp : .Value
            Vertical padding above the new mesh region.
        neg_z_exp : .Value
            Vertical padding below the new mesh region.
        use_active_nets: bool
            ``True`` will create a new mesh region defined by the active nets in the design.
            ``False`` will create a new mesh region defined by the dielectric extents in the design.
        incl_ref : bool
            ``True`` will include bot positive nets and reference nets in the definition of the new mesh region.
            ``False`` will not include bot positive nets and reference nets.
        ext : .ExtentType
            Extent type of the new mesh region.
        num_x_partitions : int
            Number of partitions to create on x-axis in the new mesh region.
        num_y_partitions : int
            Number of partitions to create on y-axis in the new mesh region.
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

    def compress_primitives(self):
        """Compress :class:`primitives <.Primitive>` into \
        :class:`primitive instance collections <.PrimitiveInstanceCollection>`.

        Primitives whose only geometric difference is location will be compressed. \
        For example, a 4x4 grid of rectangles with the same width and height will be \
        compressed into one primitive instance collection.

        .. note::
           Only :class:`.Circle`, :class:`.Rectangle`, and :class:`.Polygon` primitives \
           are supported in primitive instance collections.
        """
        self.__stub.CompressPrimitives(self.msg)
