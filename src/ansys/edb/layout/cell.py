"""Cell."""

from enum import Enum

import ansys.api.edb.v1.cell_pb2 as cell_pb2
from ansys.api.edb.v1.cell_pb2_grpc import CellServiceStub
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2

from ansys.edb.core import ObjBase, messages, variable_server
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.layout import layout
from ansys.edb.primitive import Primitive
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.simulation_setup import SimulationSetup
from ansys.edb.utility import TemperatureSettings, Value
from ansys.edb.utility.hfss_extent_info import HfssExtentInfo


class CellType(Enum):
    """Enum representing possible types of cells.

    - CIRCUIT_CELL
    - FOOTPRINT_CELL
    """

    CIRCUIT_CELL = edb_defs_pb2.CIRCUIT_CELL
    FOOTPRINT_CELL = edb_defs_pb2.FOOTPRINT_CELL


class DesignMode(Enum):
    """Enum representing possible modes.

    - GENERAL
    - IC
    """

    GENERAL = edb_defs_pb2.GENERAL_MODE
    IC = edb_defs_pb2.IC_MODE


# dict representing options of HFSS Extents available via API.
HFSS_EXTENT_ARGS = {
    "use_open_region": "bool",
    "extent_type": "HfssExtentsType",
    "open_region_type": "HfssExtentsOpenRegionType",
    "base_polygon": "EDBObjMessage",
    "dielectric_extent_type": "HfssExtentsType",
    "dielectric_base_polygon": "EDBObjMessage",
    "dielectric": "HfssExtentMessage",
    "honor_user_dielectric": "bool",
    "airbox_truncate_at_ground": "bool",
    "airbox_horizontal": "HfssExtentMessage",
    "airbox_vertical_positive": "HfssExtentMessage",
    "airbox_vertical_negative": "HfssExtentMessage",
    "sync_airbox_vertical_extent": "bool",
    "is_pml_visible": "bool",
    "operating_frequency": "ValueMessage",
    "radiation_level": "ValueMessage",
    "user_xy_data_extent_for_vertical_expansion": "bool",
}


def _return_value(value):
    """Return value as it is."""
    return value


def _translate_hfss_extent(hfss_extent_msg):
    """Convert HfssExtentMessage to tuple of expected values."""
    return hfss_extent_msg.value, hfss_extent_msg.absolute


def _translate_hfss_extents_enums(msg):
    """Convert HfssExtent enums to get it's values."""
    return msg.value


def primitive_helper(msg):
    """Convert message to primitive."""
    return Primitive(msg).cast()


# dictionary describing message type and functions to translate them
_HFSS_EXTENT_MESSAGE_HELPER = {
    "HfssExtentMessage": {
        "msg": messages.hfss_extent_message,
        "val": _translate_hfss_extent,
    },
    "bool": {
        "msg": _return_value,
        "val": bool,
    },
    "ValueMessage": {
        "msg": messages.value_message,
        "val": Value,
    },
    "EDBObjMessage": {
        "msg": messages.edb_obj_message,
        "val": primitive_helper,
    },
    "HfssExtentsType": {
        "msg": _translate_hfss_extents_enums,
        "val": HfssExtentInfo.HFSSExtentInfoType,
    },
    "HfssExtentsOpenRegionType": {
        "msg": _translate_hfss_extents_enums,
        "val": HfssExtentInfo.OpenRegionType,
    },
}


# takes user-provided arbitrary args and a list of allowed keywords
# return a copy including only the valid args
def sanitize_args(args):
    """Extract valid extent options and convert them into messages."""
    return {
        k: _HFSS_EXTENT_MESSAGE_HELPER[HFSS_EXTENT_ARGS[k]]["msg"](args[k])
        for k in filter(lambda k: k in args, HFSS_EXTENT_ARGS.keys())
    }


def parse_args(msg):
    """Extract extent options values from Hfss Extent message and add them into a dictionary."""
    res = {}
    for attribute in HFSS_EXTENT_ARGS.keys():
        value = getattr(msg, attribute)
        msg_type = HFSS_EXTENT_ARGS[attribute]
        res[attribute] = _HFSS_EXTENT_MESSAGE_HELPER[msg_type]["val"](value)
    return res


class _QueryBuilder:
    @staticmethod
    def create(db, cell_type, name):
        return cell_pb2.CellCreationMessage(database=db.msg, type=cell_type.value, name=name)

    @staticmethod
    def set_hfss_extents(cell, extents):
        return cell_pb2.CellSetHfssExtentsMessage(
            cell=cell.msg, info=messages.hfss_extent_info_message(extents)
        )


