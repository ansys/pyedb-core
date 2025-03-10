"""Bondwire."""

from enum import Enum

from ansys.api.edb.v1 import bondwire_pb2, bondwire_pb2_grpc

from ansys.edb.core.inner import messages
from ansys.edb.core.layer.layer import Layer
from ansys.edb.core.primitive.primitive import Primitive
from ansys.edb.core.session import StubAccessor, StubType
from ansys.edb.core.utility.value import Value


class BondwireCrossSectionType(Enum):
    """Provides an enum representing bondwire cross section types."""

    ROUND = bondwire_pb2.BONDWIRE_ROUND
    RECTANGLE = bondwire_pb2.BONDWIRE_RECTANGLE
    INVALID = bondwire_pb2.INVALID_BONDWIRE_CROSS_SECTION_TYPE


class BondwireType(Enum):
    """Provides an enum representing bondwire types."""

    APD = bondwire_pb2.APD_BONDWIRE
    JEDEC4 = bondwire_pb2.JEDEC4_BONDWIRE
    JEDEC5 = bondwire_pb2.JEDEC5_BONDWIRE
    NUM_OF_TYPE = bondwire_pb2.NUM_OF_BONDWIRE_TYPE
    INVALID = bondwire_pb2.INVALID_BONDWIRE_TYPE


