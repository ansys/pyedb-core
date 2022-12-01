"""HFSS Extent Info."""

from enum import Enum

import ansys.api.edb.v1.edb_defs_pb2 as edb_defs_pb2

from ansys.edb.utility.value import Value


class HfssExtentInfo:
    """HFSS Extent info class."""

    class HFSSExtentInfoType(Enum):
        """Enum representing available hfss extenct info types.

        - BOUNDING_BOX
           Bounding box extent.
        - CONFORMING
           Conforming extent.
        - CONVEX_HUL
           Convex hull extent.
        - POLYGON
           Use user defined polygon as extent.
        """

        BOUNDING_BOX = edb_defs_pb2.HFSS_EXTENT_BOUNDING_BOX
        CONFORMING = edb_defs_pb2.HFSS_EXTENT_CONFIRMING
        CONVEX_HUL = edb_defs_pb2.HFSS_EXTENT_CONVEX_HULL
        POLYGON = edb_defs_pb2.HFSS_EXTENT_POLYGON

    class OpenRegionType(Enum):
        """Enum representing available open region types.

        - RADIATION
           Bounding box extent.
        - PML
           Conforming extent.
        """

        RADIATION = edb_defs_pb2.HFSS_EXTENT_RADIATION
        PML = edb_defs_pb2.HFSS_EXTENT_PML

    def __init__(
        self,
        use_open_region=True,
        extent_type=HFSSExtentInfoType.BOUNDING_BOX,
        open_region_type=OpenRegionType.RADIATION,
        base_polygon=None,
        dielectric_extent_type=HFSSExtentInfoType.BOUNDING_BOX,
        dielectric_base_polygon=None,
        dielectric=(0, True),
        honor_user_dielectric=True,
        airbox_truncate_at_ground=False,
        airbox_horizontal=(0.15, True),
        airbox_vertical_positive=(0.15, True),
        airbox_vertical_negative=(0.15, True),
        sync_airbox_vertical_extent=False,
        is_pml_visible=False,
        operating_frequency=Value("5GHz"),
        radiation_level=Value(0),
        user_xy_data_extent_for_vertical_expansion=True,
    ):
        """Create an HfssExtentInfo object.

        Parameters
        ----------
        use_open_region: bool
            Is Open Region used?
        extent_type: HfssExtentInfo.HFSSExtentInfoType
            Extent type.
        open_region_type: HfssExtentInfo.OpenRegionType
            Check to see if the PML boxes should be rendered or not.
        base_polygon: Primitive
            Polygon to use if extent type is Polygon.
        dielectric_extent_type: HfssExtentInfo.HFSSExtentInfoType
            Dielectric extent type.
        dielectric_base_polygon: :class:`Primitive <ansys.edb.primitive.Primitive>`
            Polygon to use if dielectric extent type is Polygon.
        dielectric: (float, bool)
            Dielectric extent size. First parameter is the value and second parameter \
            indicates if the value is a multiple.
        honor_user_dielectric: bool
            Honoring user defined dielectric primitive when calculate dielectric extent.
        airbox_truncate_at_ground: bool
            Whether airbox will be truncated at the ground layers.
        airbox_horizontal: (float, bool)
            Airbox horizontal extent size. First parameter is the value and second parameter \
            indicates if the value is a multiple.
        airbox_vertical_positive: (float, bool)
            Airbox positive vertical extent size. First parameter is the value and second parameter \
            indicates if the value is a multiple.
        airbox_vertical_negative: (float, bool)
            Airbox negative vertical extent size. First parameter is the value and second parameter indicates \
            if the value is a multiple.
        sync_airbox_vertical_extent: bool
            Whether airbox positive and negative vertical extent will be synchronized.
        is_pml_visible: bool
            Check to see if the PML boxes should be rendered or not.
        operating_frequency: :class:`Value <ansys.edb.utility.Value>`
            PML Operating Frequency.
        radiation_level: :class:`Value <ansys.edb.utility.Value>`
            PML Radiation level to calculate the thickness of boundary.
        user_xy_data_extent_for_vertical_expansion: bool
            if true, retain the old behaviour for the vertical expansion of the airbox.
            The vertical extent will be calculated from the XY data extent.
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
        self.operating_frequency = operating_frequency
        self.radiation_level = radiation_level
        self.user_xy_data_extent_for_vertical_expansion = user_xy_data_extent_for_vertical_expansion
