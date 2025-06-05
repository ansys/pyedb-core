"""Primitive Instance Collection."""
from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ansys.edb.core.geometry.polygon_data import PolygonData
    from ansys.edb.core.geometry.point_data import PointData
    from ansys.edb.core.typing import PointLike, LayerLike, NetLike
    from ansys.edb.core.layout.layout import Layout

from ansys.api.edb.v1.primitive_instance_collection_pb2 import (
    PrimitiveInstanceCollectionDataMessage,
)
from ansys.api.edb.v1.primitive_instance_collection_pb2_grpc import (
    PrimitiveInstanceCollectionServiceStub,
)

from ansys.edb.core.inner.layout_obj import LayoutObj
import ansys.edb.core.inner.messages as messages
from ansys.edb.core.inner.parser import msg_to_point_data, msg_to_polygon_data, to_polygon_data
from ansys.edb.core.inner.utils import client_stream_iterator, stream_items_from_server
from ansys.edb.core.session import StubAccessor, StubType


class PrimitiveInstanceCollection(LayoutObj):
    """Efficiently represents large quantities of geometry as \
    numerous instantiations of the same geometry at different locations."""

    __stub: PrimitiveInstanceCollectionServiceStub = StubAccessor(
        StubType.primitive_instance_collection
    )

    @staticmethod
    def _point_request_iterator(points, starting_chunk):
        chunk_entry_creator = lambda point: messages.point_message(point)
        chunk_entries_getter = lambda chunk: chunk.points.points
        return client_stream_iterator(
            points,
            PrimitiveInstanceCollectionDataMessage,
            chunk_entry_creator,
            chunk_entries_getter,
            8000,
            starting_chunk,
        )

    @classmethod
    def create(
        cls,
        layout: Layout,
        net: NetLike,
        layer: LayerLike,
        geometry: PolygonData,
        positions: List[PointLike],
    ) -> PrimitiveInstanceCollection:
        """Create a primitive instance collection containing the specified geometry instantiated \
        at the provided locations. All geometry will be created on the specified layer and net.

        Parameters
        ----------
        layout : .Layout
            Layout to create the primitive instance collection in.
        net : :term:`NetLike`
            Net that the primitive instance collection geometry will exist on.
        layer : :term:`LayerLike`
            Layer that the primitive instance collection geometry will exist on.
        geometry : .PolygonData
            The geometry that will be instantiated.
        positions : list of :term:`Point2DLike`
            The points to instantiate the geometry at.

        Returns
        -------
        .PrimitiveInstanceCollection
        """
        chunk = PrimitiveInstanceCollectionDataMessage(
            lyt_or_prim_inst_col=layout.msg,
            net=messages.net_ref_message(net),
            layer=messages.layer_ref_message(layer),
            geometry=messages.polygon_data_message(geometry),
        )
        return PrimitiveInstanceCollection(
            cls.__stub.Create(cls._point_request_iterator(positions, chunk))
        )

    @property
    @to_polygon_data
    def geometry(self) -> PolygonData:
        """:class:`.PolygonData`: The geometry that the primitive instance collection instantiates."""
        return self.__stub.GetGeometry(self.msg)

    @geometry.setter
    def geometry(self, geometry: PolygonData):
        self.__stub.SetGeometry(messages.polygon_data_property_message(self, geometry))

    @property
    def positions(self) -> List[PointData]:
        """:obj:`list` of :class:`.PointData`: The positions geometry is instantiated at."""
        return stream_items_from_server(
            msg_to_point_data, self.__stub.GetPositions(self.msg), "points"
        )

    @positions.setter
    def positions(self, positions: List[PointData]):
        chunk = PrimitiveInstanceCollectionDataMessage(lyt_or_prim_inst_col=self.msg)
        self.__stub.SetPositions(self._point_request_iterator(positions, chunk))

    @property
    def instantiated_geometry(self) -> List[PolygonData]:
        """:obj:`list` of :class:`.PolygonData`: The geometry instantiated at each location in \
        the primitive instance collection.

        This property is read-only.
        """
        return stream_items_from_server(
            msg_to_polygon_data, self.__stub.GetInstantiatedGeometry(self.msg), "polygons"
        )

    def decompose(self):
        """Decompose into individual :class:`primitives <.Primitive>`. A \
        :class:`primitive <.Primitive>` will be created for each geometry instantiation."""
        return self.__stub.Decompose(self.msg)
