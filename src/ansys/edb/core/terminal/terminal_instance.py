"""Terminal Instance."""

from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import conn_obj, messages
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.terminal.terminal import Terminal


class TerminalInstance(conn_obj.ConnObj):
    """Represents a terminal instance."""

    __stub = StubAccessor(StubType.terminal_instance)
    layout_obj_type = LayoutObjType.TERMINAL_INSTANCE

    @classmethod
    def create(cls, layout, cell_instance, name, net_ref):
        """Create a terminal instance.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the terminal instance in.
        cell_instance : :class:`.CellInstance`
            Name of the cell instance to create the terminal instance on.
        name : :obj:`str`
            Name of the terminal instance.
        net_ref : :class:`.Net` or :obj:`str` or None
            Net reference.

        Returns
        -------
        TerminalInstance
        """
        return TerminalInstance(
            cls.__stub.Create(
                messages.term_inst_creation_message(layout, net_ref, cell_instance, name)
            )
        )

    @property
    def owning_cell_instance(self):
        """:class:`.CellInstance`: Cell instance that owns the terminal."""
        from ansys.edb.core.hierarchy import cell_instance

        return cell_instance.CellInstance(self.__stub.GetOwningCellInstance(self.msg))

    @property
    def definition_terminal(self):
        """:class:`Terminal`: Definition terminal, if any."""
        return Terminal(self.__stub.GetDefinitionTerminal(self.msg)).cast()

    @property
    def definition_terminal_name(self):
        """:obj:`str`: Name of the definition terminal."""
        return self.__stub.GetDefinitionTerminalName(self.msg).value
