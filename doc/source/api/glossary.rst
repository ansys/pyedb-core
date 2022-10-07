:orphan:

Glossary
========

.. glossary::

	Connectable

		The generic type for most objects in Layout.
		
		Objects of the following types are all connectables :
		
		.. toctree::
		   :maxdepth: 1

		   primitive
		   hierarchy   
		   terminal
		   
	Zone

		Multizone stackups allow a design to be divided into areas called zones. 
		
		Each zone contains a subset of layers available to the entire circuit board and is spatially defined by polygons on the Outline layer.	

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

	HFSSExtents
		
		Extent box around the design, represented by a :obj:`dict` with the following key:values
		
		| **dielectric**: (:obj:`float`, :obj:`bool`)
		| 	Dielectric extent size. First parameter is the value and second parameter indicates if the value is a multiple.
		| **airbox_horizontal**: (:obj:`float`, :obj:`bool`)
		| 	Airbox horizontal extent size. First parameter is the value and second parameter indicates if the value is a multiple.
		| **airbox_vertical_positive**: (:obj:`float`, :obj:`bool`)
		| 	Airbox positive vertical extent size. First parameter is the value and second parameter indicates if the value is a multiple.
		| **airbox_vertical_negative**: (:obj:`float`, :obj:`bool`)
		| 	Airbox negative vertical extent size. First parameter is the value and second parameter indicates if the value is a multiple.
		| **airbox_truncate_at_ground**: :obj:`bool`
		| 	Whether airbox will be truncated at the ground layers.