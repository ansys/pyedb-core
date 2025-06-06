"""Dataset definition."""
from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ansys.edb.core.database import Database
    from ansys.edb.core.geometry.point_data import PointData

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
    """A collection of data points which can be used to define piecewise functions."""

    __stub: DatasetDefServiceStub = StubAccessor(StubType.dataset_def)

    @classmethod
    def create(cls, database: Database, name: str) -> DatasetDef:
        """Create a dataset definition object.

        Parameters
        ----------
        database : .Database
            Database to create the dataset definition in.
        name : str
            Name of the dataset definition to create.

        Returns
        -------
        .DatasetDef
        """
        return DatasetDef(cls.__stub.Create(string_property_message(database, name)))

    @classmethod
    def find_by_name(cls, database: Database, name: str) -> DatasetDef:
        """Find a dataset definition by name in a given database.

        Parameters
        ----------
        database : .Database
            Database to search for the dataset definition in.
        name : str
            Name of the dataset definition.

        Returns
        -------
        .DatasetDef
            Dataset definition object found.
            If a dataset definition isn't found, the returned dataset definition is :meth:`null <.is_null>`.
        """
        return DatasetDef(cls.__stub.FindByName(edb_obj_name_message(database, name)))

    @property
    def definition_type(self) -> DefinitionObjType:
        """:class:`.DefinitionObjType`: Definition type.

        This property is read-only.
        """
        return DefinitionObjType.DATASET_DEF

    @property
    def name(self) -> str:
        """:obj:`str`: Name of the dataset definition."""
        return self.__stub.GetName(edb_obj_message(self)).value

    @name.setter
    def name(self, name: str):
        self.__stub.SetName(string_property_message(self, name))

    @to_point_data_list
    def get_data(self) -> List[PointData]:
        """Get the collection of data points the dataset definition represents.

        Returns
        -------
        list of .PointData
        """
        msg = self.__stub.GetData(edb_obj_message(self))
        return msg.points

    def set_data(self, points: List[PointData]):
        """Set the collection of data points the dataset definition represents.

        Parameters
        ----------
        points : list of .PointData
        """
        self.__stub.SetData(points_property_message(self, points))
