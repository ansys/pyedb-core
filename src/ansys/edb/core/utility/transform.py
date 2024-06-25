"""Transformations."""
import ansys.api.edb.v1.transform_pb2 as pb
from ansys.api.edb.v1.transform_pb2_grpc import TransformServiceStub

from ansys.edb.core.inner import ObjBase, messages, parser
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class Transform(ObjBase):
    """Represents a transformation."""

    __stub: TransformServiceStub = StubAccessor(StubType.transform)

    @classmethod
    def create(cls, scale, angle, mirror, offset_x, offset_y):
        """Create a transform object.

        Parameters
        ----------
        scale : :term:`ValueLike`
            Scale parameter.
        angle : :term:`ValueLike`
            Rotation angle, specified counter-clockwise in radians.
        mirror : :obj:`bool`
            Mirror about Y-axis.
        offset_x : :term:`ValueLike`
            X offset.
        offset_y : :term:`ValueLike`
            Y offset.

        Returns
        -------
        Transform
        """
        return Transform(
            cls.__stub.Create(
                pb.TransformMessage(
                    scale=messages.value_message(scale),
                    angle=messages.value_message(angle),
                    mirror=mirror,
                    offset_x=messages.value_message(offset_x),
                    offset_y=messages.value_message(offset_y),
                )
            )
        )

    @property
    def scale(self):
        """:class:`.Value`: Scale property.

        This property can be set to :term:`ValueLike`.
        """
        return Value(self.__stub.GetScale(messages.edb_obj_message(self)))

    @scale.setter
    def scale(self, value):
        self.__stub.SetScale(messages.value_property_message(target=self, value=value))

    @property
    def rotation(self):
        """:class:`.Value`: Rotation property.

        This property can be set to :term:`ValueLike`.
        """
        return Value(self.__stub.GetRotation(messages.edb_obj_message(self)))

    @rotation.setter
    def rotation(self, value):
        self.__stub.SetRotation(messages.value_property_message(target=self, value=value))

    @property
    def offset_x(self):
        """:class:`.Value`: X offset property.

        This property can be set to :term:`ValueLike`.
        """
        return Value(self.__stub.GetOffsetX(messages.edb_obj_message(self)))

    @offset_x.setter
    def offset_x(self, value):
        self.__stub.SetOffsetX(messages.value_property_message(target=self, value=value))

    @property
    def offset_y(self):
        """:class:`.Value`: Y offset property.

        This property can be set to :term:`ValueLike`.
        """
        return Value(self.__stub.GetOffsetY(messages.edb_obj_message(self)))

    @offset_y.setter
    def offset_y(self, value):
        self.__stub.SetOffsetY(messages.value_property_message(target=self, value=value))

    @property
    def mirror(self):
        """:obj:`bool`: Mirror property. If ``True``, mirror about y axis."""
        return self.__stub.GetMirror(messages.edb_obj_message(self)).value

    @mirror.setter
    def mirror(self, value):
        self.__stub.SetMirror(messages.bool_property_message(self, value))

    @property
    def is_identity(self):
        """:obj:`bool`: Flag indicating if the transformation is an identity transformation."""
        return self.__stub.IsIdentity(messages.edb_obj_message(self)).value

    def __add__(self, other_transform):
        """Add operator and concatenate two transformations.

        Parameters
        ----------
        other_transform : Transform
            Second transformation

        Returns
        -------
        Transform
            Transformation object created.
        """
        return Transform(
            self.__stub.TransformPlus(
                pb.TransformOperatorMessage(
                    target_1=messages.edb_obj_message(self.msg),
                    target_2=messages.edb_obj_message(other_transform.msg),
                )
            )
        )

    def transform_point(self, point):
        """Transform a point.

        Parameters
        ----------
        point : :class:`.PointData`
            Point values [x, y] to transform.

        Returns
        -------
        :class:`.PointData`
            Transformed point.
        """
        pnt_msg = self.__stub.TransformPoint(messages.point_property_message(self, point))
        return Value(pnt_msg.x), Value(pnt_msg.y)

    @parser.to_polygon_data
    def transform_polygon(self, polygon):
        """Transform a polygon.

        Parameters
        ----------
        polygon : :class:`.PolygonData`
            Polygon to transform.

        Returns
        -------
        :class:`.PolygonData`
            Transformed polygon.
        """
        return self.__stub.TransformPolygon(messages.polygon_data_property_message(self, polygon))
