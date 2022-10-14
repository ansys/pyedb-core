"""Import definition classes."""

from ansys.edb.definition.bondwire_def import (
    ApdBondwireDef,
    BondwireDef,
    BondwireDefType,
    Jedec4BondwireDef,
    Jedec5BondwireDef,
)
from ansys.edb.definition.component_def import ComponentDef
from ansys.edb.definition.component_model import (
    ComponentModel,
    DynamicLinkComponentModel,
    NPortComponentModel,
)
from ansys.edb.definition.component_pin import ComponentPin
from ansys.edb.definition.component_property import ComponentProperty
from ansys.edb.definition.dataset_def import DatasetDef
from ansys.edb.definition.die_property import DieOrientation, DieProperty, DieType
from ansys.edb.definition.ic_component_property import ICComponentProperty
from ansys.edb.definition.material_def import (
    DielectricMaterialModel,
    MaterialDef,
    MaterialProperty,
    ThermalModifier,
)
from ansys.edb.definition.package_def import PackageDef
from ansys.edb.definition.padstack_def import PadstackDef
from ansys.edb.definition.padstack_def_data import (
    PadGeometryType,
    PadstackDefData,
    PadstackHoleRange,
    PadType,
    SolderballPlacement,
    SolderballShape,
)
from ansys.edb.definition.port_property import PortProperty
from ansys.edb.definition.solder_ball_property import SolderBallProperty
