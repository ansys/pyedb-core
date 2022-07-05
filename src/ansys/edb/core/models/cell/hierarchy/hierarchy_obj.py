"""Hierarchy Obj."""

from ....interfaces.grpc import messages
from ....session import StubAccessor, StubType
from ....utility.edb_errors import handle_grpc_exception
from ....utility.transform import Transform
from ....utility.value import Value
from ...definition.component_def import ComponentDef
from ..conn_obj import ConnObj
from ..layer import Layer


class HierarchyObj(ConnObj):
    """Base class representing hierarchy object."""

    __stub = StubAccessor(StubType.hierarchy_obj)

    @handle_grpc_exception
    def get_transform(self):
        """Get transform.

        Returns
        -------
        Transform
        """
        transform_msg = self.__stub.GetTransform(self.msg)
        return Transform(
            transform_msg.scale,
            transform_msg.angle,
            transform_msg.mirror,
            transform_msg.offset_x,
            transform_msg.offset_y,
        )

    @handle_grpc_exception
    def set_transform(self, transform):
        """Set transform.

        Parameters
        ----------
        transform : Transform
        """
        return self.__stub.SetTransform(messages.transform_property_message(self, transform))

    @handle_grpc_exception
    def get_name(self):
        """Get name of the hierarchy object.

        Returns
        -------
        str
        """
        return self.__stub.GetName(self.msg).value

    @handle_grpc_exception
    def set_name(self, name):
        """Set name of the hierarchy object.

        Parameters
        ----------
        name : str
        """
        return self.__stub.SetName(messages.edb_obj_name_message(self, name))

    @handle_grpc_exception
    def get_component(self):
        """Get underlying component on the hierarchy object.

        Returns
        -------
        ComponentDef
        """
        return ComponentDef(self.__stub.GetComponent(self.msg))

    @handle_grpc_exception
    def get_placement_layer(self):
        """Get placement layer.

        Returns
        -------
        layer
        """
        return Layer(self.__stub.GetPlacementLayer(self.msg))

    @handle_grpc_exception
    def set_placement_layer(self, player):
        """Set placement layer.

        Parameters
        ----------
        player : layer
        """
        return self.__stub.SetPlacementLayer(messages.pointer_property_message(self, player))

    @handle_grpc_exception
    def get_location(self):
        """Get location.

        Returns
        -------
        pair of values
        """
        pnt_msg = self.__stub.GetLocation(self.msg)
        return [Value(pnt_msg.x), Value(pnt_msg.y)]

    @handle_grpc_exception
    def set_location(self, point):
        """Set location.

        Parameters
        ----------
        point : pair of values
        """
        return self.__stub.SetLocation(messages.point_property_message(self, point))

    @handle_grpc_exception
    def get_solve_independent_preference(self):
        """Get solve independent preference.

        Returns
        -------
        bool
        """
        return self.__stub.GetSolveIndependentPreference(self.msg).value

    @handle_grpc_exception
    def set_solve_independent_preference(self, ind):
        """Set solve independent preference.

        Parameters
        ----------
        ind : bool
        """
        return self.__stub.SetSolveIndependentPreference(messages.bool_property_message(self, ind))
