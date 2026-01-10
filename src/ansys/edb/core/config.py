"""Configuration management for pyedb-core."""
from enum import Enum
import os


class ComputationBackend(Enum):
    """Computation backend options for geometry operations."""

    SERVER = "server"  # Use RPC server
    SHAPELY = "shapely"  # Use Shapely library
    BUILD123D = "build123d"  # Use Build123D library
    AUTO = "auto"  # Auto-select: prefer server


class Config:
    """Global configuration for pyedb-core.

    Configuration can be set via environment variables or programmatically.
    CAUTION: if you are setting the backend programmatically by calling
    ``Config.set_computation_backend()``, the ``Config.reset()`` method is called
    automatically to clear any previous settings. However, if you set the backend
    via the environment variable ``PYEDB_COMPUTATION_BACKEND``, you need to call
    ``Config.reset()`` manually to ensure the new setting is applied.

    Environment Variables:
        PYEDB_COMPUTATION_BACKEND: Set to 'server', 'shapely', 'build123d', or 'auto' (default: 'auto')

    Examples:
        >>> # Set via environment variable (before importing)
        >>> import os
        >>> Config.reset()  # Clear previous settings
        >>> os.environ['PYEDB_COMPUTATION_BACKEND'] = 'shapely'

        >>> # Set programmatically
        >>> from ansys.edb.core.config import Config, ComputationBackend
        >>> Config.set_computation_backend(ComputationBackend.SHAPELY)
    """

    _computation_backend: ComputationBackend = None

    @classmethod
    def get_computation_backend(cls) -> ComputationBackend:
        """Get the current computation backend setting.

        Returns
        -------
        ComputationBackend
            The configured computation backend.
        """
        if cls._computation_backend is None:
            env_value = os.getenv("PYEDB_COMPUTATION_BACKEND", "auto").lower()
            try:
                cls._computation_backend = ComputationBackend(env_value)
            except ValueError:
                cls._computation_backend = ComputationBackend.AUTO

        return cls._computation_backend

    @classmethod
    def set_computation_backend(cls, backend: ComputationBackend | str):
        """Set the computation backend.

        Parameters
        ----------
        backend : ComputationBackend or str
            The backend to use for geometry computations.
            Can be 'server', 'shapely', 'build123d', or 'auto'.

        Examples:
            >>> Config.set_computation_backend(ComputationBackend.SHAPELY)
            >>> Config.set_computation_backend('shapely')
        """
        cls.reset()
        if isinstance(backend, str):
            backend = ComputationBackend(backend.lower())

        # Eagerly initialize the backend package to avoid slow first-time initialization
        # during the first computation operation
        if backend == ComputationBackend.SHAPELY:
            try:
                import shapely  # noqa: F401
            except ImportError:
                pass  # Will raise a more detailed error later when backend is used
        elif backend == ComputationBackend.BUILD123D:
            try:
                import build123d  # noqa: F401
            except ImportError:
                pass  # Will raise a more detailed error later when backend is used

        cls._computation_backend = backend

    @classmethod
    def reset(cls):
        """Reset configuration to defaults (useful for testing)."""
        cls._computation_backend = None