class Bondwire(Primitive):
    """Represents a bondwire object."""

    __stub: bondwire_pb2_grpc.BondwireServiceStub = StubAccessor(StubType.bondwire)

    @classmethod
    def create(
        cls,
        layout,
        bondwire_type,
        definition_name,
        placement_layer,
        width,
        material,
        start_context,
        start_layer_name,
        start_x,
        start_y,
        end_context,
        end_layer_name,
        end_x,
        end_y,
        net,
    ):
        """Create a bondwire.

        Parameters
        ----------
        layout : :class:`.Layout`
            Layout to create the bondwire in.
        bondwire_type : :class:`BondwireType`
            Type of the bondwire. Options are ``kAPDBondWire`` and ``kJDECBondWire``.
        definition_name : str
            Bondwire definition name.
        placement_layer : str
            Layer name to create the bondwire on.
        width : :class:`.Value`
            Bondwire width.
        material : str
            Bondwire material name.
        start_context : :class:`.CellInstance`
            Start context. ``None`` means top-level,.
        start_layer_name : str
            Name of the start layer.
        start_x : :class:`.Value`
            X value of the start point.
        start_y : :class:`.Value`
            Y value of the start point.
        end_context : :class:`.CellInstance`
            End context: End content. ``None`` means top-level.
        end_layer_name : str
            Name of the end layer.
        end_x : :class:`.Value`
            X value of the end point.
        end_y : :class:`.Value`
            Y value of the end point.
        net : str or :class:`.Net` or None
            Net of the bondwire.

        Returns
        -------
        Bondwire
            Bondwire object created.
        """
        return Bondwire(
            cls.__stub.Create(
                bondwire_pb2.BondwireCreateMessage(
                    layout=layout.msg,
                    net=messages.net_ref_message(net),
                    bondwire_type=bondwire_type.value,
                    definition_name=definition_name,
                    placement_layer=placement_layer,
                    width=messages.value_message(width),
                    material=material,
                    start_context=messages.edb_obj_message(start_context),
                    start_layer_name=start_layer_name,
                    start_x=messages.value_message(start_x),
                    start_y=messages.value_message(start_y),
                    end_context=messages.edb_obj_message(end_context),
                    end_layer_name=end_layer_name,
                    end_x=messages.value_message(end_x),
                    end_y=messages.value_message(end_y),
                )
            )
        )

    def get_material(self, evaluated=True):
        """Get the material of the bondwire.

        Parameters
        ----------
        evaluated : bool, default: True
            Whether an evaluated (in variable namespace) material name is wanted.

        Returns
        -------
        str
            Material name.
        """
        return self.__stub.GetMaterial(Bondwire._bondwire_bool_message(self, evaluated))

    def set_material(self, material):
        """Set the material of the bondwire.

        Parameters
        ----------
        material : str
            Material name.
        """
        self.__stub.SetMaterial(bondwire_pb2.SetMaterialMessage(target=self.msg, material=material))

    @property
    def type(self):
        """:class:`BondwireType`: Type of the bondwire."""
        btype_msg = self.__stub.GetType(self.msg)
        return BondwireType(btype_msg.type)

    @type.setter
    def type(self, bondwire_type):
        self.__stub.SetType(
            bondwire_pb2.SetBondwireTypeMessage(target=self.msg, type=bondwire_type.value)
        )

    @property
    def cross_section_type(self):
        """:class:`BondwireCrossSectionType`:Cross-section type of the bondwire."""
        return BondwireCrossSectionType(self.__stub.GetCrossSectionType(self.msg).type)

    @cross_section_type.setter
    def cross_section_type(self, bondwire_type):
        self.__stub.SetCrossSectionType(
            bondwire_pb2.SetCrossSectionTypeMessage(target=self.msg, type=bondwire_type.value)
        )

    @property
    def cross_section_height(self):
        """:class:`.Value`: Cross-section height of the bondwire."""
        return Value(self.__stub.GetCrossSectionHeight(self.msg))

    @cross_section_height.setter
    def cross_section_height(self, height):
        self.__stub.SetCrossSectionHeight(
            bondwire_pb2.SetCrossSectionHeightMessage(
                target=self.msg, height=messages.value_message(height)
            )
        )

    def get_definition_name(self, evaluated=True):
        """Get the definition name of the bondwire object.

        Parameters
        ----------
        evaluated : bool, default: True
            Whether an evaluated (in variable namespace) material name is wanted.

        Returns
        -------
        str
            Bondwire definition name.
        """
        return self.__stub.GetDefinitionName(Bondwire._bondwire_bool_message(self, evaluated)).value

    def set_definition_name(self, definition_name):
        """Set the definition name of a bondwire.

        Parameters
        ----------
        definition_name : str
            Bondwire definition name to set.
        """
        self.__stub.SetDefinitionName(
            bondwire_pb2.SetDefinitionNameMessage(target=self.msg, definition_name=definition_name)
        )

    def get_traj(self):
        """Get trajectory parameters of the bondwire.

        Returns
        -------
        tuple[
            :class:`.Value`,
            :class:`.Value`,
            :class:`.Value`,
            :class:`.Value`
        ]

            Returns a tuple in this format:

            **(x1, y1, x2, y2)**

            **x1** : X value of the start point.

            **y1** : Y value of the start point.

            **x1** : X value of the end point.

            **y1** : Y value of the end point.
        """
        traj_msg = self.__stub.GetTraj(self.msg)
        return (
            Value(traj_msg.x1),
            Value(traj_msg.y1),
            Value(traj_msg.x2),
            Value(traj_msg.y2),
        )

    def set_traj(self, x1, y1, x2, y2):
        """Set the parameters of the trajectory of the bondwire.

        Parameters
        ----------
        x1 : :class:`.Value`
            X value of the start point.
        y1 : :class:`.Value`
            Y value of the start point.
        x2 : :class:`.Value`
            X value of the end point.
        y2 : :class:`.Value`
            Y value of the end point.
        """
        self.__stub.SetTraj(
            bondwire_pb2.SetBondwireTrajMessage(
                target=self.msg,
                traj=bondwire_pb2.BondwireTrajMessage(
                    x1=messages.value_message(x1),
                    y1=messages.value_message(y1),
                    x2=messages.value_message(x2),
                    y2=messages.value_message(y2),
                ),
            )
        )

    @property
    def width(self):
        """:class:`.Value`: Width of the bondwire."""
        val = self.__stub.GetWidthValue(self.msg)
        return Value(val)

    @width.setter
    def width(self, width):
        self.__stub.SetWidthValue(
            bondwire_pb2.BondwireValueMessage(target=self.msg, value=messages.value_message(width))
        )

    def get_start_elevation(self, start_context):
        """Get the start elevation layer of the bondwire.

        Parameters
        ----------
        start_context : :class:`.CellInstance`
            Start cell context of the bondwire.

        Returns
        -------
        :class:`.Layer`
            Start elevation level of the bondwire.
        """
        return Layer(
            self.__stub.GetStartElevation(Bondwire._get_elevation_message(self, start_context))
        ).cast()

    def set_start_elevation(self, start_context, layer):
        """Set the start elevation of the bondwire.

        Parameters
        ----------
        start_context : :class:`.CellInstance`
            Start cell context of the bondwire. ``None`` means top-level.
        layer : str or :class:`.Layer`
            Start layer of the bondwire.
        """
        self.__stub.SetStartElevation(Bondwire._set_elevation_message(self, start_context, layer))

    def get_end_elevation(self, end_context):
        """Get the end elevation layer of the bondwire.

        Parameters
        ----------
        end_context : :class:`.CellInstance`
            End cell context of the bondwire.

        Returns
        -------
        :class:`.Layer`
            End elevation layer of the bondwire.
        """
        return Layer(
            self.__stub.GetEndElevation(Bondwire._get_elevation_message(self, end_context))
        ).cast()

    def set_end_elevation(self, end_context, layer):
        """Set the end elevation of the bondwire.

        Parameters
        ----------
        end_context : :class:`.CellInstance`
            End cell context of the bondwire. ``None`` means top-level.
        layer : str or :class:`.Layer`
            End layer of the bondwire.
        """
        self.__stub.SetEndElevation(Bondwire._set_elevation_message(self, end_context, layer))

    @staticmethod
    def _bondwire_bool_message(b, evaluated):
        return bondwire_pb2.BondwireBoolMessage(target=b.msg, evaluated=evaluated)

    @staticmethod
    def _get_elevation_message(b, cell_instance):
        return bondwire_pb2.GetElevationMessage(
            bw=b.msg, cell_instance=messages.edb_obj_message(cell_instance)
        )

    @staticmethod
    def _set_elevation_message(b, cell_instance, lyrname):
        return bondwire_pb2.SetElevationMessage(
            target=Bondwire._get_elevation_message(b, cell_instance), lyrname=lyrname
        )
