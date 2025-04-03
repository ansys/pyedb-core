"""Q3D simulation settings."""
from __future__ import annotations

from enum import Enum

import ansys.api.edb.v1.hfss_simulation_settings_pb2 as hfss_pb2
import ansys.api.edb.v1.q3d_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import (
    Q3DAdvancedMeshingSettingsServiceStub,
    Q3DAdvancedSettingsServiceStub,
    Q3DCGSettingsServiceStub,
    Q3DDCRLSettingsServiceStub,
    Q3DGeneralSettingsServiceStub,
    Q3DSettingsServiceStub,
    StubAccessor,
    StubType,
)
from ansys.edb.core.simulation_setup.hfss_simulation_settings import SolverType
from ansys.edb.core.simulation_setup.simulation_settings import (
    AdvancedMeshingSettings,
    AdvancedSettings,
    SimulationSettings,
    SimulationSettingsBase,
)


class Q3DSolutionOrder(Enum):
    """Provides an enum representing Q3D solution order."""

    NORMAL = pb.Q3DSolutionOrder.NORMAL
    HIGH = pb.Q3DSolutionOrder.HIGH
    HIGHER = pb.Q3DSolutionOrder.HIGHER
    HIGHEST = pb.Q3DSolutionOrder.HIGHEST
    NUM_SOLUTION_ORDER = pb.Q3DSolutionOrder.NUM_SOLUTION_ORDER


class Q3DSettingsType(Enum):
    """Provides an enum representing Q3D settings type."""

    DC = pb.Q3DSettingsType.DC
    AC = pb.Q3DSettingsType.AC
    CG = pb.Q3DSettingsType.CG


class Q3DSimulationSettings(SimulationSettings):
    """Represents Q3D simulation settings."""

    @property
    def general(self) -> Q3DGeneralSettings:
        """:class:`.Q3DGeneralSettings`: General settings for Q3D simulations."""
        return Q3DGeneralSettings(self._sim_setup)

    @property
    def dcrl(self) -> Q3DDCRLSettings:
        """:class:`.Q3DDCRLSettings`: DCRL settings for Q3D simulations."""
        return Q3DDCRLSettings(self._sim_setup)

    @property
    def acrl(self) -> Q3DACRLSettings:
        """:class:`.Q3DACRLSettings`: ACRL settings for Q3D simulations."""
        return Q3DACRLSettings(self._sim_setup)

    @property
    def cg(self) -> Q3DCGSettings:
        """:class:`.Q3DCGSettings`: CG settings for Q3D simulations."""
        return Q3DCGSettings(self._sim_setup)

    @property
    def advanced(self) -> Q3DAdvancedSettings:
        """:class:`.Q3DAdvancedSettings`: Advanced settings for Q3D simulations."""
        return Q3DAdvancedSettings(self._sim_setup)

    @property
    def advanced_meshing(self) -> Q3DAdvancedMeshingSettings:
        """:class:`.Q3DAdvancedMeshingSettings`: Advanced meshing settings for Q3D simulations."""
        return Q3DAdvancedMeshingSettings(self._sim_setup)


class Q3DGeneralSettings(SimulationSettingsBase):
    """Represents general settings for Q3D simulations."""

    __stub: Q3DGeneralSettingsServiceStub = StubAccessor(StubType.q3d_general_sim_settings)

    @property
    def solution_frequency(self) -> str:
        """:`obj`:str: Simulation frequency for Q3D."""
        return self.__stub.GetSolutionFrequency(self.msg).value

    @solution_frequency.setter
    def solution_frequency(self, solution_frequency: str):
        self.__stub.SetSolutionFrequency(messages.string_property_message(self, solution_frequency))

    @property
    def do_dc(self) -> bool:
        """:`obj`:bool: Whether to solve and generate mesh for for DC resistance and inductance."""
        return self.__stub.GetDoDC(self.msg).value

    @do_dc.setter
    def do_dc(self, do_dc: bool):
        self.__stub.SetDoDC(messages.bool_property_message(self, do_dc))

    @property
    def do_dc_res_only(self) -> bool:
        """:`obj`:bool: Whether to perform DC analysis with resistive only."""
        return self.__stub.GetDoDCResOnly(self.msg).value

    @do_dc_res_only.setter
    def do_dc_res_only(self, do_dc_res_only: bool):
        self.__stub.SetDoDCResOnly(messages.bool_property_message(self, do_dc_res_only))

    @property
    def do_cg(self) -> bool:
        """:`obj`:bool: Whether to solve and generate mesh for DC capacitance and conductance."""
        return self.__stub.GetDoCG(self.msg).value

    @do_cg.setter
    def do_cg(self, do_cg: bool):
        self.__stub.SetDoCG(messages.bool_property_message(self, do_cg))

    @property
    def do_ac(self) -> bool:
        """:`obj`:bool: Whether to p to solve and generate mesh for AC resistance and inductance."""
        return self.__stub.GetDoAC(self.msg).value

    @do_ac.setter
    def do_ac(self, do_ac: bool):
        self.__stub.SetDoAC(messages.bool_property_message(self, do_ac))

    @property
    def save_fields(self) -> bool:
        """:`obj`:bool: Whether to save the current settings as the new default settings."""
        return self.__stub.GetSaveFields(self.msg).value

    @save_fields.setter
    def save_fields(self, save_fields: bool):
        self.__stub.SetSaveFields(messages.bool_property_message(self, save_fields))


