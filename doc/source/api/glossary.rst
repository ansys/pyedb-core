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