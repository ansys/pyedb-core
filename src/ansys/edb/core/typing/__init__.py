"""This package contains common type definitions used throughout edb codebase."""

from typing import Iterable, Union

import ansys.edb.core.geometry.point_data as point_data
import ansys.edb.core.utility.value as value

ValueLike = Union[int, float, complex, str, value.Value]
PointLike = Union[point_data.PointData, Iterable[ValueLike]]
