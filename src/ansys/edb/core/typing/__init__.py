# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This package contains common type definitions used throughout the EDB codebase."""

from typing import Iterable
from typing import Tuple
from typing import Union

import ansys.edb.core.geometry.point_data as point_data
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.net.net import Net
from ansys.edb.core.utility.value import Value

ValueLike = Union[int, float, complex, str, Value]
PointLike = Union[point_data.PointData, Iterable[ValueLike]]
Point3DLike = tuple[ValueLike, ValueLike, ValueLike]
Triangle3DLike = tuple[Point3DLike, Point3DLike, Point3DLike]
LayerLike = Union[Layer, str]
NetLike = Union[Net, str]
