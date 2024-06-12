"""Instance array."""

from ansys.api.edb.v1.inst_array_pb2_grpc import InstArrayServiceStub

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.hierarchy import cell_instance
from ansys.edb.core.inner import messages, parser
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class InstArray(cell_instance.CellInstance):
    """Represents an instance array object."""

    __stub: InstArrayServiceStub = StubAccessor(StubType.inst_array)
    layout_obj_type = LayoutObjType.CELL_INSTANCE

    @classmethod
    def create(cls, layout, name, ref, orig, xaxis, yaxis, xcount, ycount):
        """Create an instance array with a layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the instance array in.
        name : str
            Name of the instance array.
        ref : :class:`.Layout`
            Layout that the instance array refers to.
        orig : :class:`.PointData`
            Point data that represents the origin of the instance array.
        xaxis : :class:`.PointData`
            Point data that represents the x axis of the instance array.
        yaxis : :class:`.PointData`
            Point data that represents the y axis of the instance array.
        xcount : :class:`.Value`
            Value for the x count of the instance array.
        ycount : :class:`.Value`
            Value for the y count of the instance array.

        Returns
        -------
        InstArray
            Instance array created.
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
        """Find an instance array by name in a given layout.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to search for the instance array.
        name : str
            Name of the instance array.

        Returns
        -------
        InstArray
            Instance array that is found, ``None`` otherwise.
        """
        return InstArray(cls.__stub.FindByName(messages.string_property_message(layout, name)))

    @property
    @parser.to_point_data
    def orig(self):
        """:class:`.PointData`: Origin of the instance array."""
        return self.__stub.GetOrig(self.msg)

    @property
    @parser.to_point_data
    def x_axis(self):
        """:class:`.PointData`: X axis of the instance array."""
        return self.__stub.GetXAxis(self.msg)

    @x_axis.setter
    def x_axis(self, value):
        self.__stub.SetXAxis(messages.point_property_message(self, value))

    @property
    @parser.to_point_data
    def y_axis(self):
        """:class:`.PointData`: Y axis of the instance array."""
        return self.__stub.GetYAxis(self.msg)

    @y_axis.setter
    def y_axis(self, value):
        self.__stub.SetYAxis(messages.point_property_message(self, value))

    @property
    def x_count(self):
        """:class:`.Value`: X count of the instance array."""
        return Value(self.__stub.GetXCount(self.msg))

    @x_count.setter
    def x_count(self, value):
        self.__stub.SetXCount(messages.value_property_message(self, value))

    @property
    def y_count(self):
        """:class:`.Value`: Y count of the instance array."""
        return Value(self.__stub.GetYCount(self.msg))

    @y_count.setter
    def y_count(self, value):
        self.__stub.SetYCount(messages.value_property_message(self, value))

    def decompose(self):
        """Decompose the instance array."""
        self.__stub.Decompose(self.msg)
