from typing import List, Tuple

from ansys.edb.simulation_setup.settings.mesh_operation.mesh_operation import MeshOperation


class SkinDepthMeshOperation(MeshOperation):
    def __init__(
        self,
        name: str = "",
        net_layer_info: List[Tuple[str, str, bool]] = None,
        enabled: bool = True,
        refine_inside: bool = False,
        mesh_region: str = "",
        skin_depth: str = "1um",
        surf_tri_length: str = "1mm",
        num_layers: str = "2",
        max_elems: str = "1000",
        restrict_max_elem: bool = False,
    ):
        super().__init__(name, net_layer_info, enabled, refine_inside, mesh_region)
        self.skin_depth = skin_depth
        self.surf_tri_length = surf_tri_length
        self.num_layers = num_layers
        self.num_layers = num_layers
        self.max_elems = max_elems
        self.restrict_max_elem = restrict_max_elem
