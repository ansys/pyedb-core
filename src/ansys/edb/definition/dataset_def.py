"""Dataset Def Definition."""
import ansys.api.edb.v1.dataset_def_pb2 as pb
from ansys.api.edb.v1.dataset_def_pb2_grpc import DatasetDefServiceStub

from ansys.edb.core import ObjBase, parser
from ansys.edb.core.messages import (
    edb_obj_message,
    edb_obj_name_message,
    point_message,
    string_property_message,
)
from ansys.edb.session import StubAccessor, StubType


class _QueryBuilder:
    @staticmethod
    def data_message(points):
        return pb.DatasetDefDataMessage(points=points)

    @staticmethod
    def set_data_message(dataset, points):
        return pb.SetDatasetDefDataMessage(
            target=edb_obj_message(dataset), value=_QueryBuilder.data_message(points)
        )


class DatasetDef(ObjBase):
    """Class representing a dataset definition."""

    __stub: DatasetDefServiceStub = StubAccessor(StubType.dataset_def)

    @classmethod
    def create(cls, db, name):
        """Create a Dataset definition Object.

        Parameters
        ----------
        db : :class:`Database <ansys.edb.database.Database>`
            Database that the dataset definition should belong to.
        name : :obj:`str`
            Name of the component definition to be created.


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
        database : :class:`Database <ansys.edb.database.Database>`
            Database that owns the dataset definition.
        name : :obj:`str`
            Name of the dataset definition.

        Returns
        -------
        DatasetDef
            The dataset definition object found.
        """
        return DatasetDef(cls.__stub.FindByName(edb_obj_name_message(database, name)))

    @property
    def name(self):
        """:obj:`str`: Name of the dataset definition.

        Read-Only.
        """
        return self.__stub.GetName(edb_obj_message(self)).value

    @name.setter
    def name(self, name):
        self.__stub.SetName(string_property_message(self, name))

    @parser.to_point_data_list
    def get_data(self):
        """Get a list of data points in the DatasetDef.

        Returns
        -------
        list[:class:`PointData <ansys.edb.geometry.point_data.PointData>`]
        """
        msg = self.__stub.GetData(edb_obj_message(self))
        return msg.points

    def set_data(self, points):
        """Set a list of data points in the DatasetDef.

        Parameters
        ----------
        points : list[:class:`PointData <ansys.edb.geometry.point_data.PointData>`]
        """
        self.__stub.SetData(
            _QueryBuilder.set_data_message(self, [point_message(point) for point in points])
        )
