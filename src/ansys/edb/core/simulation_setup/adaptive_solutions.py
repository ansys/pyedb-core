"""Adaptive solutions."""


class MatrixConvergenceDataEntry:
    """Class representing a matrix convergence data entry.

    Attributes
    ----------
    port_1_name : str
    port_2_name : str
    mag_limit : float
    phase_limit : float
    """

    def __init__(self, port_1_name, port_2_name, mag_limit, phase_limit):
        """Create a matrix convergence data entry."""
        self._port_1_name = port_1_name
        self._port_2_name = port_2_name
        self._mag_limit = mag_limit
        self._phase_limit = phase_limit

    @property
    def port_1_name(self):
        """:obj:`str`: Name of the first port."""
        return self._port_1_name

    @port_1_name.setter
    def port_1_name(self, port_1_name):
        self._port_1_name = port_1_name

    @property
    def port_2_name(self):
        """:obj:`str`: Name of the second port."""
        return self._port_2_name

    @port_2_name.setter
    def port_2_name(self, port_2_name):
        self._port_2_name = port_2_name

    @property
    def mag_limit(self):
        """:obj:`float`: Magnitude limit."""
        return self._mag_limit

    @mag_limit.setter
    def mag_limit(self, mag_limit):
        self._mag_limit = mag_limit

    @property
    def phase_limit(self):
        """:obj:`float`: Phase limit."""
        return self._phase_limit

    @phase_limit.setter
    def phase_limit(self, phase_limit):
        self._phase_limit = phase_limit


class MatrixConvergenceData:
    """Represents matrix convergence data for an adaptive frequency solution.

    Attributes
    ----------
    mag_min_threshold : float
    entry_list : list[:class:`.MatrixConvergenceDataEntry`]
    """

    def __init__(self, mag_min_threshold=0.01, entry_list=None):
        """Create a matrix convergence data entry."""
        self._all_constant = False
        self._all_diag_constant = False
        self._all_off_diag_constant = False
        self._mag_minThreshold = mag_min_threshold
        self._entry_list = entry_list if entry_list is not None else []

    @property
    def all_constant(self):
        """:obj:`bool`: Flag indicating if all matrix entries are the same.

        This property is read-only.
        """
        return self._all_constant

    @property
    def all_diag_constant(self):
        """:obj:`bool`: Flag indicating if all diagonal matrix entries are the same.

        This property is read-only.
        """
        return self._all_diag_constant

    @property
    def all_off_diag_constant(self):
        """:obj:`bool`: Flag indicating if all off-diagonal matrix entries are the same.

        This property is read-only.
        """
        return self._all_off_diag_constant

    @property
    def mag_min_threshold(self):
        """:obj:`float`: Minimum magnitude threshold.

        When the magnitude is less than the minimal threshold value, the phase is ignored.
        """
        return self._mag_minThreshold

    @mag_min_threshold.setter
    def mag_min_threshold(self, mag_min_threshold):
        self._mag_minThreshold = mag_min_threshold

    @property
    def entry_list(self):
        """:obj:`list` of :class:`.MatrixConvergenceDataEntry`: Matrix entries."""
        return self._entry_list

    @entry_list.setter
    def entry_list(self, entry_list):
        self._entry_list = entry_list
        self._all_constant = False
        self._all_diag_constant = False
        self._all_off_diag_constant = False

    def set_all_constant(self, mag_limit, phase_limit, port_names):
        """Set all entries in the matrix to have the given magnitude and phase values.

        Parameters
        ----------
        mag_limit : float
           Magnitude limit.
        phase_limit : float
            Phase limit.
        port_names : list[:obj:`str`]
            List of port names.
        """
        self._entry_list.clear()

        for port_name_1 in port_names:
            for port_name_2 in port_names:
                self._entry_list.append(
                    MatrixConvergenceDataEntry(port_name_1, port_name_2, mag_limit, phase_limit)
                )

        self._all_constant = True
        self._all_diag_constant = False
        self._all_off_diag_constant = False

    def set_all_diag_constant(self, mag_limit, phase_limit, port_names, clear_entries):
        """Set all diagonal entries in the matrix to have the given magnitude and phase values.

        Parameters
        ----------
        mag_limit : float
           Magnitude limit.
        phase_limit : float
            Phase limit.
        port_names : list[:obj:`str`]
            List of port names.
        clear_entries : bool
            Whether to clear entries.
        """
        if clear_entries:
            self._entry_list.clear()

        for port_name in port_names:
            self._entry_list.append(
                MatrixConvergenceDataEntry(port_name, port_name, mag_limit, phase_limit)
            )

        self._all_constant = False
        self._all_diag_constant = True
        if clear_entries:
            self._all_off_diag_constant = False

    def set_all_off_diag_constant(self, mag_limit, phase_limit, port_names, clear_entries):
        """Set all diagonal entries in the matrix to have the given magnitude and phase values.

        Parameters
        ----------
        mag_limit : float
           Magnitude limit.
        phase_limit : float
            Phase limit.
        port_names : list[:obj:`str`]
            List of port names.
        clear_entries : bool
            Whether to clear entries.
        """
        if clear_entries:
            self._entry_list.clear()

        for port_name_1 in port_names:
            for port_name_2 in port_names:
                if port_name_1 != port_name_2:
                    self._entry_list.append(
                        MatrixConvergenceDataEntry(port_name_1, port_name_2, mag_limit, phase_limit)
                    )

        self._all_constant = False
        if clear_entries:
            self._all_diag_constant = False
        self._all_off_diag_constant = True

    def add_entry(self, port_name_1, port_name_2, mag_limit, phase_limit):
        """Add a matrix entry.

        Parameters
        ----------
        port_name_1 : str
            Name of the first port.
        port_name_2 : str
            Name of the second port.
        mag_limit : float
            Magnitude limit.
        phase_limit : float
            Phase limit.
        """
        new_entry = MatrixConvergenceDataEntry(port_name_1, port_name_2, mag_limit, phase_limit)
        for idx, entry in enumerate(self._entry_list):
            if (
                entry.port_1_name == new_entry.port_1_name
                and entry.port_2_name == new_entry.port_2_name
            ):
                self._entry_list[idx] = new_entry
                return
        self._entry_list.append(new_entry)