class Q3DSettings(SimulationSettingsBase):
    """Represents settings for Q3D simulations."""

    __stub: Q3DSettingsServiceStub = StubAccessor(StubType.q3d_sim_settings)

    def __init__(self, sim_setup, sim_type):
        """Create a Q3DSettings object."""
        super().__init__(sim_setup)
        self._sim_type = sim_type

    @property
    def max_passes(self) -> int:
        """:`obj`:int: Maximum number of mesh refinement cycles to perform."""
        return self.__stub.GetMaxPasses(self._q3d_settings_message()).value

    @max_passes.setter
    def max_passes(self, max_passes: int):
        self.__stub.SetMaxPasses(self._q3d_settings_uint64_property_message(max_passes))

    @property
    def min_passes(self) -> int:
        """:`obj`:int: Minimum number of mesh refinement cycles to perform."""
        return self.__stub.GetMinPasses(self._q3d_settings_message()).value

    @min_passes.setter
    def min_passes(self, min_passes: int):
        self.__stub.SetMinPasses(self._q3d_settings_uint64_property_message(min_passes))

    @property
    def min_converged_passes(self) -> int:
        """:`obj`:int: Minimum number of passes that must meet convergence criteria before the simulation stops."""
        return self.__stub.GetMinConvergedPasses(self._q3d_settings_message()).value

    @min_converged_passes.setter
    def min_converged_passes(self, min_converged_passes: int):
        self.__stub.SetMinConvergedPasses(
            self._q3d_settings_uint64_property_message(min_converged_passes)
        )

    @property
    def percent_error(self) -> float:
        """:obj:`float`: Percent error during conduction adaptive passes."""
        return self.__stub.GetPercentError(self._q3d_settings_message()).value

    @percent_error.setter
    def percent_error(self, percent_error: float):
        self.__stub.SetPercentError(self._q3d_settings_double_property_message(percent_error))

    @property
    def max_refine_per_pass(self) -> float:
        """:`obj`:float: How many tetrahedra are added at each iteration of the adaptive refinement process."""
        return self.__stub.GetMaxRefinePerPass(self._q3d_settings_message()).value

    @max_refine_per_pass.setter
    def max_refine_per_pass(self, max_refine_per_pass: float):
        self.__stub.SetMaxRefinePerPass(
            self._q3d_settings_double_property_message(max_refine_per_pass)
        )

    def _q3d_settings_message(self):
        return pb.Q3DSettingsMessage(target=self.msg, q3d_settings_type=self._sim_type.value)

    def _q3d_settings_uint64_property_message(self, value):
        return pb.Q3DSettingsUInt64PropertyMessage(
            q3d_settings=self._q3d_settings_message(), value=value
        )

    def _q3d_settings_double_property_message(self, value):
        return pb.Q3DSettingsDoublePropertyMessage(
            q3d_settings=self._q3d_settings_message(), value=value
        )


class Q3DDCRLSettings(Q3DSettings):
    """Represents DCRL settings for Q3D simulations."""

    __stub: Q3DDCRLSettingsServiceStub = StubAccessor(StubType.q3d_dcrl_sim_settings)

    def __init__(self, sim_setup):
        """Create a Q3DDCRLSettings object."""
        super().__init__(sim_setup, Q3DSettingsType.DC)

    @property
    def solution_order(self) -> Q3DSolutionOrder:
        """:class:`.Q3DSolutionOrder`: Inductance adaptive solution accuracy. \
            The solver will give accurate results at the Normal setting for most applications."""
        return Q3DSolutionOrder(self.__stub.GetSolutionOrder(self.msg).q3d_solution_order)

    @solution_order.setter
    def solution_order(self, q3d_solution_order: Q3DSolutionOrder):
        self.__stub.SetSolutionOrder(
            pb.Q3DSolutionOrderPropertyMessage(
                target=self.msg, q3d_solution_order=q3d_solution_order.value
            )
        )


