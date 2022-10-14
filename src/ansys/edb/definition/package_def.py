"""Package Def Definition."""

from enum import Enum

from ansys.api.edb.v1 import package_def_pb2_grpc
import ansys.api.edb.v1.package_def_pb2 as pb

from ansys.edb.core import ObjBase, parser
from ansys.edb.core.messages import (
    edb_obj_message,
    get_product_property_ids_message,
    get_product_property_message,
    int_property_message,
    set_polygon_data_property_message,
    set_product_property_message,
    string_property_message,
    value_message,
    value_property_message,
)
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value


class _DielectricMaterialModelQueryBuilder:
    @staticmethod
    def heat_sink_message(thickness, spacing, base_height, height, orientation):
        return pb.HeatSinkMessage(
            thickness=value_message(thickness),
            spacing=value_message(spacing),
            base_height=value_message(base_height),
            height=value_message(height),
            orientation=orientation.value,
        )

    @staticmethod
    def set_heat_sink_message(target, thickness, spacing, base_height, height, orientation):
        return pb.SetHeatSinkMessage(
            target=edb_obj_message(target),
            value=_DielectricMaterialModelQueryBuilder.heat_sink_message(
                thickness, spacing, base_height, height, orientation
            ),
        )


class HeatSinkOrientation(Enum):
    """Enum representing bondwire types.

    - X_ORIENTED
       X axis oriented.
    - Y_ORIENTED
       Y axis oriented.
    - OTHER_ORIENTED
       Other oriented.
    """

    X_ORIENTED = pb.X_ORIENTED
    Y_ORIENTED = pb.Y_ORIENTED
    OTHER_ORIENTED = pb.OTHER_ORIENTED


class PackageDef(ObjBase):
    """Class representing a package definition."""

    __stub: package_def_pb2_grpc.PackageDefServiceStub = StubAccessor(StubType.package_def)

    @classmethod
    def create(cls, db, name):
        """Create a Package definition object.

        Parameters
        ----------
        db
        name

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
        """:class:`PolygonData <ansys.edb.geometry.PolygonData>`: Exterior doundary for package definition."""
        return self.__stub.GetExteriorBoundary(edb_obj_message(self))

    @exterior_boundary.setter
    def exterior_boundary(self, boundary):
        self.__stub.SetExteriorBoundary(set_polygon_data_property_message(self, boundary))

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
    def thermal_condactivity(self):
        """:class:`Value <ansys.edb.utility.Value>`: Relative permitivity at optical frequency."""
        return Value(self.__stub.GetTherm_Cond(edb_obj_message(self)))

    @thermal_condactivity.setter
    def thermal_condactivity(self, condactivity):
        self.__stub.SetTherm_Cond(value_property_message(self, value_message(condactivity)))

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

    def get_heat_sink(self):
        """Get the assigned heat sink model for the package definition.

        Returns
        -------
        thickness : ValueLike
            Heat sink's thinkness.
        spacing : ValueLike
            Heat sink's spacing.
        base_height : ValueLike
            Heat sink's base height.
        height : ValueLike
            Heat sink's height.
        orientation : :class:`HeatSinkOrientation`
            Heat sink's orientation.
        """
        heat_sink_paramaters = self.__stub.GetHeatSink(edb_obj_message(self))
        return (
            Value(heat_sink_paramaters.thickness),
            Value(heat_sink_paramaters.spacing),
            Value(heat_sink_paramaters.base_height),
            Value(heat_sink_paramaters.height),
            HeatSinkOrientation(heat_sink_paramaters.orientation),
        )

    def set_heat_sink(self, thickness, spacing, base_height, height, orientation):
        """Set the assigned heat sink model for the package definition.

        Parameters
        ----------
        thickness : ValueLike
            Heat sink's thinkness.
        spacing : ValueLike
            Heat sink's spacing.
        base_height : ValueLike
            Heat sink's base height.
        height : ValueLike
            Heat sink's height.
        orientation : :class:`HeatSinkOrientation`
            Heat sink's orientation.
        """
        self.__stub.SetHeatSink(
            _DielectricMaterialModelQueryBuilder.set_heat_sink_message(
                self, thickness, spacing, base_height, height, orientation
            )
        )

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