class Cell(ObjBase, variable_server.VariableServer):
    """Cell."""

    __stub: CellServiceStub = StubAccessor(StubType.cell)
    layout_obj_type = LayoutObjType.CELL

    def __init__(self, msg):
        """Initialize a new cell object.

        Parameters
        ----------
        msg : EDBObjMessage
        """
        ObjBase.__init__(self, msg)
        variable_server.VariableServer.__init__(self, msg)

    @classmethod
    def create(cls, db, cell_type, cell_name):
        """Create a cell.

        Parameters
        ----------
        db : :class:`Database <ansys.edb.database.Database>`
            Database to create the cell in.
        cell_type : CellType
            Type of the cell to create.
        cell_name : str
            Name of the cell.

        Returns
        -------
        Cell
            Newly created cell.
        """
        return Cell(cls.__stub.Create(_QueryBuilder.create(db, cell_type, cell_name)))

    @property
    def layout(self):
        """:class:`Layout <ansys.edb.layout.Layout>`: Layout of the cell.

        Read-Only.
        """
        return layout.Layout(self.__stub.GetLayout(self.msg))

    @property
    def flattened_layout(self):
        """:class:`Layout <ansys.edb.layout.Layout>`: Flattened layout of the cell.

        Read-Only.
        """
        return layout.Layout(self.__stub.GetFlattenedLayout(self.msg))

    @classmethod
    def find(cls, database, cell_type, name=None, cell_id=None):
        """Find a cell in a database by either name or id.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.database.Database>`
            Database to search for the cell in.
        cell_type : CellType
            Type of the cell to create.
        name : str, optional
            Name of the cell.
        cell_id : int, optional
            ID of the cell.

        Returns
        -------
        Cell
            Cell that was found, None otherwise.
        """
        cell = Cell(cls.__stub.Find(messages.cell_find_message(database, cell_type, name, cell_id)))
        return None if cell.is_null else cell

    def delete(self):
        """Delete a cell."""
        self.__stub.Delete(self.msg)

    @property
    def database(self):
        """:class:`Database <ansys.edb.database.Database>`: Owning database of cell.

        Read-Only.
        """
        from ansys.edb.database import Database

        return Database(self.__stub.GetDatabase(self.msg))

    @property
    def is_footprint(self):
        """:obj:`bool` : Flag to indicate if the cell is a footprint.

        Read-Only.
        """
        return self.__stub.IsFootprint(self.msg).value

    @property
    def is_blackbox(self):
        """:obj:`bool` : Flag to indicate if the cell is a blackbox."""
        return self.__stub.IsBlackBox(self.msg).value

    @is_blackbox.setter
    def is_blackbox(self, value):
        self.__stub.SetBlackBox(messages.bool_property_message(self, value))

    @property
    def anti_pads_always_on(self):
        """:obj:`bool` : Determine whether antipads are always enabled.

        True if enabled, false otherwise. If not enabled, they are triggered only when the via center point falls \
        within fill from another net.
        """
        return self.__stub.GetAntiPadsAlwaysOn(self.msg).value

    @anti_pads_always_on.setter
    def anti_pads_always_on(self, value):
        self.__stub.SetAntiPadsAlwaysOn(messages.bool_property_message(self, value))

    @property
    def anti_pads_option(self):
        """:obj:`int` : Mode for activating antipads.

        | 0 for Center-point Intersection
        | 1 for Always On
        | 2 for Pad Intersection.
        """
        return self.__stub.GetAntiPadsOption(self.msg)

    @anti_pads_option.setter
    def anti_pads_option(self, value):
        self.__stub.SetAntiPadsOption(messages.int_property_message(self, value))

    @property
    def is_symbolic_footprint(self):
        """:obj:`bool` : Flag to indicate if the cell is a symbolic footprint.

        Read-Only.
        """
        return self.__stub.IsSymbolicFootprint(self.msg).value

    @property
    def name(self):
        """:obj:`str` : Name of the cell."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def design_mode(self):
        """:obj:`DesignMode` : Design mode of the cell."""
        return DesignMode(self.__stub.GetDesignMode(self.msg).mode)

    @design_mode.setter
    def design_mode(self, value):
        self.__stub.SetDesignMode(messages.design_mode_property_message(self, value))

    @property
    def hfss_extent_info(self):
        """:class: HfssExtentInfo <ansys.edb.utility.HfssExtentInfo> : HFSS Extents for the cell."""
        msg = self.__stub.GetHfssExtentInfo(self.msg)
        return HfssExtentInfo(**parse_args(msg))

    def set_hfss_extent_info(self, extents):
        """Set HFSS Extents of this cell.

        Parameters
        ----------
        extents : :class: HfssExtentInfo <ansys.edb.utility.HfssExtentInfo>
        """
        self.__stub.SetHfssExtentInfo(_QueryBuilder.set_hfss_extents(self, extents))

    @property
    def temperature_settings(self):
        """:class:`TemperatureSettings <ansys.edb.utility.TemperatureSettings>` :Temperature settings."""
        msg = self.__stub.GetTemperatureSettings(self.msg)
        return TemperatureSettings(
            msg.include_temp_dependence, msg.enable_thermal_feedback, Value(msg.temperature)
        )

    @temperature_settings.setter
    def temperature_settings(self, value):
        self.__stub.SetTemperatureSettings(
            messages.cell_set_temperature_settings_message(self, value)
        )

    def cutout(self, included_nets, clipped_nets, clipping_polygon, clean_clipping=True):
        """Cutout an existing cell into a new cell.

        Parameters
        ----------
        included_nets : list[:class:`Net <ansys.edb.net.Net>`]
            Nets to be kept after cutout.
        clipped_nets : list[:class:`Net <ansys.edb.net.Net>`]
            Nets to be kept and clipped at the boundary after cutout.
        clipping_polygon : :class:`PolygonData <ansys.edb.geometry.PolygonData>`
            Clipping polygon.
        clean_clipping : bool, optional
            Whether to perform clean clipping.

        Returns
        -------
        Cell
            The newly created cell.
        """
        return Cell(
            self.__stub.CutOut(
                messages.cell_cutout_message(
                    self, included_nets, clipped_nets, clipping_polygon, clean_clipping
                )
            )
        )

    def get_product_property_ids(self, prod_id):
        """Get a list of attribute ids corresponding to the provided product id for the cell.

        Parameters
        ----------
        prod_id : :class:`ProductIdType <ansys.edb.database.ProductIdType>`
            ID representing a product that supports the EDB.

        Returns
        -------
        list[int]
            List of the user-defined attribute IDs for properties stored in this object
        """
        ids = self.__stub.GetProductPropertyIds(
            messages.get_product_property_ids_message(self, prod_id)
        ).ids
        return [prop_id for prop_id in ids]

    def get_product_property(self, prod_id, attr_id):
        """Get the product specific property of the cell.

        Parameters
        ----------
        prod_id : :class:`ProductIdType <ansys.edb.database.ProductIdType>`
            ID representing a product that supports the EDB.
        attr_id : int
            A user-defined id that identifies the string value stored in the property.

        Returns
        -------
        str
            The string stored in this property.
        """
        return self.__stub.GetProductProperty(
            messages.get_product_property_message(self, prod_id, attr_id)
        )

    def set_product_property(self, prod_id, attr_id, prop_value):
        """Set the product property of the cell associated with the given product and attribute ids.

        Parameters
        ----------
        prod_id : :class:`ProductIdType <ansys.edb.database.ProductIdType>`
            ID representing a product that supports the EDB.
        attr_id : int
            A user-defined id that identifies the string value stored in the property.
        prop_value : str
            The string stored in this property.
        """
        self.__stub.SetProductProperty(
            messages.set_product_property_message(self, prod_id, attr_id, prop_value)
        )

    def delete_simulation_setup(self, name):
        """Delete a simulation setup by name.

        Parameters
        ----------
        name : str
            Name of the setup to delete.
        """
        self.__stub.DeleteSimulationSetup(messages.string_property_message(self, name))

    @property
    def simulation_setups(self):
        """All simulation setups of the cell.

        .. seealso:: :obj:`add_simulation_setup`, :obj:`delete_simulation_setup`

        Returns
        -------
        list[:class:`SimulationSetup <ansys.edb.simulation_setup.SimulationSetup>`]
        """
        return [SimulationSetup(msg) for msg in self.__stub.GetSimulationSetups(self.msg)]

    def generate_auto_hfss_regions(self):
        """Generate auto HFSS regions.

        Automatically identifies areas for use as HFSS regions in SIwave simulations.
        """
        self.__stub.GenerateAutoHFSSRegions(self.msg)

    def generate_via_smart_box(self, net_name):
        """Generate via smart box.

        Automatically identifies the locations of vias and significant geometry around them.

        Parameters
        ----------
        net_name : str
            Name of the :class:`Net <ansys.edb.net.Net>` to be crawled in the search for vias.

        Returns
        -------
        list[:class:`PolygonData <ansys.edb.geometry.PolygonData>`]
            A list of boxes; one around each via discovered.
        """
        self.__stub.GenerateViaSmartBox(messages.string_property_message(self, net_name))
