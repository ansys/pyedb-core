"""Hierarchy Obj."""

from ansys.edb.core import conn_obj, messages
from ansys.edb.definition import component_def
from ansys.edb.layer import Layer
from ansys.edb.session import StubAccessor, StubType
from ansys.edb.utility import Transform, Value


class HierarchyObj(conn_obj.ConnObj):
    """Base class representing hierarchy object."""

    __stub = StubAccessor(StubType.hierarchy_obj)

    @property
    def transform(self):
        """Get the transformation information of the object.

        This property can also be used to set the transform.

        Returns
        -------
        :class:`Transform <ansys.edb.utility.transform.Transform>`
        """
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
        """Set transform.

        Parameters
        ----------
        value : :class:`Transform <ansys.edb.utility.transform.Transform>`
        """
        self.__stub.SetTransform(messages.transform_property_message(self, value))

    @property
    def name(self):
        """Get name of the hierarchy object.

        This property can also be used to set the name.

        Returns
        -------
        str
        """
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, value):
        """Set name of the hierarchy object.

        Parameters
        ----------
        value : str
        """
        self.__stub.SetName(messages.edb_obj_name_message(self, value))

    @property
    def component(self):
        """Get the component definition for this hierarchy object.

        Returns
        -------
        :class:`ComponentDef <ansys.edb.definition.component_def.ComponentDef>`
            Component definition if it exists, None otherwise.
        """
        return component_def.ComponentDef(self.__stub.GetComponent(self.msg))

    @property
    def placement_layer(self):
        """Get placement layer for this hierarchy object.

        This property can also be used to set the placement layer.

        Returns
        -------
        :class:`Layer <ansys.edb.layer.Layer>`
        """
        return Layer(self.__stub.GetPlacementLayer(self.msg))

    @placement_layer.setter
    def placement_layer(self, value):
        """Set placement layer.

        Parameters
        ----------
        value : :class:`Layer <ansys.edb.layer.Layer>`
        """
        self.__stub.SetPlacementLayer(messages.pointer_property_message(self, value))

    @property
    def location(self):
        """Get the location on placement layer.

        This property can also be used to set the location.

        Returns
        -------
        tuple[:class:`Value <ansys.edb.utility.value.Value>`]
            The [x, y] location of the object on placement layer.
        """
        pnt_msg = self.__stub.GetLocation(self.msg)
        return [Value(pnt_msg.x), Value(pnt_msg.y)]

    @location.setter
    def location(self, value):
        """Set the location on placement layer.

        Parameters
        ----------
        value : tuple[:class:`Value <ansys.edb.utility.value.Value>`]
        """
        self.__stub.SetLocation(messages.point_property_message(self, value))

    @property
    def solve_independent_preference(self):
        """Get whether the object is assigned to solve independent of its parent context.

        This property can also be used to set the solve-independent preference.

        Returns
        -------
        bool
            True if solving independently, False if embedded.

        Notes
        -----
        For a :class:`ComponentModel <ansys.edb.definition.component_model.ComponentModel>`, this flag indicates if the
        model is embedded with the field-solver or not, when applicable.
        For a :class:`CellInstance <ansys.edb.hierarchy.cell_instance.CellInstance>`, it indicates if the design's
        geometry is flattened/meshed with the parent or not, when applicable.
        """
        return self.__stub.GetSolveIndependentPreference(self.msg).value

    @solve_independent_preference.setter
    def solve_independent_preference(self, value):
        """Set solve independent preference.

        Parameters
        ----------
        value : bool
        """
        self.__stub.SetSolveIndependentPreference(messages.bool_property_message(self, value))
