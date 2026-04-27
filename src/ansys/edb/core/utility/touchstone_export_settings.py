"""Touchstone Settings."""

from enum import Enum, auto


class PassivityAlgorithm(Enum):
    """Enum representing passivity algorithm types."""

    CONVEX_OPTIMIZATION = auto()
    PASSIVITY_BY_PERTURBATION = auto()
    ITERATED_FITTING_OF_PV = auto()
    ITERATED_FITTING_OF_PVLF = auto()
    DONT_ENFORCE_PASSIVITY = auto()


class ColumnFittingAlgorithm(Enum):
    """Enum representing column fitting algorithm types."""

    COLUMN_ATA_TIME = auto()
    ENTRY_ATA_TIME = auto()
    WHOLE_MATRIX_ATA_TIME = auto()


class SSFittingAlgorithm(Enum):
    """Enum representing state space fitting algorithm types."""

    TWA = auto()
    ITERATIVE_RATIONAL = auto()
    FAST_FIT = auto()
    AUTO_FAST = auto()
    AUTO_ACCURATE = auto()


class ExportType(Enum):
    """Enum representing exported touchstone file types."""

    HFSS_TO_TOUCHSTONE_1_0 = 7
    HFSS_TO_TOUCHSTONE_2_0 = 8


class TouchstoneExportSettings:
    """Represents settings used when exporting touchstone files."""

    def __init__(
        self,
        export_after_solve: bool = False,
        export_dir: str = "",
        export_type: ExportType = ExportType.HFSS_TO_TOUCHSTONE_1_0,
        enforce_passivity: bool = False,
        enforce_causality: bool = False,
        use_common_ground: bool = True,
        show_gamma_comments: bool = False,
        do_renormalize: bool = True,
        renorm_impedance: float = 50.0,
        fitting_error: float = 0.5,
        max_poles: int = 10000,
        passivity_algorithm: PassivityAlgorithm = PassivityAlgorithm.ITERATED_FITTING_OF_PV,
        column_fitting_algorithm: ColumnFittingAlgorithm = ColumnFittingAlgorithm.WHOLE_MATRIX_ATA_TIME,
        ss_fitting_algorithm: SSFittingAlgorithm = SSFittingAlgorithm.FAST_FIT,
        relative_error_tolerance: bool = False,
        ensure_accurate_z_fit: bool = True,
        touchstone_format: str = "MA",
        touchstone_units: str = "GHz",
        touchstone_precision: int = 15,
    ):
        """
        Initialize a touchstone export settings object.

        Attributes
        ----------
        export_after_solve : bool, default: False
        export_dir : str, default = ""
        export_type : ExportType, default: ExportType.HFSS_TO_TOUCHSTONE_1_0
        enforce_passivity : bool, default: False
        enforce_causality : bool, default: False
        use_common_ground : bool, default: True
        show_gamma_comments : bool, default: False
        do_renormalize : bool, default: True
        renorm_impedance : float, default: 50.0
        fitting_error : float, default: 0.5
        max_poles : int, default: 10000
        passivity_algorithm : .PassivityAlgorithm, default: .PassivityAlgorithm.ITERATED_FITTING_OF_PV
        column_fitting_algorithm : .ColumnFittingAlgorithm, default: .ColumnFittingAlgorithm.WHOLE_MATRIX_ATA_TIME
        ss_fitting_algorithm : .SSFittingAlgorithm, default: .SSFittingAlgorithm.FAST_FIT
        relative_error_tolerance : bool, default: False
        ensure_accurate_z_fit : bool, default True
        touchstone_format : str, default: "MA"
        touchstone_units : str, default: "GHz"
        touchstone_precision : int, default: 15
        """
        self.export_after_solve = export_after_solve
        self.export_dir = export_dir
        self.export_type = export_type
        self.enforce_passivity = enforce_passivity
        self.enforce_causality = enforce_causality
        self.use_common_ground = use_common_ground
        self.show_gamma_comments = show_gamma_comments
        self.do_renormalize = do_renormalize
        self.renorm_impedance = renorm_impedance
        self.fitting_error = fitting_error
        self.max_poles = max_poles
        self.passivity_algorithm = passivity_algorithm
        self.column_fitting_algorithm = column_fitting_algorithm
        self.ss_fitting_algorithm = ss_fitting_algorithm
        self.relative_error_tolerance = relative_error_tolerance
        self.ensure_accurate_z_fit = ensure_accurate_z_fit
        self.touchstone_format = touchstone_format
        self.touchstone_units = touchstone_units
        self.touchstone_precision = touchstone_precision
