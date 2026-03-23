// -----------------------------------------------------------------
// Minimal pybind11 hello-world module.
//
// This exists solely to verify that C++ compilation and wheel
// packaging work correctly end-to-end in CI/CD.  The real
// implementation lives in a separate integration branch.
// -----------------------------------------------------------------
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(hello_world, m)
{
    m.doc() = "Minimal pybind11 hello-world module (CI/CD compilation test).";

    m.def(
        "hello_world",
        []() -> std::string { return "hello world"; },
        R"doc(
            Returns the string "hello world".

            This function exists solely to verify that pybind11 C++ compilation
            and wheel packaging work correctly end-to-end in CI/CD.

            Returns
            -------
            str
                "hello world"
        )doc"
    );
}
