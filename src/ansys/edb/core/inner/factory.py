"""This module allows for the creating of objects while avoid circular imports."""

from ansys.edb.core.edb_defs import LayoutObjType

_type_creator_params_dict = None
_primitive_type_creator_params_dict = None
_terminal_type_creator_params_dict = None


class _CreatorParams:
    def __init__(self, obj_type, do_cast=False):
        self.obj_type = obj_type
        self.do_cast = do_cast


def _initialize_type_creator_params_dict():
    global _type_creator_params_dict

    from ansys.edb.core.hierarchy.cell_instance import CellInstance
    from ansys.edb.core.hierarchy.group import Group
    from ansys.edb.core.hierarchy.pin_group import PinGroup
    from ansys.edb.core.inner.conn_obj import ConnObj
    from ansys.edb.core.layout.voltage_regulator import VoltageRegulator
    from ansys.edb.core.net.differential_pair import DifferentialPair
    from ansys.edb.core.net.extended_net import ExtendedNet
    from ansys.edb.core.net.net import Net
    from ansys.edb.core.net.net_class import NetClass
    from ansys.edb.core.primitive.padstack_instance import PadstackInstance
    from ansys.edb.core.primitive.primitive import Primitive
    from ansys.edb.core.terminal.terminal import Terminal
    from ansys.edb.core.terminal.terminal_instance import TerminalInstance

    _type_creator_params_dict = {
        LayoutObjType.PRIMITIVE: _CreatorParams(Primitive, True),
        LayoutObjType.PADSTACK_INSTANCE: _CreatorParams(PadstackInstance),
        LayoutObjType.TERMINAL: _CreatorParams(Terminal, True),
        LayoutObjType.TERMINAL_INSTANCE: _CreatorParams(TerminalInstance),
        LayoutObjType.CELL_INSTANCE: _CreatorParams(CellInstance),
        LayoutObjType.GROUP: _CreatorParams(Group, True),
        LayoutObjType.PIN_GROUP: _CreatorParams(PinGroup),
        LayoutObjType.VOLTAGE_REGULATOR: _CreatorParams(VoltageRegulator),
        LayoutObjType.NET_CLASS: _CreatorParams(NetClass),
        LayoutObjType.EXTENDED_NET: _CreatorParams(ExtendedNet),
        LayoutObjType.DIFFERENTIAL_PAIR: _CreatorParams(DifferentialPair),
        LayoutObjType.NET: _CreatorParams(Net),
        LayoutObjType.INVALID_LAYOUT_OBJ: _CreatorParams(ConnObj, True),
    }
    return _type_creator_params_dict


def _initialize_primitive_type_creator_params_dict():
    global _primitive_type_creator_params_dict

    from ansys.edb.core.primitive.board_bend_def import BoardBendDef
    from ansys.edb.core.primitive.bondwire import Bondwire
    from ansys.edb.core.primitive.circle import Circle
    from ansys.edb.core.primitive.path import Path
    from ansys.edb.core.primitive.polygon import Polygon
    from ansys.edb.core.primitive.primitive import PrimitiveType
    from ansys.edb.core.primitive.primitive_instance_collection import PrimitiveInstanceCollection
    from ansys.edb.core.primitive.rectangle import Rectangle
    from ansys.edb.core.primitive.text import Text

    _primitive_type_creator_params_dict = {
        PrimitiveType.BOARD_BEND: _CreatorParams(BoardBendDef),
        PrimitiveType.BONDWIRE: _CreatorParams(Bondwire),
        PrimitiveType.CIRCLE: _CreatorParams(Circle),
        PrimitiveType.PATH: _CreatorParams(Path),
        PrimitiveType.POLYGON: _CreatorParams(Polygon),
        PrimitiveType.RECTANGLE: _CreatorParams(Rectangle),
        PrimitiveType.TEXT: _CreatorParams(Text),
        PrimitiveType.PRIM_INST_COLLECTION: _CreatorParams(PrimitiveInstanceCollection),
    }
    return _primitive_type_creator_params_dict


def _initialize_terminal_type_creator_params_dict():
    global _terminal_type_creator_params_dict

    from ansys.edb.core.terminal.bundle_terminal import BundleTerminal
    from ansys.edb.core.terminal.edge_terminal import EdgeTerminal
    from ansys.edb.core.terminal.padstack_instance_terminal import PadstackInstanceTerminal
    from ansys.edb.core.terminal.pin_group_terminal import PinGroupTerminal
    from ansys.edb.core.terminal.point_terminal import PointTerminal
    from ansys.edb.core.terminal.terminal import TerminalType
    from ansys.edb.core.terminal.terminal_instance_terminal import TerminalInstanceTerminal

    _terminal_type_creator_params_dict = {
        TerminalType.BUNDLE: _CreatorParams(BundleTerminal),
        TerminalType.EDGE: _CreatorParams(EdgeTerminal),
        TerminalType.PADSTACK_INST: _CreatorParams(PadstackInstanceTerminal),
        TerminalType.PIN_GROUP: _CreatorParams(PinGroupTerminal),
        TerminalType.POINT: _CreatorParams(PointTerminal),
        TerminalType.TERM_INST: _CreatorParams(TerminalInstanceTerminal),
    }
    return _terminal_type_creator_params_dict


def _initialize_and_get_creator_dict(initializer, creator_dict):
    return initializer() if creator_dict is None else creator_dict


def _get_type_creator_dict():
    return _initialize_and_get_creator_dict(
        _initialize_type_creator_params_dict, _type_creator_params_dict
    )


def _get_primitive_type_creator_dict():
    return _initialize_and_get_creator_dict(
        _initialize_primitive_type_creator_params_dict, _primitive_type_creator_params_dict
    )


def _get_terminal_type_creator_dict():
    return _initialize_and_get_creator_dict(
        _initialize_terminal_type_creator_params_dict, _terminal_type_creator_params_dict
    )


def create_obj(msg, obj_type, do_cast):
    """Create an object from the provided message of the provided type."""
    obj = obj_type(msg)
    if do_cast:
        obj = obj.cast()
    return obj


def create_obj_from_creator_dict(creator_dict, msg, obj_type):
    """Create an object from the provided message of the type corresponding to the provided object type."""
    params = creator_dict[obj_type]
    return create_obj(msg, params.obj_type, params.do_cast)


def create_lyt_obj(msg, lyt_obj_type):
    """Create a layout object from the provided message of the type corresponding to the provided layout object type."""
    return create_obj_from_creator_dict(_get_type_creator_dict(), msg, lyt_obj_type)


def create_primitive(msg, prim_type):
    """Create a primitive from the provided message of the type corresponding to the provided primitive type."""
    return create_obj_from_creator_dict(_get_primitive_type_creator_dict(), msg, prim_type)


def create_terminal(msg, term_type):
    """Create a terminal from the provided message of the type corresponding to the provided terminal type."""
    return create_obj_from_creator_dict(_get_terminal_type_creator_dict(), msg, term_type)


def create_conn_obj(msg):
    """Create a connection object of its derived type based on its layout object type.

    Parameters
    ----------
    msg : ansys.api.edb.v1.edb_messages_pb2.EDBObjMessage

    Returns
    -------
    ansys.edb.core.inner.ConnObj
    """
    return create_lyt_obj(msg, LayoutObjType.INVALID_LAYOUT_OBJ)
