"""Base Hierarchy Model."""
from ansys.edb.core.base import ObjBase
from ansys.edb.core import messages
from ansys.edb.session import ModelServiceStub, StubAccessor, StubType


class Model(ObjBase):
    """Class representing a base hierarchy model object."""

    __stub: ModelServiceStub = StubAccessor(StubType.model)

    def clone(self):
        """Clone a model.

        Returns
        -------
        Model
        """
        return self.__class__(self.__stub.Clone(messages.edb_obj_message(self)))