class SingleFrequencyAdaptiveSolution:
    """Represents a single frequency adaptive solution.

    Attributes
    ----------
    adaptive_frequency : str
    max_delta : str
    max_passes : int
    mx_conv_data : MatrixConvergenceData
    use_mx_conv_data : bool
    """

    def __init__(
        self,
        adaptive_frequency="5GHz",
        max_delta="0.02",
        max_passes=10,
        mx_conv_data=None,
        use_mx_conv_data=False,
    ):
        """Create a single frequency adaptive solution."""
        self._adaptive_frequency = adaptive_frequency
        self._max_delta = max_delta
        self._max_passes = max_passes
        self._mx_conv_data = mx_conv_data if mx_conv_data is not None else MatrixConvergenceData()
        self._use_mx_conv_data = use_mx_conv_data

    @property
    def adaptive_frequency(self):
        """:obj:`str`: Adaptive frequency."""
        return self._adaptive_frequency

    @adaptive_frequency.setter
    def adaptive_frequency(self, adaptive_frequency):
        self._adaptive_frequency = adaptive_frequency

    @property
    def max_delta(self):
        """:obj:`str`: Maximum delta S between adaptive passes."""
        return self._max_delta

    @max_delta.setter
    def max_delta(self, max_delta):
        self._max_delta = max_delta

    @property
    def max_passes(self):
        """:obj:`int`: Maximum number of adaptive passes."""
        return self._max_passes

    @max_passes.setter
    def max_passes(self, max_passes):
        self._max_passes = max_passes

    @property
    def mx_conv_data(self):
        """:class:`.MatrixConvergenceData`: Matrix convergence data."""
        return self._mx_conv_data

    @mx_conv_data.setter
    def mx_conv_data(self, mx_conv_data):
        self._mx_conv_data = mx_conv_data

    @property
    def use_mx_conv_data(self):
        """:obj:`bool`: Flag indicating whether matrix convergence data is used."""
        return self._use_mx_conv_data

    @use_mx_conv_data.setter
    def use_mx_conv_data(self, use_mx_conv_data):
        self._use_mx_conv_data = use_mx_conv_data


