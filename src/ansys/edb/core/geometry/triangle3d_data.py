# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Triangle 3D data."""


class Triangle3DData:
    """Represents a triangle defined by three 3D points."""

    def __init__(self, point_1, point_2, point_3):
        """Create a 3D triangle.

        Parameters
        ----------
        point_1: :class:`Point3DData`
        point_2: :class:`Point3DData`
        point_3: :class:`Point3DData`
        """
        self._point_1 = point_1
        self._point_2 = point_2
        self._point_3 = point_3

    @property
    def point_1(self):
        """:class:`Point3DData`: First 3D point."""
        return self._point_1

    @point_1.setter
    def point_1(self, point_1):
        self._point_1 = point_1

    @property
    def point_2(self):
        """:class:`Point3DData`: Second 3D point."""
        return self._point_2

    @point_2.setter
    def point_2(self, point_2):
        self._point_2 = point_2

    @property
    def point_3(self):
        """:class:`Point3DData`: Third 3D point."""
        return self._point_3

    @point_3.setter
    def point_3(self, point_3):
        self._point_3 = point_3
