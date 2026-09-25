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

"""Shared test utilities for ansys-edb-core e2e tests."""

from __future__ import annotations

import pytest

from ansys.edb.core.geometry.point_data import PointData
from ansys.edb.core.geometry.polygon_data import PolygonData

# ---------------------------------------------------------------------------
# Physical unit constants (metres)
# ---------------------------------------------------------------------------

_MM = 1e-3  # 1 millimetre
_UM = 1e-6  # 1 micrometre


# ---------------------------------------------------------------------------
# Value assertions
# ---------------------------------------------------------------------------


def assert_edb_values_equal(v, expected, tol: float = 1e-12) -> None:
    """Assert that an EDB ``Value`` equals an expected value within absolute tolerance.

    Parameters
    ----------
    v : Value
        The EDB ``Value`` object to check.
    expected : float or Value
        Expected numeric value.  If a ``Value`` object, its ``.double`` attribute
        is used for comparison.
    tol : float, optional
        Absolute tolerance.  Defaults to ``1e-12``.
    """
    expected_float = expected.double if hasattr(expected, "double") else float(expected)
    assert v.double == pytest.approx(expected_float, abs=tol), (
        f"Value mismatch: expected {expected_float}, got {v.double}"
    )


# ---------------------------------------------------------------------------
# PointData assertions
# ---------------------------------------------------------------------------


def _point_sort_key(pt: PointData, tol: float = 1e-12) -> tuple:
    """Canonical sort key for PointData that supports both arc and regular points.

    Coordinates are quantized to *tol* before sorting so that two points whose
    coordinates differ by less than *tol* are treated as equal and do not cause
    the anchor selection to flip due to floating-point rounding.

    Regular points sort before arc points.  Within each group, points are
    sorted by their primary coordinate value.
    """
    if pt.is_arc:
        return (1, pt.arc_height.double, 0.0)
    # Round to the nearest multiple of tol to absorb floating-point noise.
    x = round(pt.x.double / tol) * tol
    y = round(pt.y.double / tol) * tol
    return (0, x, y)


def assert_point_datas_equal(pt1: PointData, pt2: PointData, tol: float = 1e-12) -> None:
    """Assert two ``PointData`` objects are equal within absolute tolerance.

    Handles both arc points (identified by ``is_arc``) and regular (x, y) points.

    Parameters
    ----------
    pt1, pt2 : PointData
        Points to compare.
    tol : float, optional
        Absolute tolerance for coordinate comparison.  Defaults to ``1e-12``.
    """
    assert pt1.is_arc == pt2.is_arc, f"Point type mismatch: pt1.is_arc={pt1.is_arc}, pt2.is_arc={pt2.is_arc}"
    if pt1.is_arc:
        assert pt1.arc_height.double == pytest.approx(pt2.arc_height.double, abs=tol), (
            f"Arc height mismatch: expected {pt2.arc_height.double}, got {pt1.arc_height.double}"
        )
    else:
        assert pt1.x.double == pytest.approx(pt2.x.double, abs=tol), (
            f"x mismatch: expected {pt2.x.double}, got {pt1.x.double}"
        )
        assert pt1.y.double == pytest.approx(pt2.y.double, abs=tol), (
            f"y mismatch: expected {pt2.y.double}, got {pt1.y.double}"
        )


# ---------------------------------------------------------------------------
# PolygonData assertions
# ---------------------------------------------------------------------------


def _points_match(pts1: list, pts2: list, tol: float) -> bool:
    """Return True if two anchor-aligned point lists are equal within *tol*."""
    for p1, p2 in zip(pts1, pts2):
        if p1.is_arc != p2.is_arc:
            return False
        if p1.is_arc:
            if abs(p1.arc_height.double - p2.arc_height.double) > tol:
                return False
        else:
            if abs(p1.x.double - p2.x.double) > tol:
                return False
            if abs(p1.y.double - p2.y.double) > tol:
                return False
    return True


