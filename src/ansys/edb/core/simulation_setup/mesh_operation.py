"""Mesh Operation."""


class MeshOperation:
    """Class representing mesh operations.

    Attributes
    ----------
    name : str
        Name of the operation.
    net_layer_info : list[tuple(str, str, bool)]
        Each entry has net name, layer name, and isSheet which is True if it is a sheet object.
    enabled : bool
        True if mesh operation is enabled.
    refine_inside : bool
        True if should refine inside.
    mesh_region : str
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
        """Create a MeshOperation."""
        self._name = name
        self._net_layer_info = [] if net_layer_info is None else net_layer_info
        self._enabled = enabled
        self._refine_inside = refine_inside
        self._mesh_region = mesh_region

    @property
    def name(self):
        """:obj:`str`: Mesh operation name."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def net_layer_info(self):
        """:obj:`list` of :obj:`tuple` of (:obj:`str`, :obj:`str`, :obj:`bool`): List of mesh op net layer info.

        tuple is of the form (net_name, layer_name, is_sheet)
        """
        return self._net_layer_info

    @net_layer_info.setter
    def net_layer_info(self, net_layer_info):
        self._net_layer_info = net_layer_info

    @property
    def enabled(self):
        """:obj:`bool`: Flag for enabling the mesh operation."""
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled

    @property
    def refine_inside(self):
        """:obj:`bool`: Flag for enabling refine inside."""
        return self._refine_inside

    @refine_inside.setter
    def refine_inside(self, refine_inside):
        self._refine_inside = refine_inside

    @property
    def mesh_region(self):
        """:obj:`str`: Name of mesh region."""
        return self._mesh_region

    @mesh_region.setter
    def mesh_region(self, mesh_region):
        self._mesh_region = mesh_region


class SkinDepthMeshOperation(MeshOperation):
    """Class representing skin depth mesh op.

    Attributes
    ----------
    name : str
        Name of the operation.
    net_layer_info : list[tuple[str, str, bool]]
        Each entry has net name, layer name, and isSheet which is True if it is a sheet object.
    enabled : bool
        True if mesh operation is enabled.
    refine_inside : bool
        True if should refine inside.
    mesh_region : str
        Mesh region.
    skin_depth : str
        Skin depth (number with optional length units).
    surface_triangle_length : str
        Surface triangle length (number with optional length units).
    num_layers : str
        Number of layers (integer).
    max_elements : str
        Maximum number of elements (integer).
    restrict_max_elements : bool
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
        surface_triangle_length="1mm",
        num_layers="2",
        max_elements="1000",
        restrict_max_elements=False,
    ):
        """Create a SkinDepthMeshOperation."""
        super().__init__(name, net_layer_info, enabled, refine_inside, mesh_region)
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
        """:obj:`bool`: Flag to restrict the maximum number of mesh elements."""
        return self._restrict_max_elements

    @restrict_max_elements.setter
    def restrict_max_elements(self, restrict_max_elements):
        self._restrict_max_elements = restrict_max_elements


class LengthMeshOperation(MeshOperation):
    """Class representing skin depth mesh op.

    Attributes
    ----------
    name : str
        Name of the operation.
    net_layer_info : list[tuple(str, str, bool)]
        Each entry has net name, layer name, and isSheet which is True if it is a sheet object.
    enabled : bool
        True if mesh operation is enabled.
    refine_inside : bool
        True if should refine inside.
    mesh_region : str
        Mesh region.
    max_length : str
        maximum length of mesh elements (number with optional length units).
    restrict_max_length : str
        True if we restrict length of mesh elements (number with optional length units).
    max_elements : str
        Number of layers (integer).
    restrict_max_elements : bool
        True if we restrict the number of elements.
    """

    def __init__(
        self,
        name="",
        net_layer_info=None,
        enabled=True,
        refine_inside=False,
        mesh_region="",
        max_length="1mm",
        restrict_max_length=True,
        max_elements="1000",
        restrict_max_elements=False,
    ):
        """Class representing skin depth mesh op."""
        super().__init__(name, net_layer_info, enabled, refine_inside, mesh_region)
        self._max_length = max_length
        self._restrict_max_length = restrict_max_length
        self._max_elements = max_elements
        self._restrict_max_elements = restrict_max_elements

    @property
    def max_length(self):
        """:obj:`str`: Maximum length of mesh elements."""
        return self._max_length

    @max_length.setter
    def max_length(self, max_length):
        self._max_length = max_length

    @property
    def restrict_max_length(self):
        """:obj:`bool`: Flag to restrict the maximum length of mesh elements."""
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
        """:obj:`bool`: Flag to restrict the maximum number of mesh elements."""
        return self._restrict_max_elements

    @restrict_max_elements.setter
    def restrict_max_elements(self, restrict_max_elements):
        self._restrict_max_elements = restrict_max_elements
