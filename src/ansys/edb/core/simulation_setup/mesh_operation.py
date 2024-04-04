"""Mesh operation."""


class MeshOperation:
    """Represents mesh operations.

    Attributes
    ----------
    name : str, default: ""
        Name of the mesh operation. The default is ``""``, in which case a name is automatically assigned.
    net_layer_info : list[tuple(str, str, bool)], default: None
        List with each entry having a net name, layer name, and ``isSheet`` flag indicating
        if the entry is a sheet.
    enabled : bool, default: True
        Whether the mesh operation is enabled.
    refine_inside : bool, default: False
        Whether to refine inside.
    mesh_region : str, default: ""
        Mesh region.
    solve_inside : bool, default: False
        Whether to solve inside.
    """

    def __init__(
        self,
        name="",
        net_layer_info=None,
        enabled=True,
        refine_inside=False,
        mesh_region="",
        solve_inside=False,
    ):
        """Create a mesh operation."""
        self._name = name
        self._net_layer_info = [] if net_layer_info is None else net_layer_info
        self._enabled = enabled
        self._refine_inside = refine_inside
        self._mesh_region = mesh_region
        self._solve_inside = solve_inside

    @property
    def name(self):
        """:obj:`str`: Name of the mesh operation."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def net_layer_info(self):
        """:obj:`list` of :obj:`tuple` of (:obj:`str`, :obj:`str`, :obj:`bool`): List of net layer \
        information for the mesh operation.

        The tuple is in this form: (net_name, layer_name, is_sheet)``.
        """
        return self._net_layer_info

    @net_layer_info.setter
    def net_layer_info(self, net_layer_info):
        self._net_layer_info = net_layer_info

    @property
    def enabled(self):
        """:obj:`bool`: Flag indicating if the mesh operation is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled

    @property
    def refine_inside(self):
        """:obj:`bool`: Flag indicating if refining inside is enabled."""
        return self._refine_inside

    @refine_inside.setter
    def refine_inside(self, refine_inside):
        self._refine_inside = refine_inside

    @property
    def mesh_region(self):
        """:obj:`str`: Name of the mesh region."""
        return self._mesh_region

    @mesh_region.setter
    def mesh_region(self, mesh_region):
        self._mesh_region = mesh_region

    @property
    def solve_inside(self):
        """:obj:`bool`: Flag indicating if solve inside is enabled."""
        return self._solve_inside

    @solve_inside.setter
    def solve_inside(self, solve_inside):
        self._solve_inside = solve_inside


class SkinDepthMeshOperation(MeshOperation):
    """Represents a skin depth mesh operation.

    Attributes
    ----------
    name : str, default: ""
        Name of the mesh operation. The default is ``""``, in which case a name is automatically assigned.
    net_layer_info : list[tuple(str, str, bool)], default: None
        List with each entry having a net name, layer name, and ``isSheet`` flag indicating
        if the entry is a sheet.
    enabled : bool, default: True
        Whether the mesh operation is enabled.
    refine_inside : bool, default: False
        Whether to refine inside.
    mesh_region : str, default: ""
        Mesh region.
    solve_inside : bool, default: False
        Whether to solve inside.
    skin_depth : str, default: "1um"
        Skin depth.`.
    surface_triangle_length : str, default: "1mm"
        Surface triangle length with units.
    num_layers : str, default: 2
        Number of layers.
    max_elements : str, default: "1000"
        Maximum number of elements.
    restrict_max_elements : bool, default: False
        Whether to restrict the number of elements.
    """

    def __init__(
        self,
        name="",
        net_layer_info=None,
        enabled=True,
        refine_inside=False,
        mesh_region="",
        solve_inside=False,
        skin_depth="1um",
        surface_triangle_length="1mm",
        num_layers="2",
        max_elements="1000",
        restrict_max_elements=False,
    ):
        """Create a skin depth mesh operation."""
        super().__init__(name, net_layer_info, enabled, refine_inside, mesh_region, solve_inside)
        self._skin_depth = skin_depth
        self._surface_triangle_length = surface_triangle_length
        self._num_layers = num_layers
        self._max_elements = max_elements
        self._restrict_max_elements = restrict_max_elements

    @property
    def skin_depth(self):
        """:obj:`str`: Skin depth."""
        return self._skin_depth

    @skin_depth.setter
    def skin_depth(self, skin_depth):
        self._skin_depth = skin_depth

    @property
    def surface_triangle_length(self):
        """:obj:`str`: Surface triangle length."""
        return self._surface_triangle_length

    @surface_triangle_length.setter
    def surface_triangle_length(self, surface_triangle_length):
        self._surface_triangle_length = surface_triangle_length

    @property
    def number_of_layers(self):
        """:obj:`str`: Number of layers."""
        return self._num_layers

    @number_of_layers.setter
    def number_of_layers(self, number_of_layers):
        self._num_layers = number_of_layers

    @property
    def max_elements(self):
        """:obj:`str`: Maximum number of mesh elements."""
        return self._max_elements

    @max_elements.setter
    def max_elements(self, max_elements):
        self._max_elements = max_elements

    @property
    def restrict_max_elements(self):
        """:obj:`bool`: Flag indicating if the maximum number of mesh elements is restricted."""
        return self._restrict_max_elements

    @restrict_max_elements.setter
    def restrict_max_elements(self, restrict_max_elements):
        self._restrict_max_elements = restrict_max_elements


