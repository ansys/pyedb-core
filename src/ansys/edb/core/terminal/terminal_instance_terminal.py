"""Terminal Instance Terminal."""

from ansys.edb.core.inner import TypeField, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.terminal.terminal import Terminal, TerminalType
from ansys.edb.core.terminal.terminal_instance import TerminalInstance


class TerminalInstanceTerminal(Terminal):
    """Represents a terminal instance terminal."""

    __stub = StubAccessor(StubType.terminal_instance_terminal)
    type = TypeField(TerminalType.TERM_INST)

    @classmethod
    def create(cls, layout, term_instance, name, net_ref, is_ref=False):
        """Create a terminal instance terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the terminal instance terminal in.
        term_instance : TerminalInstance
            Terminal instance to create the terminal instance terminal on.
        name : :obj:`str`
            Name of the terminal instance terminal.
        net_ref : :class:`.Net` or :obj:`str` or None
            Net reference.
        is_ref : bool, default: False
            Whether the terminal instance terminal is a reference terminal.

        Returns
        -------
        TerminalInstanceTerminal
        """
        return TerminalInstanceTerminal(
            cls.__stub.Create(
                messages.term_inst_term_creation_message(
                    layout, net_ref, name, term_instance, is_ref
                )
            )
        )

    @property
    def terminal_instance(self):
        """:class:`TerminalInstance`: Terminal instance."""
        return TerminalInstance(self.__stub.GetTerminalInstance(self.msg))

    @terminal_instance.setter
    def terminal_instance(self, value):
        self.__stub.SetTerminalInstance(messages.term_inst_term_set_instance_message(self, value))
