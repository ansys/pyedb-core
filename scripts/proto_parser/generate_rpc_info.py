"""Write out the rpc_info.py file."""
from collections import defaultdict
from os import environ
from typing import List

from proto_parsing_utils import ProtoParserException, RpcData, parse_all_protos_in_dir

tab = "    "
ansys_api_edb_repo_env_str = "ANSYS_API_EDB_REPO_PATH"


def _get_rpc_invalidation_info_params_str(invalidation: str, data: RpcData):
    tokens = invalidation.split(".")
    is_self_invalidation = len(tokens) == 1
    service_name = f"{tokens[0]}Service" if not is_self_invalidation else data.service_name
    return f'rpc="{tokens[0 if is_self_invalidation else 1]}", service="{data.package_name}.{service_name}"'


def _get_rpc_invalidation_infos_str(invalidations: list[str], data: RpcData):
    invalidation_infos_str = ", ".join(
        f"_InvalidationInfo({_get_rpc_invalidation_info_params_str(invalidation, data)})"
        for invalidation in invalidations
    )
    return f"[{invalidation_infos_str}]"


def _get_invalidations_params_str(invalidations: list[str | dict[list[str]]], data: RpcData):
    invalidations_params = []

    def get_invalidation_accessor_params_str(invalidation_accessor_str: str):
        invalidation_accessor_params_str = ",".join(
            [f'"{accessor}"' for accessor in invalidation_accessor_str.split(".") if accessor]
        )
        return f"[{invalidation_accessor_params_str}]"

    if isinstance(invalidations[0], str):
        for invalidation_accessor in invalidations:
            invalidations_params.append(get_invalidation_accessor_params_str(invalidation_accessor))
    else:
        for invalidation in invalidations:
            for invalidation_accessor, invalidation_infos in invalidation.items():
                invalidations_accessor = get_invalidation_accessor_params_str(invalidation_accessor)
                invalidation_infos_str = _get_rpc_invalidation_infos_str(invalidation_infos, data)
                invalidations_params.append(f"({invalidations_accessor},{invalidation_infos_str})")
    return ",".join(invalidations_params)


def _get_rpc_invalidations_str(invalidations: list[str], data: RpcData):
    return f"invalidations=[{_get_invalidations_params_str(invalidations, data)}]"


def _get_rpc_info_object_str(data: RpcData):
    io_flag_params = ", ".join(
        [f"{io_flag}={True}" for io_flag in sorted(data.io_flags.str_flags, key=str.lower)]
    )
    invalidations = data.io_flags.get_dict_flag("invalidations")
    if invalidations:
        io_flag_params += f", {_get_rpc_invalidations_str(invalidations, data)}"
    return f"_RpcInfo({io_flag_params})"


def _rpc_info_to_str_entries(rpc_datas: List[RpcData]):
    rpc_info_str_entries = []
    for data in rpc_datas:
        rpc_info_str_entries.append(
            f"""{tab}\"{data.rpc_name}\": {_get_rpc_info_object_str(data)}"""
        )
    rpc_info_str_entries = ",\n".join(rpc_info_str_entries)
    return f"{{{rpc_info_str_entries}}}"


def _rpc_info_to_str(rpc_datas: List[RpcData]):
    service_to_rpc_map = defaultdict(list)
    for data in rpc_datas:
        service_to_rpc_map[data.full_service_name].append(data)
    rpc_info_str = []
    for service_name, data in service_to_rpc_map.items():
        service_info_str = f"""{tab}\"{service_name}\": {_rpc_info_to_str_entries(data)}"""
        rpc_info_str.append(service_info_str)
    return f",\n".join(rpc_info_str)


def _get_rpc_info_file_str(rpc_datas: List[RpcData]):
    return f"""\"\"\"Defines container which gives additional information for RPC methods.\"\"\"

class _InvalidationInfo:
    def __init__(self, rpc, service=None):
        self._rpc = rpc
        self._service = service

    @property
    def rpc(self):
        return self._rpc

    @property
    def service(self):
        return self._service

    @property
    def is_self_invalidation(self):
        return self.service is None


class _RpcInfo:
    def __init__(
        self,
        read_no_cache=False,
        write_no_buffer=False,
        cache=False,
        buffer=False,
        returns_future=False,
        write_no_cache_invalidation=False,
        invalidations=None
    ):
        self._read_no_cache = read_no_cache
        self._write_no_buffer = write_no_buffer
        self._cache = cache
        self._buffer = buffer
        self._write_no_cache_invalidation = write_no_cache_invalidation
        self._returns_future = returns_future
        self._invalidations = invalidations

    @property
    def is_read(self):
        return self._cache or self._read_no_cache

    @property
    def is_write(self):
        return self._buffer or self._write_no_buffer

    @property
    def can_cache(self):
        return self._cache

    @property
    def can_buffer(self):
        return self._buffer

    @property
    def returns_future(self):
        return self._returns_future

    @property
    def invalidates_cache(self):
        return self.is_write and not self._write_no_cache_invalidation

    @property
    def invalidations(self):
        return self._invalidations

    @property
    def has_smart_invalidation(self):
        return bool(self.invalidations)


rpc_information = {{
{_rpc_info_to_str(rpc_datas)}
}}

"""


def _write_rpc_info_file(rpc_datas: List[RpcData], path: str):
    with open(path, "w") as f:
        f.write(_get_rpc_info_file_str(rpc_datas))


if __name__ == "__main__":
    try:
        rpc_data = []
        ansys_api_edb_repo = environ.get(ansys_api_edb_repo_env_str)
        if not ansys_api_edb_repo:
            raise ProtoParserException(
                f"The environment variable {ansys_api_edb_repo_env_str} is not set. "
                f"Please set it to the path of the ansys-api-edb repository on your system "
                f"so that the proto files can be successfully parsed."
            )
        parse_all_protos_in_dir(ansys_api_edb_repo + r"/ansys/api/edb/v1", rpc_data)
        _write_rpc_info_file(rpc_data, r"../../src/ansys/edb/core/inner/rpc_info.py")
    except ProtoParserException as e:
        print(e)
