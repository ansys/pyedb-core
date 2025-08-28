import pytest

from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.simulation_setup.simulation_setup import Distribution, FrequencyData, SweepData
from ansys.edb.core.simulation_setup.siwave_simulation_setup import SIWaveSimulationSetup


@pytest.mark.parametrize(
    "frequency_data",
    [
        FrequencyData(Distribution.LINC, "0GHz", "1GHz", "1001"),
        [
            FrequencyData(Distribution.LINC, "0GHz", "1GHz", "1001"),
            FrequencyData(Distribution.DEC, "1kHz", "1GHz", "20"),
        ],
    ],
)
def test_create_siwave_simulation_setup(
    circuit_cell: Cell, frequency_data: FrequencyData | list[FrequencyData]
):
    setup = SIWaveSimulationSetup.create(circuit_cell, "Setup1")
    sweep_data = SweepData("Sweep1", frequency_data)
    assert isinstance(sweep_data.frequency_data, type(frequency_data))
    setup.sweep_data = [sweep_data]
    assert isinstance(setup.sweep_data[0].frequency_data, type(frequency_data))
    if isinstance(frequency_data, list):
        for i, fd in enumerate(frequency_data):
            _assert_frequency_data_are_equal(fd, setup.sweep_data[0].frequency_data[i])
    else:
        _assert_frequency_data_are_equal(frequency_data, setup.sweep_data[0].frequency_data)


def _assert_frequency_data_are_equal(fd1: FrequencyData, fd2: FrequencyData):
    assert fd1.distribution == fd2.distribution
    assert fd1.start_f == fd2.start_f
    assert fd1.end_f == fd2.end_f
    assert fd1.step == fd2.step
