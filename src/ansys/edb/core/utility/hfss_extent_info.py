"""HFSS extent information."""
from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from ansys.edb.core.typing import ValueLike
    from ansys.edb.core.primitive.primitive import Primitive

from enum import Enum

import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2

from ansys.edb.core.utility import conversions
from ansys.edb.core.utility.value import Value


class HFSSExtentInfoType(Enum):
    """Provides an enum representing available HFSS extent information types."""

    BOUNDING_BOX = edb_defs_pb2.HFSS_EXTENT_BOUNDING_BOX
    CONFORMING = edb_defs_pb2.HFSS_EXTENT_CONFIRMING
    CONVEX_HUL = edb_defs_pb2.HFSS_EXTENT_CONVEX_HULL
    POLYGON = edb_defs_pb2.HFSS_EXTENT_POLYGON


class OpenRegionType(Enum):
    """Provides an enum representing open region types."""

    RADIATION = edb_defs_pb2.HFSS_EXTENT_RADIATION
    PML = edb_defs_pb2.HFSS_EXTENT_PML


class HfssExtentInfo:
    """Provides HFSS extent information.

    Attributes
    ----------
        use_open_region : bool, default: ``True``
            Whether an open region is used.
        extent_type : .HFSSExtentInfoType, default: BOUNDING_BOX
            Extent type.
        open_region_type : .OpenRegionType, default: RADIATION
            Open region type.
        base_polygon : .Primitive, default: None
            Polygon to use if the extent is the ``Polygon`` type.
        dielectric_extent_type : .HFSSExtentInfoType, default: BOUNDING_BOX
            Dielectric extent type.
        dielectric_base_polygon : .Primitive, default: None
            Polygon to use if dielectric extent is the ``Polygon`` type.
        dielectric : (float, bool), default: (0, True)
            Dielectric extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        honor_user_dielectric : bool, default: ``True``
            Whether to honor a user-defined dielectric primitive when calculating the dielectric
            extent.
        airbox_truncate_at_ground : bool, default: ``False``
            Whether to truncate the airbox at the ground layers.
        airbox_horizontal : (float, bool), default: (0.15, True)
            Airbox horizontal extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        airbox_vertical_positive : (float, bool), default: (0.15, True)
            Airbox positive vertical extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        airbox_vertical_negative : (float, bool), default: (0.15, True)
            Airbox negative vertical extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        sync_airbox_vertical_extent : bool, default: ``True``
            Whether to synchronize the airbox positive and negative vertical extent.
        is_pml_visible : bool, default: ``False``
            Whether to check to see if PML boxes are to be rendered.
        operating_frequency : :term:`ValueLike`, default: ``"5GHz"``
            PML operating frequency.
        radiation_level : .Value, default: 0
            PML radiation level for calculating the thickness of the boundary.
        user_xy_data_extent_for_vertical_expansion : bool, default: ``True``
            Whether to retain the old behavior for the vertical expansion of the airbox.
            The default is ``True``, in which case the vertical extent is calculated from
            the XY data extent.
    """

    def __init__(
        self,
        use_open_region: bool = True,
        extent_type: HFSSExtentInfoType = HFSSExtentInfoType.BOUNDING_BOX,
        open_region_type: OpenRegionType = OpenRegionType.RADIATION,
        base_polygon: Primitive = None,
        dielectric_extent_type: HFSSExtentInfoType = HFSSExtentInfoType.BOUNDING_BOX,
        dielectric_base_polygon: Primitive = None,
        dielectric: Tuple[float, bool] = (0, True),
        honor_user_dielectric: bool = True,
        airbox_truncate_at_ground: bool = False,
        airbox_horizontal: Tuple[float, bool] = (0.15, True),
        airbox_vertical_positive: Tuple[float, bool] = (0.15, True),
        airbox_vertical_negative: Tuple[float, bool] = (0.15, True),
        sync_airbox_vertical_extent: bool = True,
        is_pml_visible: bool = False,
        operating_frequency: ValueLike = "5GHz",
        radiation_level: Value = Value(0),
        user_xy_data_extent_for_vertical_expansion: bool = True,
    ):
        """Create an HFSS extent information object.

        Parameters
        ----------
        use_open_region : bool, default: ``True``
            Whether an open region is used.
        extent_type : .HFSSExtentInfoType, default: BOUNDING_BOX
            Extent type.
        open_region_type: .OpenRegionType, default: RADIATION
            Open region type.
        base_polygon : .Primitive, default: None
            Polygon to use if the extent is the ``Polygon`` type.
        dielectric_extent_type : .HFSSExtentInfoType, default: BOUNDING_BOX
            Dielectric extent type.
        dielectric_base_polygon : .Primitive, default: None
            Polygon to use if dielectric extent is the ``Polygon`` type.
        dielectric : (float, bool), default: (0, True)
            Dielectric extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        honor_user_dielectric : bool, default: ``True``
            Whether to honor a user-defined dielectric primitive when calculating the dielectric
            extent.
        airbox_truncate_at_ground : bool, default: ``False``
            Whether to truncate the airbox at the ground layers.
        airbox_horizontal : (float, bool), default: (0.15, True)
            Airbox horizontal extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        airbox_vertical_positive : (float, bool), default: (0.15, True)
            Airbox positive vertical extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        airbox_vertical_negative : (float, bool), default: (0.15, True)
            Airbox negative vertical extent size. The first parameter is the value.
            The second parameter is a Boolean indicating if the value is a multiple.
        sync_airbox_vertical_extent : bool, default: ``True``
            Whether to synchronize the airbox positive and negative vertical extent.
        is_pml_visible : bool, default: ``False``
            Whether to check to see if PML boxes are to be rendered.
        operating_frequency : :term:`ValueLike`, default: ``"5GHz"``
            PML operating frequency.
        radiation_level : .Value, default: 0
            PML radiation level for calculating the thickness of the boundary.
        user_xy_data_extent_for_vertical_expansion : bool, default: ``True``
            Whether to retain the old behavior for the vertical expansion of the airbox.
            The default is ``True``, in which case the vertical extent is calculated from
            the XY data extent.
        """
        self.use_open_region = use_open_region
        self.extent_type = extent_type
        self.open_region_type = open_region_type
        self.base_polygon = base_polygon
        self.dielectric_extent_type = dielectric_extent_type
        self.dielectric_base_polygon = dielectric_base_polygon
        self.dielectric = dielectric
        self.honor_user_dielectric = honor_user_dielectric
        self.airbox_truncate_at_ground = airbox_truncate_at_ground
        self.airbox_horizontal = airbox_horizontal
        self.airbox_vertical_positive = airbox_vertical_positive
        self.airbox_vertical_negative = airbox_vertical_negative
        self.sync_airbox_vertical_extent = sync_airbox_vertical_extent
        self.is_pml_visible = is_pml_visible
        self.operating_frequency = conversions.to_value(operating_frequency)
        self.radiation_level = radiation_level
        self.user_xy_data_extent_for_vertical_expansion = user_xy_data_extent_for_vertical_expansion
