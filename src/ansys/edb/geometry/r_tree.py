"""RTree class."""

from ansys.api.edb.v1 import r_tree_pb2_grpc
import ansys.api.edb.v1.r_tree_pb2 as pb

from ansys.edb.core import ObjBase, messages, parser
from ansys.edb.session import StubAccessor, StubType


class _QueryBuilder:
    @staticmethod
    def r_tree_obj_message(rtree, polygon, prop_id):
        """Create an RTreeObjMessage."""
        return pb.RTreeObjMessage(
            target=messages.edb_obj_message(rtree),
            polygon=messages.polygon_data_message(polygon),
            prop=prop_id,
        )

    @staticmethod
    def r_tree_search_message(rtree, box, bb_search):
        """Create a RTreeSearchMessage."""
        return pb.RTreeSearchMessage(
            target=messages.edb_obj_message(rtree),
            box=messages.box_message(box[0], box[1]),
            bb_search=bb_search,
        )

    @staticmethod
    def r_tree_geometry_request_message(rtree, polygon, prop_id, increment_visit):
        """Create an RTreeGeometryRequestMessage."""
        return pb.RTreeGeometryRequestMessage(
            target=messages.edb_obj_message(rtree),
            polygon=messages.polygon_data_message(polygon),
            prop=prop_id,
            increment_visit=increment_visit,
        )


