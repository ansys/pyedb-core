"""3D transformformations."""
from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ansys.edb.core.typing import Point3DLike
    from ansys.edb.core.geometry.point3d_data import Point3DData
    from ansys.edb.core.utility.transform import Transform

import ansys.api.edb.v1.transform_3d_pb2 as pb
from ansys.api.edb.v1.transform_3d_pb2_grpc import Transform3DServiceStub
from google.protobuf import empty_pb2

from ansys.edb.core.inner import ObjBase, messages
from ansys.edb.core.inner.parser import to_3_point3d_data, to_point3d_data
from ansys.edb.core.session import StubAccessor, StubType


class Transform3D(ObjBase):
    """Represents a 3D transformation.

    Parameters
    ----------
    anchor : :term:`Point3DLike`
    rot_axis_from : :term:`Point3DLike`
    rot_axis_to : :term:`Point3DLike`
    rot_angle : :term:`ValueLike`
        Rotation angle, specified counter-clockwise in radians, from the ``rot_axis_from`` parameter
        towards the ``rot_axis_to`` parameter.
    offset : :term:`Point3DLike`
    mirror : bool
        Mirror against the YZ plane.
    """

    __stub: Transform3DServiceStub = StubAccessor(StubType.transform3d)

    @classmethod
    def create_identity(cls) -> Transform3D:
        """Create an identity transformation 3D matrix.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(cls.__stub.CreateIdentity(empty_pb2.Empty()))

    @classmethod
    def create_copy(cls, transform3d: Transform3D) -> Transform3D:
        """Create a 3D transformation by copying another 3D transformation.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(cls.__stub.CreateCopy(messages.edb_obj_message(transform3d)))

    @classmethod
    def create_from_matrix(cls, matrix: List[List[float]]) -> Transform3D:
        """Create a 3D transformation from general matrix data.

        Parameters
        ----------
        matrix : :obj:`list` of :obj:`list` of :obj:`floats`
            Array (4x4) to copy from.

        Returns
        -------
        .Transform3D
        """
        trans = Transform3D(cls.__stub.CreateIdentity(empty_pb2.Empty()))
        trans.matrix = matrix
        return trans

    @classmethod
    def create_from_offset(cls, offset: Point3DLike) -> Transform3D:
        """Create a 3D transformation with an offset.

        Parameters
        ----------
        offset : :term:`Point3DLike`
            Vector offset.
        Returns
        -------
        .Transform3D
        """
        return Transform3D(cls.__stub.CreateOffset(messages.cpos_3d_message(offset)))

    @classmethod
    def create_from_center_scale(cls, center: Point3DLike, scale: float) -> Transform3D:
        """Create a 3D transformation for scaling about a point.

        Parameters
        ----------
        center : :term:`Point3DLike`
            Center of the transformation.
        scale : :obj:`float`
            Scale factor of the transformation.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(
            cls.__stub.CreateCenterScale(messages.cpos_3d_double_message(center, scale))
        )

    @classmethod
    def create_from_angle(cls, zyx_decomposition: Point3DLike) -> Transform3D:
        """Create a 3D transformation from ZYX decomposition.

        Parameters
        ----------
        zyx_decomposition : :term:`Point3DLike`
            ZYX decomposition.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(
            cls.__stub.CreateRotationFromAngle(messages.cpos_3d_message(zyx_decomposition))
        )

    @classmethod
    def create_from_axis(cls, x: Point3DLike, y: Point3DLike, z: Point3DLike) -> Transform3D:
        """Create a 3D transformation with a rotation matrix from three axes.

        Parameters
        ----------
        x : :term:`Point3DLike`
            X axis.
        y : :term:`Point3DLike`
            Y axis.
        z : :term:`Point3DLike`
            Z axis.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(
            cls.__stub.CreateRotationFromAxis(messages.cpos_3d_triple_message(x, y, z))
        )

    @classmethod
    def create_from_axis_and_angle(cls, axis: Point3DLike, angle: float) -> Transform3D:
        """Create a 3D transformation with the given axis and angle.

        Parameters
        ----------
        axis : :term:`Point3DLike`
            Axis.
        angle : :obj:`float`
            Angle.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(
            cls.__stub.CreateRotationFromAxisAndAngle(messages.cpos_3d_double_message(axis, angle))
        )

    @classmethod
    def create_from_one_axis_to_another(
        cls, from_axis: Point3DLike, to_axis: Point3DLike
    ) -> Transform3D:
        """Create a 3D transformformation with rotation from an axis to an axis.

        Parameters
        ----------
        from_axis : :term:`Point3DLike`
            From axis.
        to_axis : :term:`Point3DLike`
            To axis.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(
            cls.__stub.CreateRotationFromToAxis(messages.cpos_3d_pair_message(from_axis, to_axis))
        )

    @classmethod
    def create_from_transform_2d(cls, transform: Transform, z_off: float) -> Transform3D:
        """Create a 3D transformation with transform data.

        Parameters
        ----------
        transform : .Transform
            Transform data.
        z_off : :obj:`float`
            Z offset.

        Returns
        -------
        .Transform3D
        """
        return Transform3D(
            cls.__stub.CreateTransform2D(messages.double_property_message(transform, z_off))
        )

    def transpose(self):
        """Transpose the 3D transformation."""
        self.__stub.Transpose(messages.edb_obj_message(self))

    def invert(self):
        """Invert the 3D transformation."""
        self.__stub.Invert(messages.edb_obj_message(self))

    def is_identity(self, eps: float, rotation: bool) -> bool:
        """Get identity of the 3D transformation.

        Parameters
        ----------
        rotation : bool
        eps : float

        Returns
        -------
        bool
        """
        return self.__stub.IsIdentity(
            pb.IsIdentityMessage(
                target=messages.edb_obj_message(self),
                eps=eps,
                rotation=rotation,
            )
        ).value

    def is_equal(self, other_transform: Transform3D, rotation: bool, eps: float) -> bool:
        """Equality check for two #D transformations.

        Parameters
        ----------
        other_transform
        rotation : bool
        eps : float

        Returns
        -------
        bool
            Result of equality check.
        """
        return self.__stub.IsEqual(
            pb.IsEqualMessage(
                target=messages.edb_obj_message(self),
                value=messages.edb_obj_message(other_transform),
                eps=eps,
                rotation=rotation,
            )
        ).value

    def __add__(self, other_transform: Transform3D) -> Transform3D:
        """Add operator and concatenate two 3D transformations.

        Parameters
        ----------
        other_transform : .Transform3D
            Second 3D transformation.

        Returns
        -------
        .Transform3D
            3D transformation object created.
        """
        return Transform3D(
            self.__stub.OperatorPlus(messages.pointer_property_message(self, other_transform))
        )

    @property
    @to_3_point3d_data
    def axis(self) -> Point3DData:
        """:obj:`list` of :term:`Point3DLike`: Axis."""
        return self.__stub.GetAxis(messages.edb_obj_message(self))

    @to_point3d_data
    def transform_point(self, point: Point3DLike) -> Point3DData:
        """Get the transform point of the 3D transformation.

        Parameters
        ----------
        point : :term:`Point3DLike`

        Returns
        -------
        .Point3DData
            Transform point.
        """
        return self.__stub.TransformPoint(messages.cpos_3d_property_message(self, point))

    @property
    @to_point3d_data
    def z_y_x_rotation(self) -> Point3DData:
        """:class:`.Point3DData`: ZYX rotation.

        This property is read-only.
        """
        return self.__stub.GetZYXRotation(messages.edb_obj_message(self))

    @property
    @to_point3d_data
    def scaling(self) -> Point3DData:
        """:class:`.Point3DData`: Scaling.

        This property is read-only.
        """
        return self.__stub.GetScaling(messages.edb_obj_message(self))

    @property
    @to_point3d_data
    def shift(self) -> Point3DData:
        """:class:`.Point3DData`: Shift.

        This property is read-only.
        """
        return self.__stub.GetShift(messages.edb_obj_message(self))

    @property
    def matrix(self) -> List[List[float]]:
        """:obj:`list` of :obj:`list` of :obj:`float` : Transformation matrix as a 2D 4x4 array."""
        msg = self.__stub.GetMatrix(messages.edb_obj_message(self))
        matrix = [[float(_) for _ in msg.doubles[(i - 1) * 4 : i * 4]] for i in range(1, 5)]
        return matrix

    @matrix.setter
    def matrix(self, value: List[List[float]]):
        if (
            len(value) == 4
            and len(value[0]) == 4
            and len(value[1]) == 4
            and len(value[2]) == 4
            and len(value[3]) == 4
        ):
            unrolled_matrix = [float(j) for submatrix in value for j in submatrix]
            self.__stub.SetMatrix(messages.doubles_property_message(self, unrolled_matrix))
