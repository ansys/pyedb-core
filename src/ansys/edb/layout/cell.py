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
    """Enum representing possible types of cells."""

    CIRCUIT_CELL = edb_defs_pb2.CIRCUIT_CELL
    FOOTPRINT_CELL = edb_defs_pb2.FOOTPRINT_CELL


class DesignMode(Enum):
    """Enum representing possible modes."""

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
        "val": Primitive,
    },
    "HfssExtentsType": {
        "msg": _translate_hfss_extents_enums,
        "val": HfssExtentInfo.HFSSExtentInfoType,
    },
    "HfssExtentsOpenRegionType": {
        "msg": _translate_hfss_extents_enums,
        "val": HfssExtentInfo.HFSSExtentInfoType,
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
    def set_hfss_extents(cell, **extents):
        extents = sanitize_args(extents)
        return cell_pb2.CellSetHfssExtentsMessage(
            cell=cell.msg, info=messages.hfss_extent_info_message(**extents)
        )


class Cell(ObjBase, variable_server.VariableServer):
    """Class representing a cell object."""

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
        db : Database
        cell_type : CellType
        cell_name : str

        Returns
        -------
        Cell
        """
        return Cell(cls.__stub.Create(_QueryBuilder.create(db, cell_type, cell_name)))

    @property
    def layout(self):
        """Get layout of a cell.

        Returns
        -------
        Layout
        """
        return layout.Layout(self.__stub.GetLayout(self.msg))

    @property
    def flattened_layout(self):
        """Get flattened layout of the cell.

        Returns
        -------
        Layout
        """
        return layout.Layout(self.__stub.GetFlattenedLayout(self.msg))

    @classmethod
    def find(cls, database, cell_type, name=None, cell_id=None):
        """Find a cell in a database by either name or id.

        Parameters
        ----------
        database : ansys.edb.database.Database
        cell_type : CellType
        name : str, optional
        cell_id : int, optional

        Returns
        -------
        Cell
        """
        cell = Cell(cls.__stub.Find(messages.cell_find_message(database, cell_type, name, cell_id)))
        return None if cell.is_null() else cell

    def delete(self):
        """Delete a cell."""
        self.__stub.Delete(self.msg)

    @property
    def database(self):
        """Get the database of cell.

        Returns
        -------
        ansys.edb.database.Database
        """
        from ansys.edb.database import Database

        return Database(self.__stub.GetDatabase(self.msg))

    @property
    def is_footprint(self):
        """Return if the cell is a footprint.

        Returns
        -------
        bool
        """
        return self.__stub.IsFootprint(self.msg).value

    @property
    def is_blackbox(self):
        """Return if the cell is a blackbox.

        Returns
        -------
        bool
        """
        return self.__stub.IsBlackBox(self.msg).value

    @is_blackbox.setter
    def is_blackbox(self, value):
        """Set if the cell is blackbox.

        Parameters
        ----------
        value : bool
        """
        self.__stub.SetBlackBox(messages.bool_property_message(self, value))

    @property
    def anti_pads_always_on(self):
        """Get if the anti pads is always on.

        Returns
        -------
        bool
        """
        return self.__stub.GetAntiPadsAlwaysOn(self.msg).value

    @anti_pads_always_on.setter
    def anti_pads_always_on(self, value):
        """Set the anti pads option to always-on.

        Parameters
        ----------
        value : bool
        """
        self.__stub.SetAntiPadsAlwaysOn(messages.bool_property_message(self, value))

    @property
    def anti_pads_option(self):
        """Get the anti pads option.

        Returns
        -------
        int
        """
        return self.__stub.GetAntiPadsOption(self.msg)

    @anti_pads_option.setter
    def anti_pads_option(self, value):
        """Set the anti pads option.

        Parameters
        ----------
        value : int
        """
        self.__stub.SetAntiPadsOption(messages.int_property_message(self, value))

    @property
    def is_symbolic_footprint(self):
        """Get if the cell is symbolic footprint.

        Returns
        -------
        bool
        """
        return self.__stub.IsSymbolicFootprint(self.msg).value

    @property
    def name(self):
        """Get the name of cell.

        Returns
        -------
        str
        """
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        """Set the name of cell.

        Parameters
        ----------
        value : str
        """
        self.__stub.SetName(messages.string_property_message(self, value))

    @property
    def design_mode(self):
        """Get the design mode of cell.

        Returns
        -------
        DesignMode
        """
        return DesignMode(self.__stub.GetDesignMode(self.msg).mode)

    @design_mode.setter
    def design_mode(self, value):
        """Set the design mode of cell.

        Parameters
        ----------
        value : DesignMode
        """
        self.__stub.SetDesignMode(messages.design_mode_property_message(self, value))

    @property
    def hfss_extent_info(self):
        """Get the HFSS extent info.

        Returns
        -------
        HfssExtentInfo
        """
        msg = self.__stub.GetHfssExtentInfo(self.msg)
        return HfssExtentInfo(**parse_args(msg))

    def set_hfss_extent_info(self, **extents):
        """Set HFSS Extents of this cell.

        Parameters
        ----------
        extents : dict
            Possible keys : Values where key is HfssExtentInfo attribute and value it's value.
             - use_open_region: bool
                Is Open Region used?
             - extent_type: HfssExtentInfo.HFSSExtentInfoType
                Extent type.
             - open_region_type: HfssExtentInfo.OpenRegionType
                Check to see if the PML boxes should be rendered or not.
             - base_polygon: Primitive
                Polygon to use if extent type is Polygon.
             - dielectric_extent_type: HfssExtentInfo.HFSSExtentInfoType
                Dielectric extent type.
             - dielectric_base_polygon: Primitive
                Polygon to use if dielectric extent type is Polygon.
             - dielectric: (float, bool)
                Dielectric extent size. First parameter is the value and second parameter \
                indicates if the value is a multiple.
             - honor_user_dielectric: bool
                Honoring user defined dielectric primitive when calculate dielectric extent.
             - airbox_truncate_at_ground: bool
                Whether airbox will be truncated at the ground layers.
             - airbox_horizontal: (float, bool)
                Airbox horizontal extent size. First parameter is the value and second parameter \
                indicates if the value is a multiple.
             - airbox_vertical_positive: (float, bool)
                Airbox positive vertical extent size. First parameter is the value and second parameter \
                indicates if the value is a multiple.
             - airbox_vertical_negative: (float, bool)
                Airbox negative vertical extent size. First parameter is the value and second parameter indicates \
                if the value is a multiple.
             - sync_airbox_vertical_extent: bool
                Whether airbox positive and negative vertical extent will be synchronized.
             - is_pml_visible: bool
                Check to see if the PML boxes should be rendered or not.
             - operating_frequency: Value
                PML Operating Frequency.
             - radiation_level: Value
                PML Radiation level to calculate the thickness of boundary.
             - user_xy_data_extent_for_vertical_expansion: bool
                if true, retain the old behaviour for the vertical expansion of the airbox.
                The vertical extent will be calculated from the XY data extent.
        """
        self.__stub.SetHfssExtentInfo(_QueryBuilder.set_hfss_extents(self, **extents))

    @property
    def temperature_settings(self):
        """Get the temperature settings.

        Returns
        -------
        TemperatureSettings
        """
        return TemperatureSettings(self.__stub.GetTemperatureSettings(self.msg))

    @temperature_settings.setter
    def temperature_settings(self, value):
        """Set the temperature settings.

        Parameters
        ----------
        value : TemperatureSettings
        """
        self.__stub.SetTemperatureSettings(
            messages.cell_set_temperature_settings_message(self, value)
        )

    def cutout(self, included_nets, clipped_nets, clipping_polygon, clean_clipping):
        """Cut out a cell.

        Parameters
        ----------
        included_nets : list[ansys.edb.net.Net]
        clipped_nets : list[ansys.edb.net.Net]
        clipping_polygon : ansys.edb.geometry.PolygonData
        clean_clipping : bool

        Returns
        -------
        Cell
        """
        return Cell(
            self.__stub.CutOut(
                messages.cell_cutout_message(
                    self, included_nets, clipped_nets, clipping_polygon, clean_clipping
                )
            )
        )

    def product_property_ids(self, product_id):
        """Get product property ids for a given product.

        Parameters
        ----------
        product_id : int

        Returns
        -------
        list[int]
        """
        ids = self.__stub.GetProductPropertyIds(
            messages.get_product_property_ids_message(self, product_id)
        ).ids
        return [prop_id for prop_id in ids]

    def product_property(self, product_id, property_id):
        """Get product property value.

        Parameters
        ----------
        product_id : int
        property_id : int

        Returns
        -------
        int
        """
        return self.__stub.GetProductProperty(
            messages.get_product_property_message(self, product_id, property_id)
        )

    def set_product_property(self, product_id, property_id, value):
        """Set the product property value.

        Parameters
        ----------
        product_id : int
        property_id : int
        value : int
        """
        self.__stub.SetProductProperty(
            messages.set_product_property_message(self, product_id, property_id, value)
        )

    def add_simulation_setup(self, setup_type, name, sim_setup):
        """Add a simulation setup.

        Parameters
        ----------
        setup_type : ansys.edb.simulation_setup.simulation_setup.SimulationSetupType
        name : str
        sim_setup : str
        """
        self.__stub.AddSimulationSetup(
            messages.cell_add_sim_setup_message(self, setup_type, name, sim_setup)
        )

    def delete_simulation_setup(self, name):
        """Delete a simulation setup by name.

        Parameters
        ----------
        name : str
        """
        self.__stub.DeleteSimulationSetup(messages.string_property_message(self, name))

    @property
    def simulation_setups(self):
        """Get all simulation setups of the cell.

        Returns
        -------
        list[SimulationSetup]
        """
        return [SimulationSetup(msg) for msg in self.__stub.GetSimulationSetups(self.msg)]

    def generate_auto_hfss_regions(self):
        """Generate auto HFSS regions."""
        self.__stub.GenerateAutoHFSSRegions(self.msg)

    def generate_via_smart_box(self, net_name):
        """Generate via smart box."""
        self.__stub.GenerateViaSmartBox(messages.string_property_message(self, net_name))
