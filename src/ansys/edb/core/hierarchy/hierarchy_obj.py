"""Hierarchy Obj."""

from ansys.edb.core.inner import conn_obj, messages
from ansys.edb.core.definition import component_def
from ansys.edb.core.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility import Transform, Value


class HierarchyObj(conn_obj.ConnObj):
    """Base class representing hierarchy object."""

    __stub = StubAccessor(StubType.hierarchy_obj)

    @property
    def transform(self):
        """:class:`Transform <ansys.edb.core.utility.Transform>`: Transformation information of the object."""
        transform_msg = self.__stub.GetTransform(self.msg)
        return Transform(
            transform_msg.scale,
            transform_msg.angle,
            transform_msg.mirror,
            transform_msg.offset_x,
            transform_msg.offset_y,
        )

    @transform.setter
    def transform(self, value):
        """Set transform."""
        self.__stub.SetTransform(messages.transform_property_message(self, value))

    @property
    def name(self):
        """:obj:`str`: Name of the object."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        """Set name of the object."""
        self.__stub.SetName(messages.edb_obj_name_message(self, value))

    @property
    def component_def(self):
        """:class:`ComponentDef <ansys.edb.core.definition.ComponentDef>`: Component definition for this \
        object if it exists, None otherwise.

        Read-Only.
        """
        return component_def.ComponentDef(self.__stub.GetComponent(self.msg))

    @property
    def placement_layer(self):
        """:class:`Layer <ansys.edb.core.layer.Layer>`: Placement layer for this object."""
        return Layer(self.__stub.GetPlacementLayer(self.msg)).cast()

    @placement_layer.setter
    def placement_layer(self, value):
        """Set placement layer."""
        self.__stub.SetPlacementLayer(messages.pointer_property_message(self, value))

    @property
    def location(self):
        """:obj:`tuple` (:class:`Value <ansys.edb.core.utility.Value>`, :class:`Value <ansys.edb.core.utility.Value>`): \
         [x, y] location of the object on the :obj:`placement_layer`."""
        pnt_msg = self.__stub.GetLocation(self.msg)
        return [Value(pnt_msg.x), Value(pnt_msg.y)]

    @location.setter
    def location(self, value):
        """Set the location on placement layer."""
        self.__stub.SetLocation(messages.point_property_message(self, value))

    @property
    def solve_independent_preference(self):
        """:obj:`bool`: Determine whether the object is assigned to solve independent of its parent context.

        True if solving independently, False if embedded.

        Notes
        -----
        For a :class:`ComponentModel <ansys.edb.core.definition.ComponentModel>`, this flag indicates if the
        model is embedded with the field-solver or not, when applicable.
        For a :class:`CellInstance <ansys.edb.core.hierarchy.CellInstance>`, it indicates if the design's
        geometry is flattened/meshed with the parent or not, when applicable.
        """
        return self.__stub.GetSolveIndependentPreference(self.msg).value

    @solve_independent_preference.setter
    def solve_independent_preference(self, value):
        """Set solve independent preference."""
        self.__stub.SetSolveIndependentPreference(messages.bool_property_message(self, value))