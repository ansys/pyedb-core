# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Technology definition."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.database import Database

import ansys.api.edb.v1.technology_def_pb2 as pb

from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner import messages
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType
from ansys.edb.core.session import TechnologyDefServiceStub


class TechnologyDef(ObjBase):
    """Represents a technology."""

    __stub: TechnologyDefServiceStub = StubAccessor(StubType.technology)

    @classmethod
    def create(
        cls,
        database: Database,
        definition_name: str,
        technology_file: str,
        gfd_file: str = "",
        layer_filter_file: str = "",
        create_backplane: bool = False,
    ) -> TechnologyDef:
        """Create a technology definition in a given database.

        Parameters
        ----------
        database : .Database
            Database to create the technology definition in.
        definition_name : str
            Name of the technology definition.
        technology_file: str
            Path of the technology file.
        gfd_file: str
            Path of the GFD file.
        layer_filter_file: str
            Path of the layer filter file.
        create_backplane: bool
            Determines whether to create a backplane or not.

        Returns
        -------
        .TechnologyDef
        """
        return TechnologyDef(
            cls.__stub.Create(
                pb.TechnologyDefCreateMessage(
                    database=messages.edb_obj_message(database),
                    definition_name=definition_name,
                    vlc_tech_file=technology_file,
                    gfd_file=gfd_file,
                    layer_filter_file=layer_filter_file,
                    create_backplane=create_backplane,
                )
            )
        )

    @classmethod
    def find_by_name(cls, database: Database, definition_name: str) -> TechnologyDef:
        """Find a technology definition by name in a given database.

        Parameters
        ----------
        database : .Database
            Database to search for the technology definition.
        definition_name : str
            Name of the technology definition.

        Returns
        -------
        .TechnologyDef
            Technology definition object found. \
            If a technology definition isn't found, the returned technology definition is :meth:`null <.is_null>`.
        """
        return TechnologyDef(cls.__stub.FindByName(messages.edb_obj_name_message(database, definition_name)))

    def delete(self):
        """Delete the technology definition."""
        msg = messages.edb_obj_message(self)
        self.__stub.Delete(msg)

    @property
    def tech_file(self) -> str:
        """:obj:`str`: The technology file for this technology definition.

        This property is read-only.
        """
        return self.__stub.GetTechFile(self.msg).value

    @property
    def gfd_file(self) -> str:
        """:obj:`str`: The GFD file for this technology definition.

        This property is read-only.
        """
        return self.__stub.GetGFDFile(self.msg).value

    @property
    def layer_filter_file(self) -> str:
        """:obj:`str`: The layer filter file for this technology definition.

        This property is read-only.
        """
        return self.__stub.GetLayerFile(self.msg).value

    @property
    def name(self) -> str:
        """:obj:`str`: Name of the technology definition.

        This property is read-only.
        """
        return self.__stub.GetName(self.msg).value

    @property
    def is_create_backplane(self) -> str:
        """:obj:`bool`: Whether the technology definition creates a backplane.

        This property is read-only.
        """
        return self.__stub.GetIsCreateBackplane(self.msg).value
