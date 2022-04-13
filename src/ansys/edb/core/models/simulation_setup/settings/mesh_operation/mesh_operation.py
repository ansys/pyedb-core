"""Mesh Operation."""


class MeshOperation:
    """Class representing mesh operations."""

    def __init__(
        self,
        name="",
        net_layer_info=None,
        enabled=True,
        refine_inside=False,
        mesh_region="",
    ):
        """
        Instantiate a mesh op.

        Parameters
        ----------
        name : str, optional
        net_layer_info : list of str, str, bool, optional
        enabled : bool, optional
        refine_inside : bool, optional
        mesh_region : str, optional
        """
        self.name = name
        self.net_layer_info = [] if net_layer_info is None else net_layer_info
        self.enabled = enabled
        self.refine_inside = refine_inside
        self.mesh_region = mesh_region
