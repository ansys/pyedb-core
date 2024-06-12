"""Dataset definition."""
from ansys.api.edb.v1.dataset_def_pb2_grpc import DatasetDefServiceStub

from ansys.edb.core.edb_defs import DefinitionObjType
from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner.messages import (
    edb_obj_message,
    edb_obj_name_message,
    points_property_message,
    string_property_message,
)
from ansys.edb.core.inner.parser import to_point_data_list
from ansys.edb.core.session import StubAccessor, StubType


class DatasetDef(ObjBase):
    """Represents a dataset definition."""

    __stub: DatasetDefServiceStub = StubAccessor(StubType.dataset_def)

    @classmethod
    def create(cls, database, name):
        """Create a dataset definition object.

        Parameters
        ----------
        database : :class:`.Database`
            Database to create the dataset definition in.
        name : :obj:`str`
            Name of the dataset to create.


        Returns
        -------
        DatasetDef
        """
        return DatasetDef(cls.__stub.Create(string_property_message(database, name)))

    @classmethod
    def find_by_name(cls, database, name):
        """Find a dataset definition by name in a given database.

        Parameters
        ----------
        database : :class:`.Database`
            Database to search for the dataset definition.
        name : :obj:`str`
            Name of the dataset definition.

        Returns
        -------
        DatasetDef
            Dataset definition object found.
            If a dataset isn't found, the dataset's ``is_null`` attribute is set to ``True``.
        """
        return DatasetDef(cls.__stub.FindByName(edb_obj_name_message(database, name)))

    @property
    def definition_type(self):
        """:class:`.DefinitionObjType`: Definition type."""
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
        """Get a list of data points in the dataset definition.

        Returns
        -------
        list[:class:`.PointData`]
        """
        msg = self.__stub.GetData(edb_obj_message(self))
        return msg.points

    def set_data(self, points):
        """Set a list of data points in the dataset definition.

        Parameters
        ----------
        points : list[:class:`.PointData`]
        """
        self.__stub.SetData(points_property_message(self, points))
