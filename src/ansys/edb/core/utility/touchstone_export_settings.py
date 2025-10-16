"""TouchstoneExport settings."""
from __future__ import annotations


class TouchstoneExportSettings:
    """
    Provides touchstone export settings.

    Attributes
    ----------
    export_after_solve : bool
        Whether to export after solving.
    export_dir : str
        Directory to export to.
    export_type : int
        Type of export.
    enforce_passivity : bool
        Whether to enforce passivity.
    enforce_causality : bool
        Whether to enforce causality.
    use_common_ground : bool
        Whether to use common ground.
    show_gamma_comments : bool
        Whether to show gamma comments.
    do_renormalize : bool
        Whether to renormalize.
    renorm_impedance : float
        Renormalization impedance value.
    fitting_error : float
        Fitting error value.
    max_poles : int
        Maximum number of poles.
    passivity_algorithm : int
        Passivity algorithm type.
    column_fitting_algorithm : int
        Column fitting algorithm type.
    ss_fitting_algorithm : int
        State-space fitting algorithm type.
    relative_error_tolerance : bool
        Whether to use relative error tolerance.
    ensure_accurate_zfit : bool
        Whether to ensure accurate Z-fit.
    touchstone_format : str
        Touchstone format.
    touchstone_units : str
        Touchstone units.
    touchstone_precision : int
        Touchstone precision.
    """

    def __init__(
        self,
        export_after_solve: bool = False,
        export_dir: str = "",
        export_type: int = 7,
        enforce_passivity: bool = False,
        enforce_causality: bool = False,
        use_common_ground: bool = True,
        show_gamma_comments: bool = False,
        do_renormalize: bool = False,
        renorm_impedance: float = 50.0,
        fitting_error: float = 0.5,
        max_poles: int = 10000,
        passivity_algorithm: int = 2,
        column_fitting_algorithm: int = 2,
        ss_fitting_algorithm: int = 2,
        relative_error_tolerance: bool = False,
        ensure_accurate_zfit: bool = True,
        touchstone_format: str = "MA",
        touchstone_units: str = "GHz",
        touchstone_precision: int = 15,
    ):
        """Initialize touchstone export settings.

        Parameters
        ----------
        export_after_solve : bool
            Whether to export after solving.
        export_dir : str
            Directory to export to.
        export_type : int
            Type of export.
        enforce_passivity : bool
            Whether to enforce passivity.
        enforce_causality : bool
            Whether to enforce causality.
        use_common_ground : bool
            Whether to use common ground.
        show_gamma_comments : bool
            Whether to show gamma comments.
        do_renormalize : bool
            Whether to renormalize.
        renorm_impedance : float
            Renormalization impedance value.
        fitting_error : float
            Fitting error value.
        max_poles : int
            Maximum number of poles.
        passivity_algorithm : int
            Passivity algorithm type.
        column_fitting_algorithm : int
            Column fitting algorithm type.
        ss_fitting_algorithm : int
            State-space fitting algorithm type.
        relative_error_tolerance : bool
            Whether to use relative error tolerance.
        ensure_accurate_zfit : bool
            Whether to ensure accurate Z-fit.
        touchstone_format : str
            Touchstone format.
        touchstone_units : str
            Touchstone units.
        touchstone_precision : int
            Touchstone precision.
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
        self.ensure_accurate_zfit = ensure_accurate_zfit
        self.touchstone_format = touchstone_format
        self.touchstone_units = touchstone_units
        self.touchstone_precision = touchstone_precision

    def __eq__(self, other: TouchstoneExportSettings) -> bool:
        """Compare equality with another object."""
        if isinstance(other, TouchstoneExportSettings):
            return (
                self.export_after_solve == other.export_after_solve
                and self.export_dir == other.export_dir
                and self.export_type == other.export_type
                and self.enforce_passivity == other.enforce_passivity
                and self.enforce_causality == other.enforce_causality
                and self.use_common_ground == other.use_common_ground
                and self.show_gamma_comments == other.show_gamma_comments
                and self.do_renormalize == other.do_renormalize
                and self.renorm_impedance == other.renorm_impedance
                and self.fitting_error == other.fitting_error
                and self.max_poles == other.max_poles
                and self.passivity_algorithm == other.passivity_algorithm
                and self.column_fitting_algorithm == other.column_fitting_algorithm
                and self.ss_fitting_algorithm == other.ss_fitting_algorithm
                and self.relative_error_tolerance == other.relative_error_tolerance
                and self.ensure_accurate_zfit == other.ensure_accurate_zfit
                and self.touchstone_format == other.touchstone_format
                and self.touchstone_units == other.touchstone_units
                and self.touchstone_precision == other.touchstone_precision
            )
        return False
