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

		All zones (except the "fixed" zone) can have bends applied to them by defining :class:`BoardBendDefs <ansys.edb.core.primitive.board_bend_def.BoardBendDef>` on zone primitives.

	ValueLike

		Any of the following data types that represents a numeric value

		- :obj:`int`
		- :obj:`float`
		- :obj:`complex`
		- :obj:`str` for expressions ('1nm', 'x + 1' etc)
		- :class:`Value <ansys.edb.core.utility.value.Value>`

	Point2DLike

		Any of the following data types that represents (x, y) point on a 2D coordinate system.

		- :class:`PointData <ansys.edb.core.geometry.point_data.PointData>`
		- (:term:`ValueLike`, :term:`ValueLike`) or any other iterable with 2 :term:`ValueLike` inside

	Point3DLike

		Any of the following data types that represents (x, y, z) point on a 3D coordinate system.

		- :class:`Point3DData <ansys.edb.core.geometry.point3d_data.Point3DData>`
		- (:term:`ValueLike`, :term:`ValueLike`, :term:`ValueLike`) or any other iterable with 3 :term:`ValueLike` inside

	Triangle3DLike

		(:term:`Point3DLike`, :term:`Point3DLike`, :term:`Point3DLike`)


	LayerLike

		Any of the following data types that represent a layer.

		- :obj:`str`
		- :class:`Layer <ansys.edb.core.layer.layer.Layer>`

	NetLike

		Any of the following data types that represent a net.

		- :obj:`str`
		- :class:`Layer <ansys.edb.core.net.net.Net>`


	RoughnessModel

		A Groisse roughness model is represented by a single value containing the roughness value.
		A Huray roughness model is represented  by a tuple of the form [nodule_radius_value, surface_ratio_value]

		:obj:`Union <typing.Union>`\[:term:`ValueLike`, (:term:`ValueLike`, :term:`ValueLike`)]

	HFSSSolverProperties

		HFSS solver properties are represented by a tuple of the form [dc_thickness_type, dc_thickness_value, solve_inside_enabled]

		(:class:`DCThicknessType <ansys.edb.core.layer.stackup_layer.DCThicknessType>`, :term:`ValueLike`, :obj:`bool`)

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

	Anisotropic Material Property Component IDs

		Anisotropic material properties use component ID values to specify tensor diagonal entries. Component ID values map to tensor diagonal entries as follows:

		- ``0`` -> ``T[1,1]``
		- ``1`` -> ``T[2,2]``
		- ``2`` -> ``T[3,3]``