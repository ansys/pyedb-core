"""Skin Depth Mesh Operation."""

from .mesh_operation import MeshOperation


class SkinDepthMeshOperation(MeshOperation):
    """Class representing skin depth mesh op."""

    def __init__(
        self,
        name="",
        net_layer_info=None,
        enabled=True,
        refine_inside=False,
        mesh_region="",
        skin_depth="1um",
        surf_tri_length="1mm",
        num_layers="2",
        max_elems="1000",
        restrict_max_elem=False,
    ):
        """Initialize skin depth mesh op.

        Parameters
        ----------
        name : string, optional
        net_layer_info : list of tuple of str, str, bool, optional
        enabled : bool, optional
        refine_inside : bool, optional
        mesh_region : str, optional
        skin_depth : str, optional
        surf_tri_length : str, optional
        num_layers : str, optional
        max_elems : str, optional
        restrict_max_elem, bool, optional
        """
        super().__init__(name, net_layer_info, enabled, refine_inside, mesh_region)
        self.skin_depth = skin_depth
        self.surf_tri_length = surf_tri_length
        self.num_layers = num_layers
        self.num_layers = num_layers
        self.max_elems = max_elems
        self.restrict_max_elem = restrict_max_elem