def assert_polygon_datas_equal(
    pd1: PolygonData,
    pd2: PolygonData,
    tol: float = 1e-12,
    enforce_winding_direction: bool = True,
    check_closed: bool = True,
) -> None:
    """Assert two ``PolygonData`` objects are equal within absolute tolerance.

    Both regular polygons and arc polygons (containing arc ``PointData``
    elements) are supported.  Points from each polygon are sorted canonically
    before comparison so that the same polygon starting from different vertices
    still compares equal.

    The ``sense`` flag of both polygons is always asserted to be equal.

    When ``enforce_winding_direction`` is ``True`` (default) the vertex lists
    must also be in the same cyclic order (same winding direction).  Set to
    ``False`` when only the vertex *set* matters and the traversal direction
    is unconstrained — e.g. when the server may return the geometrically
    identical polygon in the opposite cyclic order.

    Parameters
    ----------
    pd1, pd2 : PolygonData
        Polygon data objects to compare.
    tol : float, optional
        Absolute tolerance for coordinate comparison.  Defaults to ``1e-12``.
    enforce_winding_direction : bool, optional
        When ``True`` (default) the vertex lists must traverse the polygon in
        the same cyclic order.  When ``False`` the reverse cyclic order is also
        accepted, accommodating servers that store geometrically correct
        polygons in the opposite traversal direction.  The ``sense`` flag is
        always checked regardless of this parameter.
    check_closed : bool, optional
        When ``True`` (default) the ``is_closed`` flag is asserted equal.
        Set to ``False`` when the closed state is not meaningful for the
        assertion (e.g. for centerline polylines).
    """
    # The sense flag is always checked, regardless of enforce_winding_direction.
    assert pd1.sense == pd2.sense, f"Sense mismatch: expected {pd2.sense!r}, got {pd1.sense!r}"

    pts1 = list(pd1.points)
    pts2 = list(pd2.points)
    assert len(pts1) == len(pts2), f"Vertex count mismatch: expected {len(pts2)}, got {len(pts1)}"
    # Rotate both point lists to start at their canonical anchor (minimum point
    # by _point_sort_key).  Coordinates are quantized to `tol` so that
    # floating-point noise cannot flip the anchor to a different vertex.
    anchor_idx1 = min(range(len(pts1)), key=lambda i: _point_sort_key(pts1[i], tol))
    anchor_idx2 = min(range(len(pts2)), key=lambda i: _point_sort_key(pts2[i], tol))
    pts1 = pts1[anchor_idx1:] + pts1[:anchor_idx1]
    pts2 = pts2[anchor_idx2:] + pts2[:anchor_idx2]

    # When winding direction is unconstrained, also try pts1 reversed.
    # The reversed list keeps the anchor at index 0; remaining vertices are in
    # reverse cyclic order, which is the CW↔CCW mirror image.
    forward_ok = _points_match(pts1, pts2, tol)
    if not forward_ok and not enforce_winding_direction:
        pts1_rev = [pts1[0]] + list(reversed(pts1[1:]))
        if _points_match(pts1_rev, pts2, tol):
            if check_closed:
                assert pd1.is_closed == pd2.is_closed, (
                    f"Closed flag mismatch: expected {pd2.is_closed}, got {pd1.is_closed}"
                )
            return

    # Either forward matched, or winding direction is enforced — run the
    # per-point assertions so failures produce informative messages.
    for i, (p1, p2) in enumerate(zip(pts1, pts2)):
        assert p1.is_arc == p2.is_arc, f"Point {i} type mismatch: expected is_arc={p2.is_arc}, got {p1.is_arc}"
        if p1.is_arc:
            assert p1.arc_height.double == pytest.approx(p2.arc_height.double, abs=tol), (
                f"Point {i} arc_height: expected {p2.arc_height.double}, got {p1.arc_height.double}"
            )
        else:
            assert p1.x.double == pytest.approx(p2.x.double, abs=tol), (
                f"Point {i} x: expected {p2.x.double}, got {p1.x.double}"
            )
            assert p1.y.double == pytest.approx(p2.y.double, abs=tol), (
                f"Point {i} y: expected {p2.y.double}, got {p1.y.double}"
            )
    if check_closed:
        assert pd1.is_closed == pd2.is_closed, f"Closed flag mismatch: expected {pd2.is_closed}, got {pd1.is_closed}"
