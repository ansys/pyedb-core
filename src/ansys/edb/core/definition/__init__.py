"""Import definition classes."""

from ansys.edb.core.definition.bondwire_def import (
    ApdBondwireDef,
    BondwireDef,
    BondwireDefType,
    Jedec4BondwireDef,
    Jedec5BondwireDef,
)
from ansys.edb.core.definition.component_def import ComponentDef
from ansys.edb.core.definition.component_model import (
    ComponentModel,
    DynamicLinkComponentModel,
    NPortComponentModel,
)
from ansys.edb.core.definition.component_pin import ComponentPin
from ansys.edb.core.definition.component_property import ComponentProperty
from ansys.edb.core.definition.dataset_def import DatasetDef
from ansys.edb.core.definition.debye_model import DebyeModel
from ansys.edb.core.definition.die_property import DieOrientation, DieProperty, DieType
from ansys.edb.core.definition.dielectric_material_model import (
    DielectricMaterialModel,
    DielectricMaterialModelType,
)
from ansys.edb.core.definition.djordjecvic_sarkar_model import DjordjecvicSarkarModel
from ansys.edb.core.definition.ic_component_property import ICComponentProperty
from ansys.edb.core.definition.io_component_property import IOComponentProperty
from ansys.edb.core.definition.material_def import MaterialDef, MaterialProperty, ThermalModifier
from ansys.edb.core.definition.material_property_thermal_modifier import (
    MaterialPropertyThermalModifier,
)
from ansys.edb.core.definition.multipole_debye_model import MultipoleDebyeModel
from ansys.edb.core.definition.package_def import PackageDef
from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.definition.padstack_def_data import (
    PadGeometryType,
    PadstackDefData,
    PadstackHoleRange,
    PadType,
    SolderballPlacement,
    SolderballShape,
)
from ansys.edb.core.definition.port_property import PortProperty
from ansys.edb.core.definition.rlc_component_property import RLCComponentProperty
from ansys.edb.core.definition.solder_ball_property import SolderBallProperty
from ansys.edb.core.edb_defs import DefinitionObjType
