"""RTree class."""

from ansys.api.edb.v1 import r_tree_pb2_grpc
import ansys.api.edb.v1.r_tree_pb2 as pb

from ansys.edb.core.inner import ObjBase, messages, parser
from ansys.edb.core.session import StubAccessor, StubType


class RTree(ObjBase):
    """Provides the base RTree class."""

    class RTreeObj:
        """Represents an RTree object."""

        def __init__(
            self,
            polygon,
            obj,
        ):
            """Construct an RTree object using given values.

            Parameters
            ----------
            polygon : :class:`.PolygonData`
                Polygon representation for the object in the spatial index.
            obj: ObjBase
                Object to store in the index.
            """
            self._unique_id = None
            self.polygon = polygon
            self.obj = obj

    __stub: r_tree_pb2_grpc.RTreeServiceStub = StubAccessor(StubType.r_tree)

    def __init__(self, msg):
        """Initialize an RTree object."""
        super().__init__(msg)
        self._id_to_obj = {}
        self._obj_to_id = {}
        self._unique_id = None

    @classmethod
    def create(cls, tolerance=1e-9):
        """Create an RTree.

        Parameters
        ----------
        tolerance : float, default: 1e-9
            Tolerance of the R-tree in meters.

        Returns
        -------
        RTree
            RTree created.
        """
        rtree_created = RTree(cls.__stub.Create(messages.double_message(tolerance)))
        return rtree_created

    def _handle_rtree_obj(self, rtree_obj):
        if rtree_obj._unique_id is None:
            if (rtree_obj.obj, rtree_obj.polygon) in self._obj_to_id.keys:
                rtree_obj._unique_id = self._obj_to_id[(rtree_obj.obj, rtree_obj.polygon)]
                return True
            else:
                raise Exception("RTree object does not exist in the RTree.")
        else:
            return True

    @property
    @parser.to_box
    def extent(self):
        """:obj:`tuple` of [:class:.PointData, :class:.PointData]: Bounding box \
        for the contents of the RTree."""
        return self.__stub.GetExtent(self.msg)

    def insert(self, rtree_obj):
        """Insert an RTree object from a given RTree object.

        Parameters
        ----------
        rtree_obj : :class:`.RTreeObj`
            R-tree data object with an index.
        """
        unique_id = 1 if self._unique_id is None else self._unique_id + 1
        self.__stub.InsertIntObject(RTree._r_tree_obj_message(self, rtree_obj.polygon, unique_id))
        self._unique_id = unique_id
        rtree_obj._unique_id = int(unique_id)
        self._id_to_obj[unique_id] = rtree_obj
        self._obj_to_id[(rtree_obj.obj, rtree_obj.polygon)] = unique_id

    def delete(self, rtree_obj):
        """Delete the RTree from a given RTree object.

        Parameters
        ----------
        rtree_obj : :class:`.RTreeObj`
            R-tree data object with index in this form: ``(polygon, id pair)``.
        """
        if self._handle_rtree_obj(rtree_obj):
            self.__stub.DeleteIntObject(
                RTree._r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            )
            del self._id_to_obj[rtree_obj._unique_id]
            del self._obj_to_id[(rtree_obj.obj, rtree_obj.polygon)]

    def empty(self):
        """Determine if the RTree is emppty (contains no geometry).

        Returns
        -------
        bool
            ``True`` if the RTree is empty, ``False`` otherwise.
        """
        msg_empty = self.__stub.Empty(self.msg).value
        return msg_empty

    def search(self, box, bb_search):
        """Search all objects intersecting a given box.

        Parameters
        ----------
        box : tuple[:class:`.PointData`, :class:`.PointData`]
            Testing region, described as a "lower-left, upper-right" box.
        bb_search : bool
            Whether the RTree object intersects when the bounding-box of its
            :class:`.PolygonData` instance
            intersects the testing  object. If ``False``, an explicit intersection
            is required for a hit.

        Returns
        -------
        :obj:`list` of :class:`.RTreeObj`
           List of intersecting RTree objects.
        """
        msg = self.__stub.Search(
            pb.RTreeSearchMessage(
                target=messages.edb_obj_message(self),
                box=messages.box_message(box[0], box[1]),
                bb_search=bb_search,
            )
        )
        return [self._id_to_obj[int(to_id)] for to_id in msg.props]

    def nearest_neighbor(self, rtree_obj):
        """Find the nearest neighbor of a given RTree object.

        Parameters
        ----------
        rtree_obj : :class:`.RTreeObj`
            R-tree object with index in this form: ``(polygon, id pair)``.

        Returns
        -------
        :obj:`tuple` of :class:`.RTreeObj`, tuple[.PointData, .PointData]

        - ``RTreeObj``: Nearest-neighbor in the RTree to the provided object, or null if nothing is found.
        - ``tuple[PointData, PointData]``: Line segment spanning the closest points between the object
          and the nearest neighbor.
        """
        if self._handle_rtree_obj(rtree_obj):
            msg = self.__stub.NearestNeighbor(
                RTree._r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            )
            return self._id_to_obj[int(msg.id)], parser.to_box(msg.coordinates)

    def touching_geometry(self, rtree_obj, increment_visit):
        """Find all geometries touching an RTree object.

        The provided RTree object is not returned in the touching list.

        Parameters
        ----------
        rtree_obj : :class:`.RTreeObj`
            R-tree data object with index in this form: ``(polygon, id pair)``.
        increment_visit: bool
            Whether to increment the visit counter for items returned in the list
            of connected geometries.

        Returns
        -------
        :obj:`list` of :class:`.RTreeObj`
            All touching RTree objects.
        """
        if self._handle_rtree_obj(rtree_obj):
            msg = self.__stub.TouchingGeometry(
                RTree._r_tree_geometry_request_message(
                    self, rtree_obj.polygon, rtree_obj._unique_id, increment_visit
                )
            )
            return [self._id_to_obj[int(to_id)] for to_id in msg.props]

    def connected_geometry(self, rtree_obj, increment_visit):
        """Find the connected geometries.

        If a connections exists, the provided RTree object is returned in the connected list.

        Parameters
        ----------
        rtree_obj : :class:`.RTreeObj`
            R-tree data object with index in this form: ``(polygon, id pair)``.
        increment_visit: bool
            Whether to increment the visit counter for items returned in the connected list.

        Returns
        -------
        :obj:`list` of :class:`.RTreeObj`
            List of connected geometries.
        """
        if self._handle_rtree_obj(rtree_obj):
            msg = self.__stub.ConnectedGeometry(
                RTree._r_tree_geometry_request_message(
                    self, rtree_obj.polygon, rtree_obj._unique_id, increment_visit
                )
            )
            return [self._id_to_obj[int(to_id)] for to_id in msg.props]

    @property
    def connected_geometry_sets(self):
        """:obj:`list` of :obj:`list` of :class:`.RTreeObj`: Connected geometry sets of an RTree \
         in this form: ``(ids, sizes)``."""
        msg = self.__stub.GetConnectedGeometrySets(messages.edb_obj_message(self))
        set_start = 0
        rtree_obj_sets = []
        for set_size in range(0, len(msg.sizes) - 1):
            rtree_obj_set = []
            for j in range(set_start, set_size):
                rtree_obj_set.append(self._id_to_obj[msg.id[j]])
            set_start += set_size
            rtree_obj_sets.append(rtree_obj_set)
        return rtree_obj_sets

    def increment_visit(self):
        """Increment the visit count, effectively marking all items in the tree as unvisited."""
        self.__stub.IncrementVisit(messages.edb_obj_message(self))

    def is_visited(self, rtree_obj):
        """Determine whether an RTree object has been visited.

        Parameters
        ----------
        rtree_obj : :class:`.RTreeObj`
            R-tree data object with index in this form: ``(polygon, id pair)``.

        Returns
        -------
        bool
            ``True`` if the Rtree object has been visited, ``False`` otherwise.
        """
        if self._handle_rtree_obj(rtree_obj):
            return self.__stub.IsVisited(
                RTree._r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            ).value

    def visit(self, rtree_obj):
        """Increment the count of a given RTree object.

        Parameters
        ----------
        rtree_obj : :class:`.RTreeObj`
            R-tree data object with index in this form: ``(polygon, id pair)``.
        """
        if self._handle_rtree_obj(rtree_obj):
            self.__stub.Visit(
                RTree._r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            )

    @property
    def get_visit(self):
        """:obj:`int`: Visit count for the R-tree."""
        return self.__stub.GetVisit(messages.edb_obj_message(self)).value

    @staticmethod
    def _r_tree_obj_message(rtree, polygon, prop_id):
        """Create an RTree object message."""
        return pb.RTreeObjMessage(
            target=messages.edb_obj_message(rtree),
            polygon=messages.polygon_data_message(polygon),
            prop=prop_id,
        )

    @staticmethod
    def _r_tree_geometry_request_message(rtree, polygon, prop_id, increment_visit):
        """Create an RTree geometry request message."""
        return pb.RTreeGeometryRequestMessage(
            target=messages.edb_obj_message(rtree),
            polygon=messages.polygon_data_message(polygon),
            prop=prop_id,
            increment_visit=increment_visit,
        )
