"""Pin Group Terminal."""

from ansys.edb.core.inner import TypeField, messages
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.terminal.terminal import Terminal, TerminalType


class PinGroupTerminal(Terminal):
    """Represents a pin group terminal."""

    __stub = StubAccessor(StubType.pin_group_terminal)
    type = TypeField(TerminalType.PIN_GROUP)

    @classmethod
    def create(cls, layout, name, pin_group, net, is_ref=False):
        """Create a pin group terminal.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the pin group terminal in.
        net : :class:`.Net` or :obj:`str` or None
            Net reference.
        name : :obj:`str`
            Name of the pin group terminal.
        pin_group : :class:`.PinGroup`
            Pin group.
        is_ref : :obj:`bool`, default: False
            Whether the pin group terminal is a reference terminal.

        Returns
        -------
        PinGroupTerminal
        """
        return PinGroupTerminal(
            cls.__stub.Create(
                messages.pin_group_term_creation_message(layout, net, name, pin_group, is_ref)
            )
        )

    @property
    def pin_group(self):
        """:class:`.PinGroup`: Pin group of the terminal."""
        from ansys.edb.core.hierarchy import pin_group

        return pin_group.PinGroup(self.__stub.GetPinGroup(self.msg))

    @pin_group.setter
    def pin_group(self, value):
        self.__stub.SetPinGroup(messages.pin_group_term_set_pin_group_message(self, value))

    @property
    def layer(self):
        """:class:`.Layer`: Layer."""
        return Layer(self.__stub.GetLayer(self.msg)).cast()

    @layer.setter
    def layer(self, value):
        self.__stub.SetLayer(messages.pin_group_term_set_layer_message(self, value))
