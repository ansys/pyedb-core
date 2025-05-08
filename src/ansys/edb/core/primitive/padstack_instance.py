"""Primitive classes."""

from enum import Enum

from ansys.api.edb.v1 import padstack_instance_pb2, padstack_instance_pb2_grpc

from ansys.edb.core.definition.padstack_def import PadstackDef
from ansys.edb.core.edb_defs import LayoutObjType
from ansys.edb.core.inner import conn_obj, messages
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.layer_map import LayerMap
from ansys.edb.core.utility.value import Value


class BackDrillType(Enum):
    """Provides an enum representing back drill types."""

    NO_DRILL = padstack_instance_pb2.NO_DRILL
    LAYER_DRILL = padstack_instance_pb2.LAYER_DRILL
    DEPTH_DRILL = padstack_instance_pb2.DEPTH_DRILL


class PadstackInstance(conn_obj.ConnObj):
    """Representis a padstack instance object."""

    __stub: padstack_instance_pb2_grpc.PadstackInstanceServiceStub = StubAccessor(
        StubType.padstack_instance
    )
    layout_obj_type = LayoutObjType.PADSTACK_INSTANCE

    @classmethod
    def create(
        cls,
        layout,
        net,
        name,
        padstack_def,
        position_x,
        position_y,
        rotation,
        top_layer,
        bottom_layer,
        solder_ball_layer,
        layer_map,
    ):
        """Create a padstack instance.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the padstack instance in.
        net : :class:`.Net`
            Net of the padstack instance.
        name : str
            Name of the padstack instance.
        padstack_def : :class:`.PadstackDef`
            Padstack definition of the padstack instance.
        position_x : :class:`.Value`
            Position x of the padstack instance.
        position_y : :class:`.Value`
            Position y of the padstack instance.
        rotation : :class:`.Value`
            Rotation of the padstack instance.
        top_layer : :class:`.Layer`
            Top layer of the padstack instance.
        bottom_layer : :class:`.Layer`
            Bottom layer of the padstack instance.
        solder_ball_layer : :class:`.Layer`
            Solder ball layer of the padstack instance or ``None`` for none.
        layer_map : :class:`.LayerMap`
            Layer map of the padstack instance. ``None`` or empty results in
            auto-mapping.

        Returns
        -------
        PadstackInstance
            Padstack instance created.
        """
        padstack_instance = PadstackInstance(
            cls.__stub.Create(
                padstack_instance_pb2.PadstackInstCreateMessage(
                    layout=layout.msg,
                    net=net.msg,
                    name=name,
                    padstack_def=padstack_def.msg,
                    rotation=messages.value_message(rotation),
                    top_layer=top_layer.msg,
                    bottom_layer=bottom_layer.msg,
                    solder_ball_layer=messages.edb_obj_message(solder_ball_layer),
                    layer_map=messages.edb_obj_message(layer_map),
                )
            )
        )
        padstack_instance.set_position_and_rotation(position_x, position_y, rotation)
        return padstack_instance

    @property
    def padstack_def(self):
        """:class:`.PadstackDef`: \
        Definition of the padstack instance."""
        return PadstackDef(self.__stub.GetPadstackDef(self.msg))

    @property
    def name(self):
        """:obj:`str`: Name of the padstack instance."""
        return self.__stub.GetName(self.msg).value

    @name.setter
    def name(self, name):
        self.__stub.SetName(messages.edb_obj_name_message(self, name))

    def get_position_and_rotation(self):
        """Get the position and rotation of the padstack instance.

        Returns
        -------
        tuple[
            :class:`.Value`,
            :class:`.Value`,
            :class:`.Value`
        ]

            Returns a tuple in this format:

            **(x, y, rotation)**

            **x** : X coordinate.

            **y** : Y coordinate.

            **rotation** : Rotation in radians.
        """
        params = self.__stub.GetPositionAndRotation(self.msg)
        return (
            Value(params.position.x),
            Value(params.position.y),
            Value(params.rotation),
        )

    def set_position_and_rotation(self, x, y, rotation):
        """Set the position and rotation of the padstack instance.

        Parameters
        ----------
        x : :class:`.Value`
            x : X coordinate.
        y : :class:`.Value`
            y : Y coordinate.
        rotation : :class:`.Value`
            Rotation in radians.
        """
        self.__stub.SetPositionAndRotation(
            padstack_instance_pb2.PadstackInstSetPositionAndRotationMessage(
                target=self.msg,
                params=padstack_instance_pb2.PadstackInstPositionAndRotationMessage(
                    position=messages.point_message((x, y)),
                    rotation=messages.value_message(rotation),
                ),
            )
        )

    def get_layer_range(self):
        """Get the top and bottom layers of the padstack instance.

        Returns
        -------
        tuple[:class:`.Layer`, :class:`.Layer`]
            The tuple is in this format: ``(top_layer, bottom_layer)``.

            - ``top_layer``: Top layer of the padstack instance
            - ``bottom_layer``: Bottom layer of the padstack instance
        """
        params = self.__stub.GetLayerRange(self.msg)
        return (
            Layer(params.top_layer).cast(),
            Layer(params.bottom_layer).cast(),
        )

    def set_layer_range(self, top_layer, bottom_layer):
        """Set the top and bottom layers of the padstack instance.

        Parameters
        ----------
        top_layer : :class:`.Layer`
            Top layer of the padstack instance.
        bottom_layer : :class:`.Layer`
            Bottom layer of the padstack instance.
        """
        self.__stub.SetLayerRange(
            padstack_instance_pb2.PadstackInstSetLayerRangeMessage(
                target=self.msg,
                range=padstack_instance_pb2.PadstackInstLayerRangeMessage(
                    top_layer=top_layer.msg,
                    bottom_layer=bottom_layer.msg,
                ),
            )
        )

    @property
    def solderball_layer(self):
        """:class:`.Layer`: Solderball layer of the padstack instance."""
        sb_layer = Layer(self.__stub.GetSolderBallLayer(self.msg))
        return sb_layer if sb_layer.is_null() else sb_layer.cast()

    @solderball_layer.setter
    def solderball_layer(self, solderball_layer):
        self.__stub.SetSolderBallLayer(
            padstack_instance_pb2.PadstackInstSetSolderBallLayerMessage(
                target=self.msg,
                layer=solderball_layer.msg,
            )
        )

    @property
    def layer_map(self):
        """:class:`.LayerMap`: Layer map of the padstack instance."""
        return LayerMap(self.__stub.GetLayerMap(self.msg))

    @layer_map.setter
    def layer_map(self, layer_map):
        self.__stub.SetLayerMap(messages.pointer_property_message(self, layer_map))

    def get_hole_overrides(self):
        """Get the hole overrides of the padstack instance.

        Returns
        -------
        tuple[
            bool,
            :class:`.Value`
        ]

            Returns a tuple in this format:

            **(is_hole_override, hole_override)**

            **is_hole_override** : If padstack instance is hole override.

            **hole_override** : Hole override diameter of this padstack instance.
        """
        params = self.__stub.GetHoleOverrides(self.msg)
        return (
            params.is_hole_override,
            Value(params.hole_override),
        )

    def set_hole_overrides(self, is_hole_override, hole_override):
        """Set the hole overrides of the padstack instance.

        Parameters
        ----------
        is_hole_override : bool
            Whether the padstack instance is a hole override.
        hole_override : :class:`.Value`
            Hole override diameter of the padstack instance.
        """
        self.__stub.SetHoleOverrides(
            padstack_instance_pb2.PadstackInstSetHoleOverridesMessage(
                target=self.msg,
                hole_override_msg=padstack_instance_pb2.PadstackInstHoleOverridesMessage(
                    is_hole_override=is_hole_override,
                    hole_override=messages.value_message(hole_override),
                ),
            )
        )

    @property
    def is_layout_pin(self):
        """:obj:`bool`: Flag indicating if the padstack instance is a layout pin."""
        return self.__stub.GetIsLayoutPin(self.msg).value

    @is_layout_pin.setter
    def is_layout_pin(self, is_layout_pin):
        self.__stub.SetIsLayoutPin(
            padstack_instance_pb2.PadstackInstSetIsLayoutPinMessage(
                target=self.msg,
                is_layout_pin=is_layout_pin,
            )
        )

    def get_back_drill_type(self, from_bottom):
        """Get the back drill type of the padstack instance.

        Parameters
        ----------
        from_bottom : bool
            Whether to get the back drill type from the bottom.

        Returns
        -------
        :class:`BackDrillType`
            Back drill type of the padastack instance.
        """
        return BackDrillType(
            self.__stub.GetBackDrillType(
                PadstackInstance._get_back_drill_message(self, from_bottom)
            ).type
        )

    def get_back_drill_by_layer(self, from_bottom):
        """Get the back drill type by the layer.

        Parameters
        ----------
        from_bottom : bool
            Whether to get the back drill type from the bottom.

        Returns
        -------
        tuple[
            bool,
            :class:`.Value`,
            :class:`.Value`
        ]

            Returns a tuple in this format:

            **(drill_to_layer, offset, diameter)**

            **drill_to_layer** : Layer drills to. If drill from top, drill stops at the upper elevation of the layer.\
            If from bottom, drill stops at the lower elevation of the layer.

            **offset** : Layer offset (or depth if layer is empty).

            **diameter** : Drilling diameter.
        """
        params = self.__stub.GetBackDrillByLayer(
            PadstackInstance._get_back_drill_message(self, from_bottom)
        )

        return (
            Layer(params.drill_to_layer).cast(),
            Value(params.offset),
            Value(params.diameter),
        )

    def set_back_drill_by_layer(self, drill_to_layer, offset, diameter, from_bottom):
        """Set the back drill by the layer.

        Parameters
        ----------
        drill_to_layer : :class:`.Layer`
            Layer to drill to. If drilling from the top, the drill stops at the upper
            elevation of the layer. If drilling from the bottom, the drill stops at
            the lower elevation of the layer.
        offset : :class:`.Value`
            Layer offset (or depth if the layer is empty).
        diameter : :class:`.Value`
            Drilling diameter.
        from_bottom : bool
            Whether to set the back drill type from the bottom.
        """
        self.__stub.SetBackDrillByLayer(
            padstack_instance_pb2.PadstackInstSetBackDrillByLayerMessage(
                target=self.msg,
                drill_to_layer=drill_to_layer.msg,
                offset=messages.value_message(offset),
                diameter=messages.value_message(diameter),
                from_bottom=from_bottom,
            )
        )

    def get_back_drill_by_depth(self, from_bottom):
        """Get the back drill type by depth.

        Parameters
        ----------
        from_bottom : bool
            Whether to get the back drill type from the bottom.

        Returns
        -------
        tuple[
            bool,
            :class:`.Value`
        ]
            Returns a tuple in this format:

            **(drill_depth, diameter)**

            **drill_depth** : Drilling depth, may not align with layer.

            **diameter** : Drilling diameter.
        """
        params = self.__stub.GetBackDrillByDepth(
            PadstackInstance._get_back_drill_message(self, from_bottom)
        )
        return Value(params.drill_depth), Value(params.diameter)

    def set_back_drill_by_depth(self, drill_depth, diameter, from_bottom):
        """Set the back drill type by depth.

        Parameters
        ----------
        drill_depth : :class:`.Value`
            Drilling depth, which may not align with the layer.
        diameter : :class:`.Value`
            Drilling diameter.
        from_bottom : bool
            Whether to set the back drill type from the bottom.
        """
        self.__stub.SetBackDrillByDepth(
            padstack_instance_pb2.PadstackInstSetBackDrillByDepthMessage(
                target=self.msg,
                drill_depth=messages.value_message(drill_depth),
                diameter=messages.value_message(diameter),
                from_bottom=from_bottom,
            )
        )

    def get_padstack_instance_terminal(self):
        """:class:`.PadstackInstanceTerminal`: \
        Terminal of the padstack instance."""
        from ansys.edb.core.terminal import padstack_instance_terminal

        return padstack_instance_terminal.PadstackInstanceTerminal(
            self.__stub.GetPadstackInstanceTerminal(self.msg)
        )

    def is_in_pin_group(self, pin_group):
        """Determine if the padstack instance is in a given pin group.

        Parameters
        ----------
        pin_group : :class:`.PinGroup`
            Pin group to check if the padstack instance is in it.

        Returns
        -------
        bool
            Whether the padstack instance is in a pin group.
        """
        return self.__stub.IsInPinGroup(
            padstack_instance_pb2.PadstackInstIsInPinGroupMessage(
                target=self.msg,
                pin_group=pin_group.msg,
            )
        ).value

    @property
    def pin_groups(self):
        """:obj:`list` of :class:`.PinGroup`: \
        Pin groups of the padstack instance.

        This property is read-only.
        """
        from ansys.edb.core.hierarchy import pin_group

        pins = self.__stub.GetPinGroups(self.msg).items
        return [pin_group.PinGroup(p) for p in pins]

    @staticmethod
    def _get_back_drill_message(padstack_inst, from_bottom):
        return padstack_instance_pb2.PadstackInstGetBackDrillMessage(
            target=padstack_inst.msg,
            from_bottom=from_bottom,
        )
