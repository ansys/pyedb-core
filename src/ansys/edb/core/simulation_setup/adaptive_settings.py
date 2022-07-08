"""Adaptive Settings."""

from ansys.api.edb.v1.adaptive_settings_pb2 import (
    AdaptiveFrequencyDataListMessage,
    AdaptiveFrequencyDataMessage,
    SetAdaptiveFrequencyDataListMessage,
)

from ansys.edb.core.session import get_adaptive_settings_stub
from ansys.edb.core.simulation_setup.adaptive_frequency_data import AdaptiveFrequencyData
from ansys.edb.core.utility.base import ObjBase


class _QueryBuilder:
    @staticmethod
    def get_adaptive_frequency_data_list(adaptive_settings):
        return adaptive_settings.msg

    @staticmethod
    def set_adaptive_frequency_data_list(adaptive_settings, new_adaptive_freq_list):
        list_msgs = [
            AdaptiveFrequencyDataMessage(
                adaptive_frequency=data.adaptive_frequency,
                max_passes=data.max_passes,
                max_delta=data.max_delta,
            )
            for data in new_adaptive_freq_list
        ]
        list_msg = AdaptiveFrequencyDataListMessage(adaptive_frequency_data=list_msgs)
        return SetAdaptiveFrequencyDataListMessage(
            adaptive_settings=adaptive_settings.msg, adaptive_frequency_data_list=list_msg
        )


class AdaptiveSettings(ObjBase):
    """Class representing adaptive settings."""

    @property
    def adaptive_frequency_data_list(self):
        """Get adaptive frequencies.

        Returns
        -------
        list of AdaptiveFrequencyData
        """
        msg = get_adaptive_settings_stub().GetAdaptiveFrequencyDataList(
            _QueryBuilder.get_adaptive_frequency_data_list(self)
        )
        return [
            AdaptiveFrequencyData._create(adaptive_frequency_data_msg)
            for adaptive_frequency_data_msg in msg.adaptive_frequency_data
        ]

    @adaptive_frequency_data_list.setter
    def adaptive_frequency_data_list(self, new_adaptive_freq_list):
        """Set adaptive frequencies.

        Parameters
        ----------
        new_adaptive_freq_list : list of AdaptiveFrequencyData

        Returns
        -------
        None
        """
        get_adaptive_settings_stub().SetAdaptiveFrequencyDataList(
            _QueryBuilder.set_adaptive_frequency_data_list(self, new_adaptive_freq_list)
        )
