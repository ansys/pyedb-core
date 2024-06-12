"""Package definition."""

from ansys.api.edb.v1 import package_def_pb2_grpc

from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase, parser
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    get_product_property_ids_message,
    get_product_property_message,
    int_property_message,
    polygon_data_property_message,
    set_heat_sink_message,
    set_product_property_message,
    string_property_message,
    value_message,
    value_property_message,
)
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.heat_sink import HeatSink, HeatSinkFinOrientation
from ansys.edb.core.utility.value import Value


class PackageDef(ObjBase):
    """Represents a package definition."""

    __stub: package_def_pb2_grpc.PackageDefServiceStub = StubAccessor(StubType.package_def)

    @classmethod
    def create(cls, db, name):
        """Create a package definition in a given database.

        Parameters
        ----------
        db :class:`.Database`
            Database to create the package definition in.
        name : str
            Name of the package definition.

        Returns
        -------
        PackageDef
            Package definition created.
        """
        return PackageDef(cls.__stub.Create(string_property_message(db, name)))

    @classmethod
    def find_by_name(cls, db, name):
        """Find a package definition object by name in a given database.

        Parameters
        ----------
        db :class:`.Database`
            Database to search for the package definition.
        name : str
            Name of the package definition.

        Returns
        -------
        PackageDef
            Package definition found, ``None`` otherwise.
        """
        return PackageDef(cls.__stub.FindByName(string_property_message(db, name)))

    @classmethod
    def find_by_id(cls, db, uid):
        """Find a package definition object by ID in a given database.

        Parameters
        ----------
        db :class:`.Database`
            Database to search for the package definition.
        UID : int
            Unique identifier for the package definition.

        Returns
        -------
        PackageDef
            Package definition found, ``None`` otherwise.
        """
        return PackageDef(cls.__stub.FindByEDBUId(int_property_message(db, uid)))

    @property
    def definition_type(self):
        """:class:`.DefinitionObjType`: Definition type."""
        return DefinitionObjType.PACKAGE_DEF

    @property
    def name(self):
        """:obj:`str`: Name of the package definition."""
        return self.__stub.GetName(edb_obj_message(self)).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(string_property_message(self, value))

    @property
    @parser.to_polygon_data
    def exterior_boundary(self):
        """:class:`.PolygonData`: \
        Exterior boundary of the package definition."""
        return self.__stub.GetExteriorBoundary(edb_obj_message(self))

    @exterior_boundary.setter
    def exterior_boundary(self, boundary):
        self.__stub.SetExteriorBoundary(polygon_data_property_message(self, boundary))

    @property
    def height(self):
        """:class:`.Value`: Height of the package."""
        return Value(self.__stub.GetHeight(edb_obj_message(self)))

    @height.setter
    def height(self, height):
        self.__stub.SetHeight(value_property_message(self, value_message(height)))

    @property
    def operating_power(self):
        """:class:`.Value`: Operating power of the package."""
        return Value(self.__stub.GetOperatingPower(edb_obj_message(self)))

    @operating_power.setter
    def operating_power(self, power):
        self.__stub.SetOperatingPower(value_property_message(self, value_message(power)))

    @property
    def maximum_power(self):
        """:class:`.Value`: Maximum power of the package."""
        return Value(self.__stub.GetMaximumPower(edb_obj_message(self)))

    @maximum_power.setter
    def maximum_power(self, power):
        self.__stub.SetMaximumPower(value_property_message(self, value_message(power)))

    @property
    def thermal_conductivity(self):
        """:class:`.Value`: Thermal conductivity of the package."""
        return Value(self.__stub.GetTherm_Cond(edb_obj_message(self)))

    @thermal_conductivity.setter
    def thermal_conductivity(self, conductivity):
        self.__stub.SetTherm_Cond(value_property_message(self, value_message(conductivity)))

    @property
    def theta_jb(self):
        """:class:`.Value`: Theta JB (junction to board) of the package."""
        return Value(self.__stub.GetTheta_JB(edb_obj_message(self)))

    @theta_jb.setter
    def theta_jb(self, theta):
        self.__stub.SetTheta_JB(value_property_message(self, value_message(theta)))

    @property
    def theta_jc(self):
        """:class:`.Value`: Theta JC (junction to case) of the package."""
        return Value(self.__stub.GetTheta_JC(edb_obj_message(self)))

    @theta_jc.setter
    def theta_jc(self, theta):
        self.__stub.SetTheta_JC(value_property_message(self, value_message(theta)))

    @property
    def heat_sink(self):
        """:class:`.HeatSink`: Heat sink model assigned to the package."""
        heat_sink_paramaters = self.__stub.GetHeatSink(edb_obj_message(self))
        return HeatSink(
            heat_sink_paramaters.thickness,
            heat_sink_paramaters.spacing,
            heat_sink_paramaters.base_height,
            heat_sink_paramaters.height,
            HeatSinkFinOrientation(heat_sink_paramaters.orientation),
        )

    @heat_sink.setter
    def heat_sink(self, heat_sink_value):
        self.__stub.SetHeatSink(set_heat_sink_message(self, heat_sink_value))

    def delete(self):
        """Delete the package definition."""
        self.__stub.Delete(edb_obj_message(self))

    def get_product_property(self, prod_id, attr_it):
        """Get the product property for a given product ID and attribute ID.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.

        Returns
        -------
        str
            Product property for the given product ID and attribute ID.
        """
        return self.__stub.GetProductProperty(
            get_product_property_message(self, prod_id, attr_it)
        ).value

    def set_product_property(self, prod_id, attr_it, prop_value):
        """Set the product property for the given product ID and attribute ID.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.
        prop_value : str
            New value for the product property.
        """
        self.__stub.SetProductProperty(
            set_product_property_message(self, prod_id, attr_it, prop_value)
        )

    def get_product_property_ids(self, prod_id):
        """Get the list of property IDs for a given property ID.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.

        Returns
        -------
        list[int]
            Attribute IDs for the given product ID.
        """
        attr_ids = self.__stub.GetProductPropertyIds(
            get_product_property_ids_message(self, prod_id)
        ).ids
        return [attr_id for attr_id in attr_ids]
