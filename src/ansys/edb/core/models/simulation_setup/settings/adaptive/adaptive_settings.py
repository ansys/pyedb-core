from typing import List

from ansys.api.edb.v1.adaptive_settings_pb2 import (
    AdaptiveFrequencyDataListMessage,
    AdaptiveFrequencyDataMessage,
    SetAdaptiveFrequencyDataListMessage,
)

from .....session import get_adaptive_settings_stub
from ....base import ObjBase
from .adaptive_frequency_data import AdaptiveFrequencyData


class _QueryBuilder:
    @staticmethod
    def get_adaptive_frequency_data_list(adaptive_settings: "AdaptiveSettings"):
        return adaptive_settings._msg

    @staticmethod
    def set_adaptive_frequency_data_list(
        adaptive_settings: "AdaptiveSettings", new_adaptive_freq_list: List[AdaptiveFrequencyData]
    ):
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
            adaptive_settings=adaptive_settings._msg, adaptive_frequency_data_list=list_msg
        )


class AdaptiveSettings(ObjBase):
    @property
    def adaptive_frequency_data_list(self) -> List[AdaptiveFrequencyData]:
        msg = get_adaptive_settings_stub().GetAdaptiveFrequencyDataList(
            _QueryBuilder.get_adaptive_frequency_data_list(self)
        )
        return [
            AdaptiveFrequencyData._create(adaptive_frequency_data_msg)
            for adaptive_frequency_data_msg in msg.adaptive_frequency_data
        ]

    @adaptive_frequency_data_list.setter
    def adaptive_frequency_data_list(
        self, new_adaptive_freq_list: List[AdaptiveFrequencyData]
    ) -> None:
        get_adaptive_settings_stub().SetAdaptiveFrequencyDataList(
            _QueryBuilder.set_adaptive_frequency_data_list(self, new_adaptive_freq_list)
        )
