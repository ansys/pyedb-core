"""This package contains common type definitions used throughout the EDB codebase."""

from typing import Iterable, Tuple, Union

import ansys.edb.core.geometry.point_data as point_data
from ansys.edb.core.utility.value import Value

ValueLike = Union[int, float, complex, str, Value]
PointLike = Union[point_data.PointData, Iterable[ValueLike]]
Point3DLike = Tuple[ValueLike, ValueLike, ValueLike]
Triangle3DLike = Tuple[Point3DLike, Point3DLike, Point3DLike]
