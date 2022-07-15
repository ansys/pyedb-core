"""RLC."""

from ansys.edb.core.core.base import ObjBase
from ansys.edb.core.utility.value import Value


class Rlc(ObjBase):
    """Class representing RLC."""

    def __init__(self, **kwargs):
        """Construct RLC object from message."""
        if "msg" in kwargs:
            self._msg = kwargs.get("msg")
        else:
            self._msg = None
            self._r = kwargs.get("r", 0)
            self._l = kwargs.get("l", 0)
            self._c = kwargs.get("c", 0)
            self._r_enabled = kwargs.get("r_enabled", False)
            self._l_enabled = kwargs.get("l_enabled", False)
            self._c_enabled = kwargs.get("c_enabled", False)
            self._is_parallel = kwargs.get("is_parallel", True)

    @property
    def r(self):
        """Return resistance value.

        Returns
        -------
        float
        """
        return self._r if self._msg is None else Value(self._msg.r)

    @property
    def l(self):
        """Return induction value.

        Returns
        -------
        float
        """
        return self._l if self._msg is None else Value(self._msg.l)

    @property
    def c(self):
        """Return capacitance value.

        Returns
        -------
        float
        """
        return self._c if self._msg is None else Value(self._msg.c)

    @property
    def r_enabled(self):
        """Return whether resistance is enabled.

        Returns
        -------
        bool
        """
        return self._r_enabled if self._msg is None else self._msg.r_enabled.value

    @property
    def l_enabled(self):
        """Return whether induction is enabled.

        Returns
        -------
        bool
        """
        return self._l_enabled if self._msg is None else self._msg.l_enabled.value

    @property
    def c_enabled(self):
        """Return whether capacitance is enabled.

        Returns
        -------
        bool
        """
        return self._c_enabled if self._msg is None else self._msg.c_enabled.value

    @property
    def is_parallel(self):
        """Return if parallel.

        Returns
        -------
        bool
        """
        return self._is_parallel if self._msg is None else self._msg.is_parallel.value
