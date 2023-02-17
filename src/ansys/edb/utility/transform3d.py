"""Transform 3D Class."""
import ansys.api.edb.v1.transform3d_pb2 as pb
from ansys.api.edb.v1.transform3d_pb2_grpc import Transform3DServiceStub
from google.protobuf import empty_pb2

from ansys.edb.core import ObjBase, messages
from ansys.edb.core.parser import to_3_point3d_data, to_point3d_data
from ansys.edb.session import StubAccessor, StubType


class _Transform3DQueryBuilder:
    @staticmethod
    def is_identity_message(target, eps, rotation):
        return pb.IsIdentityMessage(
            target=messages.edb_obj_message(target),
            eps=eps,
            rotation=rotation,
        )

    @staticmethod
    def is_equal_message(target, value, eps, rotation):
        return pb.IsEqualMessage(
            target=messages.edb_obj_message(target),
            value=messages.edb_obj_message(value),
            eps=eps,
            rotation=rotation,
        )


class Transform3D(ObjBase):
    """Represents a 3d transformation.

    Parameters
    ----------
    anchor : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    rot_axis_from : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    rot_axis_to : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    rot_angle : str, int, float, complex, Value
        Rotation angle, specified CCW in radians, from rot_axis_from towards rot_axis_to
    offset : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
    mirror : bool
        Mirror against YZ plane
    """

    __stub: Transform3DServiceStub = StubAccessor(StubType.transform3d)

    @classmethod
    def create_identity(cls):
        """Create a Transform3D.

        Returns
        -------
        Transform3D
        """
        return Transform3D(cls.__stub.CreateIdentity(empty_pb2.Empty()))

    @classmethod
    def create_copy(cls, transform3d):
        """Create a Transform3D by copying another Transform3D.

        Returns
        -------
        Transform3D
        """
        return Transform3D(cls.__stub.CreateCopy(messages.edb_obj_message(transform3d)))

    @classmethod
    def create_offset(cls, point3d):
        """Create a Transform3D with offset.

        Parameters
        ----------
        point3d : :class:`Point3DData <ansys.edb.geometry.Point3DData>`

        Returns
        -------
        Transform3D
        """
        return Transform3D(cls.__stub.CreateOffset(messages.cpos_3d_message(point3d)))

    @classmethod
    def create_center_scale(cls, point3d, scale):
        """Create a Transform3D with center and scale.

        Parameters
        ----------
        point3d : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
        scale : :obj:`float`

        Returns
        -------
        Transform3D
        """
        return Transform3D(
            cls.__stub.CreateCenterScale(messages.cpos_3d_double_message(point3d, scale))
        )

    @classmethod
    def create_rotation_from_angle(cls, point3d):
        """Create a Transform3D with rotation from angle.

        Parameters
        ----------
        point3d : :class:`Point3DData <ansys.edb.geometry.Point3DData>`

        Returns
        -------
        Transform3D
        """
        return Transform3D(cls.__stub.CreateRotationFromAngle(messages.cpos_3d_message(point3d)))

    @classmethod
    def create_rotation_from_axis(cls, x, y, z):
        """Create a Transform3D with rotation from axis.

        Parameters
        ----------
        x : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
        y : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
        z : :class:`Point3DData <ansys.edb.geometry.Point3DData>`

        Returns
        -------
        Transform3D
        """
        return Transform3D(
            cls.__stub.CreateRotationFromAxis(messages.cpos_3d_triple_message(x, y, z))
        )

    @classmethod
    def create_rotationfrom_axis_and_angle(cls, point3d, angle):
        """Create a Transform3D with axis and angle.

        Parameters
        ----------
        point3d : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
        angle : :obj:`float`

        Returns
        -------
        Transform3D
        """
        return Transform3D(
            cls.__stub.CreateRotationFromAxisAndAngle(
                messages.cpos_3d_double_message(point3d, angle)
            )
        )

    @classmethod
    def create_rotation_from_to_axis(cls, from_point3d, to_point3d):
        """Create a Transform3D with rotation from to axis.

        Parameters
        ----------
        from_point3d : :class:`Point3DData <ansys.edb.geometry.Point3DData>`
        to_point3d : :class:`Point3DData <ansys.edb.geometry.Point3DData>`

        Returns
        -------
        Transform3D
        """
        return Transform3D(
            cls.__stub.CreateRotationFromToAxis(
                messages.cpos_3d_pair_message(from_point3d, to_point3d)
            )
        )

    @classmethod
    def create_transform_2d(cls, transform_2d, z_off):
        """Create a Transform3D with Transform2D data.

        Parameters
        ----------
        transform_2d : :class:`Point3DData <ansys.edb.utility.Transform>`
        z_off : :obj:`float`

        Returns
        -------
        Transform3D
        """
        return Transform3D(
            cls.__stub.CreateTransform2D(messages.double_property_message(transform_2d, z_off))
        )

    def transpose(self):
        """Transpose transfrom3d."""
        self.__stub.Transpose(messages.edb_obj_message(self))

    def invert(self):
        """Invert transfrom3d."""
        self.__stub.Invert(messages.edb_obj_message(self))

    def is_identity(self, eps, rotation):
        """Get is identity of a Transform3d.

        Parameters
        ----------
        eps : :obj:`bool`
        rotation : :obj:`float`

        Returns
        -------
        :obj:`bool`
        """
        return self.__stub.IsIdentity(
            _Transform3DQueryBuilder.is_identity_message(self, eps, rotation)
        ).value

    def is_equal(self, other_transform, eps, rotation):
        """Equality check for two 3d transformations.

        Parameters
        ----------
        other_transform
        eps : :obj:`bool`
        rotation : :obj:`float`

        Returns
        -------
        :obj:`bool`
            Result of equality check

        """
        return self.__stub.IsEqual(
            _Transform3DQueryBuilder.is_equal_message(self, other_transform, eps, rotation)
        ).value

    def __add__(self, other_transform):
        """Add operator, concatenate two 3d transformations.

        Parameters
        ----------
        other_transform : Transform3D
            Second transformation3D

        Returns
        -------
        Transform
            A new transformation3d object.
        """
        return Transform3D(
            self.__stub.OperatorPlus(messages.pointer_property_message(self, other_transform))
        )

    @property
    @to_3_point3d_data
    def axis(self):
        """:class:`Point3DData <ansys.edb.geometry.Point3DData>`: Axis."""
        return self.__stub.GetAxis(messages.edb_obj_message(self))

    @to_point3d_data
    def transform_point(self, point):
        """Get the transform point of the Transform3d.

        Parameters
        ----------
        point : `Point3DData <geometry.Point3DData>`

        Returns
        -------
        :class:`Point3DData <ansys.edb.geometry.Point3DData>`
            TransformPoint.
        """
        return self.__stub.TransformPoint(messages.cpos_3d_property_message(self, point))

    @property
    @to_point3d_data
    def z_y_x_rotation(self):
        """:class:`Point3DData <ansys.edb.geometry.Point3DData>`: ZYXRotation."""
        return self.__stub.GetZYXRotation(messages.edb_obj_message(self))

    @property
    @to_point3d_data
    def scaling(self):
        """:class:`Point3DData <ansys.edb.geometry.Point3DData>`: Scaling."""
        return self.__stub.GetScaling(messages.edb_obj_message(self))

    @property
    @to_point3d_data
    def shift(self):
        """:class:`Point3DData <ansys.edb.geometry.Point3DData>`: Shift."""
        return self.__stub.GetShift(messages.edb_obj_message(self))

    @property
    def matrix(self):
        """:obj:`list` of :obj:`list` of :obj:`floats`: 2 dimensional 4x4 array."""
        msg = self.__stub.GetMatrix(messages.edb_obj_message(self))
        matrix = [[float(_) for _ in msg.doubles[(i - 1) * 4 : i * 4]] for i in range(1, 5)]
        return matrix

    @matrix.setter
    def matrix(self, value):
        if len(value) == 4 and len(value[0]) == 4:
            unrolled_matrix = [float(j) for submatrix in value for j in submatrix]
            self.__stub.SetMatrix(messages.doubles_property_message(self, unrolled_matrix))
