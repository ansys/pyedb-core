// -----------------------------------------------------------------
// Contents: pybind11 Python bindings for RPCExecutor.
//
// Build example (MSVC + CMake):
//   find_package(pybind11 REQUIRED)
//   pybind11_add_module(rpc_executor rpc_executor_bindings.cpp)
//   target_include_directories(rpc_executor PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
//   target_compile_features(rpc_executor PRIVATE cxx_std_17)
// -----------------------------------------------------------------
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdexcept>

#include "rpc_executor.h"

namespace py = pybind11;

PYBIND11_MODULE(rpc_executor, m)
{
    m.doc() = R"doc(
        Python bindings for RPCExecutor.

        Typical usage::

            import rpc_executor

            ok = rpc_executor.initialize("/path/to/ansys/em/install")
            assert ok, "Failed to load the EDB_RPC_Services shared library"

            success, response, error = rpc_executor.execute_rpc(
                "MyService", "MyMethod", serialized_proto_bytes)

        The EDB_RPC_Services shared library is loaded directly from the
        directory supplied to :func:`initialize`.  It is **not** bundled
        inside the Python package.
    )doc";

    // ------------------------------------------------------------------
    // initialize(directory_path: str) -> bool
    // ------------------------------------------------------------------
    m.def(
        "initialize",
        [](const std::string& directoryPath) -> bool
        {
            return RPCExecutor::Initialize(directoryPath);
        },
        py::arg("directory_path"),
        R"doc(
            Load the EDB_RPC_Services shared library and initialize the
            plugin interface.

            The library is loaded directly from ``directory_path``; it must
            exist there at runtime (it is not bundled in the Python package).
            On Windows the directory is also added to the DLL search path so
            that transitive dependencies of EDB_RPC_Services.dll are resolved.
            On Linux it is prepended to LD_LIBRARY_PATH for the same purpose.

            Parameters
            ----------
            directory_path : str
                Absolute path to the Ansys EM install directory containing
                EDB_RPC_Services.dll (Windows) or libEDB_RPC_Services.so
                (Linux) and their transitive dependencies.

            Returns
            -------
            bool
                ``True`` on success, ``False`` if the directory is invalid,
                the shared library cannot be found, the exported symbol is
                missing, or the plugin returned a null pointer.
        )doc");

    // ------------------------------------------------------------------
    // execute_rpc(service_name, rpc_name, serialized_request)
    //     -> tuple[bool, bytes, str]
    //
    //   Returns (success, serialized_response, error_message).
    //   serialized_response is bytes so it can be passed directly to
    //   protobuf ParseFromString().
    //   error_message is a plain str (human-readable text, not binary).
    // ------------------------------------------------------------------
    m.def(
        "execute_rpc",
        [](const std::string& serviceName,
           const std::string& rpcName,
           py::bytes serializedRequest) -> py::tuple
        {
            auto [ok, serializedResponse, errorMessage] = RPCExecutor::ExecuteRpc(
                serviceName, rpcName, std::string(serializedRequest));
            return py::make_tuple(ok, py::bytes(serializedResponse), errorMessage);
        },
        py::arg("service_name"),
        py::arg("rpc_name"),
        py::arg("serialized_request"),
        R"doc(
            Execute an RPC call through the loaded plugin.

            Must be called after a successful :func:`initialize`.

            Parameters
            ----------
            service_name : str
                Name of the gRPC service.
            rpc_name : str
                Name of the RPC method to invoke.
            serialized_request : bytes
                Serialized protobuf request payload.

            Returns
            -------
            tuple[bool, bytes, str]
                A 3-tuple of:
                - ``success`` (bool): ``True`` if the RPC succeeded.
                - ``serialized_response`` (bytes): Serialized protobuf response.
                - ``error_message`` (str): Human-readable error text on failure,
                  empty string on success.

            Raises
            ------
            RuntimeError
                If :func:`initialize` has not been called successfully.
        )doc");
}
