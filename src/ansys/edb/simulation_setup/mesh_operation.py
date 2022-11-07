"""Mesh Operation."""


class MeshOperation:
    """Class representing mesh operations.

    Attributes
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
    """

    def __init__(
        self,
        name="",
        net_layer_info=None,
        enabled=True,
        refine_inside=False,
        mesh_region="",
    ):
        """__init__ for MeshOperation."""
        self.name = name
        self.net_layer_info = [] if net_layer_info is None else net_layer_info
        self.enabled = enabled
        self.refine_inside = refine_inside
        self.mesh_region = mesh_region
