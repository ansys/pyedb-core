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

"""Layout Component."""
from ansys.api.edb.v1.layout_component_pb2 import ImportExportLayoutComponentMessage

from ansys.edb.core.hierarchy.cell_instance import CellInstance
from ansys.edb.core.inner.layout_obj import ObjBase
from ansys.edb.core.session import LayoutComponentServiceStub, StubAccessor, StubType


def _import_export_layout_component_msg(layout, output_aedb_comp_path):
    return ImportExportLayoutComponentMessage(
        layout=layout.msg, aedbcomp_path=output_aedb_comp_path
    )


class LayoutComponent(ObjBase):
    """Class representing a layout component."""

    __stub: LayoutComponentServiceStub = StubAccessor(StubType.layout_component)

    @classmethod
    def export_layout_component(cls, layout, output_aedb_comp_path):
        """Export a layout component of the provided cell to the specified output file path.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to be exported.
        output_aedb_comp_path : str
            File path to export the .aedbcomp file to.

        Returns
        -------
        bool
            ``True`` if layout component is successfully exported, ``False`` otherwise.
        """
        return cls.__stub.ExportLayoutComponent(
            _import_export_layout_component_msg(layout, output_aedb_comp_path)
        )

    @classmethod
    def import_layout_component(cls, layout, aedb_comp_path):
        """Import a layout component from the .aedbcomp file at the specified file path into the provided layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout the layout component will be imported into.
        aedb_comp_path : str
            File path of the .aedbcomp file to import the layout component from.

        Returns
        -------
        :class:`.LayoutComponent`
            Imported layout component
        """
        return LayoutComponent(
            cls.__stub.ImportLayoutComponent(
                _import_export_layout_component_msg(layout, aedb_comp_path)
            )
        )

    @property
    def cell_instance(self):
        """:class:`.CellInstance`: The underlying cell instance of the layout component."""
        return CellInstance(self.__stub.GetCellInstance(self.msg))
