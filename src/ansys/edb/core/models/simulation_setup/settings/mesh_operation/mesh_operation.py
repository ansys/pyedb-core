from typing import List, Tuple


class MeshOperation:
    def __init__(
        self,
        name: str = "",
        net_layer_info: List[Tuple[str, str, bool]] = None,
        enabled: bool = True,
        refine_inside: bool = False,
        mesh_region: str = "",
    ):
        self.name = name
        self.net_layer_info = [] if net_layer_info is None else net_layer_info
        self.enabled = enabled
        self.refine_inside = refine_inside
        self.mesh_region = mesh_region
