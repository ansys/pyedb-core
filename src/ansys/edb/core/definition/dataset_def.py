"""Dataset Def Definition."""
from ansys.api.edb.v1.dataset_def_pb2_grpc import DatasetDefServiceStub

from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    edb_obj_name_message,
    points_property_message,
    string_property_message,
)
from ansys.edb.core.inner.parser import to_point_data_list
from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.session import StubAccessor, StubType


class DatasetDef(ObjBase):
    """Class representing a dataset definition."""

    __stub: DatasetDefServiceStub = StubAccessor(StubType.dataset_def)

    @classmethod
    def create(cls, database, name):
        """Create a Dataset definition Object.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.core.database.Database>`
            Database that the dataset definition should belong to.
        name : :obj:`str`
            Name of the dataset to be created.


        Returns
        -------
        DatasetDef
        """
        return DatasetDef(cls.__stub.Create(string_property_message(database, name)))

    @classmethod
    def find_by_name(cls, database, name):
        """Find a dataset definition in the database with given name.

        Parameters
        ----------
        database : :class:`Database <ansys.edb.core.database.Database>`
            Database that owns the dataset definition.
        name : :obj:`str`
            Name of the dataset definition.

        Returns
        -------
        DatasetDef
            The dataset definition object found.
            If a dataset isn't found then dataset's is_null will result True.
        """
        return DatasetDef(cls.__stub.FindByName(edb_obj_name_message(database, name)))

    @property
    def definition_type(self):
        """:class:`DefinitionObjType`: type."""
        return DefinitionObjType.DATASET_DEF

    @property
    def name(self):
        """:obj:`str`: Name of the dataset definition."""
        return self.__stub.GetName(edb_obj_message(self)).value

    @name.setter
    def name(self, name):
        self.__stub.SetName(string_property_message(self, name))

    @to_point_data_list
    def get_data(self):
        """Get a list of data points in the DatasetDef.

        Returns
        -------
        list[:class:`PointData <ansys.edb.core.geometry.PointData>`]
        """
        msg = self.__stub.GetData(edb_obj_message(self))
        return msg.points

    def set_data(self, points):
        """Set a list of data points in the DatasetDef.

        Parameters
        ----------
        points : list[:class:`PointData <ansys.edb.core.geometry.PointData>`]
        """
        self.__stub.SetData(points_property_message(self, points))