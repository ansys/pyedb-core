from ansys.edb.core.layout.cell import Cell
from ansys.edb.core.simulation_setup.simulation_setup import Distribution, FrequencyData, SweepData
from ansys.edb.core.simulation_setup.siwave_simulation_setup import SIWaveSimulationSetup


def test_create_siwave_simulation_setup(circuit_cell: Cell):
    setup = SIWaveSimulationSetup.create(circuit_cell, "Setup1")
    ff = [
        FrequencyData(Distribution.LINC, "0GHz", "1GHz", "1001"),
        FrequencyData(Distribution.DEC, "1kHz", "1GHz", "20"),
    ]
    sweep_data = SweepData("Sweep1", ff)
    assert isinstance(sweep_data.frequency_data, list)
    setup.sweep_data = [sweep_data]
    assert isinstance(setup.sweep_data[0].frequency_data, list)
    for i, fd in enumerate(ff):
        fd_read = setup.sweep_data[0].frequency_data[i]
        assert fd.distribution == fd_read.distribution
        assert fd.start_f == fd_read.start_f
        assert fd.end_f == fd_read.end_f
        assert fd.step == fd_read.step
