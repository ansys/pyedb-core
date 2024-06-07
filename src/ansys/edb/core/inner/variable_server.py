"""Variable server class."""

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage
import ansys.api.edb.v1.variable_server_pb2 as variable_server_msgs

from ansys.edb.core.inner.messages import value_message
from ansys.edb.core.session import get_variable_server_stub
from ansys.edb.core.utility.value import Value


class VariableServer:
    """Provides a class that owns variables.

    A variables can be either a database, cell, or component definition object.
    """

    def __init__(self, variable_owner):
        """Initialize the variable server object.

        Parameters
        ----------
        variable_owner : EdbObjMessage
            ID of either a database, cell, or component definition.
        """
        assert variable_owner.id > 0, "Invalid variable owner ID,"
        self.variable_owner = EDBObjMessage(id=variable_owner.id)

    def add_variable(self, name, value, is_param=False):
        """Add a variable.

        Parameters
        ----------
        name : str
            Variable name.
        value : str, int, float, complex, :class:`.Value`
            Value, which can be any type that can be converted to a :class:`.Value`
            instance.
        is_param : bool, default: False
            Whether the new variable is a parameter. The default is ``False``, which means it is a local variable.

        Notes
        -----
        Variables can be added to the following EDB objects:

        * :class:`.Database` (Variable names must begin with a '$'.)
        * :class:`.ComponentDef`
        * :class:`.Cell`
        * :class:`.Layout` (Adds variable to the corresponding
          :class:`.Cell` instance.)

        Examples
        --------
        Add variables to a cell and create a value that references these variables.

        >>> param = Value(33.1)
        >>> cell.add_variable("blue1", param)
        >>> cell.add_variable("blue2", "25mm")
        >>> vv = cell.create_value("blue1 + blue2")
        >>> print(vv.double)
        33.125
        """
        temp = variable_server_msgs.AddVariableMessage(
            variable_owner=self.variable_owner,
            name=name,
            value=value_message(value),
            isparam=is_param,
        )
        get_variable_server_stub().AddVariable(temp)

    def add_menu_variable(self, name, values, is_param=False, index=0):
        """Add a menu variable.

        Parameters
        ----------
        name : str
            Variable name.
        values : list[str, int, float, complex, :class:`.Value`]
            Each element can be any type that can be converted to a :class:`.Value`
            instance.
        is_param : bool, default: False
            Whether the new variable is a parameter. The default is ``False``, which means it is a local variable.
        index : int, default: 0
            Index of the value that is initially selected.
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

    def delete_variable(self, name):
        """Delete a variable.

        Parameters
        ----------
        name : str
            Variable name.
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        get_variable_server_stub().DeleteVariable(temp)

    def set_variable_value(self, name, new_value):
        """Set a variable to a new value.

        Parameters
        ----------
        name : str
            Variable name.
        new_value : str, int, float, complex, :class:`.Value`
            New value.
        """
        temp = variable_server_msgs.SetVariableMessage(
            variable_owner=self.variable_owner, name=name, value=value_message(new_value)
        )
        get_variable_server_stub().SetVariableValue(temp)

    def get_variable_value(self, name):
        """Get the value for a given variable.

        Parameters
        ----------
        name : str
            Variable name.

        Returns
        -------
        :class:`.Value`
            Variable value.
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return Value(get_variable_server_stub().GetVariableValue(temp))

    def is_parameter(self, name):
        """Determine if the variable is a parameter.

        Parameters
        ----------
        name : str
            Variable name.

        Returns
        -------
        bool
            ``True`` if the variable is a parameter, ``False`` otherwise.
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return get_variable_server_stub().IsParameter(temp).value

    def get_all_variable_names(self):
        """Get all variable names.

        Returns
        -------
        list[str]
            Names of all variables.
        """
        return get_variable_server_stub().GetAllVariableNames(self.variable_owner).names

    def get_variable_desc(self, name):
        """Get the description of a variable.

        Parameters
        ----------
        name : str
            Variable name.

        Returns
        -------
        str
            Description of the variable.
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return get_variable_server_stub().GetVariableDesc(temp).value

    def set_variable_desc(self, name, desc):
        """Set a variable to have a new description.

        Parameters
        ----------
        name : str
            Variable name.
        desc : str
             New variable description.
        """
        temp = variable_server_msgs.SetDescriptionMessage(
            variable_owner=self.variable_owner, name=name, desc=desc
        )
        get_variable_server_stub().SetVariableDesc(temp)

    def create_value(self, val):
        """Create a value instance.

        This value instance can reference variables on the variable server.

        Parameters
        ----------
        val : str, int, float, complex
            Value, which can be any type that can be converted to a :class:`.Value`
            instance.


        Returns
        -------
        :class:`.Value`

        Notes
        -----
        Creating a value from a :class:`.Database` instance can reference variables
        in the :class:`.Database` instance.

        Creating a value from a :class:`.Cell` instance can reference variables in
        both the :class:`.Database` instance and the
        :class:`.Cell` instance

        Creating a value from a :class:`.ComponentDef`
        instance can reference variables in both the :class:`.Database` instance and
        the :class:`.ComponentDef` instance.
        """
        if isinstance(val, str):
            return Value(val, self)

        return Value(val)
