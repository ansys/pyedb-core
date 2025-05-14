"""Bundle Terminal."""

from ansys.edb.core.inner import TypeField, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.terminal.terminal import Terminal, TerminalType


class BundleTerminal(Terminal):
    """Represents a bundle terminal object."""

    __stub = StubAccessor(StubType.bundle_terminal)
    type = TypeField(TerminalType.BUNDLE)

    @classmethod
    def create(cls, terminals):
        """Create a bundle terminal.

        Parameters
        ----------
        terminals : list of Terminal

        Returns
        -------
        BundleTerminal
        """
        return BundleTerminal(cls.__stub.Create(messages.edb_obj_collection_message(terminals)))

    @property
    def terminals(self):
        """:obj:`list` of Terminal: All terminals grouped in the terminal."""
        return [Terminal(msg).cast() for msg in self.__stub.GetTerminals(self.msg).items]

    def ungroup(self):
        """Delete the grouping."""
        self.__stub.Ungroup(self.msg)
        self.msg = None
