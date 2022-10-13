:orphan:

.. glossary::

	Connectable

		The generic type for most objects in Layout.
		
		Objects of the following types are all connectables :
		
		.. toctree::
		   :maxdepth: 1

		   primitive
		   hierarchy   
		   terminal

	ValueLike

		:obj:`Union <typing.Union>`\[:obj:`int`, :obj:`float`, :obj:`complex`, :obj:`str`, :class:`Value <ansys.edb.utility.Value>`\]

	Point3DLike

		:obj:`tuple`\[:term:`ValueLike`, :term:`ValueLike`, :term:`ValueLike`\]

	Triangle3DLike

		:obj:`tuple`\[:term:`Point3DLike`, :term:`Point3DLike`, :term:`Point3DLike`\]

	RoughnessModel

		A Groisse roughness model is represented by a single value containing the roughness value.
		A Huray roughness model is represented  by a tuple of the form [nodule_radius_value, surface_ratio_value]

		:obj:`Union <typing.Union>`\[:term:`ValueLike`, :obj:`tuple`\[:term:`ValueLike`, :term:`ValueLike`\]]

	HFSSSolverProperties

		HFSS solver properties are represented by a tuple of the form [dc_thickness_type, dc_thickness_value, solve_inside_enabled]

		:obj:`tuple`\[:class:`DCThicknessType <ansys.edb.layer.DCThicknessType>`, :term:`ValueLike`, :obj:`bool`\]