class LengthMeshOperation(MeshOperation):
    """Represents a length mesh operation.

    Attributes
    ----------
    name : str, default: ""
        Name of the mesh operation. The default is ``""``, in which case a name is automatically assigned.
    net_layer_info : list[tuple(str, str, bool)], default: None
        List with each entry having a net name, layer name, and ``isSheet`` flag indicating
        if the entry is a sheet.
    enabled : bool, default: True
        Whether the mesh operation is enabled.
    refine_inside : bool, default: False
        Whether to refine inside.
    mesh_region : str, default: ""
        Mesh region.
    solve_inside : bool, default: False
        Whether to solve inside.
    max_length : str, default: "1mm"
        maximum length of the mesh elements.
    restrict_max_length : str, default: True
        Whether to restrict the length of the mesh elements.
    max_elements : str, default: "1000"
        Number of layers.
    restrict_max_elements : bool, default: False
        Whether to restrict the number of elements.
    """

    def __init__(
        self,
        name="",
        net_layer_info=None,
        enabled=True,
        refine_inside=False,
        mesh_region="",
        solve_inside=False,
        max_length="1mm",
        restrict_max_length=True,
        max_elements="1000",
        restrict_max_elements=False,
    ):
        """Initialize an instance of a skin depth mesh operation."""
        super().__init__(name, net_layer_info, enabled, refine_inside, mesh_region, solve_inside)
        self._max_length = max_length
        self._restrict_max_length = restrict_max_length
        self._max_elements = max_elements
        self._restrict_max_elements = restrict_max_elements

    @property
    def max_length(self):
        """:obj:`str`: Maximum length of the mesh elements."""
        return self._max_length

    @max_length.setter
    def max_length(self, max_length):
        self._max_length = max_length

    @property
    def restrict_max_length(self):
        """:obj:`bool`: Flag indicating if the maximum length of mesh elements is restricted."""
        return self._restrict_max_length

    @restrict_max_length.setter
    def restrict_max_length(self, restrict_max_length):
        self._restrict_max_length = restrict_max_length

    @property
    def max_elements(self):
        """:obj:`str`: Maximum number of mesh elements."""
        return self._max_elements

    @max_elements.setter
    def max_elements(self, max_elements):
        self._max_elements = max_elements

    @property
    def restrict_max_elements(self):
        """:obj:`bool`: Flag indicating if the maximum number of mesh elements is restricted."""
        return self._restrict_max_elements

    @restrict_max_elements.setter
    def restrict_max_elements(self, restrict_max_elements):
        self._restrict_max_elements = restrict_max_elements
