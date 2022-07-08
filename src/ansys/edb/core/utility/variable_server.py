"""VariableServer Class."""

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage
import ansys.api.edb.v1.value_pb2 as value_server_msgs
import ansys.api.edb.v1.variable_server_pb2 as variable_server_msgs

from ..interface.grpc.messages import value_message
from ..session import get_value_stub, get_variable_server_stub
from ..utility.edb_errors import handle_grpc_exception
from ..utility.value import Value


class _VariableServer:
    """Class that owns variables.

    It can be either database, cell, or component_def object.
    """

    def __init__(self, variable_owner):
        """Initialize VariableServer object.

        Parameters
        ----------
        variable_owner : EdbObjMessage
            id of either a database, cell, or component_def.
        """
        assert variable_owner.id > 0, "Invalid variable owner id"
        self.variable_owner = EDBObjMessage(id=variable_owner.id)

    @handle_grpc_exception
    def add_variable(self, name, value, is_param=False):
        """Add new variable to the VariableServer.

        Parameters
        ----------
        name : str
        value : str, int, double, complex, Value
        is_param : bool, optional
            True means the new variable is a parameter, False means it is a local variable
        """
        temp = variable_server_msgs.AddVariableMessage(
            variable_owner=self.variable_owner,
            name=name,
            value=value_message(value),
            isparam=is_param,
        )
        get_variable_server_stub().AddVariable(temp)

    @handle_grpc_exception
    def add_menu_variable(self, name, values, is_param, index=0):
        """Add new menu variable to the VariableServer.

        Parameters
        ----------
        name : str
        values : list of str, double, complex
        is_param : bool
            True means the new variable is a parameter, False means it is a local variable
        index : int, optional
            The index of the value that is initially selected
        """
        list_of_vms = []
        for value in values:
            list_of_vms.append(value_message(value))

        temp = variable_server_msgs.AddMenuVariableMessage(
            variable_owner=self.variable_owner,
            name=name,
            values=list_of_vms,
            isparam=is_param,
            index=index,
        )
        get_variable_server_stub().AddMenuVariable(temp)

    @handle_grpc_exception
    def delete_variable(self, name):
        """Add new menu variable to the VariableServer.

        Parameters
        ----------
        name : str
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        get_variable_server_stub().DeleteVariable(temp)

    @handle_grpc_exception
    def set_variable_value(self, name, new_value):
        """Set variable to have a new value.

        Parameters
        ----------
        name : str
        new_value : str, double, complex, Value
        """
        temp = variable_server_msgs.SetVariableMessage(
            variable_owner=self.variable_owner, name=name, value=value_message(new_value)
        )
        get_variable_server_stub().SetVariableValue(temp)

    @handle_grpc_exception
    def get_variable_value(self, name):
        """Get the existing value from the variable.

        Parameters
        ----------
        name : str

        Returns
        -------
        Value
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return Value(get_variable_server_stub().GetVariableValue(temp))

    @handle_grpc_exception
    def is_parameter(self, name):
        """Return True if the variable is a parameter, otherwise False.

        Parameters
        ----------
        name : str

        Returns
        -------
        bool
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return get_variable_server_stub().IsParameter(temp).value

    @handle_grpc_exception
    def get_all_variable_names(self):
        """Return names of all variables in the VariableServer.

        Returns
        -------
        list of str
        """
        return get_variable_server_stub().GetAllVariableNames(self.variable_owner).names

    @handle_grpc_exception
    def get_variable_desc(self, name):
        """Set variable to have a new description.

        Parameters
        ----------
        name : str

        Returns
        -------
        str
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return get_variable_server_stub().GetVariableDesc(temp).value

    @handle_grpc_exception
    def set_variable_desc(self, name, desc):
        """Set variable to have a new value.

        Parameters
        ----------
        name : str
        desc : str
        """
        temp = variable_server_msgs.SetDescriptionMessage(
            variable_owner=self.variable_owner, name=name, desc=desc
        )
        get_variable_server_stub().SetVariableDesc(temp)

    def create_value(self, val):
        """Create a Value that can reference variables in this VariableServer.

        Parameters
        ----------
        val : str, int, float, complex

        Returns
        -------
        Value
        """
        if isinstance(val, str):
            temp = value_server_msgs.ValueTextMessage(text=val, variable_owner=self.msg)
            return Value(get_value_stub().CreateValue(temp))

        return Value(val)
