User Guide
==========

**[Ansys Internal - Confidential]**

The classes and functions are in the **ansys.edb.core** namespace

The Electronics Database (EDB) API allows access and manipulation of EDB databases. Design types managing Layout data in ANSYS Electronics Desktop have a corresponding aedb directory alongside the aedt file -- the aedb directory contains the EDB database. EDB databases can also be created by ANSYS translators, or by using these API functions directly; the resulting EBD can then be imported into ANSYS Electronics Desktop. 

Please note that in many cases an object added to the database hierarchy is no longer mutable. For example, if you add a models.cell.layer object to a Cell object's LayerCollection, the layer is deep copied into the LayerCollection and afterwards you can only access the added layer as a ILayerReadOnly object. ReadOnly objects generally have a Clone method which allows you to copy, modify, and replace already added objects. 

Quick Start
-----------

Go to recent 2023 R1 installation folder and double-click EDB_RPC_Server.exe to run it



