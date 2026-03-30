<#
.SYNOPSIS
    Bootstrap script for the pyedb-core developer environment on Windows.

.DESCRIPTION
    1. Checks for Microsoft C++ Build Tools (required to compile the pybind11 extension).
    2. Installs them automatically via winget if they are not present.
    3. Activates the 64-bit MSVC environment (vcvars64.bat) in a cmd sub-shell.
    4. Runs `python -m build` inside that sub-shell so CMake finds the compiler.

.EXAMPLE
    # From the repository root, in PowerShell:
    .\scripts\bootstrap.ps1

.EXAMPLE
    # Pass extra arguments straight through to `python -m build`:
    .\scripts\bootstrap.ps1 --no-isolation

.EXAMPLE
    # Compile the C++ extension in Debug mode:
    .\scripts\bootstrap.ps1 -DebugBuild
#>

param(
    # When specified, the C++ extension is compiled in Debug mode instead of Release.
    [switch] $DebugBuild,

    # Any additional arguments are forwarded verbatim to `python -m build`.
    [Parameter(ValueFromRemainingArguments)]
    [string[]] $BuildArgs
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path $PSScriptRoot -Parent

# ---------------------------------------------------------------------------
# Helper: compute a 16-hex-char SHA-256 fingerprint of the C++ source tree
# (deps/*.cpp, deps/*.h, CMakeLists.txt) so that the compiled .pyd can be
# cached and reused across builds without recompilation.
# ---------------------------------------------------------------------------
function Get-SourceHash {
    $files = @(
        Get-ChildItem (Join-Path $repoRoot 'deps') -Include '*.cpp','*.h' -Recurse
        Get-Item (Join-Path $repoRoot 'CMakeLists.txt')
    ) | Sort-Object FullName

    $sha = [Security.Cryptography.SHA256]::Create()
    foreach ($f in $files) {
        $bytes = [IO.File]::ReadAllBytes($f.FullName)
        $null = $sha.TransformBlock($bytes, 0, $bytes.Length, $null, 0)
    }
    $null = $sha.TransformFinalBlock(@(), 0, 0)
    return ([BitConverter]::ToString($sha.Hash) -replace '-').ToLower().Substring(0, 16)
}

# ---------------------------------------------------------------------------
# Helper: extract rpc_executor*.pyd from the most recently built wheel in
# dist/ and save it to the given cache directory.
# ---------------------------------------------------------------------------
function Save-PydToCache {
    param([string]$CacheDir)

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $wheel = Get-ChildItem (Join-Path $repoRoot 'dist') -Filter '*.whl' -ErrorAction SilentlyContinue |
             Sort-Object LastWriteTime -Descending |
             Select-Object -First 1
    if (-not $wheel) { Write-Warning "No wheel found in dist/ - skipping cache."; return }

    $zip = [IO.Compression.ZipFile]::OpenRead($wheel.FullName)
    try {
        $entry = $zip.Entries | Where-Object { $_.Name -match '^rpc_executor.*\.pyd$' } |
                 Select-Object -First 1
        if (-not $entry) { Write-Warning "rpc_executor*.pyd not found in wheel - skipping cache."; return }

        $null = New-Item -ItemType Directory -Force -Path $CacheDir
        $dest = Join-Path $CacheDir $entry.Name
        $src = $entry.Open()
        $dst = [IO.File]::Create($dest)
        $src.CopyTo($dst)
        $dst.Dispose()
        $src.Dispose()
        Write-Host "Cached: $dest" -ForegroundColor DarkGreen
    } finally {
        $zip.Dispose()
    }
}

# ---------------------------------------------------------------------------
# Helper: locate vcvars64.bat using vswhere (the canonical tool) and then
# fall back to a set of well-known hard-coded paths.
# ---------------------------------------------------------------------------
function Find-Vcvars64 {
    # vswhere is installed by every Visual Studio / Build Tools installer.
    $vswhere = Join-Path ${env:ProgramFiles(x86)} `
                         "Microsoft Visual Studio\Installer\vswhere.exe"

    if (Test-Path $vswhere) {
        $installDir = & $vswhere -latest -products * `
            -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 `
            -property installationPath 2>$null |
            Select-Object -First 1

        if ($installDir) {
            $candidate = Join-Path $installDir "VC\Auxiliary\Build\vcvars64.bat"
            if (Test-Path $candidate) { return $candidate }
        }
    }

    # Hard-coded fallbacks covering BuildTools and full IDE installs.
    $fallbacks = @(
        "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    )
    foreach ($path in $fallbacks) {
        if (Test-Path $path) { return $path }
    }

    return $null
}

# ---------------------------------------------------------------------------
# 1. Compute the C++ source fingerprint and check the .pyd cache.
#    Cache key: (Python ABI tag) + (SHA-256 of deps C++ sources + CMakeLists).
#    Hit  -> set PREBUILT_PYD env var; CMakeLists.txt uses LANGUAGES NONE and
#            installs the file directly - no compiler needed.
#    Miss -> run a full MSVC-activated build, then save the .pyd to cache.
# ---------------------------------------------------------------------------
$pythonTag  = & python -c "import sys; print('cp{}{}'.format(*sys.version_info[:2]))" 2>$null
if (-not $pythonTag) { $pythonTag = 'cpXX' }

$buildType  = if ($DebugBuild) { 'Debug' } else { 'Release' }
$sourceHash = Get-SourceHash
$cacheDir   = Join-Path $repoRoot ".pyd-cache\$pythonTag\$buildType\$sourceHash"
$cachedPyd  = Get-ChildItem $cacheDir -Filter 'rpc_executor*.pyd' -ErrorAction SilentlyContinue |
              Select-Object -First 1

if ($cachedPyd) {
    # ------------------------------------------------------------------
    # Cache hit: PREBUILT_PYD tells CMakeLists.txt to install the cached
    # file directly (LANGUAGES NONE - no C++ compiler needed).
    # ------------------------------------------------------------------
    Write-Host ""
    Write-Host "Cache hit [$sourceHash] ($buildType) - skipping C++ compilation." -ForegroundColor Green
    Write-Host "Using: $($cachedPyd.FullName)" -ForegroundColor DarkGray
    Write-Host ""

    $env:PREBUILT_PYD = $cachedPyd.FullName
    try {
        Write-Host "Running: python -m build --config-setting cmake.build-type=$buildType $($BuildArgs -join ' ')" -ForegroundColor Cyan
        Write-Host ""
        & python -m build --config-setting "cmake.build-type=$buildType" @BuildArgs
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Build failed (exit code $LASTEXITCODE)."
            exit $LASTEXITCODE
        }
    } finally {
        Remove-Item Env:PREBUILT_PYD -ErrorAction SilentlyContinue
    }

} else {
    # ------------------------------------------------------------------
    # Cache miss: full C++ compilation - MSVC required.
    # ------------------------------------------------------------------
    Remove-Item Env:PREBUILT_PYD -ErrorAction SilentlyContinue

    Write-Host ""
    Write-Host "Cache miss [$sourceHash] ($buildType) - full C++ compilation required." -ForegroundColor Yellow

    # ---------------------------------------------------------------------------
    # 2. Ensure MSVC Build Tools are installed.
    # ---------------------------------------------------------------------------
    $vcvars = Find-Vcvars64

    if (-not $vcvars) {
        Write-Host ""
        Write-Host "Microsoft C++ Build Tools not found." -ForegroundColor Yellow
        Write-Host "Installing via winget - this may take several minutes..." -ForegroundColor Yellow
        Write-Host ""

        $winget = Get-Command winget -ErrorAction SilentlyContinue
        if (-not $winget) {
            Write-Error ("winget is not available. Please install Microsoft C++ Build Tools manually:`n" +
                         "  https://visualstudio.microsoft.com/visual-cpp-build-tools/`n" +
                         "Select the 'Desktop development with C++' workload, then re-run this script.")
            exit 1
        }

        winget install Microsoft.VisualStudio.2022.BuildTools `
            --override "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended" `
            --accept-package-agreements --accept-source-agreements

        if ($LASTEXITCODE -ne 0) {
            Write-Error "winget reported a failure (exit code $LASTEXITCODE). Please install Build Tools manually and re-run."
            exit 1
        }

        $vcvars = Find-Vcvars64
        if (-not $vcvars) {
            Write-Error ("Installation appeared to succeed but vcvars64.bat was not found.`n" +
                         "Please open a new terminal and re-run this script.")
            exit 1
        }
    }

    Write-Host ""
    Write-Host "MSVC environment: $vcvars" -ForegroundColor Green

    # ---------------------------------------------------------------------------
    # 3. Build inside a cmd sub-shell with the MSVC environment active.
    #    Environment variables set by vcvars64.bat are scoped to that process.
    #    We write a temporary .bat file because PowerShell 5.x rejects '&&'
    #    even inside quoted strings; cmd.exe handles it natively.
    # ---------------------------------------------------------------------------
    $buildCmd = "python -m build --config-setting cmake.build-type=$buildType $($BuildArgs -join ' ')".Trim()

    Write-Host "Running: $buildCmd" -ForegroundColor Cyan
    Write-Host ""

    $tmpBat = [IO.Path]::GetTempFileName() -replace '\.tmp$', '.bat'
    try {
        $batContent = "@echo off", "call `"$vcvars`"", "if errorlevel 1 exit /b 1", $buildCmd
        [IO.File]::WriteAllLines($tmpBat, $batContent, [Text.Encoding]::ASCII)
        cmd /c $tmpBat
    } finally {
        Remove-Item $tmpBat -ErrorAction SilentlyContinue
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Build failed (exit code $LASTEXITCODE)."
        exit $LASTEXITCODE
    }

    # Store the compiled .pyd for future builds.
    Save-PydToCache -CacheDir $cacheDir
}

Write-Host ""
Write-Host "Build succeeded. Wheel and sdist are in the dist/ directory." -ForegroundColor Green
