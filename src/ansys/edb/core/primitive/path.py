"""Path."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.edb.core.layout.layout import Layout
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.typing import NetLike, ValueLike, LayerLike

from enum import Enum

from ansys.api.edb.v1 import path_pb2, path_pb2_grpc

from ansys.edb.core.inner import messages, parser
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class PathEndCapType(Enum):
    """Provides an enum representing end cap types."""

    ROUND = path_pb2.ROUND
    FLAT = path_pb2.FLAT
    EXTENDED = path_pb2.EXTENDED
    CLIPPED = path_pb2.CLIPPED
    INVALID = path_pb2.INVALID_END_CAP


class PathCornerType(Enum):
    """Provides an enum representing corner types."""

    ROUND = path_pb2.ROUND_CORNER
    SHARP = path_pb2.SHARP_CORNER
    MITER = path_pb2.MITER_CORNER


class Path(Primitive):
    """Represents a path object."""

    __stub: path_pb2_grpc.PathServiceStub = StubAccessor(StubType.path)

    @classmethod
    def create(
        cls,
        layout: Layout,
        layer: LayerLike,
        net: NetLike | None,
        width: ValueLike,
        end_cap1: PathEndCapType,
        end_cap2: PathEndCapType,
        corner_style: PathCornerType,
        points: PolygonData,
    ) -> Path:
        """Create a path.

        Parameters
        ----------
        layout : .Layout
            Layout to create the path in.
        layer : :term:`LayerLike`
            Layer to place the path on.
        net : :term:`NetLike` or None
            Net of the path.
        width : :term:`ValueLike`
            Path width.
        end_cap1 : .PathEndCapType
            End cap style for the start of the path.
        end_cap2 : .PathEndCapType
            End cap style for the end of the path.
        corner_style : .PathCornerType
            Corner style.
        points : .PolygonData
            Centerline polygon data to set.

        Returns
        -------
        Path
            Path created.
        """
        return Path(
            cls.__stub.Create(
                path_pb2.PathCreationMessage(
                    layout=layout.msg,
                    layer=messages.layer_ref_message(layer),
                    net=messages.net_ref_message(net),
                    width=messages.value_message(width),
                    end_cap1=end_cap1.value,
                    end_cap2=end_cap2.value,
                    corner=corner_style.value,
                    points=messages.polygon_data_message(points),
                )
            )
        )

    @classmethod
    @parser.to_polygon_data
    def render(
        cls,
        width: ValueLike,
        end_cap1: PathEndCapType,
        end_cap2: PathEndCapType,
        corner_style: PathCornerType,
        path: PolygonData,
    ) -> PolygonData:
        """Render a path.

        Parameters
        ----------
        width : :term:`ValueLike`
            Path width.
        end_cap1 : .PathEndCapType
            End cap style for the start of the path.
        end_cap2 : .PathEndCapType
            End cap style for the end of the path.
        corner_style : .PathCornerType
            Corner style.
        path : .PolygonData
            Polygon data to set.

        Returns
        -------
        .PolygonData
            Path rendered.
        """
        return cls.__stub.Render(
            path_pb2.PathRenderMessage(
                width=messages.value_message(width),
                end_cap1=end_cap1.value,
                end_cap2=end_cap2.value,
                corner_style=corner_style.value,
                path=messages.polygon_data_message(path),
            )
        )

    @property
    @parser.to_polygon_data
    def polygon_data(self) -> PolygonData:
        """:class:`.PolygonData`: Polygon data of this Path.

        This property is read-only.
        """
        return self.__stub.GetPolygonData(self.msg)

    @property
    @parser.to_polygon_data
    def center_line(self) -> PolygonData:
        """:class:`.PolygonData`: Center line for the path."""
        return self.__stub.GetCenterLine(self.msg)

    @center_line.setter
    def center_line(self, center_line: PolygonData):
        path_pb2.SetCenterLineMessage(
            target=self.msg, center_line=messages.polygon_data_message(center_line)
        )

    def get_end_cap_style(self) -> tuple[PathEndCapType, PathEndCapType]:
        """Get end cap styles for the path.

        Returns
        -------
        tuple of (.PathEndCapType, .PathEndCapType)

            Returns a tuple in this format:

            **(end_cap1, end_cap2)**

            **end_cap1** : End cap style of path start end cap.

            **end_cap2** : End cap style of path end end cap.
        """
        end_cap_msg = self.__stub.GetEndCapStyle(self.msg)
        return PathEndCapType(end_cap_msg.end_cap1), PathEndCapType(end_cap_msg.end_cap2)

    def set_end_cap_style(self, end_cap1: PathEndCapType, end_cap2: PathEndCapType):
        """Set end cap styles for the path.

        Parameters
        ----------
        end_cap1 : .PathEndCapType
            End cap style for the start of the path.
        end_cap2 : .PathEndCapType
            End cap style for the end of the path.
        """
        self.__stub.SetEndCapStyle(
            path_pb2.SetEndCapStyleMessage(
                target=self.msg,
                end_cap=path_pb2.EndCapStyleMessage(
                    end_cap1=end_cap1.value, end_cap2=end_cap2.value
                ),
            )
        )

    def get_clip_info(self) -> tuple[PolygonData, bool]:
        """Get the data used to clip the path.

        Returns
        -------
        tuple of (.PolygonData, bool)

            Returns a tuple in this format:

            **(clipping_poly, keep_inside)**

            **clipping_poly** : PolygonData used to clip the path.

            **keep_inside** : Indicates whether the part of the path inside the polygon is preserved.
        """
        clip_info_msg = self.__stub.GetClipInfo(self.msg)
        return (
            parser.to_polygon_data(clip_info_msg.clipping_poly),
            clip_info_msg.keep_inside,
        )

    def set_clip_info(self, clipping_poly: PolygonData, keep_inside=True):
        """Set the data used to clip the path.

        Parameters
        ----------
        clipping_poly : .PolygonData
            Polygon data to use to clip the path.
        keep_inside : bool, default: True
            Whether the part of the path inside the polygon should be preserved.
        """
        self.__stub.SetClipInfo(
            path_pb2.SetClipInfoMessage(
                target=self.msg,
                clipping_poly=messages.polygon_data_message(clipping_poly),
                keep_inside=keep_inside,
            )
        )

    @property
    def corner_style(self) -> PathCornerType:
        """:class:`PathCornerType`: Corner style of the path."""
        return PathCornerType(self.__stub.GetCornerStyle(self.msg).corner_style)

    @corner_style.setter
    def corner_style(self, corner_type: PathCornerType):
        self.__stub.SetCornerStyle(
            path_pb2.SetCornerStyleMessage(
                target=self.msg,
                corner_style=path_pb2.CornerStyleMessage(corner_style=corner_type.value),
            )
        )

    @property
    def width(self) -> Value:
        """:class:`.Value`: Path width."""
        return Value(self.__stub.GetWidth(self.msg).width)

    @width.setter
    def width(self, width: ValueLike):
        self.__stub.SetWidth(
            path_pb2.SetWidthMessage(
                target=self.msg,
                width=path_pb2.WidthMessage(width=messages.value_message(width)),
            )
        )

    @property
    def miter_ratio(self) -> Value:
        """:class:`.Value`: Miter ratio."""
        return Value(self.__stub.GetMiterRatio(self.msg).miter_ratio)

    @miter_ratio.setter
    def miter_ratio(self, miter_ratio: ValueLike):
        self.__stub.SetMiterRatio(
            path_pb2.SetMiterRatioMessage(
                target=self.msg,
                miter_ratio=path_pb2.MiterRatioMessage(
                    miter_ratio=messages.value_message(miter_ratio)
                ),
            )
        )

    @property
    def can_be_zone_primitive(self) -> bool:
        """:obj:`bool`: Flag indicating if the path can be a zone.

        This property is read-only.
        """
        return True
