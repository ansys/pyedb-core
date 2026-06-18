"""Base hierarchy model."""

from ansys.edb.core.inner import ObjBase
from ansys.edb.core.inner import messages
from ansys.edb.core.session import ModelServiceStub
from ansys.edb.core.session import StubAccessor
from ansys.edb.core.session import StubType


class Model(ObjBase):
    """Represents a base hierarchy model object."""

    __stub: ModelServiceStub = StubAccessor(StubType.model)

    def clone(self):
        """Clone a model.

        Returns
        -------
        Model cloned.
        """
        return self.__class__(self.__stub.Clone(messages.edb_obj_message(self)))
