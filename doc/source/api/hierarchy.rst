Hierarchy
=========

Hierarchy objects are :term:`connectables <Connectable>` that can act as a container for other :term:`connectables <Connectable>`.
Examples of hierarchy objects include subdesigns, MCAD components, and coordinate systems.


Object types
------------

.. currentmodule:: ansys.edb.core.hierarchy

.. autosummary::
   :toctree: _autosummary

   cell_instance.CellInstance
   inst_array.InstArray
   component_group.ComponentGroup
   group.Group
   pin_group.PinGroup
   model.Model
   pin_pair_model.PinPairModel
   netlist_model.NetlistModel
   sparameter_model.SParameterModel
   spice_model.SPICEModel
   structure3d.Structure3D
   via_group.ViaGroup
   layout_component.LayoutComponent


Enums
-----

.. autosummary::
   :toctree: _autosummary

   component_group.ComponentType
   structure3d.MeshClosure