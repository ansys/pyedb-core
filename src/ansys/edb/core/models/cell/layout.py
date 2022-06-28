"""Layout."""

import ansys.api.edb.v1.layout_pb2 as layout_pb2
from ansys.api.edb.v1.layout_pb2_grpc import LayoutServiceStub

import ansys.edb.core.interfaces.grpc.messages as messages

from ...session import StubAccessor, StubType
from ...utility.variable_server import _VariableServer
from ..base import ObjBase
from ..polygon_data import PolygonData
from .differential_pair import DifferentialPair
from .extended_net import ExtendedNet
from .hierarchy.cell_instance import CellInstance
from .hierarchy.group import Group
from .layer_collection import LayerCollection
from .layout_obj import LayoutObjType
from .net import Net
from .net_class import NetClass
from .pin_group import PinGroup
from .primitive import BoardBendDef, PadstackInstance, Primitive
from .terminals import Terminal
from .voltage_regulator import VoltageRegulator


class Layout(ObjBase, _VariableServer):
    """Class representing layout object."""

    __stub: LayoutServiceStub = StubAccessor(StubType.layout)

    def __init__(self, msg):
        """Initialize a new layout.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        _VariableServer.__init__(self, msg)

    @property
    def cell(self):
        """Get cell.

        Returns
        -------
        ansys.edb.core.models.cell.Cell
        """
        from .cell import Cell

        return Cell(self.__stub.GetCell(self.msg))

    @property
    def layer_collection(self):
        """
        Get layer collection.

        Returns
        -------
        LayerCollection
        """
        return LayerCollection(False, self.__stub.GetLayerCollection(self.msg))

    @layer_collection.setter
    def layer_collection(self, layer_collection):
        """
        Set layer collection.

        Parameters
        ----------
        layer_collection : LayerCollection
        """
        self.__stub.SetLayerCollection(
            layout_pb2.SetLayerCollectionMessage(
                layout=self.msg, layer_collection=layer_collection.msg
            )
        )

    @property
    def primitives(self):
        """
        Get list of primitives.

        Returns
        -------
        list[Primitive]
        """
        return [
            Primitive(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.PRIMITIVE)
            )
        ]

    @property
    def padstack_instances(self):
        """Get list of padstack instances.

        Returns
        -------
        list[PadstackInstance]
        """
        return [
            PadstackInstance(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.PADSTACK_INSTANCE)
            )
        ]

    @property
    def terminals(self):
        """Get list of terminals.

        Returns
        -------
        list[Terminal]
        """
        return [
            Terminal(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.TERMINAL)
            )
        ]

    @property
    def cell_instances(self):
        """Get list of cell instances.

        Returns
        -------
        list[CellInstance]
        """
        return [
            CellInstance(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.CELL_INSTANCE)
            )
        ]

    @property
    def nets(self):
        """Get list of nets.

        Returns
        -------
        list[Net]
        """
        return [
            Net(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.NET)
            )
        ]

    @property
    def groups(self):
        """Get list of groups.

        Returns
        -------
        list[Net]
        """
        return [
            Group(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.GROUP)
            )
        ]

    @property
    def net_classes(self):
        """Get list of net classes.

        Returns
        -------
        list[NetClass]
        """
        return [
            NetClass(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.NET_CLASS)
            )
        ]

    @property
    def differential_pairs(self):
        """Get list of differential pairs.

        Returns
        -------
        list[DifferentialPair]
        """
        return [
            DifferentialPair(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.DIFFERENTIAL_PAIR)
            )
        ]

    @property
    def pin_groups(self):
        """Get list of pin groups.

        Returns
        -------
        list[PinGroup]
        """
        return [
            PinGroup(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.PIN_GROUP)
            )
        ]

    @property
    def voltage_regulators(self):
        """Get list of voltage regulators.

        Returns
        -------
        list[VoltageRegulator]
        """
        return [
            VoltageRegulator(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.VOLTAGE_REGULATOR)
            )
        ]

    @property
    def extended_nets(self):
        """Get list of extended nets.

        Returns
        -------
        list[ExtendedNet]
        """
        return [
            ExtendedNet(msg)
            for msg in self.__stub.GetItems(
                messages.layout_get_items_message(self, LayoutObjType.EXTENDED_NET)
            )
        ]

    def expanded_extent(
        self, nets, extent, expansion_factor, expansion_unitless, use_round_corner, num_increments
    ):
        """Get expanded extent from nets.

        Parameters
        ----------
        nets : list[Net]
        extent : GeometryExtentType
        expansion_factor : float
        expansion_unitless : bool
        use_round_corner : bool
        num_increments : num

        Returns
        -------
        PolygonData
        """
        return PolygonData(
            self.__stub.GetExpandedExtentFromNets(
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
        )

    def convert_primitives_to_vias(self, primitives, is_pins=False):
        """Convert primitives to vias.

        Parameters
        ----------
        primitives : list[Primitive]
        is_pins : bool, optional
        """
        self.__stub.ConvertPrimitivesToVias(
            messages.layout_convert_p2v_message(self, primitives, is_pins)
        )

    @property
    def port_reference_terminals_connected(self):
        """Get if the port reference terminals are connected.

        Returns
        -------
        bool
        """
        return self.__stub.ArePortReferenceTerminalsConnected(self.msg).is_connected

    @property
    def zone_primitives(self):
        """Get zone primitives.

        Returns
        -------
        list[Primitive]
        """
        return [Primitive(msg) for msg in self.__stub.GetZonePrimitives(self.msg)]

    @property
    def fixed_zone_primitive(self):
        """Get fixed zone primitive.

        Returns
        -------
        Primitive
        """
        msg = self.__stub.GetFixedZonePrimitive(self.msg)
        return None if msg is None else Primitive(msg)

    @fixed_zone_primitive.setter
    def fixed_zone_primitive(self, value):
        """Set fixed zone primitive.

        Parameters
        ----------
        value : Primitive
        """
        self.__stub.SetFixedZonePrimitives(messages.pointer_property_message(self, value))

    @property
    def board_bend_defs(self):
        """Get board bend definitions.

        Returns
        -------
        list[BoardBendDef]
        """
        return [BoardBendDef(msg) for msg in self.__stub.GetBoardBendDefs(self.msg)]

    def synchronize_bend_manager(self):
        """Synchronize bend manager."""
        self.__stub.SynchronizeBendManager(self.msg)
