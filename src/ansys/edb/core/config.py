"""Configuration management for pyedb-core."""
import os
from enum import Enum


class ComputationBackend(Enum):
    """Computation backend options for geometry operations."""

    SERVER = "server"  # Use RPC server (server-side)
    SHAPELY = "shapely"  # Use Shapely library (client-side)
    AUTO = "auto"  # Auto-select: prefer shapely if available, fallback to server


class Config:
    """Global configuration for pyedb-core.

    Configuration can be set via environment variables or programmatically.

    Environment Variables:
        PYEDB_COMPUTATION_BACKEND: Set to 'server', 'shapely', or 'auto' (default: 'auto')

    Examples:
        >>> # Set via environment variable (before importing)
        >>> import os
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
            # Read from environment variable
            env_value = os.getenv("PYEDB_COMPUTATION_BACKEND", "auto").lower()
            try:
                cls._computation_backend = ComputationBackend(env_value)
            except ValueError:
                # Invalid value, default to AUTO
                cls._computation_backend = ComputationBackend.AUTO

        return cls._computation_backend

    @classmethod
    def set_computation_backend(cls, backend: ComputationBackend | str):
        """Set the computation backend.

        Parameters
        ----------
        backend : ComputationBackend or str
            The backend to use for geometry computations.
            Can be 'server', 'shapely', or 'auto'.

        Examples:
            >>> Config.set_computation_backend(ComputationBackend.SHAPELY)
            >>> Config.set_computation_backend('shapely')
        """
        if isinstance(backend, str):
            backend = ComputationBackend(backend.lower())
        cls._computation_backend = backend

    @classmethod
    def reset(cls):
        """Reset configuration to defaults (useful for testing)."""
        cls._computation_backend = None