class AdaptiveFrequency:
    """Represents an adaptive frequency.

    Attributes
    ----------
    adaptive_frequency : str
    max_delta : str
    output_variables : dict{ str : str }
    """

    def __init__(self, adaptive_frequency, max_delta="0.02", output_variables=None):
        """Create an adaptive frequency."""
        self._adaptive_frequency = adaptive_frequency
        self._max_delta = max_delta
        self._output_variables = output_variables if output_variables is not None else {}

    @property
    def adaptive_frequency(self):
        """:obj:`str`: Adaptive frequency."""
        return self._adaptive_frequency

    @adaptive_frequency.setter
    def adaptive_frequency(self, adaptive_frequency):
        self._adaptive_frequency = adaptive_frequency

    @property
    def max_delta(self):
        """:obj:`str`: Maximum delta S between adaptive passes."""
        return self._max_delta

    @max_delta.setter
    def max_delta(self, max_delta):
        self._max_delta = max_delta

    @property
    def output_variables(self):
        """:obj:`dict` { :obj:`str` : :obj:`str` }: Map of output variable names to maximum delta S."""
        return self._output_variables

    @output_variables.setter
    def output_variables(self, output_variables):
        self._output_variables = output_variables


class MultiFrequencyAdaptiveSolution:
    """Represents a multi-frequency adaptive solution.

    Attributes
    ----------
    max_passes : int
        Maximum number of adaptive passes.
    adaptive_frequencies : list[:class:`.AdaptiveFrequency`]
    """

    def __init__(self, max_passes=10, adaptive_frequencies=None):
        """Create a multi-frequency adaptive solution."""
        self._max_passes = max_passes
        if adaptive_frequencies is None or len(adaptive_frequencies) == 0:
            self._adaptive_frequencies = [
                AdaptiveFrequency(freq) for freq in ["2.5GHz", "5GHz", "10GHz"]
            ]
        else:
            self._adaptive_frequencies = adaptive_frequencies

    @property
    def adaptive_frequencies(self):
        """:obj:`list` of :class:`.AdaptiveFrequency`: Frequencies that adaptive solutions are calculated for."""
        return self._adaptive_frequencies

    @adaptive_frequencies.setter
    def adaptive_frequencies(self, adaptive_frequencies):
        self._adaptive_frequencies = adaptive_frequencies

    @property
    def max_passes(self):
        """:obj:`int`: Maximum number of adaptive passes."""
        return self._max_passes

    @max_passes.setter
    def max_passes(self, max_passes):
        self._max_passes = max_passes


class BroadbandAdaptiveSolution:
    """Represents a broadband adaptive solution.

    Attributes
    ----------
    low_frequency : str
    high_frequency : str
    max_num_passes : int
    max_delta : str
    """

    def __init__(
        self, low_frequency="5GHz", high_frequency="10GHz", max_num_passes=10, max_delta="0.02"
    ):
        """Create a broadband adaptive solution."""
        self._low_frequency = low_frequency
        self._high_frequency = high_frequency
        self._max_num_passes = max_num_passes
        self._max_delta = max_delta

    @property
    def low_frequency(self):
        """:obj:`str`: Lower-bound adaptive frequency."""
        return self._low_frequency

    @low_frequency.setter
    def low_frequency(self, low_frequency):
        self._low_frequency = low_frequency

    @property
    def high_frequency(self):
        """:obj:`str`: Higher-bound adaptive frequency."""
        return self._high_frequency

    @high_frequency.setter
    def high_frequency(self, high_frequency):
        self._high_frequency = high_frequency

    @property
    def max_num_passes(self):
        """:obj:`int`: Maximum number of adaptive passes."""
        return self._max_num_passes

    @max_num_passes.setter
    def max_num_passes(self, max_num_passes):
        self._max_num_passes = max_num_passes

    @property
    def max_delta(self):
        """:obj:`str`: Maximum delta S between adaptive passes."""
        return self._max_delta

    @max_delta.setter
    def max_delta(self, max_delta):
        self._max_delta = max_delta
