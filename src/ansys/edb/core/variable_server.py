"""VariableServer Class."""

from ansys.api.edb.v1.edb_messages_pb2 import EDBObjMessage
import ansys.api.edb.v1.variable_server_pb2 as variable_server_msgs

from ansys.edb.core.messages import value_message
from ansys.edb.session import get_variable_server_stub
from ansys.edb.utility import Value


class VariableServer:
    """Class that owns variables.

    It can be either a Database, Cell, or ComponentDef object.
    """

    def __init__(self, variable_owner):
        """Initialize VariableServer object.

        Parameters
        ----------
        variable_owner : EdbObjMessage
            ID of either a Database, Cell, or ComponentDef.
        """
        assert variable_owner.id > 0, "Invalid variable owner id"
        self.variable_owner = EDBObjMessage(id=variable_owner.id)

    def add_variable(self, name, value, is_param=False):
        """Add new variable.

        Parameters
        ----------
        name : str
            Variable name
        value : str, int, float, complex, :class:`Value <ansys.edb.utility.Value>`
            value can be any type that can be converted to a :class:`Value <ansys.edb.utility.Value>`
        is_param : bool, optional
            True means the new variable is a parameter, False means it is a local variable

        Notes
        -----
        Variables can be added to the following EDB objects

        *   :class:`Database <ansys.edb.database.Database>`. Variable names must begin with a '$'
        *   :class:`ComponentDef <ansys.edb.definition.ComponentDef>`
        *   :class:`Cell <ansys.edb.layout.Cell>`
        *   :class:`Layout <ansys.edb.layout.Layout>` -- adds variable
            to corresponding :class:`Cell <ansys.edb.layout.Cell>`

        Examples
        --------
        Adding variables to a Cell and creating a Value that references those variables

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
        """Add new menu variable.

        Parameters
        ----------
        name : str
            Variable name
        values : list[str, int, float, complex, :class:`Value <ansys.edb.utility.Value>`]
            each element can be any type that can be converted to a :class:`Value <ansys.edb.utility.Value>`
        is_param : bool, optional
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

    def delete_variable(self, name):
        """Delete an existing variable.

        Parameters
        ----------
        name : str
            Variable name
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        get_variable_server_stub().DeleteVariable(temp)

    def set_variable_value(self, name, new_value):
        """Set variable to have a new value.

        Parameters
        ----------
        name : str
            Variable name
        new_value : str, int, float, complex, :class:`Value <ansys.edb.utility.Value>`
        """
        temp = variable_server_msgs.SetVariableMessage(
            variable_owner=self.variable_owner, name=name, value=value_message(new_value)
        )
        get_variable_server_stub().SetVariableValue(temp)

    def get_variable_value(self, name):
        """Get the value from an existing variable.

        Parameters
        ----------
        name : str
            Variable name

        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return Value(get_variable_server_stub().GetVariableValue(temp))

    def is_parameter(self, name):
        """Return the type of the variable.

        Parameters
        ----------
        name : str
            Variable name

        Returns
        -------
        bool
            True if the variable is a parameter, otherwise False
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return get_variable_server_stub().IsParameter(temp).value

    def get_all_variable_names(self):
        """Return names of all variables that were added.

        Returns
        -------
        list[str]
            Names of each variable
        """
        return get_variable_server_stub().GetAllVariableNames(self.variable_owner).names

    def get_variable_desc(self, name):
        """Get the description of a variable.

        Parameters
        ----------
        name : str
            Variable name

        Returns
        -------
        str
            Description of the variable
        """
        temp = variable_server_msgs.VariableNameMessage(
            variable_owner=self.variable_owner, name=name
        )
        return get_variable_server_stub().GetVariableDesc(temp).value

    def set_variable_desc(self, name, desc):
        """Set variable to have a new description.

        Parameters
        ----------
        name : str
            Variable name
        desc : str
             New variable description
        """
        temp = variable_server_msgs.SetDescriptionMessage(
            variable_owner=self.variable_owner, name=name, desc=desc
        )
        get_variable_server_stub().SetVariableDesc(temp)

    def create_value(self, val):
        """Create a :class:`Value <ansys.edb.utility.Value>` that can reference variables in this VariableServer.

        Parameters
        ----------
        val : str, int, float, complex
            val can be any type that can be converted to a :class:`Value <ansys.edb.utility.Value>`


        Returns
        -------
        :class:`Value <ansys.edb.utility.Value>`

        Notes
        -----
        Creating a value from a :class:`Database <ansys.edb.database.Database>` can reference variables in the
        :class:`Database <ansys.edb.database.Database>`.

        Creating a value from a :class:`Cell <ansys.edb.layout.Cell>` can reference variables in both the
        :class:`Database <ansys.edb.database.Database>` and the :class:`Cell <ansys.edb.layout.Cell>`.

        Creating a value from a :class:`ComponentDef <ansys.edb.definition.ComponentDef>` can reference variables
        in both the :class:`Database <ansys.edb.database.Database>` and
        the :class:`ComponentDef <ansys.edb.definition.ComponentDef>`.
        """
        if isinstance(val, str):
            return Value(val, self)

        return Value(val)
