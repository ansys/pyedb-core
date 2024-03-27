"""Import simulation setup classes."""

from ansys.edb.core.simulation_setup.adaptive_solutions import (
    AdaptiveFrequency,
    BroadbandAdaptiveSolution,
    MatrixConvergenceData,
    MatrixConvergenceDataEntry,
    MultiFrequencyAdaptiveSolution,
    SingleFrequencyAdaptiveSolution,
)
from ansys.edb.core.simulation_setup.hfss_simulation_settings import (
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
from ansys.edb.core.simulation_setup.hfss_simulation_setup import HfssSimulationSetup
from ansys.edb.core.simulation_setup.mesh_operation import (
    LengthMeshOperation,
    MeshOperation,
    SkinDepthMeshOperation,
)
from ansys.edb.core.simulation_setup.raptor_x_simulation_settings import (
    RaptorXAdvancedSettings,
    RaptorXGeneralSettings,
    RaptorXSimulationSettings,
)
from ansys.edb.core.simulation_setup.raptor_x_simulation_setup import RaptorXSimulationSetup
from ansys.edb.core.simulation_setup.simulation_settings import (
    AdvancedMeshingSettings,
    AdvancedSettings,
    SettingsOptions,
    SimulationSettings,
    SolverSettings,
    ViaStyle,
)
from ansys.edb.core.simulation_setup.simulation_setup import (
    FreqSweepType,
    HFSSRegionComputeResource,
    InterpolatingSweepData,
    SimulationSetup,
    SimulationSetupType,
    SweepData,
)
from ansys.edb.core.simulation_setup.siwave_dcir_simulation_settings import (
    SIWaveDCIRSimulationSettings,
)
from ansys.edb.core.simulation_setup.siwave_dcir_simulation_setup import SIWaveDCIRSimulationSetup
from ansys.edb.core.simulation_setup.siwave_simulation_settings import (
    SIWaveAdvancedSettings,
    SIWaveDCAdvancedSettings,
    SIWaveDCSettings,
    SIWaveGeneralSettings,
    SIWaveSimulationSettings,
    SIWaveSParameterSettings,
    SParamDCBehavior,
    SParamExtrapolation,
    SParamInterpolation,
)
from ansys.edb.core.simulation_setup.siwave_simulation_setup import SIWaveSimulationSetup
