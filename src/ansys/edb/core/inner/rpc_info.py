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


rpc_information = {
    "ansys.api.edb.v1.ArcDataService": {
        "GetHeight": _RpcInfo(cache=True),
        "GetCenter": _RpcInfo(cache=True),
        "GetMidpoint": _RpcInfo(cache=True),
        "GetRadius": _RpcInfo(cache=True),
        "GetBoundingBox": _RpcInfo(cache=True),
        "GetAngle": _RpcInfo(cache=True),
        "ClosestPoints": _RpcInfo(cache=True),
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
                        )
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
                        )
                    ],
                )
            ],
        ),
        "GetDefinitionName": _RpcInfo(cache=True, invalidations=[[]]),
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
                    [_InvalidationInfo(rpc="GetTraj", service="ansys.api.edb.v1.BondwireService")],
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
                        )
                    ],
                )
            ],
        ),
    },
    "ansys.api.edb.v1.BondwireDefService": {
        "Delete": _RpcInfo(buffer=True),
        "GetName": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.ApdBondwireDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "FindByName": _RpcInfo(cache=True),
        "GetParameters": _RpcInfo(cache=True),
        "SetParameters": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Jedec4BondwireDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "FindByName": _RpcInfo(cache=True),
        "GetParameters": _RpcInfo(cache=True),
        "SetParameters": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Jedec5BondwireDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "FindByName": _RpcInfo(cache=True),
        "GetParameters": _RpcInfo(cache=True),
        "SetParameters": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.BundleTerminalService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "Ungroup": _RpcInfo(buffer=True),
        "GetTerminals": _RpcInfo(read_no_cache=True),
        "StreamTerminals": _RpcInfo(read_no_cache=True),
    },
    "ansys.api.edb.v1.CellService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["database"],
                    [_InvalidationInfo(rpc="Find", service="ansys.api.edb.v1.CellService")],
                )
            ],
        ),
        "GetLayout": _RpcInfo(cache=True, invalidations=[[]]),
        "Find": _RpcInfo(cache=True, invalidations=[["database"]]),
        "Delete": _RpcInfo(buffer=True),
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
        "SetName": _RpcInfo(buffer=True),
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
                        )
                    ],
                )
            ],
        ),
        "GetSimulationSetups": _RpcInfo(read_no_cache=True),
        "StreamSimulationSetups": _RpcInfo(read_no_cache=True),
        "GenerateAutoHFSSRegions": _RpcInfo(buffer=True),
        "GenerateViaSmartBox": _RpcInfo(cache=True),
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
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetReferenceLayout": _RpcInfo(cache=True, invalidations=[[]]),
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
                        )
                    ],
                )
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
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "FindByName": _RpcInfo(cache=True),
        "SetName": _RpcInfo(buffer=True),
        "GetName": _RpcInfo(cache=True),
        "SetFootprintCell": _RpcInfo(buffer=True),
        "GetFootprintCell": _RpcInfo(cache=True),
        "GetComponentModels": _RpcInfo(read_no_cache=True),
        "StreamComponentModels": _RpcInfo(read_no_cache=True),
        "GetComponentPins": _RpcInfo(read_no_cache=True),
        "StreamComponentPins": _RpcInfo(read_no_cache=True),
        "AddComponentModel": _RpcInfo(buffer=True),
        "RemoveComponentModel": _RpcInfo(buffer=True),
        "ReorderPins": _RpcInfo(buffer=True),
        "RemovePin": _RpcInfo(buffer=True),
        "GetProductProperty": _RpcInfo(cache=True),
        "SetProductProperty": _RpcInfo(buffer=True),
        "GetProductPropertyIds": _RpcInfo(cache=True),
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
        "FindByDef": _RpcInfo(cache=True, invalidations=[["target"]]),
    },
    "ansys.api.edb.v1.ComponentModelService": {
        "SetReferenceFile": _RpcInfo(buffer=True),
        "GetReferenceFile": _RpcInfo(cache=True),
        "FindByName": _RpcInfo(cache=True),
        "FindById": _RpcInfo(cache=True),
        "GetName": _RpcInfo(cache=True),
        "GetType": _RpcInfo(cache=True),
        "GetId": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.NPortComponentModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True)
    },
    "ansys.api.edb.v1.DynamicLinkComponentModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "SetDesignName": _RpcInfo(buffer=True),
        "GetDesignName": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.ComponentPinService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "FindByName": _RpcInfo(cache=True),
        "SetName": _RpcInfo(buffer=True),
        "GetName": _RpcInfo(cache=True),
        "GetNumber": _RpcInfo(cache=True),
        "GetComponentDef": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.ComponentPropertyService": {
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetPackageMountingOffset": _RpcInfo(cache=True),
        "SetPackageMountingOffset": _RpcInfo(buffer=True),
        "GetPackageDef": _RpcInfo(cache=True),
        "SetPackageDef": _RpcInfo(buffer=True),
        "GetModel": _RpcInfo(cache=True),
        "SetModel": _RpcInfo(buffer=True),
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
        "IsReadOnly": _RpcInfo(cache=True),
        "GetTopCircuits": _RpcInfo(cache=True),
        "GetId": _RpcInfo(cache=True),
        "FindById": _RpcInfo(cache=True),
        "GetVersionByRelease": _RpcInfo(cache=True),
        "GetDirectory": _RpcInfo(cache=True),
        "GetProductProperty": _RpcInfo(cache=True),
        "SetProductProperty": _RpcInfo(buffer=True),
        "GetProductPropertyIds": _RpcInfo(cache=True),
        "GetVersion": _RpcInfo(cache=True),
        "Scale": _RpcInfo(buffer=True),
        "GetSource": _RpcInfo(cache=True),
        "SetSource": _RpcInfo(buffer=True),
        "GetSourceVersion": _RpcInfo(cache=True),
        "SetSourceVersion": _RpcInfo(buffer=True),
        "GetDefinitionObjs": _RpcInfo(cache=True),
        "TopCircuitCells": _RpcInfo(cache=True),
        "GetCircuits": _RpcInfo(cache=True),
        "GetFootprints": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.DatasetDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "FindByName": _RpcInfo(cache=True),
        "GetName": _RpcInfo(cache=True),
        "SetName": _RpcInfo(buffer=True),
        "GetData": _RpcInfo(cache=True),
        "SetData": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.DebyeModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetFrequencyRange": _RpcInfo(cache=True),
        "SetFrequencyRange": _RpcInfo(buffer=True),
        "GetRelativePermitivityAtHighLowFrequency": _RpcInfo(cache=True),
        "SetRelativePermitivityAtHighLowFrequency": _RpcInfo(buffer=True),
        "IsRelativePermitivityEnabledAtOpticalFrequency": _RpcInfo(cache=True),
        "SetRelativePermitivityEnabledAtOpticalFrequency": _RpcInfo(buffer=True),
        "GetRelativePermitivityAtOpticalFrequency": _RpcInfo(cache=True),
        "SetRelativePermitivityAtOpticalFrequency": _RpcInfo(buffer=True),
        "UseDCConductivity": _RpcInfo(cache=True),
        "SetUseDCConductivity": _RpcInfo(buffer=True),
        "GetDCConductivity": _RpcInfo(cache=True),
        "SetDCConductivity": _RpcInfo(buffer=True),
        "GetLossTangentAtHighLowFrequency": _RpcInfo(cache=True),
        "SetLossTangentAtHighLowFrequency": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.DielectricMaterialModelService": {"GetType": _RpcInfo(cache=True)},
    "ansys.api.edb.v1.DiePropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetDieType": _RpcInfo(cache=True),
        "SetDieType": _RpcInfo(buffer=True),
        "GetHeight": _RpcInfo(cache=True),
        "SetHeight": _RpcInfo(buffer=True),
        "GetOrientation": _RpcInfo(cache=True),
        "SetOrientation": _RpcInfo(buffer=True),
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
                        )
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
        "GetFrequency": _RpcInfo(cache=True),
        "SetFrequency": _RpcInfo(buffer=True),
        "GetRelativePermitivityAtFrequency": _RpcInfo(cache=True),
        "SetRelativePermitivityAtFrequency": _RpcInfo(buffer=True),
        "GetLossTangentAtFrequency": _RpcInfo(cache=True),
        "SetLossTangentAtFrequency": _RpcInfo(buffer=True),
        "GetHighFrequencyCorner": _RpcInfo(cache=True),
        "SetHighFrequencyCorner": _RpcInfo(buffer=True),
        "UseDCRelativePermitivity": _RpcInfo(cache=True),
        "SetUseDCRelativePermitivity": _RpcInfo(buffer=True),
        "GetDCRelativePermitivity": _RpcInfo(cache=True),
        "SetDCRelativePermitivity": _RpcInfo(buffer=True),
        "GetDCConductivity": _RpcInfo(cache=True),
        "SetDCConductivity": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.EDBErrorManagerService": {"GetErrors": _RpcInfo(read_no_cache=True)},
    "ansys.api.edb.v1.EdgeService": {
        "GetEdgeType": _RpcInfo(cache=True),
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "GetParameters": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.EdgeTerminalService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "GetEdges": _RpcInfo(read_no_cache=True),
        "StreamEdges": _RpcInfo(read_no_cache=True),
        "SetEdges": _RpcInfo(buffer=True),
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
                        )
                    ],
                )
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
                    ],
                )
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
                        )
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
                        )
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
        "Ungroup": _RpcInfo(buffer=True),
        "GetMembers": _RpcInfo(read_no_cache=True),
        "StreamMembers": _RpcInfo(read_no_cache=True),
        "GetGroupType": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.HFSSPIGeneralSettingsService": {
        "GetPISliderPos": _RpcInfo(cache=True),
        "SetPISliderPos": _RpcInfo(buffer=True),
        "GetHFSSPIModelType": _RpcInfo(cache=True),
        "SetHFSSPIModelType": _RpcInfo(buffer=True),
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
    "ansys.api.edb.v1.HFSSPINetProcessingSettingsService": {
        "GetAutoSelectNetsForSimulation": _RpcInfo(cache=True),
        "SetAutoSelectNetsForSimulation": _RpcInfo(buffer=True),
        "GetIgnoreDummyNetsForSelectedNets": _RpcInfo(cache=True),
        "SetIgnoreDummyNetsForSelectedNets": _RpcInfo(buffer=True),
        "GetIncludeNets": _RpcInfo(cache=True),
        "SetIncludeNets": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSPIPowerGroundNetsService": {
        "GetImprovedLossModel": _RpcInfo(cache=True),
        "SetImprovedLossModel": _RpcInfo(buffer=True),
        "GetAutoDetectIgnoreSmallHolesMinDiameter": _RpcInfo(cache=True),
        "SetAutoDetectIgnoreSmallHolesMinDiameter": _RpcInfo(buffer=True),
        "GetIgnoreSmallHolesMinDiameter": _RpcInfo(cache=True),
        "SetIgnoreSmallHolesMinDiameter": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSPISignalNetsSettingsService": {
        "GetSignalNetsErrorTolerance": _RpcInfo(cache=True),
        "SetSignalNetsErrorTolerance": _RpcInfo(buffer=True),
        "GetSignalNetsConductorModeling": _RpcInfo(cache=True),
        "SetSignalNetsConductorModeling": _RpcInfo(buffer=True),
        "GetSignalNetsIncludeImprovedLossHandling": _RpcInfo(cache=True),
        "SetSignalNetsIncludeImprovedLossHandling": _RpcInfo(buffer=True),
        "GetSignalNetsIncludeImprovedDielectricFillRefinement": _RpcInfo(cache=True),
        "SetSignalNetsIncludeImprovedDielectricFillRefinement": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSGeneralSettingsService": {
        "GetSingleFrequencyAdaptiveSolution": _RpcInfo(cache=True),
        "SetSingleFrequencyAdaptiveSolution": _RpcInfo(buffer=True),
        "GetMultiFrequencyAdaptiveSolution": _RpcInfo(cache=True),
        "SetMultiFrequencyAdaptiveSolution": _RpcInfo(buffer=True),
        "GetBroadbandFrequencyAdaptiveSolution": _RpcInfo(cache=True),
        "SetBroadbandFrequencyAdaptiveSolution": _RpcInfo(buffer=True),
        "GetSaveFieldsFlag": _RpcInfo(cache=True),
        "SetSaveFieldsFlag": _RpcInfo(buffer=True),
        "GetUseMeshRegion": _RpcInfo(cache=True),
        "SetUseMeshRegion": _RpcInfo(buffer=True),
        "GetMeshRegionName": _RpcInfo(cache=True),
        "SetMeshRegionName": _RpcInfo(buffer=True),
        "GetUseParallelRefinement": _RpcInfo(cache=True),
        "SetUseParallelRefinement": _RpcInfo(buffer=True),
        "GetAdaptType": _RpcInfo(cache=True),
        "SetAdaptType": _RpcInfo(buffer=True),
        "GetSaveRadFieldsOnlyFlag": _RpcInfo(cache=True),
        "SetSaveRadFieldsOnlyFlag": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSOptionsSettingsService": {
        "GetMaxRefinementPerPass": _RpcInfo(cache=True),
        "SetMaxRefinementPerPass": _RpcInfo(buffer=True),
        "GetMinPasses": _RpcInfo(cache=True),
        "SetMinPasses": _RpcInfo(buffer=True),
        "GetMinConvergedPasses": _RpcInfo(cache=True),
        "SetMinConvergedPasses": _RpcInfo(buffer=True),
        "GetUseMaxRefinement": _RpcInfo(cache=True),
        "SetUseMaxRefinement": _RpcInfo(buffer=True),
        "GetBasisFunctionOrder": _RpcInfo(cache=True),
        "SetBasisFunctionOrder": _RpcInfo(buffer=True),
        "GetSolverTypeOrder": _RpcInfo(cache=True),
        "SetSolverTypeOrder": _RpcInfo(buffer=True),
        "GetRelativeResidual": _RpcInfo(cache=True),
        "SetRelativeResidual": _RpcInfo(buffer=True),
        "GetUseShellElements": _RpcInfo(cache=True),
        "SetUseShellElements": _RpcInfo(buffer=True),
        "GetEnhancedLowFrequencyAccuracy": _RpcInfo(cache=True),
        "SetEnhancedLowFrequencyAccuracy": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSAdvancedSettingsService": {
        "GetICModeAutoResolution": _RpcInfo(cache=True),
        "SetICModeAutoResolution": _RpcInfo(buffer=True),
        "GetICModeLength": _RpcInfo(cache=True),
        "SetICModeLength": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSAdvancedMeshingSettingsService": {
        "GetLayerAlignment": _RpcInfo(cache=True),
        "SetLayerAlignment": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HFSSSolverSettingsService": {
        "GetMaxDeltaZ0": _RpcInfo(cache=True),
        "SetMaxDeltaZ0": _RpcInfo(buffer=True),
        "GetSetTrianglesForWaveport": _RpcInfo(cache=True),
        "SetSetTrianglesForWaveport": _RpcInfo(buffer=True),
        "GetMinTrianglesForWavePort": _RpcInfo(cache=True),
        "SetMinTrianglesForWavePort": _RpcInfo(buffer=True),
        "GetMaxTrianglesForWavePort": _RpcInfo(cache=True),
        "SetMaxTrianglesForWavePort": _RpcInfo(buffer=True),
        "GetIntraPlaneCouplingEnabled": _RpcInfo(cache=True),
        "SetIntraPlaneCouplingEnabled": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.DCRSettingsService": {
        "GetMaxPasses": _RpcInfo(cache=True),
        "SetMaxPasses": _RpcInfo(buffer=True),
        "GetMinPasses": _RpcInfo(cache=True),
        "SetMinPasses": _RpcInfo(buffer=True),
        "GetMinConvergedPasses": _RpcInfo(cache=True),
        "SetMinConvergedPasses": _RpcInfo(buffer=True),
        "GetPercentError": _RpcInfo(cache=True),
        "SetPercentError": _RpcInfo(buffer=True),
        "GetPercentRefinementPerPass": _RpcInfo(cache=True),
        "SetPercentRefinementPerPass": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.HfssSimulationSetupService": {
        "GetMeshOperations": _RpcInfo(cache=True),
        "SetMeshOperations": _RpcInfo(buffer=True),
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
                    ],
                )
            ],
        ),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(buffer=True),
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
        "SetSolderBallProperty": _RpcInfo(buffer=True),
        "GetSolderBallProperty": _RpcInfo(cache=True),
        "SetDieProperty": _RpcInfo(buffer=True),
        "GetDieProperty": _RpcInfo(cache=True),
        "SetPortProperty": _RpcInfo(buffer=True),
        "GetPortProperty": _RpcInfo(cache=True),
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
                )
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
        "Decompose": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.IOComponentPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "SetSolderBallProperty": _RpcInfo(buffer=True),
        "GetSolderBallProperty": _RpcInfo(cache=True),
        "SetPortProperty": _RpcInfo(buffer=True),
        "GetPortProperty": _RpcInfo(cache=True),
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
                )
            ],
        ),
        "IsViaLayer": _RpcInfo(cache=True, invalidations=[[]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(buffer=True),
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
                        )
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
                        )
                    ],
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
                        )
                    ],
                )
            ],
        ),
        "IsValid": _RpcInfo(cache=True, invalidations=[[]]),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layer_collection"]]),
        "GetTopBottomStackupLayers": _RpcInfo(cache=True),
        "GetLayers": _RpcInfo(read_no_cache=True),
        "StreamLayers": _RpcInfo(read_no_cache=True),
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
        "MergeDielectrics": _RpcInfo(buffer=True, returns_future=True),
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
        "RemoveZone": _RpcInfo(buffer=True),
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
        "Clear": _RpcInfo(buffer=True),
        "SetMapping": _RpcInfo(buffer=True),
        "GetMappingForward": _RpcInfo(cache=True),
        "GetMappingBackward": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.LayoutService": {
        "GetCell": _RpcInfo(cache=True, invalidations=[[]]),
        "GetLayerCollection": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLayerCollection": _RpcInfo(buffer=True),
        "GetItems": _RpcInfo(read_no_cache=True),
        "StreamItems": _RpcInfo(read_no_cache=True),
        "GetExpandedExtentFromNets": _RpcInfo(cache=True),
        "ConvertPrimitivesToVias": _RpcInfo(buffer=True),
        "ArePortReferenceTerminalsConnected": _RpcInfo(cache=True),
        "GetZonePrimitives": _RpcInfo(read_no_cache=True),
        "StreamZonePrimitives": _RpcInfo(read_no_cache=True),
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
        "GetBoardBendDefs": _RpcInfo(read_no_cache=True),
        "StreamBoardBendDefs": _RpcInfo(read_no_cache=True),
        "GetLayoutInstance": _RpcInfo(cache=True),
        "CompressPrimitives": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.LayoutComponentService": {
        "ExportLayoutComponent": _RpcInfo(write_no_cache_invalidation=True),
        "ImportLayoutComponent": _RpcInfo(write_no_cache_invalidation=True),
        "GetCellInstance": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.LayoutInstanceService": {
        "QueryLayoutObjInstances": _RpcInfo(cache=True),
        "StreamLayoutObjInstancesQuery": _RpcInfo(read_no_cache=True),
        "GetLayoutObjInstanceInContext": _RpcInfo(cache=True),
        "GetConnectedObjects": _RpcInfo(read_no_cache=True),
        "StreamConnectedObjects": _RpcInfo(read_no_cache=True),
    },
    "ansys.api.edb.v1.LayoutInstanceContextService": {
        "GetLayout": _RpcInfo(cache=True),
        "GetBBox": _RpcInfo(cache=True),
        "IsTopOrBlackBox": _RpcInfo(cache=True),
        "GetTopOrBlackBox": _RpcInfo(cache=True),
        "GetPlacementElevation": _RpcInfo(cache=True),
        "Is3DPlacement": _RpcInfo(cache=True),
        "GetTransformation": _RpcInfo(cache=True),
        "GetTransformationBetweenContexts": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.LayoutObjService": {
        "GetLayout": _RpcInfo(cache=True, invalidations=[[]]),
        "Delete": _RpcInfo(buffer=True),
        "GetProductProperty": _RpcInfo(cache=True, invalidations=[[]]),
        "SetProductProperty": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
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
        "GetLayers": _RpcInfo(cache=True),
        "StreamLayers": _RpcInfo(read_no_cache=True),
        "GetGeometries": _RpcInfo(cache=True),
        "GetContext": _RpcInfo(cache=True),
        "GetLayoutInstanceContext": _RpcInfo(cache=True),
        "GetLayoutObj": _RpcInfo(cache=True),
        "GetBBox": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.LayoutObjInstance2DGeometryService": {
        "IsNegative": _RpcInfo(cache=True),
        "GetPolygonData": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.LayoutObjInstance3DGeometryService": {
        "GetTesselationData": _RpcInfo(cache=True)
    },
    "ansys.api.edb.v1.LayoutObjInstanceGeometryService": {
        "GetMaterial": _RpcInfo(cache=True),
        "GetColor": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.MaterialDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "SetProperty": _RpcInfo(buffer=True),
        "FindByName": _RpcInfo(cache=True),
        "Delete": _RpcInfo(buffer=True),
        "GetProperty": _RpcInfo(cache=True),
        "GetAllProperties": _RpcInfo(cache=True),
        "RemoveProperty": _RpcInfo(buffer=True),
        "GetName": _RpcInfo(cache=True),
        "GetDielectricMaterialModel": _RpcInfo(cache=True),
        "SetDielectricMaterialModel": _RpcInfo(buffer=True),
        "GetDimensions": _RpcInfo(cache=True),
        "SetThermalModifier": _RpcInfo(buffer=True),
        "SetAnisotropicThermalModifier": _RpcInfo(buffer=True),
        "GetThermalModifier": _RpcInfo(cache=True),
        "GetAnisotropicThermalModifier": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.MaterialPropertyThermalModifierService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetQuadraticModelParams": _RpcInfo(cache=True),
        "GetThermalModifierExpression": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.McadModelService": {
        "CreateStride": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
        ),
        "CreateHfss": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "Create3dComp": _RpcInfo(
            buffer=True, returns_future=True, write_no_cache_invalidation=True
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
        "GetParameters": _RpcInfo(cache=True),
        "SetParameters": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.NetService": {
        "Create": _RpcInfo(
            buffer=True,
            returns_future=True,
            invalidations=[
                (
                    ["target"],
                    [_InvalidationInfo(rpc="FindByName", service="ansys.api.edb.v1.NetService")],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "SetName": _RpcInfo(buffer=True),
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
                )
            ],
        ),
        "GetLayoutObjects": _RpcInfo(read_no_cache=True),
        "StreamLayoutObjects": _RpcInfo(read_no_cache=True),
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
                        )
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
                )
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
        "AddNet": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="ContainsNet", service="ansys.api.edb.v1.NetClassService"
                        )
                    ],
                )
            ],
        ),
        "RemoveNet": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["target"],
                    [
                        _InvalidationInfo(
                            rpc="ContainsNet", service="ansys.api.edb.v1.NetClassService"
                        )
                    ],
                )
            ],
        ),
        "ContainsNet": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.PackageDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "Delete": _RpcInfo(buffer=True),
        "FindByName": _RpcInfo(cache=True),
        "FindByEDBUId": _RpcInfo(cache=True),
        "GetName": _RpcInfo(cache=True),
        "SetName": _RpcInfo(buffer=True),
        "GetExteriorBoundary": _RpcInfo(cache=True),
        "SetExteriorBoundary": _RpcInfo(buffer=True),
        "GetHeight": _RpcInfo(cache=True),
        "SetHeight": _RpcInfo(buffer=True),
        "GetOperatingPower": _RpcInfo(cache=True),
        "SetOperatingPower": _RpcInfo(buffer=True),
        "GetMaximumPower": _RpcInfo(cache=True),
        "SetMaximumPower": _RpcInfo(buffer=True),
        "GetTherm_Cond": _RpcInfo(cache=True),
        "SetTherm_Cond": _RpcInfo(buffer=True),
        "GetTheta_JB": _RpcInfo(cache=True),
        "SetTheta_JB": _RpcInfo(buffer=True),
        "GetTheta_JC": _RpcInfo(cache=True),
        "SetTheta_JC": _RpcInfo(buffer=True),
        "GetHeatSink": _RpcInfo(cache=True),
        "SetHeatSink": _RpcInfo(buffer=True),
        "GetProductProperty": _RpcInfo(cache=True),
        "SetProductProperty": _RpcInfo(buffer=True),
        "GetProductPropertyIds": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.PadstackDefService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "Delete": _RpcInfo(buffer=True),
        "FindByName": _RpcInfo(cache=True),
        "GetName": _RpcInfo(cache=True),
        "GetData": _RpcInfo(cache=True),
        "SetData": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.PadstackDefDataService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetMaterial": _RpcInfo(cache=True),
        "SetMaterial": _RpcInfo(buffer=True),
        "GetLayerNames": _RpcInfo(cache=True),
        "GetLayerIds": _RpcInfo(cache=True),
        "AddLayers": _RpcInfo(buffer=True),
        "GetPadParameters": _RpcInfo(cache=True),
        "SetPadParameters": _RpcInfo(buffer=True),
        "GetHoleRange": _RpcInfo(cache=True),
        "SetHoleRange": _RpcInfo(buffer=True),
        "GetPlatingPercentage": _RpcInfo(cache=True),
        "SetPlatingPercentage": _RpcInfo(buffer=True),
        "GetSolderBallShape": _RpcInfo(cache=True),
        "SetSolderBallShape": _RpcInfo(buffer=True),
        "GetSolderBallPlacement": _RpcInfo(cache=True),
        "SetSolderBallPlacement": _RpcInfo(buffer=True),
        "GetSolderBallParam": _RpcInfo(cache=True),
        "SetSolderBallParam": _RpcInfo(buffer=True),
        "GetSolderBallMaterial": _RpcInfo(cache=True),
        "SetSolderBallMaterial": _RpcInfo(buffer=True),
        "GetConnectionPt": _RpcInfo(cache=True),
        "SetConnectionPt": _RpcInfo(buffer=True),
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
                        )
                    ],
                )
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
                        )
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
                        )
                    ],
                )
            ],
        ),
        "GetPadstackInstanceTerminal": _RpcInfo(cache=True, invalidations=[[]]),
        "IsInPinGroup": _RpcInfo(cache=True, invalidations=[["target"]]),
        "GetPinGroups": _RpcInfo(read_no_cache=True, invalidations=[[]]),
        "StreamPinGroups": _RpcInfo(read_no_cache=True),
    },
    "ansys.api.edb.v1.PadstackInstanceTerminalService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "GetParameters": _RpcInfo(cache=True),
        "SetParameters": _RpcInfo(buffer=True),
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
                        )
                    ],
                )
            ],
        ),
        "Render": _RpcInfo(cache=True),
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
                    ],
                )
            ],
        ),
        "FindByName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetUniqueName": _RpcInfo(cache=True, invalidations=[["layout"]]),
        "GetName": _RpcInfo(cache=True, invalidations=[[]]),
        "AddPins": _RpcInfo(buffer=True),
        "RemovePins": _RpcInfo(buffer=True),
        "GetPins": _RpcInfo(read_no_cache=True),
        "StreamPins": _RpcInfo(read_no_cache=True),
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
        "GetPinGroup": _RpcInfo(cache=True),
        "SetPinGroup": _RpcInfo(buffer=True),
        "GetLayer": _RpcInfo(cache=True),
        "SetLayer": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.PinPairModelService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetRlc": _RpcInfo(cache=True, invalidations=[[]]),
        "SetRlc": _RpcInfo(
            buffer=True,
            invalidations=[
                (
                    ["model"],
                    [
                        _InvalidationInfo(
                            rpc="GetRlc", service="ansys.api.edb.v1.PinPairModelService"
                        )
                    ],
                )
            ],
        ),
        "DeleteRlc": _RpcInfo(buffer=True),
        "GetPinPairs": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.PointDataService": {
        "Rotate": _RpcInfo(cache=True),
        "ClosestPoint": _RpcInfo(cache=True),
        "Distance": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.PointTerminalService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "GetParameters": _RpcInfo(cache=True),
        "SetParameters": _RpcInfo(buffer=True),
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
                        )
                    ],
                )
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
        "GetNormalizedPoints": _RpcInfo(cache=True),
        "IsCircle": _RpcInfo(cache=True),
        "IsBox": _RpcInfo(cache=True),
        "HasSelfIntersections": _RpcInfo(cache=True),
        "RemoveSelfIntersections": _RpcInfo(cache=True),
        "IsConvex": _RpcInfo(cache=True),
        "GetArea": _RpcInfo(cache=True),
        "Transform": _RpcInfo(cache=True),
        "GetBBox": _RpcInfo(cache=True),
        "GetStreamedBBox": _RpcInfo(read_no_cache=True),
        "GetConvexHull": _RpcInfo(cache=True),
        "RemoveArcs": _RpcInfo(cache=True),
        "Defeature": _RpcInfo(cache=True),
        "GetBoundingCircle": _RpcInfo(cache=True),
        "IsInside": _RpcInfo(cache=True),
        "CircleIntersectsPolygon": _RpcInfo(cache=True),
        "GetIntersectionType": _RpcInfo(cache=True),
        "GetClosestPoints": _RpcInfo(cache=True),
        "GetUnion": _RpcInfo(cache=True),
        "GetIntersection": _RpcInfo(cache=True),
        "Subtract": _RpcInfo(cache=True),
        "Xor": _RpcInfo(cache=True),
        "Expand": _RpcInfo(cache=True),
        "Get2DAlphaShape": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.PortPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "Clone": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetReferenceHeight": _RpcInfo(cache=True),
        "SetReferenceHeight": _RpcInfo(buffer=True),
        "GetReferenceSizeAuto": _RpcInfo(cache=True),
        "SetReferenceSizeAuto": _RpcInfo(buffer=True),
        "GetReferenceSize": _RpcInfo(cache=True),
        "SetReferenceSize": _RpcInfo(buffer=True),
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
                        )
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
        "Voids": _RpcInfo(read_no_cache=True),
        "StreamVoids": _RpcInfo(read_no_cache=True),
        "GetOwner": _RpcInfo(cache=True, invalidations=[[]]),
        "IsParameterized": _RpcInfo(cache=True),
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
                )
            ],
        ),
    },
    "ansys.api.edb.v1.PrimitiveInstanceCollectionService": {
        "GetGeometry": _RpcInfo(cache=True),
        "SetGeometry": _RpcInfo(buffer=True),
        "GetPositions": _RpcInfo(read_no_cache=True),
        "GetInstantiatedGeometry": _RpcInfo(read_no_cache=True),
        "Decompose": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Q3DGeneralSettingsService": {
        "GetSolutionFrequency": _RpcInfo(cache=True),
        "SetSolutionFrequency": _RpcInfo(buffer=True),
        "GetDoDC": _RpcInfo(cache=True),
        "SetDoDC": _RpcInfo(buffer=True),
        "GetDoDCResOnly": _RpcInfo(cache=True),
        "SetDoDCResOnly": _RpcInfo(buffer=True),
        "GetDoCG": _RpcInfo(cache=True),
        "SetDoCG": _RpcInfo(buffer=True),
        "GetDoAC": _RpcInfo(cache=True),
        "SetDoAC": _RpcInfo(buffer=True),
        "GetSaveFields": _RpcInfo(cache=True),
        "SetSaveFields": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Q3DSettingsService": {
        "GetMaxPasses": _RpcInfo(cache=True),
        "SetMaxPasses": _RpcInfo(buffer=True),
        "GetMinPasses": _RpcInfo(cache=True),
        "SetMinPasses": _RpcInfo(buffer=True),
        "GetMinConvergedPasses": _RpcInfo(cache=True),
        "SetMinConvergedPasses": _RpcInfo(buffer=True),
        "GetPercentError": _RpcInfo(cache=True),
        "SetPercentError": _RpcInfo(buffer=True),
        "GetMaxRefinePerPass": _RpcInfo(cache=True),
        "SetMaxRefinePerPass": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Q3DDCRLSettingsService": {
        "GetSolutionOrder": _RpcInfo(cache=True),
        "SetSolutionOrder": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Q3DCGSettingsService": {
        "GetAutoIncrSolOrder": _RpcInfo(cache=True),
        "SetAutoIncrSolOrder": _RpcInfo(buffer=True),
        "GetSolutionOrder": _RpcInfo(cache=True),
        "SetSolutionOrder": _RpcInfo(buffer=True),
        "GetSolverType": _RpcInfo(cache=True),
        "SetSolverType": _RpcInfo(buffer=True),
        "GetCompressionTol": _RpcInfo(cache=True),
        "SetCompressionTol": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Q3DAdvancedSettingsService": {
        "GetICModeAutoResolution": _RpcInfo(cache=True),
        "SetICModeAutoResolution": _RpcInfo(buffer=True),
        "GetICModeLength": _RpcInfo(cache=True),
        "SetICModeLength": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.Q3DAdvancedMeshingSettingsService": {
        "GetLayerAlignment": _RpcInfo(cache=True),
        "SetLayerAlignment": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.RaptorXGeneralSettingsService": {
        "GetUseGoldEMSolver": _RpcInfo(cache=True),
        "SetUseGoldEMSolver": _RpcInfo(buffer=True),
        "GetMaxFrequency": _RpcInfo(cache=True),
        "SetMaxFrequency": _RpcInfo(buffer=True),
        "GetGlobalTemperature": _RpcInfo(cache=True),
        "SetGlobalTemperature": _RpcInfo(buffer=True),
        "GetSaveNetlist": _RpcInfo(cache=True),
        "SetSaveNetlist": _RpcInfo(buffer=True),
        "GetNetlistExportSpectre": _RpcInfo(cache=True),
        "SetNetlistExportSpectre": _RpcInfo(buffer=True),
        "GetSaveRFM": _RpcInfo(cache=True),
        "SetSaveRFM": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.RaptorXAdvancedSettingsService": {
        "GetUseMeshFrequency": _RpcInfo(cache=True),
        "SetUseMeshFrequency": _RpcInfo(buffer=True),
        "GetMeshFrequency": _RpcInfo(cache=True),
        "SetMeshFrequency": _RpcInfo(buffer=True),
        "GetUseEdgeMesh": _RpcInfo(cache=True),
        "SetUseEdgeMesh": _RpcInfo(buffer=True),
        "GetEdgeMesh": _RpcInfo(cache=True),
        "SetEdgeMesh": _RpcInfo(buffer=True),
        "GetUseCellsPerWavelength": _RpcInfo(cache=True),
        "SetUseCellsPerWavelength": _RpcInfo(buffer=True),
        "GetCellsPerWavelength": _RpcInfo(cache=True),
        "SetCellsPerWavelength": _RpcInfo(buffer=True),
        "GetUsePlaneProjectionFactor": _RpcInfo(cache=True),
        "SetUsePlaneProjectionFactor": _RpcInfo(buffer=True),
        "GetPlaneProjectionFactor": _RpcInfo(cache=True),
        "SetPlaneProjectionFactor": _RpcInfo(buffer=True),
        "GetUseRelaxedZAxis": _RpcInfo(cache=True),
        "SetUseRelaxedZAxis": _RpcInfo(buffer=True),
        "GetUseEliminateSlitPerHoles": _RpcInfo(cache=True),
        "SetUseEliminateSlitPerHoles": _RpcInfo(buffer=True),
        "GetEliminateSlitPerHoles": _RpcInfo(cache=True),
        "SetEliminateSlitPerHoles": _RpcInfo(buffer=True),
        "GetUseAutoRemovalSliverPoly": _RpcInfo(cache=True),
        "SetUseAutoRemovalSliverPoly": _RpcInfo(buffer=True),
        "GetAutoRemovalSliverPoly": _RpcInfo(cache=True),
        "SetAutoRemovalSliverPoly": _RpcInfo(buffer=True),
        "GetUseAccelerateViaExtraction": _RpcInfo(cache=True),
        "SetUseAccelerateViaExtraction": _RpcInfo(buffer=True),
        "GetUseEnableSubstrateNetworkExtraction": _RpcInfo(cache=True),
        "SetUseEnableSubstrateNetworkExtraction": _RpcInfo(buffer=True),
        "GetUseLDE": _RpcInfo(cache=True),
        "SetUseLDE": _RpcInfo(buffer=True),
        "GetUseExtractFloatingMetalsDummy": _RpcInfo(cache=True),
        "SetUseExtractFloatingMetalsDummy": _RpcInfo(buffer=True),
        "GetUseExtractFloatingMetalsFloating": _RpcInfo(cache=True),
        "SetUseExtractFloatingMetalsFloating": _RpcInfo(buffer=True),
        "GetUseEnableEtchTransform": _RpcInfo(cache=True),
        "SetUseEnableEtchTransform": _RpcInfo(buffer=True),
        "GetUseEnableHybridExtraction": _RpcInfo(cache=True),
        "SetUseEnableHybridExtraction": _RpcInfo(buffer=True),
        "GetUseEnableAdvancedCapEffects": _RpcInfo(cache=True),
        "SetUseEnableAdvancedCapEffects": _RpcInfo(buffer=True),
        "GetUseOverrideShrinkFac": _RpcInfo(cache=True),
        "SetUseOverrideShrinkFac": _RpcInfo(buffer=True),
        "GetOverrideShrinkFac": _RpcInfo(cache=True),
        "SetOverrideShrinkFac": _RpcInfo(buffer=True),
        "GetAdvancedOptions": _RpcInfo(cache=True),
        "SetAdvancedOptions": _RpcInfo(buffer=True),
        "GetNetSettingsOptions": _RpcInfo(cache=True),
        "SetNetSettingsOptions": _RpcInfo(buffer=True),
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
                        )
                    ],
                )
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
        "Render": _RpcInfo(cache=True),
        "GetPolygonData": _RpcInfo(cache=True, invalidations=[[]]),
    },
    "ansys.api.edb.v1.RLCComponentPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetEnabled": _RpcInfo(cache=True),
        "SetEnabled": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.RTreeService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetExtent": _RpcInfo(cache=True),
        "InsertIntObject": _RpcInfo(buffer=True),
        "DeleteIntObject": _RpcInfo(buffer=True),
        "Empty": _RpcInfo(cache=True),
        "Search": _RpcInfo(cache=True),
        "NearestNeighbor": _RpcInfo(cache=True),
        "TouchingGeometry": _RpcInfo(cache=True),
        "ConnectedGeometry": _RpcInfo(cache=True),
        "GetConnectedGeometrySets": _RpcInfo(cache=True),
        "IncrementVisit": _RpcInfo(buffer=True),
        "IsVisited": _RpcInfo(cache=True),
        "Visit": _RpcInfo(buffer=True),
        "GetVisit": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.SimulationSettingsService": {
        "GetEnabled": _RpcInfo(cache=True),
        "SetEnabled": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SettingsOptionsService": {
        "GetDoLamdaRefineFlag": _RpcInfo(cache=True),
        "SetDoLamdaRefineFlag": _RpcInfo(buffer=True),
        "GetLamdaTarget": _RpcInfo(cache=True),
        "SetLamdaTarget": _RpcInfo(buffer=True),
        "GetMeshSizefactor": _RpcInfo(cache=True),
        "SetMeshSizefactor": _RpcInfo(buffer=True),
        "GetUseDefaultLamda": _RpcInfo(cache=True),
        "SetUseDefaultLamda": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.AdvancedSettingsService": {
        "GetUnionPolygons": _RpcInfo(cache=True),
        "SetUnionPolygons": _RpcInfo(buffer=True),
        "GetRemoveFloatingGeometry": _RpcInfo(cache=True),
        "SetRemoveFloatingGeometry": _RpcInfo(buffer=True),
        "GetHealingOption": _RpcInfo(cache=True),
        "SetHealingOption": _RpcInfo(buffer=True),
        "GetSmallVoidArea": _RpcInfo(cache=True),
        "SetSmallVoidArea": _RpcInfo(buffer=True),
        "GetUseDefeature": _RpcInfo(cache=True),
        "SetUseDefeature": _RpcInfo(buffer=True),
        "GetUseDefeatureAbsoluteLength": _RpcInfo(cache=True),
        "SetUseDefeatureAbsoluteLength": _RpcInfo(buffer=True),
        "GetDefeatureAbsoluteLength": _RpcInfo(cache=True),
        "SetDefeatureAbsoluteLength": _RpcInfo(buffer=True),
        "GetDefeatureRatio": _RpcInfo(cache=True),
        "SetDefeatureRatio": _RpcInfo(buffer=True),
        "GetViaModelType": _RpcInfo(cache=True),
        "SetViaModelType": _RpcInfo(buffer=True),
        "GetNumViaSides": _RpcInfo(cache=True),
        "SetNumViaSides": _RpcInfo(buffer=True),
        "GetViaDensity": _RpcInfo(cache=True),
        "SetViaDensity": _RpcInfo(buffer=True),
        "GetViaMaterial": _RpcInfo(cache=True),
        "SetViaMaterial": _RpcInfo(buffer=True),
        "GetMeshForViaPlating": _RpcInfo(cache=True),
        "SetMeshForViaPlating": _RpcInfo(buffer=True),
        "GetModelType": _RpcInfo(cache=True),
        "SetModelType": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.AdvancedMeshingSettingsService": {
        "GetArcStepSize": _RpcInfo(cache=True),
        "SetArcStepSize": _RpcInfo(buffer=True),
        "GetCircleStartAzimuth": _RpcInfo(cache=True),
        "SetCircleStartAzimuth": _RpcInfo(buffer=True),
        "GetMaxNumArcPoints": _RpcInfo(cache=True),
        "SetMaxNumArcPoints": _RpcInfo(buffer=True),
        "GetUseArcChordErrorApprox": _RpcInfo(cache=True),
        "SetUseArcChordErrorApprox": _RpcInfo(buffer=True),
        "GetArcChordErrorApprox": _RpcInfo(cache=True),
        "SetArcChordErrorApprox": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SolverSettingsService": {
        "GetThinSignalLayerThreshold": _RpcInfo(cache=True),
        "SetThinSignalLayerThreshold": _RpcInfo(buffer=True),
        "GetThinDielectricLayerThreshold": _RpcInfo(cache=True),
        "SetThinDielectricLayerThreshold": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SimulationSetupService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetName": _RpcInfo(cache=True),
        "SetName": _RpcInfo(buffer=True),
        "GetPosition": _RpcInfo(cache=True),
        "SetPosition": _RpcInfo(buffer=True),
        "GetSweepData": _RpcInfo(cache=True),
        "SetSweepData": _RpcInfo(buffer=True),
        "GetType": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.SIWaveDCIRSimulationSettingsService": {
        "GetIcepakTempFile": _RpcInfo(cache=True),
        "SetIcepakTempFile": _RpcInfo(buffer=True),
        "GetSourceTermsToGround": _RpcInfo(cache=True),
        "SetSourceTermsToGround": _RpcInfo(buffer=True),
        "GetExportDCThermalData": _RpcInfo(cache=True),
        "SetExportDCThermalData": _RpcInfo(buffer=True),
        "GetImportThermalData": _RpcInfo(cache=True),
        "SetImportThermalData": _RpcInfo(buffer=True),
        "GetFullDCReportPath": _RpcInfo(cache=True),
        "SetFullDCReportPath": _RpcInfo(buffer=True),
        "GetViaReportPath": _RpcInfo(cache=True),
        "SetViaReportPath": _RpcInfo(buffer=True),
        "GetPerPinResPath": _RpcInfo(cache=True),
        "SetPerPinResPath": _RpcInfo(buffer=True),
        "GetDCReportConfigFile": _RpcInfo(cache=True),
        "SetDCReportConfigFile": _RpcInfo(buffer=True),
        "GetDCReportShowActiveDevices": _RpcInfo(cache=True),
        "SetDCReportShowActiveDevices": _RpcInfo(buffer=True),
        "GetPerPinUsePinFormat": _RpcInfo(cache=True),
        "SetPerPinUsePinFormat": _RpcInfo(buffer=True),
        "GetUseLoopResForPerPin": _RpcInfo(cache=True),
        "SetUseLoopResForPerPin": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWaveGeneralSettingsService": {
        "GetUseSISettings": _RpcInfo(cache=True),
        "SetUseSISettings": _RpcInfo(buffer=True),
        "GetUseCustomSettings": _RpcInfo(cache=True),
        "SetUseCustomSettings": _RpcInfo(buffer=True),
        "GetSISliderPos": _RpcInfo(cache=True),
        "SetSISliderPos": _RpcInfo(buffer=True),
        "GetPISliderPos": _RpcInfo(cache=True),
        "SetPISliderPos": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWaveAdvancedSettingsService": {
        "GetIncludeCoPlaneCoupling": _RpcInfo(cache=True),
        "SetIncludeCoPlaneCoupling": _RpcInfo(buffer=True),
        "GetIncludeInterPlaneCoupling": _RpcInfo(cache=True),
        "SetIncludeInterPlaneCoupling": _RpcInfo(buffer=True),
        "GetIncludeSplitPlaneCoupling": _RpcInfo(cache=True),
        "SetIncludeSplitPlaneCoupling": _RpcInfo(buffer=True),
        "GetIncludeFringePlaneCoupling": _RpcInfo(cache=True),
        "SetIncludeFringePlaneCoupling": _RpcInfo(buffer=True),
        "GetIncludeTracePlaneCoupling": _RpcInfo(cache=True),
        "SetIncludeTracePlaneCoupling": _RpcInfo(buffer=True),
        "GetCrossTalkThreshold": _RpcInfo(cache=True),
        "SetCrossTalkThreshold": _RpcInfo(buffer=True),
        "GetMaxCoupledLines": _RpcInfo(cache=True),
        "SetMaxCoupledLines": _RpcInfo(buffer=True),
        "GetMinVoidArea": _RpcInfo(cache=True),
        "SetMinVoidArea": _RpcInfo(buffer=True),
        "GetMinPadAreaToMesh": _RpcInfo(cache=True),
        "SetMinPadAreaToMesh": _RpcInfo(buffer=True),
        "GetMinPlaneAreaToMesh": _RpcInfo(cache=True),
        "SetMinPlaneAreaToMesh": _RpcInfo(buffer=True),
        "GetSnapLengthThreshold": _RpcInfo(cache=True),
        "SetSnapLengthThreshold": _RpcInfo(buffer=True),
        "GetMeshAutomatic": _RpcInfo(cache=True),
        "SetMeshAutomatic": _RpcInfo(buffer=True),
        "GetMeshFrequency": _RpcInfo(cache=True),
        "SetMeshFrequency": _RpcInfo(buffer=True),
        "GetAcDcMergeMode": _RpcInfo(cache=True),
        "SetAcDcMergeMode": _RpcInfo(buffer=True),
        "Get3DReturnCurrentDistribution": _RpcInfo(cache=True),
        "Set3DReturnCurrentDistribution": _RpcInfo(buffer=True),
        "GetIncludeVISources": _RpcInfo(cache=True),
        "SetIncludeVISources": _RpcInfo(buffer=True),
        "GetIncludeInfGnd": _RpcInfo(cache=True),
        "SetIncludeInfGnd": _RpcInfo(buffer=True),
        "GetInfGndLocation": _RpcInfo(cache=True),
        "SetInfGndLocation": _RpcInfo(buffer=True),
        "GetPerformERC": _RpcInfo(cache=True),
        "SetPerformERC": _RpcInfo(buffer=True),
        "GetIgnoreNonFunctionalPads": _RpcInfo(cache=True),
        "SetIgnoreNonFunctionalPads": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWaveDCSettingsService": {
        "GetUseDCCustomSettings": _RpcInfo(cache=True),
        "SetUseDCCustomSettings": _RpcInfo(buffer=True),
        "GetComputeInductance": _RpcInfo(cache=True),
        "SetComputeInductance": _RpcInfo(buffer=True),
        "GetPlotJV": _RpcInfo(cache=True),
        "SetPlotJV": _RpcInfo(buffer=True),
        "GetContactRadius": _RpcInfo(cache=True),
        "SetContactRadius": _RpcInfo(buffer=True),
        "GetDCSliderPos": _RpcInfo(cache=True),
        "SetDCSliderPos": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWaveDCAdvancedSettingsService": {
        "GetDCMinPlaneAreaToMesh": _RpcInfo(cache=True),
        "SetDCMinPlaneAreaToMesh": _RpcInfo(buffer=True),
        "GetDCMinVoidAreaToMesh": _RpcInfo(cache=True),
        "SetDCMinVoidAreaToMesh": _RpcInfo(buffer=True),
        "GetMaxInitMeshEdgeLength": _RpcInfo(cache=True),
        "SetMaxInitMeshEdgeLength": _RpcInfo(buffer=True),
        "GetPerformAdaptiveRefinement": _RpcInfo(cache=True),
        "SetPerformAdaptiveRefinement": _RpcInfo(buffer=True),
        "GetMaxNumPasses": _RpcInfo(cache=True),
        "SetMaxNumPasses": _RpcInfo(buffer=True),
        "GetMinNumPasses": _RpcInfo(cache=True),
        "SetMinNumPasses": _RpcInfo(buffer=True),
        "GetPercentLocalRefinement": _RpcInfo(cache=True),
        "SetPercentLocalRefinement": _RpcInfo(buffer=True),
        "GetEnergyError": _RpcInfo(cache=True),
        "SetEnergyError": _RpcInfo(buffer=True),
        "GetMeshBws": _RpcInfo(cache=True),
        "SetMeshBws": _RpcInfo(buffer=True),
        "GetRefineBws": _RpcInfo(cache=True),
        "SetRefineBws": _RpcInfo(buffer=True),
        "GetMeshVias": _RpcInfo(cache=True),
        "SetMeshVias": _RpcInfo(buffer=True),
        "GetRefineVias": _RpcInfo(cache=True),
        "SetRefineVias": _RpcInfo(buffer=True),
        "GetNumBwSides": _RpcInfo(cache=True),
        "SetNumBwSides": _RpcInfo(buffer=True),
        "GetNumViaSides": _RpcInfo(cache=True),
        "SetNumViaSides": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SIWaveSParameterSettingsService": {
        "GetUseStateSpace": _RpcInfo(cache=True),
        "SetUseStateSpace": _RpcInfo(buffer=True),
        "GetInterpolation": _RpcInfo(cache=True),
        "SetInterpolation": _RpcInfo(buffer=True),
        "GetExtrapolation": _RpcInfo(cache=True),
        "SetExtrapolation": _RpcInfo(buffer=True),
        "GetDCBehavior": _RpcInfo(cache=True),
        "SetDCBehavior": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.SolderBallPropertyService": {
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetShape": _RpcInfo(cache=True),
        "SetShape": _RpcInfo(buffer=True),
        "GetPlacement": _RpcInfo(cache=True),
        "SetPlacement": _RpcInfo(buffer=True),
        "GetDiameter": _RpcInfo(cache=True),
        "SetDiameter": _RpcInfo(buffer=True),
        "GetHeight": _RpcInfo(cache=True),
        "SetHeight": _RpcInfo(buffer=True),
        "GetMaterialName": _RpcInfo(cache=True),
        "SetMaterialName": _RpcInfo(buffer=True),
        "UsesSolderball": _RpcInfo(cache=True),
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
        "SetThickness": _RpcInfo(buffer=True),
        "GetLowerElevation": _RpcInfo(cache=True, invalidations=[[]]),
        "SetLowerElevation": _RpcInfo(buffer=True),
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
    "ansys.api.edb.v1.TerminalService": {
        "FindByName": _RpcInfo(buffer=True, returns_future=True),
        "GetParams": _RpcInfo(cache=True),
        "SetParams": _RpcInfo(buffer=True),
        "GetProductSolvers": _RpcInfo(cache=True),
        "SetProductSolverOptions": _RpcInfo(buffer=True),
    },
    "ansys.api.edb.v1.TerminalInstanceService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "GetOwningCellInstance": _RpcInfo(cache=True),
        "GetDefinitionTerminal": _RpcInfo(cache=True),
        "GetDefinitionTerminalName": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.TerminalInstanceTerminalService": {
        "Create": _RpcInfo(buffer=True, returns_future=True),
        "GetTerminalInstance": _RpcInfo(cache=True),
        "SetTerminalInstance": _RpcInfo(buffer=True),
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
                        )
                    ],
                )
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
        "Rotate": _RpcInfo(cache=True),
        "Create": _RpcInfo(buffer=True, returns_future=True, write_no_cache_invalidation=True),
        "GetScale": _RpcInfo(cache=True),
        "SetScale": _RpcInfo(buffer=True),
        "GetMirror": _RpcInfo(cache=True),
        "SetMirror": _RpcInfo(buffer=True),
        "GetRotation": _RpcInfo(cache=True),
        "SetRotation": _RpcInfo(buffer=True),
        "GetOffsetX": _RpcInfo(cache=True),
        "SetOffsetX": _RpcInfo(buffer=True),
        "GetOffsetY": _RpcInfo(cache=True),
        "SetOffsetY": _RpcInfo(buffer=True),
        "TransformPlus": _RpcInfo(buffer=True, returns_future=True),
        "IsIdentity": _RpcInfo(cache=True),
        "TransformPoint": _RpcInfo(cache=True),
        "TransformPolygon": _RpcInfo(cache=True),
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
        "TransformPoint": _RpcInfo(cache=True),
        "GetZYXRotation": _RpcInfo(cache=True),
        "GetAxis": _RpcInfo(cache=True),
        "Transpose": _RpcInfo(buffer=True),
        "Invert": _RpcInfo(buffer=True),
        "IsIdentity": _RpcInfo(cache=True),
        "IsEqual": _RpcInfo(cache=True),
        "GetScaling": _RpcInfo(cache=True),
        "GetShift": _RpcInfo(cache=True),
        "SetMatrix": _RpcInfo(buffer=True),
        "GetMatrix": _RpcInfo(cache=True),
    },
    "ansys.api.edb.v1.ValueService": {
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
                        )
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
                        )
                    ],
                )
            ],
        ),
        "DeleteVariable": _RpcInfo(buffer=True),
        "SetVariableValue": _RpcInfo(buffer=True),
        "GetVariableValue": _RpcInfo(cache=True, invalidations=[[]]),
        "IsParameter": _RpcInfo(cache=True, invalidations=[[]]),
        "GetAllVariableNames": _RpcInfo(cache=True, invalidations=[[]]),
        "GetVariableDesc": _RpcInfo(cache=True, invalidations=[[]]),
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
        "SetRefLayer": _RpcInfo(buffer=True),
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
                        )
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
