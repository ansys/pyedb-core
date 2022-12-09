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
    def r_tree_poly_message(rtree, polygon, prop_id):
        """Create an RTreePolyMessage."""
        return pb.RTreePolyMessage(
            target=messages.edb_obj_message(rtree),
            polygon=messages.edb_obj_message(polygon),
            id=prop_id,
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

    __stub: r_tree_pb2_grpc.RTreeServiceStub = StubAccessor(StubType.r_tree)

    @classmethod
    def create(cls, tolerance):
        """Create an RTree.

        Parameters
        ----------
        tolerance : double
            The tolerance of the R-tree, in meters.

        Returns
        -------
        RTree
            RTree created
        """
        return RTree(cls.__stub.Create(messages.double_message(tolerance)))

    @property
    @parser.to_box
    def extent(self):
        """Tuple[geometry.PointData, geometry.PointData]: Get the bounding-box for the contents of the RTree."""
        return self.__stub.GetExtent(self.msg)

    def insert_int_object(self, polygon, prop_id):
        """Insert RTree int object.

        Parameters
        ----------
        polygon: Polygon of the RTree object
        prop_id: Id of the RTree object
        """
        self.__stub.InsertIntObject(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))

    def delete_int_object(self, polygon, prop_id):
        """Delete RTree int object.

        Parameters
        ----------
        polygon: Polygon of the RTree object
        prop_id: Id of the RTree object
        """
        self.__stub.DeleteIntObject(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))

    def empty(self):
        """Empty an RTree.

        Returns
        -------
        bool
        """
        return self.__stub.Empty(self.msg).value

    def search(self, box, bb_search):
        """Search all objects intersecting the given box.

        Parameters
        ----------
        box: The testing region, described as a (lower-left, upper-right) box.
        bb_search: If true, an RTreeObj intersects when the bounding-box of it's PolygonData intersects the testing \
        object. If false, an explicit intersection is required for a hit.

        Returns
        -------
        :obj:`list` of int
            A list of intersecting RTreeObj.
        """
        msg = self.__stub.Search(_QueryBuilder.r_tree_search_message(self, box, bb_search))
        return [int(to_id) for to_id in msg.props]

    def nearest_neighbor(self, polygon, prop_id):
        """Find the nearest-neighbor of the given RTree object (polygon, id pair).

        Parameters
        ----------
        polygon: Polygon of the RTree object
        prop_id: Id of the RTree object

        Returns
        -------
        :obj:`tuple` of int, tuple[geometry.PointData, geometry.PointData]
        int: The nearest-neighbor in the RTree to the provided obj, or null if nothing is found.
        tuple[geometry.PointData, geometry.PointData]: A line-segment spanning the closest points between obj and \
        nearest.
        """
        msg = self.__stub.NearestNeighbor(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))
        return msg.id, parser.to_box(msg.coordinates)

    def touching_geometry(self, polygon, prop_id, increment_visit):
        """Find all geometry touching the provided RTree object (polygon, id pair).  Note that the  provided RTree \
        object is not returned in the touching list.

        Parameters
        ----------
        polygon: Polygon of the RTree object
        prop_id: Id of the RTree object
        increment_visit: If True, increment the visit counter for items returned in connected.

        Returns
        -------
        :obj:`list` of int
            All touching RTree objects.
        """
        msg = self.__stub.TouchingGeometry(
            _QueryBuilder.r_tree_geometry_request_message(self, polygon, prop_id, increment_visit)
        )
        return [int(to_id) for to_id in msg.props]

    def connected_geometry(self, polygon, prop_id, increment_visit):
        """Find connected geometry.  Note that, if connections exists, the provided RTree object \
        will be returned in the connected list.

        Parameters
        ----------
        polygon: Polygon of the RTree object
        prop_id: Id of the RTree object
        increment_visit: If True, increment the visit counter for items returned in connected.

        Returns
        -------
        :obj:`list` of int
            The connected geometry list.
        """
        msg = self.__stub.ConnectedGeometry(
            _QueryBuilder.r_tree_geometry_request_message(self, polygon, prop_id, increment_visit)
        )
        return [int(to_id) for to_id in msg.props]

    @property
    def connected_geometry_sets(self):
        """:obj:`tuple` of :obj:`list` of int, :obj:`list` of int (ids, sizes): Connected geometry sets of an RTree \
        (ids, sizes)."""
        msg = self.__stub.GetConnectedGeometrySets(messages.edb_obj_message(self))
        return [i for i in msg.id], [i for i in msg.sizes]

    def increment_visit(self):
        """Increment the visit count, effectively marking all items in the tree unvisited."""
        self.__stub.IncrementVisit(messages.edb_obj_message(self))

    def is_visited(self, polygon, prop_id):
        """Check whether a given object has been visited.

        Parameters
        ----------
        polygon: Polygon of the RTree object
        prop_id: Id of the RTree object

        Returns
        -------
        bool
        """
        return self.__stub.IsVisited(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id)).value

    def visit(self, polygon, prop_id):
        """Increment a given RTree object (polygon, id pair) count.

        Parameters
        ----------
        polygon: Polygon of the RTree object
        prop_id: Id of the RTree object
        """
        self.__stub.Visit(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))

    @property
    def get_visit(self):
        """Int: Visit count for the tree."""
        return self.__stub.GetVisit(messages.edb_obj_message(self)).value
