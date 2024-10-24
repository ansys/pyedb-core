# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
