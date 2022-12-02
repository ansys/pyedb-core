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
        tolerance : float

        Returns
        -------
        RTree
        """
        return RTree(cls.__stub.Create(messages.double_message(tolerance)))

    @property
    @parser.to_box
    def extent(self):
        """Rtree's extent."""
        return self.__stub.GetExtent(self.msg)

    def insert_int_object(self, polygon, prop_id):
        """Insert RTree int object."""
        self.__stub.InsertIntObject(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))

    def delete_int_object(self, polygon, prop_id):
        """Delete RTree int object."""
        self.__stub.DeleteIntObject(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))

    def empty(self):
        """Empty an RTree."""
        return self.__stub.Empty(self.msg).value

    def search(self, box, bb_search):
        """Search for a node in the RTree."""
        msg = self.__stub.Search(_QueryBuilder.r_tree_search_message(self, box, bb_search))
        return [int(to_id) for to_id in msg.props]

    def nearest_neighbor(self, polygon, prop_id):
        """Nearest Neighbor for the polygon of an RTree Node."""
        msg = self.__stub.NearestNeighbor(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))
        return msg.id, parser.to_box((lambda a: a)(msg.coordinates))

    def touching_geometry(self, polygon, prop_id, increment_visit):
        """Touching geometries for the polygon of an RTree Node."""
        msg = self.__stub.TouchingGeometry(
            _QueryBuilder.r_tree_geometry_request_message(self, polygon, prop_id, increment_visit)
        )
        return [int(to_id) for to_id in msg.props]

    def connected_geometry(self, polygon, prop_id, increment_visit):
        """Connect geometries for the polygon of an RTree Node."""
        msg = self.__stub.ConnectedGeometry(
            _QueryBuilder.r_tree_geometry_request_message(self, polygon, prop_id, increment_visit)
        )
        return [int(to_id) for to_id in msg.props]

    @property
    def connected_geometry_sets(self):
        """Ge a bondwire definition."""
        msg = self.__stub.GetConnectedGeometrySets(messages.edb_obj_message(self))
        return [i for i in msg.id], [i for i in msg.sizes]

    def increment_visit(self):
        """Nearest Neighbor for the polygon of an RTree Node."""
        self.__stub.IncrementVisit(messages.edb_obj_message(self))

    def is_visited(self, polygon, prop_id):
        """Is visited value for an RTree Node."""
        return self.__stub.IsVisited(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id)).value

    def visit(self, polygon, prop_id):
        """Visit a Node of the RTree."""
        self.__stub.Visit(_QueryBuilder.r_tree_obj_message(self, polygon, prop_id))

    @property
    def get_visit(self):
        """Visit value of an RTree."""
        return self.__stub.GetVisit(messages.edb_obj_message(self)).id
