Release Notes
=============

v1.0
----

Known Issues:
	* If a new database is opened after another one is closed, the server may fail to properly fetch objects that are created after the new database is opened.
		* See `issue #154 <https://github.com/pyansys/pyedb/issues/154>`_