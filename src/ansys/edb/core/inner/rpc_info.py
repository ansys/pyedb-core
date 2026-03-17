"""Defines container which gives additional information for RPC methods."""


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
        invalidations=None,
        read_no_buffer_flush=False,
    ):
        self._read_no_cache = read_no_cache
        self._write_no_buffer = write_no_buffer
        self._cache = cache
        self._buffer = buffer
        self._write_no_cache_invalidation = write_no_cache_invalidation
        self._returns_future = returns_future
        self._invalidations = invalidations
        self._read_no_buffer_flush = read_no_buffer_flush

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

    @property
    def read_no_buffer_flush(self):
        return self._read_no_buffer_flush


rpc_information = {
    "ansys.api.edb.v1.ArcDataService": {
        "GetHeight": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetCenter": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetMidpoint": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetRadius": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetBoundingBox": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetAngle": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "ClosestPoints": _RpcInfo(cache=True, read_no_buffer_flush=True),
    },
    "ansys.api.edb.v1.BoardBendDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="GetBoardBendDefs", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamBoardBendDefs", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "GetBoundaryPrim": _RpcInfo(cache=True, invalidations=[[]]),
        "GetBendMiddle": _RpcInfo(cache=True, invalidations=[[]]),
        "SetBendMiddle": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetBendMiddle", service="ansys.api.edb.v1.BoardBendDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetBentRegions", service="ansys.api.edb.v1.BoardBendDefService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameterized", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                )
            ],
        ),
        "GetRadius": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRadius": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRadius", service="ansys.api.edb.v1.BoardBendDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetBentRegions", service="ansys.api.edb.v1.BoardBendDefService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameterized", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                )
            ],
        ),
        "GetAngle": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAngle": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAngle", service="ansys.api.edb.v1.BoardBendDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetBentRegions", service="ansys.api.edb.v1.BoardBendDefService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameterized", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                )
            ],
        ),
        "GetBentRegions": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.BondwireService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetMaterial": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaterial", service="ansys.api.edb.v1.BondwireService"
                        )
                    ],
                )
            ],
        ),
        "GetType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="GetType", service="ansys.api.edb.v1.BondwireService")],
                )
            ],
        ),
        "GetCrossSectionType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCrossSectionType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCrossSectionType", service="ansys.api.edb.v1.BondwireService"
                        )
                    ],
                )
            ],
        ),
        "GetCrossSectionHeight": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCrossSectionHeight": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCrossSectionHeight", service="ansys.api.edb.v1.BondwireService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameterized", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                )
            ],
        ),
        "GetDefinitionName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetDefinitionName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDefinitionName", service="ansys.api.edb.v1.BondwireService"
                        )
                    ],
                )
            ],
        ),
        "GetStartElevation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetStartElevation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetStartElevation", service="ansys.api.edb.v1.BondwireService"
                        )
                    ],
                )
            ],
        ),
        "GetEndElevation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEndElevation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEndElevation", service="ansys.api.edb.v1.BondwireService"
                        )
                    ],
                )
            ],
        ),
        "GetTraj": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTraj": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetTraj", service="ansys.api.edb.v1.BondwireService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameterized", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                )
            ],
        ),
        "GetWidthValue": _RpcInfo(cache=True, invalidations=[[]]),
        "SetWidthValue": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetWidthValue", service="ansys.api.edb.v1.BondwireService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameterized", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.BondwireDefService": {
        "Delete": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.BondwireDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.ApdBondwireDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["object"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ApdBondwireDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "LoadDefinitionsFromFile": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["object"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ApdBondwireDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["object"]]),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["object"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters", service="ansys.api.edb.v1.ApdBondwireDefService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Jedec4BondwireDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["object"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.Jedec4BondwireDefService"
                        )
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["object"]]),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters", service="ansys.api.edb.v1.Jedec4BondwireDefService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Jedec5BondwireDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["object"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.Jedec5BondwireDefService"
                        )
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["object"]]),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters", service="ansys.api.edb.v1.Jedec5BondwireDefService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.BundleTerminalService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetParams", service="ansys.api.edb.v1.TerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.TerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "Ungroup": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetTerminals", service="ansys.api.edb.v1.BundleTerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamTerminals", service="ansys.api.edb.v1.BundleTerminalService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetParams", service="ansys.api.edb.v1.TerminalService"
                        )
                    ],
                ),
            ],
        ),
        "GetTerminals": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamTerminals": _RpcInfo(read_no_cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.CellService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["database"],
                    [
                        _InvalidationInfo(rpc="Find", service="ansys.api.edb.v1.CellService"),
                        _InvalidationInfo(
                            rpc="GetTopCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="TopCircuitCells", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="GetCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="GetFootprints", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamFootprints", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "GetLayout": _RpcInfo(cache=True, invalidations=[[]]),
        "Find": _RpcInfo(cache=True, invalidations=[["database"]]),
        "Delete": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(rpc="Find", service="ansys.api.edb.v1.CellService"),
                        _InvalidationInfo(
                            rpc="GetTopCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="TopCircuitCells", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="GetCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="GetFootprints", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamFootprints", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "GetDatabase": _RpcInfo(cache=True, invalidations=[[]]),
        "IsFootprint": _RpcInfo(cache=True, invalidations=[[]]),
        "IsBlackBox": _RpcInfo(cache=True, invalidations=[[]]),
        "SetBlackBox": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="IsBlackBox", service="ansys.api.edb.v1.CellService")],
                )
            ],
        ),
        "GetSuppressPads": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSuppressPads": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSuppressPads", service="ansys.api.edb.v1.CellService"
                        )
                    ],
                )
            ],
        ),
        "GetAntiPadsAlwaysOn": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAntiPadsAlwaysOn": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAntiPadsAlwaysOn", service="ansys.api.edb.v1.CellService"
                        )
                    ],
                )
            ],
        ),
        "GetAntiPadsOption": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAntiPadsOption": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAntiPadsOption", service="ansys.api.edb.v1.CellService"
                        )
                    ],
                )
            ],
        ),
        "IsSymbolicFootprint": _RpcInfo(cache=True, invalidations=[[]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="GetName", service="ansys.api.edb.v1.CellService")],
                ),
                (None, [_InvalidationInfo(rpc="Find", service="ansys.api.edb.v1.CellService")]),
            ],
        ),
        "GetDesignMode": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDesignMode": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDesignMode", service="ansys.api.edb.v1.CellService"
                        )
                    ],
                )
            ],
        ),
        "GetHfssExtentInfo": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHfssExtentInfo": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["cell"],
                    [
                        _InvalidationInfo(
                            rpc="GetHfssExtentInfo", service="ansys.api.edb.v1.CellService"
                        )
                    ],
                )
            ],
        ),
        "GetTemperatureSettings": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTemperatureSettings": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["cell"],
                    [
                        _InvalidationInfo(
                            rpc="GetTemperatureSettings", service="ansys.api.edb.v1.CellService"
                        )
                    ],
                )
            ],
        ),
        "GetTouchstoneExportSettings": _RpcInfo(cache=True),
        "SetTouchstoneExportSettings": _RpcInfo(buffer=True),
        "GetProductPropertyIds": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductProperty", service="ansys.api.edb.v1.CellService"
                        ),
                        _InvalidationInfo(
                            rpc="GetProductPropertyIds", service="ansys.api.edb.v1.CellService"
                        ),
                    ],
                )
            ],
        ),
        "DeleteSimulationSetup": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSimulationSetups", service="ansys.api.edb.v1.CellService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamSimulationSetups", service="ansys.api.edb.v1.CellService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.Q3DGeneralSettingsService"
                        ),
                        _InvalidationInfo(rpc="*", service="ansys.api.edb.v1.Q3DSettingsService"),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.Q3DDCRLSettingsService"
                        ),
                        _InvalidationInfo(rpc="*", service="ansys.api.edb.v1.Q3DCGSettingsService"),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.Q3DAdvancedSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.RaptorXGeneralSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.RaptorXAdvancedSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSPIGeneralSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSPINetProcessingSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSPIPowerGroundNetsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSPISignalNetsSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSGeneralSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSOptionsSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSAdvancedSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSAdvancedMeshingSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HFSSSolverSettingsService"
                        ),
                        _InvalidationInfo(rpc="*", service="ansys.api.edb.v1.DCRSettingsService"),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.HfssSimulationSetupService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.SIWaveGeneralSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.SIWaveAdvancedSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.SIWaveDCSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.SIWaveSParameterSettingsService"
                        ),
                    ],
                ),
            ],
        ),
        "GetSimulationSetups": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamSimulationSetups": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GenerateAutoHFSSRegions": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                    ],
                )
            ],
        ),
        "GenerateViaSmartBox": _RpcInfo(read_no_cache=True),
        "ApplyTechnology": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.CellInstanceService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target", "layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.CellInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "CreateWithComponent": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target", "layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.CellInstanceService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                ),
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetReferenceLayout": _RpcInfo(cache=True, invalidations=[[]]),
        "GetTermInsts": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamTermInsts": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetIs3DPlacement": _RpcInfo(cache=True, invalidations=[[]]),
        "Set3DPlacement": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIs3DPlacement", service="ansys.api.edb.v1.CellInstanceService"
                        )
                    ],
                )
            ],
        ),
        "Get3DTransform": _RpcInfo(cache=True, invalidations=[[]]),
        "Set3DTransform": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="Get3DTransform", service="ansys.api.edb.v1.CellInstanceService"
                        )
                    ],
                )
            ],
        ),
        "GetParameterOverride": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameterOverride": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.CircleService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "Render": _RpcInfo(cache=True),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters", service="ansys.api.edb.v1.CircleService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.ComponentDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["db"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ComponentDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetName", service="ansys.api.edb.v1.ComponentDefService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ComponentDefService"
                        )
                    ],
                ),
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetFootprintCell": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj_0"],
                    [
                        _InvalidationInfo(
                            rpc="GetFootprintCell", service="ansys.api.edb.v1.ComponentDefService"
                        )
                    ],
                )
            ],
        ),
        "GetFootprintCell": _RpcInfo(cache=True, invalidations=[[]]),
        "GetComponentModels": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamComponentModels": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetComponentPins": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamComponentPins": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "AddComponentModel": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj_0"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponentModels", service="ansys.api.edb.v1.ComponentDefService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamComponentModels",
                            service="ansys.api.edb.v1.ComponentDefService",
                        ),
                    ],
                )
            ],
        ),
        "RemoveComponentModel": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj_0"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponentModels", service="ansys.api.edb.v1.ComponentDefService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamComponentModels",
                            service="ansys.api.edb.v1.ComponentDefService",
                        ),
                    ],
                )
            ],
        ),
        "ReorderPins": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponentPins", service="ansys.api.edb.v1.ComponentDefService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetNumber", service="ansys.api.edb.v1.ComponentPinService"
                        )
                    ],
                ),
            ],
        ),
        "RemovePin": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj_0"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponentPins", service="ansys.api.edb.v1.ComponentDefService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ComponentPinService"
                        )
                    ],
                ),
            ],
        ),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductProperty", service="ansys.api.edb.v1.ComponentDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetProductPropertyIds",
                            service="ansys.api.edb.v1.ComponentDefService",
                        ),
                    ],
                )
            ],
        ),
        "GetProductPropertyIds": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
    },
    "ansys.api.edb.v1.ComponentGroupService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target", "layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.GroupService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByDef", service="ansys.api.edb.v1.ComponentGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "GetNumberOfPins": _RpcInfo(cache=True, invalidations=[[]]),
        "GetComponentProperty": _RpcInfo(cache=True, invalidations=[[]]),
        "SetComponentProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponentProperty",
                            service="ansys.api.edb.v1.ComponentGroupService",
                        )
                    ],
                )
            ],
        ),
        "GetComponentType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetComponentType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponentType", service="ansys.api.edb.v1.ComponentGroupService"
                        )
                    ],
                )
            ],
        ),
        "FindByDef": _RpcInfo(cache=True, invalidations=[["layout"]]),
    },
    "ansys.api.edb.v1.ComponentModelService": {
        "SetReferenceFile": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetReferenceFile", service="ansys.api.edb.v1.ComponentModelService"
                        )
                    ],
                )
            ],
        ),
        "GetReferenceFile": _RpcInfo(cache=True, invalidations=[[]]),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "FindById": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "GetType": _RpcInfo(cache=True, invalidations=[[]]),
        "GetId": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.NPortComponentModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True)
    },
    "ansys.api.edb.v1.DynamicLinkComponentModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "SetDesignName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDesignName",
                            service="ansys.api.edb.v1.DynamicLinkComponentModelService",
                        )
                    ],
                )
            ],
        ),
        "GetDesignName": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.ComponentPinService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            write_no_cache_invalidation=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ComponentPinService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetComponentPins", service="ansys.api.edb.v1.ComponentDefService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamComponentPins",
                            service="ansys.api.edb.v1.ComponentDefService",
                        ),
                    ],
                ),
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ComponentPinService"
                        )
                    ],
                )
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "GetNumber": _RpcInfo(cache=True),
        "GetComponentDef": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.ComponentPropertyService": {
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetPackageMountingOffset": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPackageMountingOffset": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPackageMountingOffset",
                            service="ansys.api.edb.v1.ComponentPropertyService",
                        )
                    ],
                )
            ],
        ),
        "GetPackageDef": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPackageDef": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPackageDef", service="ansys.api.edb.v1.ComponentPropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetModel": _RpcInfo(cache=True, invalidations=[[]]),
        "SetModel": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetModel", service="ansys.api.edb.v1.ComponentPropertyService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.ConnectableService": {
        "GetObjType": _RpcInfo(cache=True, invalidations=[[]]),
        "FindByIdAndType": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetId": _RpcInfo(cache=True, invalidations=[[]]),
        "GetComponent": _RpcInfo(cache=True, invalidations=[[]]),
        "GetGroup": _RpcInfo(cache=True, invalidations=[[]]),
        "SetGroup": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetGroup", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="GetComponent", service="ansys.api.edb.v1.ConnectableService"
                        ),
                    ],
                )
            ],
        ),
        "GetNet": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNet": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNet", service="ansys.api.edb.v1.ConnectableService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.DatabaseService": {
        "Create": _RpcInfo(write_no_cache_invalidation=True),
        "Open": _RpcInfo(read_no_cache=True),
        "Delete": _RpcInfo(write_no_cache_invalidation=True),
        "IsReadOnly": _RpcInfo(cache=True, invalidations=[[]]),
        "GetTopCircuits": _RpcInfo(cache=True, invalidations=[[]]),
        "StreamTopCircuits": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetId": _RpcInfo(cache=True, invalidations=[[]]),
        "FindById": _RpcInfo(cache=True),
        "GetVersionByRelease": _RpcInfo(cache=True),
        "GetDirectory": _RpcInfo(cache=True, invalidations=[[]]),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductProperty", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="GetProductPropertyIds", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "GetProductPropertyIds": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "GetVersion": _RpcInfo(cache=True, invalidations=[[]]),
        "Scale": _RpcInfo(buffer=True),
        "GetSource": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSource": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSource", service="ansys.api.edb.v1.DatabaseService"
                        )
                    ],
                )
            ],
        ),
        "GetSourceVersion": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSourceVersion": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSourceVersion", service="ansys.api.edb.v1.DatabaseService"
                        )
                    ],
                )
            ],
        ),
        "CopyCells": _RpcInfo(
            write_no_buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(rpc="Find", service="ansys.api.edb.v1.CellService"),
                        _InvalidationInfo(
                            rpc="GetTopCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="TopCircuitCells", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="GetCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="GetFootprints", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamCircuits", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamFootprints", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "GetDefinitionObjs": _RpcInfo(read_no_cache=True, invalidations=[["target"]]),
        "StreamDefinitionObjs": _RpcInfo(read_no_cache=True, invalidations=[["target"]]),
        "TopCircuitCells": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetCircuits": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamCircuits": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetFootprints": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamFootprints": _RpcInfo(read_no_cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.DatasetDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.DatasetDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetName", service="ansys.api.edb.v1.DatasetDefService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.DatasetDefService"
                        )
                    ],
                ),
            ],
        ),
        "GetData": _RpcInfo(cache=True, invalidations=[[]]),
        "SetData": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetData", service="ansys.api.edb.v1.DatasetDefService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.DebyeModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetFrequencyRange": _RpcInfo(cache=True, invalidations=[[]]),
        "SetFrequencyRange": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetFrequencyRange", service="ansys.api.edb.v1.DebyeModelService"
                        )
                    ],
                )
            ],
        ),
        "GetRelativePermitivityAtHighLowFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRelativePermitivityAtHighLowFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRelativePermitivityAtHighLowFrequency",
                            service="ansys.api.edb.v1.DebyeModelService",
                        )
                    ],
                )
            ],
        ),
        "IsRelativePermitivityEnabledAtOpticalFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRelativePermitivityEnabledAtOpticalFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="IsRelativePermitivityEnabledAtOpticalFrequency",
                            service="ansys.api.edb.v1.DebyeModelService",
                        )
                    ],
                )
            ],
        ),
        "GetRelativePermitivityAtOpticalFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRelativePermitivityAtOpticalFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRelativePermitivityAtOpticalFrequency",
                            service="ansys.api.edb.v1.DebyeModelService",
                        )
                    ],
                )
            ],
        ),
        "UseDCConductivity": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseDCConductivity": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="UseDCConductivity", service="ansys.api.edb.v1.DebyeModelService"
                        )
                    ],
                )
            ],
        ),
        "GetDCConductivity": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCConductivity": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCConductivity", service="ansys.api.edb.v1.DebyeModelService"
                        )
                    ],
                )
            ],
        ),
        "GetLossTangentAtHighLowFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLossTangentAtHighLowFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLossTangentAtHighLowFrequency",
                            service="ansys.api.edb.v1.DebyeModelService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.DielectricMaterialModelService": {
        "GetType": _RpcInfo(cache=True, invalidations=[[]])
    },
    "ansys.api.edb.v1.DiePropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetDieType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDieType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDieType", service="ansys.api.edb.v1.DiePropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetHeight": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHeight": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHeight", service="ansys.api.edb.v1.DiePropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetOrientation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetOrientation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetOrientation", service="ansys.api.edb.v1.DiePropertyService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.DifferentialPairService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.DifferentialPairService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetDifferentialPair": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDifferentialPair": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["dp"],
                    [
                        _InvalidationInfo(
                            rpc="GetDifferentialPair",
                            service="ansys.api.edb.v1.DifferentialPairService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.DjordjecvicSarkarModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetFrequency",
                            service="ansys.api.edb.v1.DjordjecvicSarkarModelService",
                        )
                    ],
                )
            ],
        ),
        "GetRelativePermitivityAtFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRelativePermitivityAtFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRelativePermitivityAtFrequency",
                            service="ansys.api.edb.v1.DjordjecvicSarkarModelService",
                        )
                    ],
                )
            ],
        ),
        "GetLossTangentAtFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLossTangentAtFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLossTangentAtFrequency",
                            service="ansys.api.edb.v1.DjordjecvicSarkarModelService",
                        )
                    ],
                )
            ],
        ),
        "GetHighFrequencyCorner": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHighFrequencyCorner": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHighFrequencyCorner",
                            service="ansys.api.edb.v1.DjordjecvicSarkarModelService",
                        )
                    ],
                )
            ],
        ),
        "UseDCRelativePermitivity": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseDCRelativePermitivity": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="UseDCRelativePermitivity",
                            service="ansys.api.edb.v1.DjordjecvicSarkarModelService",
                        )
                    ],
                )
            ],
        ),
        "GetDCRelativePermitivity": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCRelativePermitivity": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCRelativePermitivity",
                            service="ansys.api.edb.v1.DjordjecvicSarkarModelService",
                        )
                    ],
                )
            ],
        ),
        "GetDCConductivity": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCConductivity": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCConductivity",
                            service="ansys.api.edb.v1.DjordjecvicSarkarModelService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.EDBErrorManagerService": {"GetErrors": _RpcInfo(read_no_cache=True)},
    "ansys.api.edb.v1.EdgeService": {
        "GetEdgeType": _RpcInfo(cache=True, invalidations=[[]]),
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                    ],
                )
            ],
        ),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.EdgeTerminalService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.TerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetEdges": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamEdges": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "SetEdges": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetEdges", service="ansys.api.edb.v1.EdgeTerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamEdges", service="ansys.api.edb.v1.EdgeTerminalService"
                        ),
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.ExtendedNetService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ExtendedNetService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "RemoveNet": _RpcInfo(buffer=True, write_no_cache_invalidation=True),
        "AddNet": _RpcInfo(buffer=True, write_no_cache_invalidation=True),
        "RemoveAllNets": _RpcInfo(buffer=True, write_no_cache_invalidation=True),
    },
    "ansys.api.edb.v1.GroupService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.GroupService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "AddMember": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNumberOfPins", service="ansys.api.edb.v1.ComponentGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="GetMembers", service="ansys.api.edb.v1.GroupService"
                        ),
                    ],
                ),
                (
                    ["member"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponent", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="GetGroup", service="ansys.api.edb.v1.ConnectableService"
                        ),
                    ],
                ),
            ],
        ),
        "RemoveMember": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNumberOfPins", service="ansys.api.edb.v1.ComponentGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="GetMembers", service="ansys.api.edb.v1.GroupService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamMembers", service="ansys.api.edb.v1.GroupService"
                        ),
                    ],
                ),
                (
                    ["member"],
                    [
                        _InvalidationInfo(
                            rpc="GetComponent", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="GetGroup", service="ansys.api.edb.v1.ConnectableService"
                        ),
                    ],
                ),
            ],
        ),
        "Ungroup": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetComponent", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="GetGroup", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.GroupService"
                        ),
                    ],
                )
            ],
        ),
        "GetMembers": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamMembers": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetGroupType": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.HFSSPIGeneralSettingsService": {
        "GetHFSSPIModelType": _RpcInfo(cache=True),
        "SetHFSSPIModelType": _RpcInfo(buffer=True),
        "GetUseAutoMeshRegion": _RpcInfo(cache=True),
        "SetUseAutoMeshRegion": _RpcInfo(buffer=True),
        "GetUseMeshRegion": _RpcInfo(cache=True),
        "SetUseMeshRegion": _RpcInfo(buffer=True),
        "GetMeshRegionName": _RpcInfo(cache=True),
        "SetMeshRegionName": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSPIAdvancedSettingsService": {
        "GetICModeAutoResolution": _RpcInfo(cache=True),
        "SetICModeAutoResolution": _RpcInfo(buffer=True),
        "GetICModeLength": _RpcInfo(cache=True),
        "SetICModeLength": _RpcInfo(buffer=True),
        "GetSmallPlaneArea": _RpcInfo(cache=True),
        "SetSmallPlaneArea": _RpcInfo(buffer=True),
        "GetZeroMetalLayerThickness": _RpcInfo(cache=True),
        "SetZeroMetalLayerThickness": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSPISolverSettingsService": {
        "GetEnhancedLowFrequencyAccuracy": _RpcInfo(cache=True),
        "SetEnhancedLowFrequencyAccuracy": _RpcInfo(buffer=True),
        "GetViaAreaCutoffCircElems": _RpcInfo(cache=True),
        "SetViaAreaCutoffCircElems": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSGeneralSettingsService": {
        "GetSingleFrequencyAdaptiveSolution": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSingleFrequencyAdaptiveSolution": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSingleFrequencyAdaptiveSolution",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMultiFrequencyAdaptiveSolution": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMultiFrequencyAdaptiveSolution": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMultiFrequencyAdaptiveSolution",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetBroadbandFrequencyAdaptiveSolution": _RpcInfo(cache=True, invalidations=[[]]),
        "SetBroadbandFrequencyAdaptiveSolution": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetBroadbandFrequencyAdaptiveSolution",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSaveFieldsFlag": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSaveFieldsFlag": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSaveFieldsFlag",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseMeshRegion": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseMeshRegion": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseMeshRegion",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMeshRegionName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshRegionName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshRegionName",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseParallelRefinement": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseParallelRefinement": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseParallelRefinement",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetAdaptType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAdaptType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAdaptType",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSaveRadFieldsOnlyFlag": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSaveRadFieldsOnlyFlag": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSaveRadFieldsOnlyFlag",
                            service="ansys.api.edb.v1.HFSSGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.HFSSOptionsSettingsService": {
        "GetMaxRefinementPerPass": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxRefinementPerPass": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxRefinementPerPass",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMinPasses": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinPasses",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMinConvergedPasses": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinConvergedPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinConvergedPasses",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseMaxRefinement": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseMaxRefinement": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseMaxRefinement",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetBasisFunctionOrder": _RpcInfo(cache=True, invalidations=[[]]),
        "SetBasisFunctionOrder": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetBasisFunctionOrder",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSolveInsideMetalBasis": _RpcInfo(cache=True),
        "SetSolveInsideMetalBasis": _RpcInfo(buffer=True),
        "GetSolverTypeOrder": _RpcInfo(cache=True),
        "SetSolverTypeOrder": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolverTypeOrder",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetRelativeResidual": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRelativeResidual": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRelativeResidual",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseShellElements": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseShellElements": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseShellElements",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetEnhancedLowFrequencyAccuracy": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEnhancedLowFrequencyAccuracy": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEnhancedLowFrequencyAccuracy",
                            service="ansys.api.edb.v1.HFSSOptionsSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.HFSSAdvancedSettingsService": {
        "GetICModeAutoResolution": _RpcInfo(cache=True, invalidations=[[]]),
        "SetICModeAutoResolution": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetICModeAutoResolution",
                            service="ansys.api.edb.v1.HFSSAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetICModeLength": _RpcInfo(cache=True, invalidations=[[]]),
        "SetICModeLength": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetICModeLength",
                            service="ansys.api.edb.v1.HFSSAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.HFSSAdvancedMeshingSettingsService": {
        "GetLayerAlignment": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayerAlignment": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayerAlignment",
                            service="ansys.api.edb.v1.HFSSAdvancedMeshingSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.HFSSSolverSettingsService": {
        "GetMaxDeltaZ0": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxDeltaZ0": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxDeltaZ0",
                            service="ansys.api.edb.v1.HFSSSolverSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSetTrianglesForWaveport": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSetTrianglesForWaveport": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSetTrianglesForWaveport",
                            service="ansys.api.edb.v1.HFSSSolverSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMinTrianglesForWavePort": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinTrianglesForWavePort": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinTrianglesForWavePort",
                            service="ansys.api.edb.v1.HFSSSolverSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMaxTrianglesForWavePort": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxTrianglesForWavePort": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxTrianglesForWavePort",
                            service="ansys.api.edb.v1.HFSSSolverSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIntraPlaneCouplingEnabled": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIntraPlaneCouplingEnabled": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIntraPlaneCouplingEnabled",
                            service="ansys.api.edb.v1.HFSSSolverSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.DCRSettingsService": {
        "GetMaxPasses": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxPasses", service="ansys.api.edb.v1.DCRSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetMinPasses": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinPasses", service="ansys.api.edb.v1.DCRSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetMinConvergedPasses": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinConvergedPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinConvergedPasses",
                            service="ansys.api.edb.v1.DCRSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPercentError": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPercentError": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPercentError", service="ansys.api.edb.v1.DCRSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetPercentRefinementPerPass": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPercentRefinementPerPass": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPercentRefinementPerPass",
                            service="ansys.api.edb.v1.DCRSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.HfssSimulationSetupService": {
        "GetMeshOperations": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshOperations": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshOperations",
                            service="ansys.api.edb.v1.HfssSimulationSetupService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.HierarchyObjectService": {
        "GetTransform": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTransform": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetTransform", service="ansys.api.edb.v1.HierarchyObjectService"
                        ),
                        _InvalidationInfo(
                            rpc="GetOrig", service="ansys.api.edb.v1.InstArrayService"
                        ),
                        _InvalidationInfo(
                            rpc="GetLocation", service="ansys.api.edb.v1.HierarchyObjectService"
                        ),
                    ],
                )
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.GroupService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.InstArrayService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.CellInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ViaGroupService"
                        ),
                    ],
                )
            ],
        ),
        "GetComponent": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPlacementLayer": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPlacementLayer": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPlacementLayer",
                            service="ansys.api.edb.v1.HierarchyObjectService",
                        )
                    ],
                )
            ],
        ),
        "GetLocation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLocation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLocation", service="ansys.api.edb.v1.HierarchyObjectService"
                        ),
                        _InvalidationInfo(
                            rpc="GetOrig", service="ansys.api.edb.v1.InstArrayService"
                        ),
                    ],
                )
            ],
        ),
        "GetSolveIndependentPreference": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolveIndependentPreference": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolveIndependentPreference",
                            service="ansys.api.edb.v1.HierarchyObjectService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.ICComponentPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "SetSolderBallProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolderBallProperty",
                            service="ansys.api.edb.v1.ICComponentPropertyService",
                        )
                    ],
                )
            ],
        ),
        "GetSolderBallProperty": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDieProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDieProperty",
                            service="ansys.api.edb.v1.ICComponentPropertyService",
                        )
                    ],
                )
            ],
        ),
        "GetDieProperty": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPortProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPortProperty",
                            service="ansys.api.edb.v1.ICComponentPropertyService",
                        )
                    ],
                )
            ],
        ),
        "GetPortProperty": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.InstArrayService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.InstArrayService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                ),
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetOrig": _RpcInfo(cache=True, invalidations=[[]]),
        "GetXAxis": _RpcInfo(cache=True, invalidations=[[]]),
        "SetXAxis": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetXAxis", service="ansys.api.edb.v1.InstArrayService"
                        )
                    ],
                )
            ],
        ),
        "GetYAxis": _RpcInfo(cache=True, invalidations=[[]]),
        "SetYAxis": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetYAxis", service="ansys.api.edb.v1.InstArrayService"
                        )
                    ],
                )
            ],
        ),
        "GetXCount": _RpcInfo(cache=True, invalidations=[[]]),
        "SetXCount": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetXCount", service="ansys.api.edb.v1.InstArrayService"
                        )
                    ],
                )
            ],
        ),
        "GetYCount": _RpcInfo(cache=True, invalidations=[[]]),
        "SetYCount": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetYCount", service="ansys.api.edb.v1.InstArrayService"
                        )
                    ],
                )
            ],
        ),
        "Decompose": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.IOComponentPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "SetSolderBallProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolderBallProperty",
                            service="ansys.api.edb.v1.IOComponentPropertyService",
                        )
                    ],
                )
            ],
        ),
        "GetSolderBallProperty": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPortProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPortProperty",
                            service="ansys.api.edb.v1.IOComponentPropertyService",
                        )
                    ],
                )
            ],
        ),
        "GetPortProperty": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.LayerService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetLayerType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayerType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayerType", service="ansys.api.edb.v1.LayerService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                    ],
                ),
            ],
        ),
        "IsViaLayer": _RpcInfo(cache=True, invalidations=[[]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [_InvalidationInfo(rpc="GetName", service="ansys.api.edb.v1.LayerService")],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.LayerCollectionService"
                        )
                    ],
                ),
            ],
        ),
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetLayerId": _RpcInfo(cache=True, invalidations=[[]]),
        "GetTopBottomAssociation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTopBottomAssociation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetTopBottomAssociation", service="ansys.api.edb.v1.LayerService"
                        )
                    ],
                )
            ],
        ),
        "GetColor": _RpcInfo(cache=True, invalidations=[[]]),
        "SetColor": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [_InvalidationInfo(rpc="GetColor", service="ansys.api.edb.v1.LayerService")],
                )
            ],
        ),
        "GetVisibilityMask": _RpcInfo(cache=True, invalidations=[[]]),
        "SetVisibilityMask": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetVisibilityMask", service="ansys.api.edb.v1.LayerService"
                        )
                    ],
                )
            ],
        ),
        "GetLocked": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLocked": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [_InvalidationInfo(rpc="GetLocked", service="ansys.api.edb.v1.LayerService")],
                )
            ],
        ),
        "GetTransparency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTransparency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetTransparency", service="ansys.api.edb.v1.LayerService"
                        )
                    ],
                )
            ],
        ),
        "GetDrawOverride": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDrawOverride": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetDrawOverride", service="ansys.api.edb.v1.LayerService"
                        )
                    ],
                )
            ],
        ),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductProperty", service="ansys.api.edb.v1.LayerService"
                        ),
                        _InvalidationInfo(
                            rpc="GetProductPropertyIds", service="ansys.api.edb.v1.LayerService"
                        ),
                    ],
                )
            ],
        ),
        "GetProductPropertyIds": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "IsInZone": _RpcInfo(cache=True, invalidations=[["layer"]]),
        "SetIsInZone": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["zone_msg", "layer"],
                    [
                        _InvalidationInfo(rpc="IsInZone", service="ansys.api.edb.v1.LayerService"),
                        _InvalidationInfo(rpc="GetZones", service="ansys.api.edb.v1.LayerService"),
                        _InvalidationInfo(rpc="GetZone", service="ansys.api.edb.v1.LayerService"),
                    ],
                )
            ],
        ),
        "GetZones": _RpcInfo(cache=True, invalidations=[[]]),
        "GetZone": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.LayerCollectionService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetMode": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMode": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [
                        _InvalidationInfo(
                            rpc="GetMode", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="IsValid", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                    ],
                )
            ],
        ),
        "AddLayers": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="GetLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="IsValid", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                    ],
                )
            ],
        ),
        "ImportFromControlFile": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [_InvalidationInfo(rpc="*", service="ansys.api.edb.v1.LayerCollectionService")],
                )
            ],
        ),
        "AddLayer": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="GetLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="IsValid", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                    ],
                )
            ],
        ),
        "IsValid": _RpcInfo(cache=True, invalidations=[[]]),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layer_collection"]]),
        "GetTopBottomStackupLayers": _RpcInfo(cache=True, invalidations=[["layer_collection"]]),
        "GetLayers": _RpcInfo(read_no_cache=True, invalidations=[["layer_collection"]]),
        "StreamLayers": _RpcInfo(read_no_cache=True, invalidations=[["layer_collection"]]),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductProperty",
                            service="ansys.api.edb.v1.LayerCollectionService",
                        ),
                        _InvalidationInfo(
                            rpc="GetProductPropertyIds",
                            service="ansys.api.edb.v1.LayerCollectionService",
                        ),
                    ],
                )
            ],
        ),
        "GetProductPropertyIds": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "MergeDielectrics": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="GetLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayers", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(
                            rpc="IsValid", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                    ],
                )
            ],
        ),
        "GetZoneIds": _RpcInfo(cache=True, invalidations=[[]]),
        "GetZoneName": _RpcInfo(cache=True, invalidations=[["layer_collection"]]),
        "SetZoneName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [
                        _InvalidationInfo(
                            rpc="GetZoneName", service="ansys.api.edb.v1.LayerCollectionService"
                        )
                    ],
                )
            ],
        ),
        "InsertZone": _RpcInfo(
            write_no_buffer=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [
                        _InvalidationInfo(
                            rpc="GetZoneIds", service="ansys.api.edb.v1.LayerCollectionService"
                        )
                    ],
                )
            ],
        ),
        "RemoveZone": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [
                        _InvalidationInfo(
                            rpc="GetZoneIds", service="ansys.api.edb.v1.LayerCollectionService"
                        )
                    ],
                )
            ],
        ),
        "SimplifyDielectricsForPhi": _RpcInfo(
            write_no_buffer=True,
            invalidations=[
                (
                    ["layer_collection"],
                    [_InvalidationInfo(rpc="*", service="ansys.api.edb.v1.LayerCollectionService")],
                )
            ],
        ),
        "AddZoneToLayer": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(rpc="IsInZone", service="ansys.api.edb.v1.LayerService"),
                        _InvalidationInfo(rpc="GetZones", service="ansys.api.edb.v1.LayerService"),
                        _InvalidationInfo(rpc="GetZone", service="ansys.api.edb.v1.LayerService"),
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.LayerMapService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "Clear": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetMappingForward", service="ansys.api.edb.v1.LayerMapService"
                        ),
                        _InvalidationInfo(
                            rpc="GetMappingBackward", service="ansys.api.edb.v1.LayerMapService"
                        ),
                    ],
                )
            ],
        ),
        "SetMapping": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetMappingForward", service="ansys.api.edb.v1.LayerMapService"
                        ),
                        _InvalidationInfo(
                            rpc="GetMappingBackward", service="ansys.api.edb.v1.LayerMapService"
                        ),
                    ],
                )
            ],
        ),
        "GetMappingForward": _RpcInfo(cache=True, invalidations=[[]]),
        "GetMappingBackward": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.LayoutService": {
        "GetCell": _RpcInfo(cache=True, invalidations=[[]]),
        "GetLayerCollection": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayerCollection": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayerCollection", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.LayerCollectionService"
                        ),
                        _InvalidationInfo(rpc="*", service="ansys.api.edb.v1.LayerService"),
                        _InvalidationInfo(rpc="*", service="ansys.api.edb.v1.StackupLayerService"),
                        _InvalidationInfo(rpc="*", service="ansys.api.edb.v1.ViaLayerService"),
                    ],
                ),
            ],
        ),
        "GetItems": _RpcInfo(read_no_cache=True, invalidations=[["target"]]),
        "StreamItems": _RpcInfo(read_no_cache=True, invalidations=[["target"]]),
        "GetExpandedExtentFromNets": _RpcInfo(read_no_cache=True),
        "ConvertPrimitivesToVias": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                    ],
                )
            ],
        ),
        "ArePortReferenceTerminalsConnected": _RpcInfo(read_no_cache=True),
        "GetZonePrimitives": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamZonePrimitives": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "SetFixedZonePrimitives": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetFixedZonePrimitive", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                )
            ],
        ),
        "GetFixedZonePrimitive": _RpcInfo(cache=True, invalidations=[[]]),
        "GetBoardBendDefs": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamBoardBendDefs": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "SynchronizeBendManager": _RpcInfo(
            write_no_buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetBoardBendDefs", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                ),
                (
                    None,
                    [_InvalidationInfo(rpc="*", service="ansys.api.edb.v1.BoardBendDefService")],
                ),
            ],
        ),
        "GetLayoutInstance": _RpcInfo(cache=True, invalidations=[[]]),
        "ReconstructArcs": _RpcInfo(buffer=True),
        "UnitePrimitives": _RpcInfo(buffer=True),
        "GroupVias": _RpcInfo(buffer=True),
        "SnapVias": _RpcInfo(buffer=True),
        "SnapPrimitives": _RpcInfo(buffer=True),
        "CreateMeshRegion": _RpcInfo(buffer=True, write_no_cache_invalidation=True),
        "CompressPrimitives": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.LayoutComponentService": {
        "ExportLayoutComponent": _RpcInfo(write_no_cache_invalidation=True),
        "ImportLayoutComponent": _RpcInfo(
            write_no_cache_invalidation=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.LayoutComponentService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "GetCellInstance": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.LayoutInstanceService": {
        "Refresh": _RpcInfo(
            write_no_buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.LayoutInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.LayoutInstanceContextService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.LayoutObjInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.LayoutObjInstance2DGeometryService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.LayoutObjInstance3DGeometryService"
                        ),
                        _InvalidationInfo(
                            rpc="*", service="ansys.api.edb.v1.LayoutObjInstanceGeometryService"
                        ),
                    ],
                )
            ],
        ),
        "QueryLayoutObjInstances": _RpcInfo(cache=True, invalidations=[["layout_inst"]]),
        "StreamLayoutObjInstancesQuery": _RpcInfo(read_no_cache=True),
        "GetLayoutObjInstanceInContext": _RpcInfo(cache=True, invalidations=[["layout_inst"]]),
        "GetConnectedObjects": _RpcInfo(read_no_cache=True, invalidations=[["layout_inst"]]),
        "StreamConnectedObjects": _RpcInfo(read_no_cache=True, invalidations=[["layout_inst"]]),
    },
    "ansys.api.edb.v1.LayoutInstanceContextService": {
        "GetLayout": _RpcInfo(cache=True, invalidations=[[]]),
        "GetBBox": _RpcInfo(cache=True, invalidations=[["target"]]),
        "IsTopOrBlackBox": _RpcInfo(cache=True, invalidations=[[]]),
        "GetTopOrBlackBox": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPlacementElevation": _RpcInfo(cache=True, invalidations=[[]]),
        "Is3DPlacement": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetTransformation": _RpcInfo(cache=True, invalidations=[[]]),
        "GetTransformationBetweenContexts": _RpcInfo(cache=True, invalidations=[["edb_obj_0"]]),
    },
    "ansys.api.edb.v1.LayoutObjService": {
        "GetLayout": _RpcInfo(cache=True, invalidations=[["target"]]),
        "Delete": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.LayoutObjService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                    ],
                )
            ],
        ),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[["target", "edb_obj"]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target", "edb_obj"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductProperty", service="ansys.api.edb.v1.LayoutObjService"
                        ),
                        _InvalidationInfo(
                            rpc="GetProductPropertyIds", service="ansys.api.edb.v1.LayoutObjService"
                        ),
                    ],
                )
            ],
        ),
        "GetProductPropertyIds": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.LayoutObjInstanceService": {
        "GetLayers": _RpcInfo(cache=True, invalidations=[[]]),
        "StreamLayers": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetGeometries": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "GetContext": _RpcInfo(cache=True, invalidations=[[]]),
        "GetLayoutInstanceContext": _RpcInfo(cache=True, invalidations=[[]]),
        "GetLayoutObj": _RpcInfo(cache=True, invalidations=[[]]),
        "GetBBox": _RpcInfo(cache=True, invalidations=[["target"]]),
    },
    "ansys.api.edb.v1.LayoutObjInstance2DGeometryService": {
        "IsNegative": _RpcInfo(cache=True, invalidations=[["layout_obj_inst_geom", "geometry"]]),
        "GetPolygonData": _RpcInfo(
            cache=True, invalidations=[["layout_obj_inst_geom", "geometry"]]
        ),
    },
    "ansys.api.edb.v1.LayoutObjInstance3DGeometryService": {
        "GetTesselationData": _RpcInfo(cache=True, invalidations=[["geometry"]])
    },
    "ansys.api.edb.v1.LayoutObjInstanceGeometryService": {
        "GetMaterial": _RpcInfo(cache=True, invalidations=[["geometry"]]),
        "GetColor": _RpcInfo(cache=True, invalidations=[["geometry"]]),
    },
    "ansys.api.edb.v1.MaterialDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["database"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "SetProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["materialDef"],
                    [
                        _InvalidationInfo(
                            rpc="GetProperty", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetAllProperties", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDimensions", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "Delete": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "GetProperty": _RpcInfo(cache=True, invalidations=[["materialDef"]]),
        "GetAllProperties": _RpcInfo(cache=True, invalidations=[[]]),
        "RemoveProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["materialDef"],
                    [
                        _InvalidationInfo(
                            rpc="GetProperty", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetAllProperties", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDimensions", service="ansys.api.edb.v1.MaterialDefService"
                        ),
                    ],
                )
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "GetDielectricMaterialModel": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDielectricMaterialModel": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDielectricMaterialModel",
                            service="ansys.api.edb.v1.MaterialDefService",
                        )
                    ],
                )
            ],
        ),
        "GetDimensions": _RpcInfo(cache=True, invalidations=[["materialDef"]]),
        "SetThermalModifier": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["materialDef"],
                    [
                        _InvalidationInfo(
                            rpc="GetThermalModifier", service="ansys.api.edb.v1.MaterialDefService"
                        )
                    ],
                )
            ],
        ),
        "SetAnisotropicThermalModifier": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["materialDef"],
                    [
                        _InvalidationInfo(
                            rpc="GetAnisotropicThermalModifier",
                            service="ansys.api.edb.v1.MaterialDefService",
                        )
                    ],
                )
            ],
        ),
        "GetThermalModifier": _RpcInfo(cache=True, invalidations=[["materialDef"]]),
        "GetAnisotropicThermalModifier": _RpcInfo(cache=True, invalidations=[["materialDef"]]),
    },
    "ansys.api.edb.v1.MaterialPropertyThermalModifierService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetQuadraticModelParams": _RpcInfo(cache=True, invalidations=[[]]),
        "GetThermalModifierExpression": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.McadModelService": {
        "CreateStride": _RpcInfo(
            buffer=True,
            returns_future=True,
            write_no_cache_invalidation=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                )
            ],
        ),
        "CreateHfss": _RpcInfo(
            buffer=True,
            returns_future=True,
            write_no_cache_invalidation=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                )
            ],
        ),
        "Create3dComp": _RpcInfo(
            buffer=True,
            returns_future=True,
            write_no_cache_invalidation=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        )
                    ],
                )
            ],
        ),
        "IsMcad": _RpcInfo(cache=True, invalidations=[[]]),
        "IsMcadStride": _RpcInfo(cache=True, invalidations=[[]]),
        "IsMcadHfss": _RpcInfo(cache=True, invalidations=[[]]),
        "IsMcad3dComp": _RpcInfo(cache=True, invalidations=[[]]),
        "GetOrigin": _RpcInfo(cache=True, invalidations=[[]]),
        "SetOrigin": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetOrigin", service="ansys.api.edb.v1.McadModelService"
                        )
                    ],
                )
            ],
        ),
        "GetRotation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRotation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["model"],
                    [
                        _InvalidationInfo(
                            rpc="GetRotation", service="ansys.api.edb.v1.McadModelService"
                        )
                    ],
                )
            ],
        ),
        "GetScale": _RpcInfo(cache=True, invalidations=[[]]),
        "SetScale": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetScale", service="ansys.api.edb.v1.McadModelService"
                        )
                    ],
                )
            ],
        ),
        "GetMaterial": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["model"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaterial", service="ansys.api.edb.v1.McadModelService"
                        )
                    ],
                )
            ],
        ),
        "GetVisible": _RpcInfo(cache=True, invalidations=[[]]),
        "SetVisible": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["model"],
                    [
                        _InvalidationInfo(
                            rpc="GetVisible", service="ansys.api.edb.v1.McadModelService"
                        )
                    ],
                )
            ],
        ),
        "GetModeled": _RpcInfo(cache=True, invalidations=[[]]),
        "SetModeled": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["model"],
                    [
                        _InvalidationInfo(
                            rpc="GetModeled", service="ansys.api.edb.v1.McadModelService"
                        )
                    ],
                )
            ],
        ),
        "GetCellInst": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPartCount": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPartName": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPartIndex": _RpcInfo(cache=True, invalidations=[[]]),
        "GetModelName": _RpcInfo(cache=True, invalidations=[[]]),
        "GetDesignName": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.ModelService": {
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True)
    },
    "ansys.api.edb.v1.MultipoleDebyeModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters",
                            service="ansys.api.edb.v1.MultipoleDebyeModelService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.NetService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(rpc="FindByName", service="ansys.api.edb.v1.NetService"),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="GetName", service="ansys.api.edb.v1.NetService")],
                ),
                (
                    None,
                    [_InvalidationInfo(rpc="FindByName", service="ansys.api.edb.v1.NetService")],
                ),
            ],
        ),
        "GetIsPowerGround": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIsPowerGround": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIsPowerGround", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetNets", service="ansys.api.edb.v1.NetClassService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamNets", service="ansys.api.edb.v1.NetClassService"
                        ),
                    ],
                ),
            ],
        ),
        "GetLayoutObjects": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamLayoutObjects": _RpcInfo(read_no_cache=True, invalidations=[["target"]]),
    },
    "ansys.api.edb.v1.NetlistModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetNetlist": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNetlist": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNetlist", service="ansys.api.edb.v1.NetlistModelService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.NetClassService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.NetClassService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="GetName", service="ansys.api.edb.v1.NetClassService")],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.NetClassService"
                        )
                    ],
                ),
            ],
        ),
        "GetDescription": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDescription": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDescription", service="ansys.api.edb.v1.NetClassService"
                        )
                    ],
                )
            ],
        ),
        "IsPowerGround": _RpcInfo(cache=True, invalidations=[[]]),
        "GetNets": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamNets": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "AddNet": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["netclass"],
                    [
                        _InvalidationInfo(
                            rpc="ContainsNet", service="ansys.api.edb.v1.NetClassService"
                        ),
                        _InvalidationInfo(
                            rpc="GetNets", service="ansys.api.edb.v1.NetClassService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamNets", service="ansys.api.edb.v1.NetClassService"
                        ),
                    ],
                )
            ],
        ),
        "RemoveNet": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["netclass"],
                    [
                        _InvalidationInfo(
                            rpc="ContainsNet", service="ansys.api.edb.v1.NetClassService"
                        ),
                        _InvalidationInfo(
                            rpc="GetNets", service="ansys.api.edb.v1.NetClassService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamNets", service="ansys.api.edb.v1.NetClassService"
                        ),
                    ],
                )
            ],
        ),
        "ContainsNet": _RpcInfo(cache=True, invalidations=[["netclass"]]),
    },
    "ansys.api.edb.v1.PackageDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.PackageDefService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByEDBUId", service="ansys.api.edb.v1.PackageDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "Delete": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.PackageDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "FindByEDBUId": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetName", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                ),
            ],
        ),
        "GetExteriorBoundary": _RpcInfo(cache=True, invalidations=[[]]),
        "SetExteriorBoundary": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetExteriorBoundary", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetHeight": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHeight": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHeight", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetOperatingPower": _RpcInfo(cache=True, invalidations=[[]]),
        "SetOperatingPower": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetOperatingPower", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetMaximumPower": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaximumPower": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaximumPower", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetTherm_Cond": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTherm_Cond": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetTherm_Cond", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetTheta_JB": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTheta_JB": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetTheta_JB", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetTheta_JC": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTheta_JC": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetTheta_JC", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetHeatSink": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHeatSink": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHeatSink", service="ansys.api.edb.v1.PackageDefService"
                        )
                    ],
                )
            ],
        ),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductProperty", service="ansys.api.edb.v1.PackageDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetProductPropertyIds",
                            service="ansys.api.edb.v1.PackageDefService",
                        ),
                    ],
                )
            ],
        ),
        "GetProductPropertyIds": _RpcInfo(cache=True, invalidations=[["edb_obj"]]),
    },
    "ansys.api.edb.v1.PadstackDefService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.PadstackDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "Delete": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.PadstackDefService"
                        ),
                        _InvalidationInfo(
                            rpc="GetDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamDefinitionObjs", service="ansys.api.edb.v1.DatabaseService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "GetData": _RpcInfo(cache=True, invalidations=[[]]),
        "SetData": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetData", service="ansys.api.edb.v1.PadstackDefService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PadstackDefDataService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetMaterial": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaterial", service="ansys.api.edb.v1.PadstackDefDataService"
                        )
                    ],
                )
            ],
        ),
        "GetLayerNames": _RpcInfo(cache=True, invalidations=[[]]),
        "GetLayerIds": _RpcInfo(cache=True, invalidations=[[]]),
        "AddLayers": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayerIds", service="ansys.api.edb.v1.PadstackDefDataService"
                        ),
                        _InvalidationInfo(
                            rpc="GetLayerNames", service="ansys.api.edb.v1.PadstackDefDataService"
                        ),
                    ],
                )
            ],
        ),
        "GetPadParameters": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetPadParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetPadParameters",
                            service="ansys.api.edb.v1.PadstackDefDataService",
                        ),
                        _InvalidationInfo(
                            rpc="GetLayerIds", service="ansys.api.edb.v1.PadstackDefDataService"
                        ),
                        _InvalidationInfo(
                            rpc="GetLayerNames", service="ansys.api.edb.v1.PadstackDefDataService"
                        ),
                    ],
                )
            ],
        ),
        "GetHoleRange": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHoleRange": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHoleRange", service="ansys.api.edb.v1.PadstackDefDataService"
                        )
                    ],
                )
            ],
        ),
        "GetPlatingPercentage": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPlatingPercentage": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPlatingPercentage",
                            service="ansys.api.edb.v1.PadstackDefDataService",
                        )
                    ],
                )
            ],
        ),
        "GetSolderBallShape": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolderBallShape": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolderBallShape",
                            service="ansys.api.edb.v1.PadstackDefDataService",
                        )
                    ],
                )
            ],
        ),
        "GetSolderBallPlacement": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolderBallPlacement": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolderBallPlacement",
                            service="ansys.api.edb.v1.PadstackDefDataService",
                        )
                    ],
                )
            ],
        ),
        "GetSolderBallParam": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolderBallParam": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolderBallParam",
                            service="ansys.api.edb.v1.PadstackDefDataService",
                        )
                    ],
                )
            ],
        ),
        "GetSolderBallMaterial": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolderBallMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolderBallMaterial",
                            service="ansys.api.edb.v1.PadstackDefDataService",
                        )
                    ],
                )
            ],
        ),
        "GetConnectionPt": _RpcInfo(cache=True, invalidations=[[]]),
        "SetConnectionPt": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetConnectionPt", service="ansys.api.edb.v1.PadstackDefDataService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PadstackInstanceService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetPadstackDef": _RpcInfo(cache=True, invalidations=[[]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetName", service="ansys.api.edb.v1.PadstackInstanceService"
                        )
                    ],
                )
            ],
        ),
        "GetPositionAndRotation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPositionAndRotation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPositionAndRotation",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        )
                    ],
                )
            ],
        ),
        "GetLayerRange": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayerRange": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayerRange", service="ansys.api.edb.v1.PadstackInstanceService"
                        )
                    ],
                )
            ],
        ),
        "GetSolderBallLayer": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolderBallLayer": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolderBallLayer",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        )
                    ],
                )
            ],
        ),
        "GetLayerMap": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayerMap": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayerMap", service="ansys.api.edb.v1.PadstackInstanceService"
                        )
                    ],
                )
            ],
        ),
        "GetHoleOverrides": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHoleOverrides": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHoleOverrides",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        )
                    ],
                )
            ],
        ),
        "GetIsLayoutPin": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIsLayoutPin": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIsLayoutPin", service="ansys.api.edb.v1.PadstackInstanceService"
                        )
                    ],
                )
            ],
        ),
        "GetBackDrillType": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetBackDrillByLayer": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetBackDrillByDepth": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetBackDrillByLayer": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetBackDrillByLayer",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        ),
                        _InvalidationInfo(
                            rpc="GetBackDrillType",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        ),
                    ],
                )
            ],
        ),
        "SetBackDrillByDepth": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetBackDrillByDepth",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        ),
                        _InvalidationInfo(
                            rpc="GetBackDrillType",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        ),
                    ],
                )
            ],
        ),
        "GetPadstackInstanceTerminal": _RpcInfo(cache=True, invalidations=[[]]),
        "IsInPinGroup": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetPinGroups": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamPinGroups": _RpcInfo(read_no_cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.PadstackInstanceTerminalService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.TerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    ["params", "padstack_instance"],
                    [
                        _InvalidationInfo(
                            rpc="GetPadstackInstanceTerminal",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters",
                            service="ansys.api.edb.v1.PadstackInstanceTerminalService",
                        )
                    ],
                ),
                (
                    ["params", "padstack_instance"],
                    [
                        _InvalidationInfo(
                            rpc="GetPadstackInstanceTerminal",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        )
                    ],
                ),
            ],
        ),
    },
    "ansys.api.edb.v1.PathService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "Render": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPolygonData": _RpcInfo(cache=True, invalidations=[[]]),
        "GetCenterLine": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCenterLine": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCenterLine", service="ansys.api.edb.v1.PathService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPolygonData", service="ansys.api.edb.v1.PathService"
                        ),
                    ],
                )
            ],
        ),
        "GetEndCapStyle": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEndCapStyle": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEndCapStyle", service="ansys.api.edb.v1.PathService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPolygonData", service="ansys.api.edb.v1.PathService"
                        ),
                    ],
                )
            ],
        ),
        "GetClipInfo": _RpcInfo(cache=True, invalidations=[[]]),
        "SetClipInfo": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="GetClipInfo", service="ansys.api.edb.v1.PathService")],
                )
            ],
        ),
        "GetCornerStyle": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCornerStyle": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCornerStyle", service="ansys.api.edb.v1.PathService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPolygonData", service="ansys.api.edb.v1.PathService"
                        ),
                    ],
                )
            ],
        ),
        "GetWidth": _RpcInfo(cache=True, invalidations=[[]]),
        "SetWidth": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(rpc="GetWidth", service="ansys.api.edb.v1.PathService"),
                        _InvalidationInfo(
                            rpc="GetPolygonData", service="ansys.api.edb.v1.PathService"
                        ),
                    ],
                )
            ],
        ),
        "GetMiterRatio": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMiterRatio": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMiterRatio", service="ansys.api.edb.v1.PathService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPolygonData", service="ansys.api.edb.v1.PathService"
                        ),
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PinGroupService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.PinGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="GetUniqueName", service="ansys.api.edb.v1.PinGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="IsInPinGroup", service="ansys.api.edb.v1.PadstackInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPinGroups", service="ansys.api.edb.v1.PadstackInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamPinGroups",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        ),
                    ],
                ),
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetUniqueName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "AddPins": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["pin_group"],
                    [
                        _InvalidationInfo(
                            rpc="GetPins", service="ansys.api.edb.v1.PinGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamPins", service="ansys.api.edb.v1.PinGroupService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="IsInPinGroup", service="ansys.api.edb.v1.PadstackInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPinGroups", service="ansys.api.edb.v1.PadstackInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamPinGroups",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        ),
                    ],
                ),
            ],
        ),
        "RemovePins": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["pin_group"],
                    [
                        _InvalidationInfo(
                            rpc="GetPins", service="ansys.api.edb.v1.PinGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamPins", service="ansys.api.edb.v1.PinGroupService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="IsInPinGroup", service="ansys.api.edb.v1.PadstackInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPinGroups", service="ansys.api.edb.v1.PadstackInstanceService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamPinGroups",
                            service="ansys.api.edb.v1.PadstackInstanceService",
                        ),
                    ],
                ),
            ],
        ),
        "GetPins": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamPins": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetPinGroupTerminal": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.PinGroupTerminalService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.TerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    ["pin_group"],
                    [
                        _InvalidationInfo(
                            rpc="GetPinGroupTerminal", service="ansys.api.edb.v1.PinGroupService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetPinGroup": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPinGroup": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetPinGroup", service="ansys.api.edb.v1.PinGroupTerminalService"
                        )
                    ],
                ),
                (
                    ["pin_group"],
                    [
                        _InvalidationInfo(
                            rpc="GetPinGroupTerminal", service="ansys.api.edb.v1.PinGroupService"
                        )
                    ],
                ),
            ],
        ),
        "GetLayer": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayer": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayer", service="ansys.api.edb.v1.PinGroupTerminalService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PinPairModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetRlc": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetRlc": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["model"],
                    [
                        _InvalidationInfo(
                            rpc="GetRlc", service="ansys.api.edb.v1.PinPairModelService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPinPairs", service="ansys.api.edb.v1.PinPairModelService"
                        ),
                    ],
                )
            ],
        ),
        "DeleteRlc": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRlc", service="ansys.api.edb.v1.PinPairModelService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPinPairs", service="ansys.api.edb.v1.PinPairModelService"
                        ),
                    ],
                )
            ],
        ),
        "GetPinPairs": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.PointDataService": {
        "Rotate": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "ClosestPoint": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "Distance": _RpcInfo(cache=True, read_no_buffer_flush=True),
    },
    "ansys.api.edb.v1.PointTerminalService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.TerminalService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters", service="ansys.api.edb.v1.PointTerminalService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PolygonService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetPolygonData": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPolygonData": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPolygonData", service="ansys.api.edb.v1.PolygonService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PolygonDataService": {
        "GetNormalizedPoints": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "IsCircle": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "IsBox": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "HasSelfIntersections": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "RemoveSelfIntersections": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "IsConvex": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetArea": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "Transform": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetBBox": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetStreamedBBox": _RpcInfo(read_no_buffer_flush=True, read_no_cache=True),
        "GetConvexHull": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "RemoveArcs": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "Defeature": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetBoundingCircle": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "IsInside": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "CircleIntersectsPolygon": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetIntersectionType": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetClosestPoints": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetUnion": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "GetIntersection": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "Subtract": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "Xor": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "Expand": _RpcInfo(cache=True, read_no_buffer_flush=True),
        "Get2DAlphaShape": _RpcInfo(cache=True, read_no_buffer_flush=True),
    },
    "ansys.api.edb.v1.PortPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetReferenceHeight": _RpcInfo(cache=True, invalidations=[[]]),
        "SetReferenceHeight": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetReferenceHeight", service="ansys.api.edb.v1.PortPropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetReferenceSizeAuto": _RpcInfo(cache=True, invalidations=[[]]),
        "SetReferenceSizeAuto": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetReferenceSizeAuto",
                            service="ansys.api.edb.v1.PortPropertyService",
                        )
                    ],
                )
            ],
        ),
        "GetReferenceSize": _RpcInfo(cache=True, invalidations=[[]]),
        "SetReferenceSize": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetReferenceSize", service="ansys.api.edb.v1.PortPropertyService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PrimitiveService": {
        "GetPrimitiveType": _RpcInfo(cache=True, invalidations=[[]]),
        "AddVoid": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="HasVoids", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                        _InvalidationInfo(rpc="Voids", service="ansys.api.edb.v1.PrimitiveService"),
                        _InvalidationInfo(
                            rpc="StreamVoids", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                ),
                (
                    ["hole"],
                    [
                        _InvalidationInfo(
                            rpc="IsVoid", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                        _InvalidationInfo(
                            rpc="GetOwner", service="ansys.api.edb.v1.PrimitiveService"
                        ),
                    ],
                ),
            ],
        ),
        "SetHfssProp": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHfssProp", service="ansys.api.edb.v1.PrimitiveService"
                        )
                    ],
                )
            ],
        ),
        "GetLayer": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayer": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayer", service="ansys.api.edb.v1.PrimitiveService"
                        )
                    ],
                )
            ],
        ),
        "GetIsNegative": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIsNegative": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIsNegative", service="ansys.api.edb.v1.PrimitiveService"
                        )
                    ],
                )
            ],
        ),
        "IsVoid": _RpcInfo(cache=True, invalidations=[[]]),
        "HasVoids": _RpcInfo(cache=True, invalidations=[[]]),
        "Voids": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamVoids": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "GetOwner": _RpcInfo(cache=True, invalidations=[[]]),
        "IsParameterized": _RpcInfo(cache=True, invalidations=[[]]),
        "GetHfssProp": _RpcInfo(cache=True, invalidations=[[]]),
        "RemoveHfssProp": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetHfssProp", service="ansys.api.edb.v1.PrimitiveService"
                        )
                    ],
                )
            ],
        ),
        "IsZonePrimitive": _RpcInfo(cache=True, invalidations=[[]]),
        "MakeZonePrimitive": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="IsZonePrimitive", service="ansys.api.edb.v1.PrimitiveService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetZonePrimitives", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamZonePrimitives", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
            ],
        ),
    },
    "ansys.api.edb.v1.PrimitiveInstanceCollectionService": {
        "Create": _RpcInfo(
            write_no_buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                    ],
                )
            ],
        ),
        "GetGeometry": _RpcInfo(cache=True, invalidations=[[]]),
        "SetGeometry": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetGeometry",
                            service="ansys.api.edb.v1.PrimitiveInstanceCollectionService",
                        ),
                        _InvalidationInfo(
                            rpc="GetInstantiatedGeometry",
                            service="ansys.api.edb.v1.PrimitiveInstanceCollectionService",
                        ),
                    ],
                )
            ],
        ),
        "GetPositions": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "SetPositions": _RpcInfo(
            write_no_buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetPositions",
                            service="ansys.api.edb.v1.PrimitiveInstanceCollectionService",
                        ),
                        _InvalidationInfo(
                            rpc="GetInstantiatedGeometry",
                            service="ansys.api.edb.v1.PrimitiveInstanceCollectionService",
                        ),
                    ],
                )
            ],
        ),
        "GetInstantiatedGeometry": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "Decompose": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Q3DGeneralSettingsService": {
        "GetSolutionFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolutionFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolutionFrequency",
                            service="ansys.api.edb.v1.Q3DGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDoDC": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDoDC": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDoDC", service="ansys.api.edb.v1.Q3DGeneralSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetDoDCResOnly": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDoDCResOnly": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDoDCResOnly",
                            service="ansys.api.edb.v1.Q3DGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDoCG": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDoCG": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDoCG", service="ansys.api.edb.v1.Q3DGeneralSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetDoAC": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDoAC": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDoAC", service="ansys.api.edb.v1.Q3DGeneralSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetSaveFields": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSaveFields": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSaveFields",
                            service="ansys.api.edb.v1.Q3DGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Q3DSettingsService": {
        "GetMaxPasses": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetMaxPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["q3d_settings", "target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxPasses", service="ansys.api.edb.v1.Q3DSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetMinPasses": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetMinPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["q3d_settings", "target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinPasses", service="ansys.api.edb.v1.Q3DSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetMinConvergedPasses": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetMinConvergedPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["q3d_settings", "target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinConvergedPasses",
                            service="ansys.api.edb.v1.Q3DSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPercentError": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetPercentError": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["q3d_settings", "target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPercentError", service="ansys.api.edb.v1.Q3DSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetMaxRefinePerPass": _RpcInfo(cache=True, invalidations=[["target"]]),
        "SetMaxRefinePerPass": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["q3d_settings", "target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxRefinePerPass", service="ansys.api.edb.v1.Q3DSettingsService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Q3DDCRLSettingsService": {
        "GetSolutionOrder": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolutionOrder": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolutionOrder",
                            service="ansys.api.edb.v1.Q3DDCRLSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Q3DCGSettingsService": {
        "GetAutoIncrSolOrder": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAutoIncrSolOrder": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAutoIncrSolOrder",
                            service="ansys.api.edb.v1.Q3DCGSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSolutionOrder": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolutionOrder": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolutionOrder", service="ansys.api.edb.v1.Q3DCGSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetSolverType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSolverType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSolverType", service="ansys.api.edb.v1.Q3DCGSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetCompressionTol": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCompressionTol": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCompressionTol", service="ansys.api.edb.v1.Q3DCGSettingsService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Q3DAdvancedSettingsService": {
        "GetICModeAutoResolution": _RpcInfo(cache=True, invalidations=[[]]),
        "SetICModeAutoResolution": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetICModeAutoResolution",
                            service="ansys.api.edb.v1.Q3DAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetICModeLength": _RpcInfo(cache=True, invalidations=[[]]),
        "SetICModeLength": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetICModeLength",
                            service="ansys.api.edb.v1.Q3DAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.Q3DAdvancedMeshingSettingsService": {
        "GetLayerAlignment": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayerAlignment": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLayerAlignment",
                            service="ansys.api.edb.v1.Q3DAdvancedMeshingSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.RaptorXGeneralSettingsService": {
        "GetUseGoldEMSolver": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseGoldEMSolver": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseGoldEMSolver",
                            service="ansys.api.edb.v1.RaptorXGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMaxFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxFrequency",
                            service="ansys.api.edb.v1.RaptorXGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetGlobalTemperature": _RpcInfo(cache=True, invalidations=[[]]),
        "SetGlobalTemperature": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetGlobalTemperature",
                            service="ansys.api.edb.v1.RaptorXGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSaveNetlist": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSaveNetlist": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSaveNetlist",
                            service="ansys.api.edb.v1.RaptorXGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetNetlistExportSpectre": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNetlistExportSpectre": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNetlistExportSpectre",
                            service="ansys.api.edb.v1.RaptorXGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSaveRFM": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSaveRFM": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSaveRFM",
                            service="ansys.api.edb.v1.RaptorXGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.RaptorXAdvancedSettingsService": {
        "GetUseMeshFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseMeshFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseMeshFrequency",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMeshFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshFrequency",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseEdgeMesh": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseEdgeMesh": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseEdgeMesh",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetEdgeMesh": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEdgeMesh": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEdgeMesh",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseCellsPerWavelength": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseCellsPerWavelength": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseCellsPerWavelength",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetCellsPerWavelength": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCellsPerWavelength": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCellsPerWavelength",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUsePlaneProjectionFactor": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUsePlaneProjectionFactor": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUsePlaneProjectionFactor",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPlaneProjectionFactor": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPlaneProjectionFactor": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPlaneProjectionFactor",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseRelaxedZAxis": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseRelaxedZAxis": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseRelaxedZAxis",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseEliminateSlitPerHoles": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseEliminateSlitPerHoles": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseEliminateSlitPerHoles",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetEliminateSlitPerHoles": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEliminateSlitPerHoles": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEliminateSlitPerHoles",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseAutoRemovalSliverPoly": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseAutoRemovalSliverPoly": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseAutoRemovalSliverPoly",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetAutoRemovalSliverPoly": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAutoRemovalSliverPoly": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAutoRemovalSliverPoly",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseAccelerateViaExtraction": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseAccelerateViaExtraction": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseAccelerateViaExtraction",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseEnableSubstrateNetworkExtraction": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseEnableSubstrateNetworkExtraction": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseEnableSubstrateNetworkExtraction",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseLDE": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseLDE": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseLDE",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseExtractFloatingMetalsDummy": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseExtractFloatingMetalsDummy": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseExtractFloatingMetalsDummy",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseExtractFloatingMetalsFloating": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseExtractFloatingMetalsFloating": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseExtractFloatingMetalsFloating",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseEnableEtchTransform": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseEnableEtchTransform": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseEnableEtchTransform",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseEnableHybridExtraction": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseEnableHybridExtraction": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseEnableHybridExtraction",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseEnableAdvancedCapEffects": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseEnableAdvancedCapEffects": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseEnableAdvancedCapEffects",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseOverrideShrinkFac": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseOverrideShrinkFac": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseOverrideShrinkFac",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetOverrideShrinkFac": _RpcInfo(cache=True, invalidations=[[]]),
        "SetOverrideShrinkFac": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetOverrideShrinkFac",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetAdvancedOptions": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAdvancedOptions": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAdvancedOptions",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetNetSettingsOptions": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNetSettingsOptions": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNetSettingsOptions",
                            service="ansys.api.edb.v1.RaptorXAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.RectangleService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetParameters": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParameters": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetParameters", service="ansys.api.edb.v1.RectangleService"
                        ),
                        _InvalidationInfo(
                            rpc="GetPolygonData", service="ansys.api.edb.v1.RectangleService"
                        ),
                    ],
                )
            ],
        ),
        "Render": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPolygonData": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.RLCComponentPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetEnabled": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEnabled": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEnabled", service="ansys.api.edb.v1.RLCComponentPropertyService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.RTreeService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetExtent": _RpcInfo(cache=True, invalidations=[[]]),
        "InsertIntObject": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(rpc="GetExtent", service="ansys.api.edb.v1.RTreeService"),
                        _InvalidationInfo(rpc="Empty", service="ansys.api.edb.v1.RTreeService"),
                        _InvalidationInfo(rpc="Search", service="ansys.api.edb.v1.RTreeService"),
                        _InvalidationInfo(
                            rpc="NearestNeighbor", service="ansys.api.edb.v1.RTreeService"
                        ),
                        _InvalidationInfo(
                            rpc="TouchingGeometry", service="ansys.api.edb.v1.RTreeService"
                        ),
                        _InvalidationInfo(
                            rpc="ConnectedGeometry", service="ansys.api.edb.v1.RTreeService"
                        ),
                        _InvalidationInfo(
                            rpc="GetConnectedGeometrySets", service="ansys.api.edb.v1.RTreeService"
                        ),
                    ],
                )
            ],
        ),
        "DeleteIntObject": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(rpc="GetExtent", service="ansys.api.edb.v1.RTreeService"),
                        _InvalidationInfo(rpc="Empty", service="ansys.api.edb.v1.RTreeService"),
                        _InvalidationInfo(rpc="Search", service="ansys.api.edb.v1.RTreeService"),
                        _InvalidationInfo(
                            rpc="NearestNeighbor", service="ansys.api.edb.v1.RTreeService"
                        ),
                        _InvalidationInfo(
                            rpc="TouchingGeometry", service="ansys.api.edb.v1.RTreeService"
                        ),
                        _InvalidationInfo(
                            rpc="ConnectedGeometry", service="ansys.api.edb.v1.RTreeService"
                        ),
                        _InvalidationInfo(
                            rpc="GetConnectedGeometrySets", service="ansys.api.edb.v1.RTreeService"
                        ),
                    ],
                )
            ],
        ),
        "Empty": _RpcInfo(cache=True, invalidations=[[]]),
        "Search": _RpcInfo(cache=True, invalidations=[["target"]]),
        "NearestNeighbor": _RpcInfo(cache=True, invalidations=[["target"]]),
        "TouchingGeometry": _RpcInfo(cache=True, invalidations=[["target"]]),
        "ConnectedGeometry": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetConnectedGeometrySets": _RpcInfo(cache=True, invalidations=[[]]),
        "IncrementVisit": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="GetVisit", service="ansys.api.edb.v1.RTreeService")],
                )
            ],
        ),
        "IsVisited": _RpcInfo(cache=True, invalidations=[["target"]]),
        "Visit": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="IsVisited", service="ansys.api.edb.v1.RTreeService")],
                )
            ],
        ),
        "GetVisit": _RpcInfo(cache=True, invalidations=[["target"]]),
    },
    "ansys.api.edb.v1.SimulationSettingsService": {
        "GetEnabled": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEnabled": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEnabled", service="ansys.api.edb.v1.SimulationSettingsService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SettingsOptionsService": {
        "GetDoLamdaRefineFlag": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDoLamdaRefineFlag": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDoLamdaRefineFlag",
                            service="ansys.api.edb.v1.SettingsOptionsService",
                        )
                    ],
                )
            ],
        ),
        "GetLamdaTarget": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLamdaTarget": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLamdaTarget", service="ansys.api.edb.v1.SettingsOptionsService"
                        )
                    ],
                )
            ],
        ),
        "GetMeshSizefactor": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshSizefactor": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshSizefactor",
                            service="ansys.api.edb.v1.SettingsOptionsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseDefaultLamda": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseDefaultLamda": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseDefaultLamda",
                            service="ansys.api.edb.v1.SettingsOptionsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.AdvancedSettingsService": {
        "GetUnionPolygons": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUnionPolygons": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUnionPolygons",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetRemoveFloatingGeometry": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRemoveFloatingGeometry": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRemoveFloatingGeometry",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetHealingOption": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHealingOption": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHealingOption",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSmallVoidArea": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSmallVoidArea": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSmallVoidArea",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseDefeature": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseDefeature": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseDefeature",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseDefeatureAbsoluteLength": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseDefeatureAbsoluteLength": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseDefeatureAbsoluteLength",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDefeatureAbsoluteLength": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDefeatureAbsoluteLength": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDefeatureAbsoluteLength",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDefeatureRatio": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDefeatureRatio": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDefeatureRatio",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetViaModelType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetViaModelType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetViaModelType",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetNumViaSides": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNumViaSides": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNumViaSides", service="ansys.api.edb.v1.AdvancedSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetViaDensity": _RpcInfo(cache=True, invalidations=[[]]),
        "SetViaDensity": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetViaDensity", service="ansys.api.edb.v1.AdvancedSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetViaMaterial": _RpcInfo(cache=True, invalidations=[[]]),
        "SetViaMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetViaMaterial", service="ansys.api.edb.v1.AdvancedSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetMeshForViaPlating": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshForViaPlating": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshForViaPlating",
                            service="ansys.api.edb.v1.AdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetModelType": _RpcInfo(cache=True, invalidations=[[]]),
        "SetModelType": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetModelType", service="ansys.api.edb.v1.AdvancedSettingsService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.AdvancedMeshingSettingsService": {
        "GetArcStepSize": _RpcInfo(cache=True, invalidations=[[]]),
        "SetArcStepSize": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetArcStepSize",
                            service="ansys.api.edb.v1.AdvancedMeshingSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetCircleStartAzimuth": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCircleStartAzimuth": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCircleStartAzimuth",
                            service="ansys.api.edb.v1.AdvancedMeshingSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMaxNumArcPoints": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxNumArcPoints": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxNumArcPoints",
                            service="ansys.api.edb.v1.AdvancedMeshingSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseArcChordErrorApprox": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseArcChordErrorApprox": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseArcChordErrorApprox",
                            service="ansys.api.edb.v1.AdvancedMeshingSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetArcChordErrorApprox": _RpcInfo(cache=True, invalidations=[[]]),
        "SetArcChordErrorApprox": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetArcChordErrorApprox",
                            service="ansys.api.edb.v1.AdvancedMeshingSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SolverSettingsService": {
        "GetThinSignalLayerThreshold": _RpcInfo(cache=True, invalidations=[[]]),
        "SetThinSignalLayerThreshold": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetThinSignalLayerThreshold",
                            service="ansys.api.edb.v1.SolverSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetThinDielectricLayerThreshold": _RpcInfo(cache=True, invalidations=[[]]),
        "SetThinDielectricLayerThreshold": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetThinDielectricLayerThreshold",
                            service="ansys.api.edb.v1.SolverSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SimulationSetupService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["cell"],
                    [
                        _InvalidationInfo(
                            rpc="GetSimulationSetups", service="ansys.api.edb.v1.CellService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamSimulationSetups", service="ansys.api.edb.v1.CellService"
                        ),
                    ],
                )
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetName", service="ansys.api.edb.v1.SimulationSetupService"
                        )
                    ],
                )
            ],
        ),
        "GetPosition": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPosition": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPosition", service="ansys.api.edb.v1.SimulationSetupService"
                        )
                    ],
                )
            ],
        ),
        "GetSweepData": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSweepData": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSweepData", service="ansys.api.edb.v1.SimulationSetupService"
                        )
                    ],
                )
            ],
        ),
        "GetType": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService": {
        "GetIcepakTempFile": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIcepakTempFile": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIcepakTempFile",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSourceTermsToGround": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSourceTermsToGround": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSourceTermsToGround",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetExportDCThermalData": _RpcInfo(cache=True, invalidations=[[]]),
        "SetExportDCThermalData": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetExportDCThermalData",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetImportThermalData": _RpcInfo(cache=True, invalidations=[[]]),
        "SetImportThermalData": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetImportThermalData",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetFullDCReportPath": _RpcInfo(cache=True, invalidations=[[]]),
        "SetFullDCReportPath": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetFullDCReportPath",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetViaReportPath": _RpcInfo(cache=True, invalidations=[[]]),
        "SetViaReportPath": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetViaReportPath",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPerPinResPath": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPerPinResPath": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPerPinResPath",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDCReportConfigFile": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCReportConfigFile": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCReportConfigFile",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDCReportShowActiveDevices": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCReportShowActiveDevices": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCReportShowActiveDevices",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPerPinUsePinFormat": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPerPinUsePinFormat": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPerPinUsePinFormat",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseLoopResForPerPin": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseLoopResForPerPin": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseLoopResForPerPin",
                            service="ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SIWavePSIGeneralSettingsService": {
        "GetPISliderPos": _RpcInfo(cache=True),
        "SetPISliderPos": _RpcInfo(buffer=True),
        "GetSIWavePSIModelType": _RpcInfo(cache=True),
        "SetSIWavePSIModelType": _RpcInfo(buffer=True),
        "GetMinPlaneAreaToMesh": _RpcInfo(cache=True),
        "SetMinPlaneAreaToMesh": _RpcInfo(buffer=True),
        "GetMinVoidAreaToMesh": _RpcInfo(cache=True),
        "SetMinVoidAreaToMesh": _RpcInfo(buffer=True),
        "GetSnapLengthThreshold": _RpcInfo(cache=True),
        "SetSnapLengthThreshold": _RpcInfo(buffer=True),
        "GetIncludeEnhancedBondWireModeling": _RpcInfo(cache=True),
        "SetIncludeEnhancedBondWireModeling": _RpcInfo(buffer=True),
        "GetSurfaceRoughnessModel": _RpcInfo(cache=True),
        "SetSurfaceRoughnessModel": _RpcInfo(buffer=True),
        "GetRMSSurfaceRoughness": _RpcInfo(cache=True),
        "SetRMSSurfaceRoughness": _RpcInfo(buffer=True),
        "GetPerformERC": _RpcInfo(cache=True),
        "SetPerformERC": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWavePSINetProcessingSettingsService": {
        "GetAutoSelectNetsForSimulation": _RpcInfo(cache=True),
        "SetAutoSelectNetsForSimulation": _RpcInfo(buffer=True),
        "GetIgnoreDummyNetsForSelectedNets": _RpcInfo(cache=True),
        "SetIgnoreDummyNetsForSelectedNets": _RpcInfo(buffer=True),
        "GetIncludeNets": _RpcInfo(cache=True),
        "SetIncludeNets": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWavePSIPowerGroundNetsService": {
        "GetImprovedLossModel": _RpcInfo(cache=True),
        "SetImprovedLossModel": _RpcInfo(buffer=True),
        "GetAutoDetectIgnoreSmallHolesMinDiameter": _RpcInfo(cache=True),
        "SetAutoDetectIgnoreSmallHolesMinDiameter": _RpcInfo(buffer=True),
        "GetIgnoreSmallHolesMinDiameter": _RpcInfo(cache=True),
        "SetIgnoreSmallHolesMinDiameter": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWavePSISignalNetsSettingsService": {
        "GetSignalNetsErrorTolerance": _RpcInfo(cache=True),
        "SetSignalNetsErrorTolerance": _RpcInfo(buffer=True),
        "GetSignalNetsConductorModeling": _RpcInfo(cache=True),
        "SetSignalNetsConductorModeling": _RpcInfo(buffer=True),
        "GetSignalNetsIncludeImprovedLossHandling": _RpcInfo(cache=True),
        "SetSignalNetsIncludeImprovedLossHandling": _RpcInfo(buffer=True),
        "GetSignalNetsIncludeImprovedDielectricFillRefinement": _RpcInfo(cache=True),
        "SetSignalNetsIncludeImprovedDielectricFillRefinement": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWaveGeneralSettingsService": {
        "GetUseSISettings": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseSISettings": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseSISettings",
                            service="ansys.api.edb.v1.SIWaveGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetUseCustomSettings": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseCustomSettings": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseCustomSettings",
                            service="ansys.api.edb.v1.SIWaveGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSISliderPos": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSISliderPos": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSISliderPos",
                            service="ansys.api.edb.v1.SIWaveGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPISliderPos": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPISliderPos": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPISliderPos",
                            service="ansys.api.edb.v1.SIWaveGeneralSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SIWaveAdvancedSettingsService": {
        "GetIncludeCoPlaneCoupling": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIncludeCoPlaneCoupling": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIncludeCoPlaneCoupling",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIncludeInterPlaneCoupling": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIncludeInterPlaneCoupling": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIncludeInterPlaneCoupling",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIncludeSplitPlaneCoupling": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIncludeSplitPlaneCoupling": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIncludeSplitPlaneCoupling",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIncludeFringePlaneCoupling": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIncludeFringePlaneCoupling": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIncludeFringePlaneCoupling",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIncludeTracePlaneCoupling": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIncludeTracePlaneCoupling": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIncludeTracePlaneCoupling",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetCrossTalkThreshold": _RpcInfo(cache=True, invalidations=[[]]),
        "SetCrossTalkThreshold": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetCrossTalkThreshold",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMaxCoupledLines": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxCoupledLines": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxCoupledLines",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMinVoidArea": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinVoidArea": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinVoidArea",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMinPadAreaToMesh": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinPadAreaToMesh": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinPadAreaToMesh",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMinPlaneAreaToMesh": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinPlaneAreaToMesh": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinPlaneAreaToMesh",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetSnapLengthThreshold": _RpcInfo(cache=True, invalidations=[[]]),
        "SetSnapLengthThreshold": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetSnapLengthThreshold",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMeshAutomatic": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshAutomatic": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshAutomatic",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMeshFrequency": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshFrequency": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshFrequency",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetAcDcMergeMode": _RpcInfo(cache=True, invalidations=[[]]),
        "SetAcDcMergeMode": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAcDcMergeMode",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "Get3DReturnCurrentDistribution": _RpcInfo(cache=True, invalidations=[[]]),
        "Set3DReturnCurrentDistribution": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="Get3DReturnCurrentDistribution",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIncludeVISources": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIncludeVISources": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIncludeVISources",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIncludeInfGnd": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIncludeInfGnd": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIncludeInfGnd",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetInfGndLocation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetInfGndLocation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetInfGndLocation",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPerformERC": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPerformERC": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPerformERC",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetIgnoreNonFunctionalPads": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIgnoreNonFunctionalPads": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetIgnoreNonFunctionalPads",
                            service="ansys.api.edb.v1.SIWaveAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SIWaveDCSettingsService": {
        "GetUseDCCustomSettings": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseDCCustomSettings": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseDCCustomSettings",
                            service="ansys.api.edb.v1.SIWaveDCSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetComputeInductance": _RpcInfo(cache=True, invalidations=[[]]),
        "SetComputeInductance": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetComputeInductance",
                            service="ansys.api.edb.v1.SIWaveDCSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPlotJV": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPlotJV": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPlotJV", service="ansys.api.edb.v1.SIWaveDCSettingsService"
                        )
                    ],
                )
            ],
        ),
        "GetContactRadius": _RpcInfo(cache=True, invalidations=[[]]),
        "SetContactRadius": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetContactRadius",
                            service="ansys.api.edb.v1.SIWaveDCSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDCSliderPos": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCSliderPos": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCSliderPos", service="ansys.api.edb.v1.SIWaveDCSettingsService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SIWaveDCAdvancedSettingsService": {
        "GetDCMinPlaneAreaToMesh": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCMinPlaneAreaToMesh": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCMinPlaneAreaToMesh",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDCMinVoidAreaToMesh": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCMinVoidAreaToMesh": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCMinVoidAreaToMesh",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMaxInitMeshEdgeLength": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxInitMeshEdgeLength": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxInitMeshEdgeLength",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPerformAdaptiveRefinement": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPerformAdaptiveRefinement": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPerformAdaptiveRefinement",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMaxNumPasses": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaxNumPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaxNumPasses",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMinNumPasses": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMinNumPasses": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMinNumPasses",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetPercentLocalRefinement": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPercentLocalRefinement": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPercentLocalRefinement",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetEnergyError": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEnergyError": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetEnergyError",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMeshBws": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshBws": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshBws",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetRefineBws": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRefineBws": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRefineBws",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetMeshVias": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshVias": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshVias",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetRefineVias": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRefineVias": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRefineVias",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetNumBwSides": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNumBwSides": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNumBwSides",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetNumViaSides": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNumViaSides": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNumViaSides",
                            service="ansys.api.edb.v1.SIWaveDCAdvancedSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SIWaveSParameterSettingsService": {
        "GetUseStateSpace": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseStateSpace": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseStateSpace",
                            service="ansys.api.edb.v1.SIWaveSParameterSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetInterpolation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetInterpolation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetInterpolation",
                            service="ansys.api.edb.v1.SIWaveSParameterSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetExtrapolation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetExtrapolation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetExtrapolation",
                            service="ansys.api.edb.v1.SIWaveSParameterSettingsService",
                        )
                    ],
                )
            ],
        ),
        "GetDCBehavior": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDCBehavior": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDCBehavior",
                            service="ansys.api.edb.v1.SIWaveSParameterSettingsService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SolderBallPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetShape": _RpcInfo(cache=True, invalidations=[[]]),
        "SetShape": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetShape", service="ansys.api.edb.v1.SolderBallPropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetPlacement": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPlacement": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPlacement", service="ansys.api.edb.v1.SolderBallPropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetDiameter": _RpcInfo(cache=True, invalidations=[[]]),
        "SetDiameter": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetDiameter", service="ansys.api.edb.v1.SolderBallPropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetHeight": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHeight": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetHeight", service="ansys.api.edb.v1.SolderBallPropertyService"
                        )
                    ],
                )
            ],
        ),
        "GetMaterialName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaterialName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaterialName",
                            service="ansys.api.edb.v1.SolderBallPropertyService",
                        )
                    ],
                )
            ],
        ),
        "UsesSolderball": _RpcInfo(cache=True, invalidations=[[]]),
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
    },
    "ansys.api.edb.v1.SpiceModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetProperties": _RpcInfo(cache=True, invalidations=[[]]),
        "SetModelPath": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetProperties", service="ansys.api.edb.v1.SpiceModelService"
                        )
                    ],
                )
            ],
        ),
        "SetModelName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetProperties", service="ansys.api.edb.v1.SpiceModelService"
                        )
                    ],
                )
            ],
        ),
        "SetSubCkt": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetProperties", service="ansys.api.edb.v1.SpiceModelService"
                        )
                    ],
                )
            ],
        ),
        "AddTerminalPinPair": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetTerminalPinPairs", service="ansys.api.edb.v1.SpiceModelService"
                        )
                    ],
                )
            ],
        ),
        "RemoveTerminalPinPair": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetTerminalPinPairs", service="ansys.api.edb.v1.SpiceModelService"
                        )
                    ],
                )
            ],
        ),
        "GetTerminalPinPairs": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.StackupLayerService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetNegative": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNegative": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetNegative", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                )
            ],
        ),
        "GetThickness": _RpcInfo(cache=True, invalidations=[[]]),
        "SetThickness": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetThickness", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetTopBottomStackupLayers",
                            service="ansys.api.edb.v1.LayerCollectionService",
                        )
                    ],
                ),
            ],
        ),
        "GetLowerElevation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLowerElevation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetLowerElevation", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetTopBottomStackupLayers",
                            service="ansys.api.edb.v1.LayerCollectionService",
                        )
                    ],
                ),
            ],
        ),
        "GetUpperElevation": _RpcInfo(cache=True, invalidations=[[]]),
        "GetMaterial": _RpcInfo(cache=True, invalidations=[["layer"]]),
        "SetMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaterial", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                )
            ],
        ),
        "GetFillMaterial": _RpcInfo(cache=True, invalidations=[["layer"]]),
        "SetFillMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetFillMaterial", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                )
            ],
        ),
        "SetRoughnessEnabled": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="IsRoughnessEnabled", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                )
            ],
        ),
        "IsRoughnessEnabled": _RpcInfo(cache=True, invalidations=[[]]),
        "GetRoughnessModel": _RpcInfo(cache=True, invalidations=[["layer"]]),
        "SetRoughnessModel": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer_rough_region", "layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetRoughnessModel", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                )
            ],
        ),
        "IsEtchFactorEnabled": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEtchFactorEnabled": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="IsEtchFactorEnabled",
                            service="ansys.api.edb.v1.StackupLayerService",
                        )
                    ],
                )
            ],
        ),
        "SetEtchFactor": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetEtchFactor", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                )
            ],
        ),
        "GetEtchFactor": _RpcInfo(cache=True, invalidations=[[]]),
        "SetEtchNetClass": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetEtchNetClass", service="ansys.api.edb.v1.StackupLayerService"
                        )
                    ],
                )
            ],
        ),
        "GetEtchNetClass": _RpcInfo(cache=True, invalidations=[[]]),
        "GetUseSolverProperties": _RpcInfo(cache=True, invalidations=[[]]),
        "SetUseSolverProperties": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetUseSolverProperties",
                            service="ansys.api.edb.v1.StackupLayerService",
                        )
                    ],
                )
            ],
        ),
        "GetHFSSSolverProperties": _RpcInfo(cache=True, invalidations=[[]]),
        "SetHFSSSolverProperties": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["layer"],
                    [
                        _InvalidationInfo(
                            rpc="GetHFSSSolverProperties",
                            service="ansys.api.edb.v1.StackupLayerService",
                        )
                    ],
                )
            ],
        ),
        "GetReferencingViaLayerIds": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.Structure3DService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetMaterial": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMaterial": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMaterial", service="ansys.api.edb.v1.Structure3DService"
                        )
                    ],
                )
            ],
        ),
        "GetThickness": _RpcInfo(cache=True, invalidations=[[]]),
        "SetThickness": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetThickness", service="ansys.api.edb.v1.Structure3DService"
                        )
                    ],
                )
            ],
        ),
        "GetMeshClosureProp": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMeshClosureProp": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMeshClosureProp", service="ansys.api.edb.v1.Structure3DService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.SParameterModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetProperties": _RpcInfo(cache=True, invalidations=[[]]),
        "SetComponentModelName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetProperties", service="ansys.api.edb.v1.SParameterModelService"
                        )
                    ],
                )
            ],
        ),
        "SetReferenceNet": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetProperties", service="ansys.api.edb.v1.SParameterModelService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.TechnologyDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "FindByName": _RpcInfo(cache=True),
        "Delete": _RpcInfo(buffer=True),
        "GetTechFile": _RpcInfo(cache=True),
        "GetGFDFile": _RpcInfo(cache=True),
        "GetLayerFile": _RpcInfo(cache=True),
        "GetName": _RpcInfo(cache=True),
        "GetIsCreateBackplane": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.TerminalService": {
        "FindByName": _RpcInfo(buffer=True, returns_future=True, invalidations=[["layout"]]),
        "GetParams": _RpcInfo(cache=True, invalidations=[[]]),
        "SetParams": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetParams", service="ansys.api.edb.v1.TerminalService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
            ],
        ),
        "GetProductSolvers": _RpcInfo(cache=True, invalidations=[[]]),
        "SetProductSolverOptions": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetProductSolvers", service="ansys.api.edb.v1.TerminalService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.TerminalInstanceService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        )
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
                (
                    ["cell_inst"],
                    [
                        _InvalidationInfo(
                            rpc="GetTermInsts", service="ansys.api.edb.v1.CellInstanceService"
                        )
                    ],
                ),
            ],
        ),
        "GetOwningCellInstance": _RpcInfo(cache=True, invalidations=[[]]),
        "GetDefinitionTerminal": _RpcInfo(cache=True, invalidations=[[]]),
        "GetDefinitionTerminalName": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.TerminalInstanceTerminalService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.TerminalService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        ),
                    ],
                ),
            ],
        ),
        "GetTerminalInstance": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTerminalInstance": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["term"],
                    [
                        _InvalidationInfo(
                            rpc="GetTerminalInstance",
                            service="ansys.api.edb.v1.TerminalInstanceTerminalService",
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.TextService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                ),
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="StreamLayoutObjects", service="ansys.api.edb.v1.NetService"
                        )
                    ],
                ),
            ],
        ),
        "GetTextData": _RpcInfo(cache=True, invalidations=[[]]),
        "SetTextData": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="GetTextData", service="ansys.api.edb.v1.TextService")],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.TransformService": {
        "Rotate": _RpcInfo(cache=True, invalidations=[[]]),
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetScale": _RpcInfo(cache=True, invalidations=[[]]),
        "SetScale": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetScale", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPolygon", service="ansys.api.edb.v1.TransformService"
                        ),
                    ],
                )
            ],
        ),
        "GetMirror": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMirror": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetMirror", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPolygon", service="ansys.api.edb.v1.TransformService"
                        ),
                    ],
                )
            ],
        ),
        "GetRotation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRotation": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetRotation", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPolygon", service="ansys.api.edb.v1.TransformService"
                        ),
                    ],
                )
            ],
        ),
        "GetOffsetX": _RpcInfo(cache=True, invalidations=[[]]),
        "SetOffsetX": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetOffsetX", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPolygon", service="ansys.api.edb.v1.TransformService"
                        ),
                    ],
                )
            ],
        ),
        "GetOffsetY": _RpcInfo(cache=True, invalidations=[[]]),
        "SetOffsetY": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetOffsetY", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.TransformService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPolygon", service="ansys.api.edb.v1.TransformService"
                        ),
                    ],
                )
            ],
        ),
        "TransformPlus": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "IsIdentity": _RpcInfo(cache=True, invalidations=[[]]),
        "TransformPoint": _RpcInfo(cache=True, invalidations=[["target"]]),
        "TransformPolygon": _RpcInfo(cache=True, invalidations=[["target"]]),
    },
    "ansys.api.edb.v1.Transform3DService": {
        "CreateIdentity": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateCopy": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "CreateOffset": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateCenterScale": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateRotationFromAngle": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateRotationFromAxis": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateRotationFromAxisAndAngle": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateRotationFromToAxis": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateTransform2D": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "OperatorPlus": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "TransformPoint": _RpcInfo(cache=True, invalidations=[[]]),
        "GetZYXRotation": _RpcInfo(cache=True, invalidations=[[]]),
        "GetAxis": _RpcInfo(cache=True, invalidations=[[]]),
        "Transpose": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetAxis", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetZYXRotation", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="IsEqual", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetScaling", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetShift", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetMatrix", service="ansys.api.edb.v1.Transform3DService"
                        ),
                    ],
                )
            ],
        ),
        "Invert": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetAxis", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetZYXRotation", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="IsEqual", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetScaling", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetShift", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetMatrix", service="ansys.api.edb.v1.Transform3DService"
                        ),
                    ],
                )
            ],
        ),
        "IsIdentity": _RpcInfo(cache=True, invalidations=[["target"]]),
        "IsEqual": _RpcInfo(cache=True, invalidations=[["target"], ["value"]]),
        "GetScaling": _RpcInfo(cache=True, invalidations=[[]]),
        "GetShift": _RpcInfo(cache=True, invalidations=[[]]),
        "SetMatrix": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetAxis", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetZYXRotation", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="IsIdentity", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="TransformPoint", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="IsEqual", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetScaling", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetShift", service="ansys.api.edb.v1.Transform3DService"
                        ),
                        _InvalidationInfo(
                            rpc="GetMatrix", service="ansys.api.edb.v1.Transform3DService"
                        ),
                    ],
                )
            ],
        ),
        "GetMatrix": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.ValueService": {
        "CreateValue": _RpcInfo(write_no_cache_invalidation=True),
        "GetDouble": _RpcInfo(cache=True),
        "GetComplex": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.VariableServerService": {
        "AddVariable": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["variable_owner"],
                    [
                        _InvalidationInfo(
                            rpc="GetAllVariableNames",
                            service="ansys.api.edb.v1.VariableServerService",
                        ),
                        _InvalidationInfo(
                            rpc="GetVariableValue", service="ansys.api.edb.v1.VariableServerService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameter", service="ansys.api.edb.v1.VariableServerService"
                        ),
                    ],
                )
            ],
        ),
        "AddMenuVariable": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["variable_owner"],
                    [
                        _InvalidationInfo(
                            rpc="GetAllVariableNames",
                            service="ansys.api.edb.v1.VariableServerService",
                        ),
                        _InvalidationInfo(
                            rpc="GetVariableValue", service="ansys.api.edb.v1.VariableServerService"
                        ),
                        _InvalidationInfo(
                            rpc="IsParameter", service="ansys.api.edb.v1.VariableServerService"
                        ),
                    ],
                )
            ],
        ),
        "DeleteVariable": _RpcInfo(buffer=True),
        "SetVariableValue": _RpcInfo(buffer=True),
        "GetVariableValue": _RpcInfo(cache=True, invalidations=[["variable_owner"]]),
        "IsParameter": _RpcInfo(cache=True, invalidations=[["variable_owner"]]),
        "GetAllVariableNames": _RpcInfo(cache=True, invalidations=[[]]),
        "GetVariableDesc": _RpcInfo(cache=True, invalidations=[["variable_owner"]]),
        "SetVariableDesc": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["variable_owner"],
                    [
                        _InvalidationInfo(
                            rpc="GetVariableDesc", service="ansys.api.edb.v1.VariableServerService"
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.ViaGroupService": {
        "CreateWithOutline": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="FindByName", service="ansys.api.edb.v1.ViaGroupService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetOutline": _RpcInfo(cache=True, invalidations=[[]]),
        "GetConductorPercentage": _RpcInfo(cache=True, invalidations=[[]]),
        "IsPersistent": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.ViaLayerService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetRefLayerName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRefLayer": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    None,
                    [
                        _InvalidationInfo(
                            rpc="GetReferencingViaLayerIds",
                            service="ansys.api.edb.v1.StackupLayerService",
                        )
                    ],
                )
            ],
        ),
        "GetIsTSV": _RpcInfo(cache=True),
        "SetIsTSV": _RpcInfo(buffer=True),
        "AddOxideLayers": _RpcInfo(buffer=True),
        "RemoveOxideLayers": _RpcInfo(buffer=True),
        "GetNumOxideLayers": _RpcInfo(cache=True),
        "GetOxideLayers": _RpcInfo(cache=True),
        "SetOxideLayerData": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.VoltageRegulatorService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["layout"],
                    [
                        _InvalidationInfo(
                            rpc="FindByIdAndType", service="ansys.api.edb.v1.ConnectableService"
                        ),
                        _InvalidationInfo(
                            rpc="StreamItems", service="ansys.api.edb.v1.LayoutService"
                        ),
                    ],
                )
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetName", service="ansys.api.edb.v1.VoltageRegulatorService"
                        )
                    ],
                )
            ],
        ),
        "IsActive": _RpcInfo(cache=True, invalidations=[[]]),
        "SetIsActive": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="IsActive", service="ansys.api.edb.v1.VoltageRegulatorService"
                        )
                    ],
                )
            ],
        ),
        "GetVoltage": _RpcInfo(cache=True, invalidations=[[]]),
        "SetVoltage": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetVoltage", service="ansys.api.edb.v1.VoltageRegulatorService"
                        )
                    ],
                )
            ],
        ),
        "GetLoadRegulationCurrent": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLoadRegulationCurrent": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLoadRegulationCurrent",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        )
                    ],
                )
            ],
        ),
        "GetLoadRegulationPercent": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLoadRegulationPercent": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetLoadRegulationPercent",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        )
                    ],
                )
            ],
        ),
        "GetPosRemoteSensePin": _RpcInfo(cache=True, invalidations=[[]]),
        "SetPosRemoteSensePin": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetPosRemoteSensePin",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        )
                    ],
                )
            ],
        ),
        "GetNegRemoteSensePin": _RpcInfo(cache=True, invalidations=[[]]),
        "SetNegRemoteSensePin": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetNegRemoteSensePin",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        )
                    ],
                )
            ],
        ),
        "GetNPowerModules": _RpcInfo(cache=True, invalidations=[[]]),
        "GetNActivePowerModules": _RpcInfo(cache=True, invalidations=[[]]),
        "GetPowerModule": _RpcInfo(cache=True, invalidations=[[]]),
        "GetAllPowerModules": _RpcInfo(cache=True, invalidations=[[]]),
        "AddPowerModule": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["vrm"],
                    [
                        _InvalidationInfo(
                            rpc="GetAllPowerModules",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        ),
                        _InvalidationInfo(
                            rpc="GetPowerModule", service="ansys.api.edb.v1.VoltageRegulatorService"
                        ),
                    ],
                )
            ],
        ),
        "RemovePowerModule": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="GetAllPowerModules",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        ),
                        _InvalidationInfo(
                            rpc="GetPowerModule", service="ansys.api.edb.v1.VoltageRegulatorService"
                        ),
                    ],
                )
            ],
        ),
        "AddPowerModules": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["vrm"],
                    [
                        _InvalidationInfo(
                            rpc="GetAllPowerModules",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        ),
                        _InvalidationInfo(
                            rpc="GetPowerModule", service="ansys.api.edb.v1.VoltageRegulatorService"
                        ),
                    ],
                )
            ],
        ),
        "RemovePowerModules": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["edb_obj"],
                    [
                        _InvalidationInfo(
                            rpc="GetAllPowerModules",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        ),
                        _InvalidationInfo(
                            rpc="GetPowerModule", service="ansys.api.edb.v1.VoltageRegulatorService"
                        ),
                    ],
                )
            ],
        ),
        "RemoveAllPowerModules": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    [],
                    [
                        _InvalidationInfo(
                            rpc="GetAllPowerModules",
                            service="ansys.api.edb.v1.VoltageRegulatorService",
                        ),
                        _InvalidationInfo(
                            rpc="GetPowerModule", service="ansys.api.edb.v1.VoltageRegulatorService"
                        ),
                    ],
                )
            ],
        ),
    },
}
