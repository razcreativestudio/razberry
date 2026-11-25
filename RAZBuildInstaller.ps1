# ==============================================================================
# RAZBuildInstaller.ps1
# Skrip Build Standalone Uninstall RAZBerry.exe, RAZBerrySetup.exe,
# dan razberry.installer.exe menggunakan .NET Framework C# Compiler (csc.exe)
# Author: RAZ Creative Studio
# Timestamp: 2026-11-25
# ==============================================================================

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RootDir

Write-Host "[RAZ-INSTALLER] Memulai proses kompilasi Uninstaller & Setup Installer..." -ForegroundColor Magenta

$DistBrowserDir   = Join-Path $RootDir "dist\RAZBerry"
$PayloadZip       = Join-Path $RootDir "dist\razberry_payload_temp.zip"
$OutputUninstExe  = Join-Path $RootDir "dist\Uninstall RAZBerry.exe"
$OutputSetupExe   = Join-Path $RootDir "dist\RAZBerrySetup.exe"
$OutputAliasExe   = Join-Path $RootDir "dist\razberry.installer.exe"
$LogoBerry        = Join-Path $RootDir "razberry-www\public\logo-razberry.png"
$LogoStudio       = Join-Path $RootDir "razberry-www\public\raz-creative-studio.png"
$IconFile         = Join-Path $RootDir "dist\RAZBerry\RAZBerry.ico"
$SourceSetupCs    = Join-Path $RootDir "RAZSetupWizard.cs"
$SourceUninstCs   = Join-Path $RootDir "RAZUninstaller.cs"
$CscExe           = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"

if (-not (Test-Path $DistBrowserDir)) { throw "Folder dist\RAZBerry tidak ditemukan!" }
if (-not (Test-Path $CscExe)) { throw "Compiler .NET Framework csc.exe tidak ditemukan!" }

# 1. Compile RAZUninstaller.cs -> dist\Uninstall RAZBerry.exe
Write-Host "[RAZ-INSTALLER] Mengompilasi RAZUninstaller.cs -> dist\Uninstall RAZBerry.exe..." -ForegroundColor Cyan
$uninstArgs = @(
    "/nologo",
    "/target:winexe",
    "/platform:x64",
    "/optimize+",
    "/win32icon:$IconFile",
    "/out:$OutputUninstExe",
    "/reference:System.Windows.Forms.dll",
    "/reference:System.Drawing.dll",
    "/resource:$LogoBerry,LogoRazBerry.png",
    "/resource:$LogoStudio,LogoRazStudio.png",
    "$SourceUninstCs"
)
& $CscExe @uninstArgs
if ($LASTEXITCODE -ne 0) { throw "Kompilasi Uninstall RAZBerry.exe gagal!" }

# Salin juga ke dist\RAZBerry agar ikut tersedia di instalasi portabel
Copy-Item -Path $OutputUninstExe -Destination (Join-Path $DistBrowserDir "Uninstall RAZBerry.exe") -Force

# 2. Buat arsip ZIP payload dari dist\RAZBerry
Write-Host "[RAZ-INSTALLER] Mengompresi berkas browser dist\RAZBerry menjadi payload..." -ForegroundColor Cyan
if (Test-Path $PayloadZip) { Remove-Item $PayloadZip -Force }

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $DistBrowserDir,
    $PayloadZip,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $false
)

$ZipSizeMB = [math]::Round(((Get-Item $PayloadZip).Length / 1MB), 2)
Write-Host "[RAZ-INSTALLER] Payload terkompresi: $ZipSizeMB MB" -ForegroundColor Green

# 3. Compile RAZSetupWizard.cs -> dist\RAZBerrySetup.exe
Write-Host "[RAZ-INSTALLER] Mengompilasi RAZSetupWizard.cs -> dist\RAZBerrySetup.exe..." -ForegroundColor Cyan
$setupArgs = @(
    "/nologo",
    "/target:winexe",
    "/platform:x64",
    "/optimize+",
    "/win32icon:$IconFile",
    "/out:$OutputSetupExe",
    "/reference:System.Windows.Forms.dll",
    "/reference:System.Drawing.dll",
    "/reference:System.IO.Compression.dll",
    "/reference:System.IO.Compression.FileSystem.dll",
    "/resource:$PayloadZip,RAZBerryPayload.zip",
    "/resource:$OutputUninstExe,UninstallRAZBerry.exe",
    "/resource:$LogoBerry,LogoRazBerry.png",
    "/resource:$LogoStudio,LogoRazStudio.png",
    "$SourceSetupCs"
)
& $CscExe @setupArgs
if ($LASTEXITCODE -ne 0) { throw "Kompilasi RAZBerrySetup.exe gagal!" }

# 4. Salin alias razberry.installer.exe & bersihkan zip sementara
Copy-Item -Path $OutputSetupExe -Destination $OutputAliasExe -Force
if (Test-Path $PayloadZip) { Remove-Item $PayloadZip -Force }

$FinalSizeMB = [math]::Round(((Get-Item $OutputSetupExe).Length / 1MB), 2)
Write-Host "[RAZ-INSTALLER] SUKSES! Uninstaller : $OutputUninstExe" -ForegroundColor Green
Write-Host "[RAZ-INSTALLER] SUKSES! Setup EXE   : $OutputSetupExe ($FinalSizeMB MB)" -ForegroundColor Green
Write-Host "[RAZ-INSTALLER] SUKSES! Release EXE : $OutputAliasExe" -ForegroundColor Green
