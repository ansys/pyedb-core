"""Import simulation setup classes."""

from ansys.edb.simulation_setup.adaptive_solutions import (
    AdaptiveFrequency,
    BroadbandAdaptiveSolution,
    MatrixConvergenceData,
    MatrixConvergenceDataEntry,
    MultiFrequencyAdaptiveSolution,
    SingleFrequencyAdaptiveSolution,
)
from ansys.edb.simulation_setup.hfss_simulation_settings import (
    AdaptType,
    BasisFunctionOrder,
    HFSSAdvancedMeshingSettings,
    HFSSAdvancedSettings,
    HFSSDCRSettings,
    HFSSGeneralSettings,
    HFSSSettingsOptions,
    HFSSSimulationSettings,
    HFSSSolverSettings,
    SolverType,
)
from ansys.edb.simulation_setup.hfss_simulation_setup import HfssSimulationSetup
from ansys.edb.simulation_setup.mesh_operation import (
    LengthMeshOperation,
    MeshOperation,
    SkinDepthMeshOperation,
)
from ansys.edb.simulation_setup.simulation_settings import (
    AdvancedMeshingSettings,
    AdvancedSettings,
    SettingsOptions,
    SimulationSettings,
    SolverSettings,
    ViaStyle,
)
from ansys.edb.simulation_setup.simulation_setup import (
    SimulationSetup,
    SimulationSetupType,
    SweepData,
)