class RTree(ObjBase):
    """Class representing an RTree."""

    class RTreeObj:
        """Class representing an RTreeObj object."""

        def __init__(
            self,
            polygon,
            obj,
        ):
            """Construct a RTreeObj object using given values.

            Parameters
            ----------
            polygon: :class:`PolygonData <ansys.edb.geometry.PolygonData>`
                The polygon representation for the object in the spatial index.
            obj: ObjBase
                The object to be stored in the index.
            """
            self._unique_id = None
            self.polygon = polygon
            self.obj = obj

    __stub: r_tree_pb2_grpc.RTreeServiceStub = StubAccessor(StubType.r_tree)

    def __init__(self, msg):
        """Init method for RTree."""
        super().__init__(msg)
        self._id_to_obj = {}
        self._obj_to_id = {}
        self._unique_id = None

    @classmethod
    def create(cls, tolerance=1e-9):
        """Create an RTree.

        Parameters
        ----------
        tolerance : double
            The tolerance of the R-tree, in meters.

        Returns
        -------
        RTree
            The new RTree created.
        """
        rtree_created = RTree(cls.__stub.Create(messages.double_message(tolerance)))
        return rtree_created

    def _handle_rtree_obj(self, rtree_obj):
        if rtree_obj._unique_id is None:
            if (rtree_obj.obj, rtree_obj.polygon) in self._obj_to_id.keys:
                rtree_obj._unique_id = self._obj_to_id[(rtree_obj.obj, rtree_obj.polygon)]
                return True
            else:
                raise Exception("RTreeObj does not exist in RTree.")
        else:
            return True

    @property
    @parser.to_box
    def extent(self):
        """Tuple[geometry.PointData, geometry.PointData]: Get the bounding-box for the contents of the RTree."""
        return self.__stub.GetExtent(self.msg)

    def insert(self, rtree_obj):
        """Insert RTreeObj from the RTree object.

        Parameters
        ----------
        rtree_obj: RTreeObj
            An R-tree data object, with index.
        """
        unique_id = 1 if self._unique_id is None else self._unique_id + 1
        self.__stub.InsertIntObject(
            _QueryBuilder.r_tree_obj_message(self, rtree_obj.polygon, unique_id)
        )
        self._unique_id = unique_id
        rtree_obj._unique_id = int(unique_id)
        self._id_to_obj[unique_id] = rtree_obj
        self._obj_to_id[(rtree_obj.obj, rtree_obj.polygon)] = unique_id

    def delete(self, rtree_obj):
        """Delete RTreeObj from the RTree object.

        Parameters
        ----------
        rtree_obj: RTreeObj
            An R-tree data object, with index.
        """
        if self._handle_rtree_obj(rtree_obj):
            self.__stub.DeleteIntObject(
                _QueryBuilder.r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            )
            del self._id_to_obj[rtree_obj._unique_id]
            del self._obj_to_id[(rtree_obj.obj, rtree_obj.polygon)]

    def empty(self):
        """Check if the RTree is contains no geometry.

        Returns
        -------
        bool
        """
        msg_empty = self.__stub.Empty(self.msg).value
        return msg_empty

    def search(self, box, bb_search):
        """Search all objects intersecting the given box.

        Parameters
        ----------
        box: Tuple[:class:`PointData <geometry.PointData>`, :class:`PointData <geometry.PointData>`]
            The testing region, described as a (lower-left, upper-right) box.
        bb_search: bool
            If true, an RTreeObj intersects when the bounding-box of it's \
            :class:`PolygonData <ansys.edb.geometry.PolygonData>` intersects the testing  object. If false, an explicit\
             intersection is required for a hit.

        Returns
        -------
        :obj:`list` of RTreeObj
            A list of intersecting RTreeObj.
        """
        msg = self.__stub.Search(_QueryBuilder.r_tree_search_message(self, box, bb_search))
        return [self._id_to_obj[int(to_id)] for to_id in msg.props]

    def nearest_neighbor(self, rtree_obj):
        """Find the nearest-neighbor of the given RTree object (polygon, id pair).

        Parameters
        ----------
        rtree_obj: RTreeObj
            An R-tree data object, with index.

        Returns
        -------
        :obj:`tuple` of RTreeObj, tuple[geometry.PointData, geometry.PointData]
        RTreeObj: The nearest-neighbor in the RTree to the provided obj, or null if nothing is found.
        tuple[geometry.PointData, geometry.PointData]: A line-segment spanning the closest points between obj and \
        nearest.
        """
        if self._handle_rtree_obj(rtree_obj):
            msg = self.__stub.NearestNeighbor(
                _QueryBuilder.r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            )
            return self._id_to_obj[int(msg.id)], parser.to_box(msg.coordinates)

    def touching_geometry(self, rtree_obj, increment_visit):
        """Find all geometry touching the provided RTree object (polygon, id pair).  Note that the  provided RTree \
        object is not returned in the touching list.

        Parameters
        ----------
        rtree_obj: RTreeObj
            An R-tree data object, with index.
        increment_visit: bool
            If True, increment the visit counter for items returned in connected.

        Returns
        -------
        :obj:`list` of RTreeObj
            All touching RTree objects.
        """
        if self._handle_rtree_obj(rtree_obj):
            msg = self.__stub.TouchingGeometry(
                _QueryBuilder.r_tree_geometry_request_message(
                    self, rtree_obj.polygon, rtree_obj._unique_id, increment_visit
                )
            )
            return [self._id_to_obj[int(to_id)] for to_id in msg.props]

    def connected_geometry(self, rtree_obj, increment_visit):
        """Find connected geometry.  Note that, if connections exists, the provided RTree object \
        will be returned in the connected list.

        Parameters
        ----------
        rtree_obj: RTreeObj
            An R-tree data object, with index.
        increment_visit: If True, increment the visit counter for items returned in connected.

        Returns
        -------
        :obj:`list` of RTreeObj
            The connected geometry list.
        """
        if self._handle_rtree_obj(rtree_obj):
            msg = self.__stub.ConnectedGeometry(
                _QueryBuilder.r_tree_geometry_request_message(
                    self, rtree_obj.polygon, rtree_obj._unique_id, increment_visit
                )
            )
            return [self._id_to_obj[int(to_id)] for to_id in msg.props]

    @property
    def connected_geometry_sets(self):
        """:obj:`list` of :obj:`list` of RTreeObj: Connected geometry sets of an RTree \
        (ids, sizes)."""
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
        """Increment the visit count, effectively marking all items in the tree unvisited."""
        self.__stub.IncrementVisit(messages.edb_obj_message(self))

    def is_visited(self, rtree_obj):
        """Check whether a given object has been visited.

        Parameters
        ----------
        rtree_obj: RTreeObj
            An R-tree data object, with index.

        Returns
        -------
        bool
        """
        if self._handle_rtree_obj(rtree_obj):
            return self.__stub.IsVisited(
                _QueryBuilder.r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            ).value

    def visit(self, rtree_obj):
        """Increment a given RTree object (polygon, id pair) count.

        Parameters
        ----------
        rtree_obj: RTreeObj
            An R-tree data object, with index.
        """
        if self._handle_rtree_obj(rtree_obj):
            self.__stub.Visit(
                _QueryBuilder.r_tree_obj_message(self, rtree_obj.polygon, rtree_obj._unique_id)
            )

    @property
    def get_visit(self):
        """Int: Visit count for the tree."""
        return self.__stub.GetVisit(messages.edb_obj_message(self)).value
