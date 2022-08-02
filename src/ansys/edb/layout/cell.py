"""Cell."""

from enum import Enum

import ansys.api.edb.v1.cell_pb2 as cell_pb2
from ansys.api.edb.v1.cell_pb2_grpc import CellServiceStub
import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2

from ansys.edb.core import LayoutObjType, ObjBase, VariableServer, messages
from ansys.edb.layout.layout import Layout
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.simulation_setup import SimulationSetup
from ansys.edb.utility import HfssExtentInfo, TemperatureSettings


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
    "dielectric": messages.hfss_extent_message,
    "airbox_horizontal": messages.hfss_extent_message,
    "airbox_vertical": messages.hfss_extent_message,
    "airbox_vertical_positive": messages.hfss_extent_message,
    "airbox_vertical_negative": messages.hfss_extent_message,
    "airbox_truncate_at_ground": messages.bool_message,
}


# takes user-provided arbitrary args and a list of allowed keywords
# return a copy including only the valid args
def sanitize_args(args):
    """Extract valid extent options and convert them into messages."""
    return {
        k: HFSS_EXTENT_ARGS[k](args[k])
        for k in filter(lambda k: k in args, HFSS_EXTENT_ARGS.keys())
    }


class _QueryBuilder:
    @staticmethod
    def create(db, cell_type, name):
        return cell_pb2.CellCreationMessage(database=db.msg, type=cell_type.value, name=name)

    @staticmethod
    def set_hfss_extents(cell, **extents):
        extents = sanitize_args(extents)
        return cell_pb2.CellSetHfssExtentsMessage(cell=cell.msg, **extents)


class Cell(ObjBase, VariableServer):
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
        VariableServer.__init__(self, msg)

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
        return Layout(self.__stub.GetLayout(self.msg))

    @property
    def flattened_layout(self):
        """Get flattened layout of the cell.

        Returns
        -------
        Layout
        """
        return Layout(self.__stub.GetFlattenedLayout(self.msg))

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
        return HfssExtentInfo(self.__stub.GetHfssExtentInfo(self.msg))

    def set_hfss_extent_info(self, **extents):
        """Set HFSS Extents of this cell.

        Parameters
        ----------
        extents : dict
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
