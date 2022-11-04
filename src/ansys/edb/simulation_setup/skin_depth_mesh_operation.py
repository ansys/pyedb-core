"""Skin Depth Mesh Operation."""

from ansys.edb.simulation_setup.mesh_operation import MeshOperation


class SkinDepthMeshOperation(MeshOperation):
    """Class representing skin depth mesh op.

    Parameters
    ----------
    name : str, optional
        Name of the operation.
    net_layer_info : list[tuple(str, str, bool)], optional
        Each entry has net name, layer name, and isSheet which is True if it is a sheet object.
    enabled : bool, optional
        True if mesh operation is enabled.
    refine_inside : bool, optional
        True if should refine inside.
    mesh_region : str, optional
        Mesh region.
    skin_depth : str, optional
        Skin depth (number with optional length units).
    surf_tri_length : str, optional
        Surface triangle length (number with optional length units).
    num_layers : str, optional
        Number of layers (integer).
    max_elems : str, optional
        Maximum number of elements (integer).
    restrict_max_elem : bool, optional
        True if we restrict the number of elements.
    """

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
        """Initialize skin depth mesh op."""
        super().__init__(name, net_layer_info, enabled, refine_inside, mesh_region)
        self.skin_depth = skin_depth
        self.surf_tri_length = surf_tri_length
        self.num_layers = num_layers
        self.num_layers = num_layers
        self.max_elems = max_elems
        self.restrict_max_elem = restrict_max_elem
