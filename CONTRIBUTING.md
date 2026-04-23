# Contributing

For general contribution guidelines, please refer to the [PyAnsys Developer's Guide].

[PyAnsys Developer's Guide]: https://dev.docs.pyansys.com/

## Prerequisites

This package contains a C++ extension module compiled with [pybind11] and
[scikit-build-core]. Before you can build it locally you need:

| Prerequisite | Minimum version | Notes |
|---|---|---|
| Python | 3.10 | [python.org](https://www.python.org/downloads/) |
| Microsoft C++ Build Tools | VS 2022 | Windows only — see below |

[pybind11]: https://pybind11.readthedocs.io/
[scikit-build-core]: https://scikit-build-core.readthedocs.io/

> **Linux / macOS**: GCC or Clang is typically available by default (`sudo apt install build-essential` on Debian/Ubuntu).

## Setting up the build environment on Windows

A bootstrap script is provided that:
1. Checks whether Microsoft C++ Build Tools are installed.
2. Installs them automatically via `winget` if they are not found.
3. Activates the 64-bit MSVC environment (`vcvars64.bat`) and runs `python -m build`.

From a PowerShell prompt at the repository root, run:

```powershell
.\scripts\bootstrap.ps1
```

The built wheel and source distribution will appear in the `dist/` directory.

If you prefer to install the tools manually, download the **Build Tools for Visual Studio 2022**
installer from <https://visualstudio.microsoft.com/visual-cpp-build-tools/>, select the
**Desktop development with C++** workload, and complete the installation.  Then activate the
compiler environment before building:

```powershell
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" && python -m build'
```
