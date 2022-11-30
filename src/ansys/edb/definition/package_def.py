"""Package Def Definition."""

from ansys.api.edb.v1 import package_def_pb2_grpc

from ansys.edb.core import ObjBase, parser
from ansys.edb.core.messages import (
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
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value
from ansys.edb.utility.heat_sink import HeatSink, HeatSinkFinOrientation


class PackageDef(ObjBase):
    """Class representing a package definition."""

    __stub: package_def_pb2_grpc.PackageDefServiceStub = StubAccessor(StubType.package_def)

    @classmethod
    def create(cls, db, name):
        """Create a Package definition object.

        Parameters
        ----------
        db :class:`Database <ansys.edb.database.Database>`
            Database in which we save the Package Definition.
        name : str
            Name of the Package Definition.

        Returns
        -------
        PackageDef
        """
        return PackageDef(cls.__stub.Create(string_property_message(db, name)))

    def delete(self):
        """Delete the Package definition."""
        self.__stub.Delete(edb_obj_message(self))

    @classmethod
    def find_by_name(cls, self, name):
        """Find a Package definition object by name.

        Returns
        -------
        PackageDef
        """
        return PackageDef(cls.__stub.FindByName(string_property_message(self, name)))

    @classmethod
    def find_by_id(cls, self, uid):
        """Find a Package definition object by Id.

        Returns
        -------
        PackageDef
        """
        return PackageDef(cls.__stub.FindByEDBUId(int_property_message(self, uid)))

    @property
    def name(self):
        """:obj:`str`: Name of the Package definition object."""
        return self.__stub.GetName(edb_obj_message(self)).value

    @name.setter
    def name(self, value):
        self.__stub.SetName(string_property_message(self, value))

    @property
    @parser.to_polygon_data
    def exterior_boundary(self):
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Exterior boundary for package definition."""
        return self.__stub.GetExteriorBoundary(edb_obj_message(self))

    @exterior_boundary.setter
    def exterior_boundary(self, boundary):
        self.__stub.SetExteriorBoundary(polygon_data_property_message(self, boundary))

    @property
    def height(self):
        """:class:`Value <ansys.edb.utility.Value>`: Height of the package definition object."""
        return Value(self.__stub.GetHeight(edb_obj_message(self)))

    @height.setter
    def height(self, height):
        self.__stub.SetHeight(value_property_message(self, value_message(height)))

    @property
    def operating_power(self):
        """:class:`Value <ansys.edb.utility.Value>`: Operating power of the package."""
        return Value(self.__stub.GetOperatingPower(edb_obj_message(self)))

    @operating_power.setter
    def operating_power(self, power):
        self.__stub.SetOperatingPower(value_property_message(self, value_message(power)))

    @property
    def maximum_power(self):
        """:class:`Value <ansys.edb.utility.Value>`: Maximum power of the package."""
        return Value(self.__stub.GetMaximumPower(edb_obj_message(self)))

    @maximum_power.setter
    def maximum_power(self, power):
        self.__stub.SetMaximumPower(value_property_message(self, value_message(power)))

    @property
    def thermal_conductivity(self):
        """:class:`Value <ansys.edb.utility.Value>`: Thermal conductivity of the package."""
        return Value(self.__stub.GetTherm_Cond(edb_obj_message(self)))

    @thermal_conductivity.setter
    def thermal_conductivity(self, conductivity):
        self.__stub.SetTherm_Cond(value_property_message(self, value_message(conductivity)))

    @property
    def theta_jb(self):
        """:class:`Value <ansys.edb.utility.Value>`: Theta_JB (junction to board) of the package."""
        return Value(self.__stub.GetTheta_JB(edb_obj_message(self)))

    @theta_jb.setter
    def theta_jb(self, theta):
        self.__stub.SetTheta_JB(value_property_message(self, value_message(theta)))

    @property
    def theta_jc(self):
        """:class:`Value <ansys.edb.utility.Value>`: Theta_JC (junction to case) of the package."""
        return Value(self.__stub.GetTheta_JC(edb_obj_message(self)))

    @theta_jc.setter
    def theta_jc(self, theta):
        self.__stub.SetTheta_JC(value_property_message(self, value_message(theta)))

    @property
    def heat_sink(self):
        """:class:`HeatSink <ansys.edb.utility.HeatSink>`: Assigned heat sink model for the package definition."""
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

    def get_product_property(self, prod_id, attr_it):
        """Get the product-specific property value.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.

        Returns
        -------
        str
            Property value returned.
        """
        return self.__stub.GetProductProperty(
            get_product_property_message(self, prod_id, attr_it)
        ).value

    def set_product_property(self, prod_id, attr_it, prop_value):
        """Set the product property associated with the given product and attribute ids.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.
        attr_it : int
            Attribute ID.
        prop_value : str
            Product property's new value
        """
        self.__stub.SetProductProperty(
            set_product_property_message(self, prod_id, attr_it, prop_value)
        )

    def get_product_property_ids(self, prod_id):
        """Get a list of attribute ids corresponding to a product property id.

        Parameters
        ----------
        prod_id : ProductIdType
            Product ID.

        Returns
        -------
        list[int]
            The attribute ids associated with this product property.
        """
        attr_ids = self.__stub.GetProductPropertyIds(
            get_product_property_ids_message(self, prod_id)
        ).ids
        return [attr_id for attr_id in attr_ids]
