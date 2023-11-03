"""Inst Array."""

from ansys.api.edb.v1.inst_array_pb2_grpc import InstArrayServiceStub

from ansys.edb.core import messages, parser
from ansys.edb.edb_defs import LayoutObjType
from ansys.edb.hierarchy import cell_instance
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Value


class InstArray(cell_instance.CellInstance):
    """Class representing an instance array object."""

    __stub: InstArrayServiceStub = StubAccessor(StubType.inst_array)
    layout_obj_type = LayoutObjType.INST_ARRAY

    @classmethod
    def create(cls, layout, name, ref, orig, xaxis, yaxis, xcount, ycount):
        """Create an instance array object with a layout.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that owns the instance array.
        name : str
            Name of instance array to be created.
        ref : :class:`Layout <ansys.edb.layout.Layout>`
            Layout that the instance array refers to.
        orig : :class:`PointData <ansys.edb.geometry.PointData>`
            PointData that represents the origin of the instance array.
        xaxis : :class:`PointData <ansys.edb.geometry.PointData>`
            PointData that represents the xaxis of the instance array.
        yaxis : :class:`PointData <ansys.edb.geometry.PointData>`
            PointData that represents the yaxis of the instance array.
        xcount : :class:`Value <ansys.edb.layout.Value>`
            Value of x count of the instance array.
        ycount : :class:`Value <ansys.edb.utility.Value>`
            Value of y count of the instance array.

        Returns
        -------
        InstArray
            Newly created instance array.
        """
        return InstArray(
            cls.__stub.Create(
                messages.inst_array_creation_message(
                    layout, name, ref, orig, xaxis, yaxis, xcount, ycount
                )
            )
        )

    @classmethod
    def find(cls, layout, name):
        """Find an instance array in layout by name.

        Parameters
        ----------
        layout : :class:`Layout <ansys.edb.layout.Layout>`
            Layout to search for the instance array in.
        name : str
            Name of the instance array to be searched for.

        Returns
        -------
        InstArray
            instance array that is found, None otherwise.
        """
        return InstArray(cls.__stub.FindByName(messages.string_property_message(layout, name)))

    @property
    @parser.to_point_data
    def orig(self):
        """:class:`PointData <geometry.PointData>`: origin of the instance array."""
        return self.__stub.GetOrig(self.msg)

    @property
    @parser.to_point_data
    def x_axis(self):
        """:class:`PointData <geometry.PointData>`: x axis of the instance array."""
        return self.__stub.GetXAxis(self.msg)

    @x_axis.setter
    def x_axis(self, value):
        self.__stub.SetXAxis(messages.point_property_message(self, value))

    @property
    @parser.to_point_data
    def y_axis(self):
        """:class:`PointData <geometry.PointData>`: y axis of the instance array."""
        return self.__stub.GetYAxis(self.msg)

    @y_axis.setter
    def y_axis(self, value):
        self.__stub.SetYAxis(messages.point_property_message(self, value))

    @property
    def x_count(self):
        """:class:`Value <ansys.edb.utility.Value>`: x count of the instance array."""
        return Value(self.__stub.GetXCount(self.msg))

    @x_count.setter
    def x_count(self, value):
        self.__stub.SetXCount(messages.value_property_message(self, value))

    @property
    def y_count(self):
        """:class:`Value <ansys.edb.utility.Value>`: y count of the instance array."""
        return Value(self.__stub.GetYCount(self.msg))

    @y_count.setter
    def y_count(self, value):
        self.__stub.SetYCount(messages.value_property_message(self, value))

    def decompose(self):
        """Decompose the instance array."""
        self.__stub.Decompose(self.msg)
