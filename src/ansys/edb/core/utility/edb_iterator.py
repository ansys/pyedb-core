"""EDB Iterator."""

from ..models.base import ObjBase
from ..session import get_edb_iterator_stub


class EDBIterator(ObjBase):
    """Class representing an iterator over arbitrary EDB objects."""

    def __init__(self, msg, edb_obj_creator):
        """Initialize an iterator."""
        super().__init__(msg)
        self.edb_obj_creator = edb_obj_creator

    def __iter__(self):
        """Load next batch into memory."""
        self._get_next_chunk()
        return self

    def __next__(self):
        """Get next item in the iteration."""
        if not self.chunk:
            raise StopIteration
        elif self.edb_obj_idx == len(self.chunk):
            self._get_next_chunk()
            return self.__next__()
        else:
            edb_obj = self.edb_obj_creator(self.chunk[self.edb_obj_idx])
            self.edb_obj_idx += 1
            return edb_obj

    def _get_next_chunk(self):
        self.chunk = get_edb_iterator_stub().NextChunk(self.msg).edb_obj_collection
        self.edb_obj_idx = 0
