"""SIWave DCIR simulation settings."""

import ansys.api.edb.v1.siwave_dcir_simulation_settings_pb2 as pb

from ansys.edb.core.inner import messages
from ansys.edb.core.session import SIWaveDCIRSimulationSettingsServiceStub, StubAccessor, StubType
from ansys.edb.core.simulation_setup.siwave_simulation_settings import SIWaveSimulationSettings


class SIWaveDCIRSimulationSettings(SIWaveSimulationSettings):
    """Represents SIWave DCIR simulation settings."""

    __stub: SIWaveDCIRSimulationSettingsServiceStub = StubAccessor(
        StubType.siwave_dcir_sim_settings
    )

    @property
    def icepak_temp_file(self):
        """:obj:`bool`: Path to the file containing the Icepak temperature map to import."""
        return self.__stub.GetIcepakTempFile(self.msg).value

    @icepak_temp_file.setter
    def icepak_temp_file(self, icepak_temp_file):
        self.__stub.SetIcepakTempFile(messages.string_property_message(self, icepak_temp_file))

    @property
    def source_terms_to_ground(self):
        """:obj:`dict` { :obj:`str` : :obj:`int` }: Dictionary of ``SourceName, NodeToGround`` pairs.

        ``NodeToGround`` options are ``0`` (unspecified), ``1`` (negative), and ``2`` (positive).
        """
        return {
            source: t_to_g
            for (source, t_to_g) in self.__stub.GetSourceTermsToGround(
                self.msg
            ).source_terms_to_ground.items()
        }

    @source_terms_to_ground.setter
    def source_terms_to_ground(self, source_terms_to_ground):
        self.__stub.SetSourceTermsToGround(
            pb.SourceTermsToGroundPropertyMessage(
                target=self.msg,
                value=pb.SourceTermsToGroundMessage(source_terms_to_ground=source_terms_to_ground),
            )
        )

    @property
    def export_dc_thermal_data(self):
        """:obj:`bool`: Flag indicating if DC thermal data is exported."""
        return self.__stub.GetExportDCThermalData(self.msg).value

    @export_dc_thermal_data.setter
    def export_dc_thermal_data(self, export_dc_thermal_data):
        self.__stub.SetExportDCThermalData(
            messages.bool_property_message(self, export_dc_thermal_data)
        )

    @property
    def import_thermal_data(self):
        """:obj:`bool`: Flag indicating if thermal data is imported."""
        return self.__stub.GetImportThermalData(self.msg).value

    @import_thermal_data.setter
    def import_thermal_data(self, import_thermal_data):
        self.__stub.SetImportThermalData(messages.bool_property_message(self, import_thermal_data))

    @property
    def full_dc_report_path(self):
        """:obj:`str`: Path to the DC report."""
        return self.__stub.GetFullDCReportPath(self.msg).value

    @full_dc_report_path.setter
    def full_dc_report_path(self, full_dc_report_path):
        self.__stub.SetFullDCReportPath(messages.string_property_message(self, full_dc_report_path))

    @property
    def via_report_path(self):
        """:obj:`str`: Path to the via report."""
        return self.__stub.GetViaReportPath(self.msg).value

    @via_report_path.setter
    def via_report_path(self, via_report_path):
        self.__stub.SetViaReportPath(messages.string_property_message(self, via_report_path))

    @property
    def per_pin_res_path(self):
        """:obj:`str`: Path to the per pin resolution."""
        return self.__stub.GetPerPinResPath(self.msg).value

    @per_pin_res_path.setter
    def per_pin_res_path(self, per_pin_res_path):
        self.__stub.SetPerPinResPath(messages.string_property_message(self, per_pin_res_path))

    @property
    def dc_report_config_file(self):
        """:obj:`str`: Configuration file for the DC report."""
        return self.__stub.GetDCReportConfigFile(self.msg).value

    @dc_report_config_file.setter
    def dc_report_config_file(self, dc_report_config_file):
        self.__stub.SetDCReportConfigFile(
            messages.string_property_message(self, dc_report_config_file)
        )

    @property
    def dc_report_show_active_devices(self):
        """:obj:`bool`: Flag indicating if active devices are shown in the DC report."""
        return self.__stub.GetDCReportShowActiveDevices(self.msg).value

    @dc_report_show_active_devices.setter
    def dc_report_show_active_devices(self, dc_report_show_active_devices):
        self.__stub.SetDCReportShowActiveDevices(
            messages.bool_property_message(self, dc_report_show_active_devices)
        )

    @property
    def per_pin_use_pin_format(self):
        """:obj:`bool`: Flag indicating if the per pin uses the pin format."""
        return self.__stub.GetPerPinUsePinFormat(self.msg).value

    @per_pin_use_pin_format.setter
    def per_pin_use_pin_format(self, per_pin_use_pin_format):
        self.__stub.SetPerPinUsePinFormat(
            messages.bool_property_message(self, per_pin_use_pin_format)
        )

    @property
    def use_loop_res_for_per_pin(self):
        """:obj:`bool`: Flag indicating if the per pin uses the loop resolution."""
        return self.__stub.GetUseLoopResForPerPin(self.msg).value

    @use_loop_res_for_per_pin.setter
    def use_loop_res_for_per_pin(self, use_loop_res_for_per_pin):
        self.__stub.SetUseLoopResForPerPin(
            messages.bool_property_message(self, use_loop_res_for_per_pin)
        )
