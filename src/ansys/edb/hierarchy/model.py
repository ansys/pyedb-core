"""Base Hierarchy Model."""
from ansys.edb.core import LOGGER, ObjBase, messages
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

    def cast(self):
        """Cast the model object to correct concrete type.

        Returns
        -------
        Model
        """
        # temporarily stop logging since we expect exceptions here.
        LOGGER.stop_logging_to_stdout()

        def get_derived_type():
            from ansys.edb.hierarchy import (
                netlist_model,
                pin_pair_model,
                sparameter_model,
                spice_model,
            )

            # This is a hack to isolate changes to client side and will be cleaned up in R24.1.
            # To get a model object of the correct derived type, try creating an object of each
            # model type and calling a method on it. If we get an exception, then the model is
            # not of that type and we try the next one. Otherwise, return that object since it is
            # of the correct type.
            try:
                spice_model_obj = spice_model.SPICEModel(self.msg)
                spice_model_obj.model_name
                return spice_model_obj
            except:
                try:
                    s_param_model_obj = sparameter_model.SParameterModel(self.msg)
                    s_param_model_obj.reference_net
                    return s_param_model_obj
                except:
                    try:
                        netlist_model_obj = netlist_model.NetlistModel(self.msg)
                        netlist_model_obj.netlist
                        return netlist_model_obj
                    except:
                        try:
                            pin_pair_model_obj = pin_pair_model.PinPairModel(self.msg)
                            pin_pair_model_obj.pin_pairs()
                            return pin_pair_model_obj
                        except:
                            raise Exception("Encountered invalid component model object.")

        # Get the derived type
        derived_obj = get_derived_type()

        # Enable logging again
        LOGGER.log_to_stdout()
        return derived_obj