class Q3DACRLSettings(Q3DSettings):
    """Represents ACRL settings for Q3D simulations."""

    def __init__(self, sim_setup):
        """Create a Q3DACRLSettings object."""
        super().__init__(sim_setup, Q3DSettingsType.AC)


class Q3DCGSettings(Q3DSettings):
    """Represents CG settings for Q3D simulations."""

    __stub: Q3DCGSettingsServiceStub = StubAccessor(StubType.q3d_cg_sim_settings)

    def __init__(self, sim_setup):
        """Create a Q3DCGSettings object."""
        super().__init__(sim_setup, Q3DSettingsType.CG)

    @property
    def auto_incr_sol_order(self) -> bool:
        """:`obj`:bool: Whether to automatically increase accuracy."""
        return self.__stub.GetAutoIncrSolOrder(self.msg).value

    @auto_incr_sol_order.setter
    def auto_incr_sol_order(self, auto_incr_sol_order: bool):
        self.__stub.SetAutoIncrSolOrder(messages.bool_property_message(self, auto_incr_sol_order))

    @property
    def solution_order(self) -> Q3DSolutionOrder:
        """:class:`.Q3DSolutionOrder`: Adaptive solution accuracy. \
            The solver will give accurate results at the Normal setting for most applications."""
        return Q3DSolutionOrder(self.__stub.GetSolutionOrder(self.msg).q3d_solution_order)

    @solution_order.setter
    def solution_order(self, q3d_solution_order: Q3DSolutionOrder):
        self.__stub.SetSolutionOrder(
            pb.Q3DSolutionOrderPropertyMessage(
                target=self.msg, q3d_solution_order=q3d_solution_order.value
            )
        )

    @property
    def solver_type(self):
        """:class:`.SolverType`: Q3D solver type."""
        return SolverType(self.__stub.GetSolverType(self.msg).solver_type)

    @solver_type.setter
    def solver_type(self, solver_type):
        self.__stub.SetSolverType(
            hfss_pb2.SolverTypePropertyMessage(target=self.msg, solver_type=solver_type.value)
        )

    @property
    def compression_tol(self) -> float:
        """:`obj`:float: Compression tolerance value."""
        return self.__stub.GetCompressionTol(self.msg).value

    @compression_tol.setter
    def compression_tol(self, compression_tol: float):
        self.__stub.SetCompressionTol(messages.double_property_message(self, compression_tol))


class Q3DAdvancedSettings(AdvancedSettings, Q3DSettings):
    """Represents advanced settings for Q3D simulations."""

    __stub: Q3DAdvancedSettingsServiceStub = StubAccessor(StubType.q3d_advanced_sim_settings)

    @property
    def ic_mode_auto_resolution(self) -> bool:
        """:obj:`bool`: Flag indicating if model resolution is automatically calculated for IC designs."""
        return self.__stub.GetICModeAutoResolution(self.msg).value

    @ic_mode_auto_resolution.setter
    def ic_mode_auto_resolution(self, ic_mode_auto_resolution: bool):
        self.__stub.SetICModeAutoResolution(
            messages.bool_property_message(self, ic_mode_auto_resolution)
        )

    @property
    def ic_mode_length(self) -> str:
        """:obj:`str`: Model resolution to use when manually setting the model resolution of IC designs."""
        return self.__stub.GetICModeLength(self.msg).value

    @ic_mode_length.setter
    def ic_mode_length(self, ic_mode_length: str):
        self.__stub.SetICModeLength(messages.string_property_message(self, ic_mode_length))


class Q3DAdvancedMeshingSettings(AdvancedMeshingSettings):
    """Represents advanced meshing settings for Q3D simulations."""

    __stub: Q3DAdvancedMeshingSettingsServiceStub = StubAccessor(
        StubType.q3d_advanced_meshing_sim_settings
    )

    @property
    def layer_alignment(self) -> str:
        """:obj:`str`: Snapping tolerance for hierarchical layer alignment.

        Unitless values represent a fraction of the total stackup height.
        """
        return self.__stub.GetLayerAlignment(self.msg).value

    @layer_alignment.setter
    def layer_alignment(self, layer_alignment: str):
        self.__stub.SetLayerAlignment(messages.bool_property_message(self, layer_alignment))
