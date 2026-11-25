# ==============================================================================
# RAZBuildInstaller.ps1
# Skrip Build Standalone RAZBerrySetup.exe & razberry.installer.exe
# Menggunakan .NET Framework C# Compiler (csc.exe) + Embedded Zip Payload
# Author: RAZ Creative Studio
# Timestamp: 2026-11-25
# ==============================================================================

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RootDir

Write-Host "[RAZ-INSTALLER] Memulai proses kompilasi RAZBerrySetup.exe..." -ForegroundColor Magenta

$DistBrowserDir = Join-Path $RootDir "dist\RAZBerry"
$PayloadZip     = Join-Path $RootDir "dist\razberry_payload_temp.zip"
$OutputSetupExe = Join-Path $RootDir "dist\RAZBerrySetup.exe"
$OutputAliasExe = Join-Path $RootDir "dist\razberry.installer.exe"
$LogoBerry      = Join-Path $RootDir "razberry-www\public\logo-razberry.png"
$LogoStudio     = Join-Path $RootDir "razberry-www\public\raz-creative-studio.png"
$IconFile       = Join-Path $RootDir "dist\RAZBerry\RAZBerry.ico"
$SourceCs       = Join-Path $RootDir "RAZSetupWizard.cs"
$CscExe         = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"

if (-not (Test-Path $DistBrowserDir)) { throw "Folder dist\RAZBerry tidak ditemukan!" }
if (-not (Test-Path $CscExe)) { throw "Compiler .NET Framework csc.exe tidak ditemukan!" }

# 1. Buat arsip ZIP payload dari dist\RAZBerry jika belum ada atau perbarui
Write-Host "[RAZ-INSTALLER] Mengompresi berkas browser dist\RAZBerry menjadi payload..." -ForegroundColor Cyan
if (-not (Test-Path $PayloadZip)) {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        $DistBrowserDir,
        $PayloadZip,
        [System.IO.Compression.CompressionLevel]::Optimal,
        $false
    )
}

$ZipSizeMB = [math]::Round(((Get-Item $PayloadZip).Length / 1MB), 2)
Write-Host "[RAZ-INSTALLER] Payload terkompresi: $ZipSizeMB MB" -ForegroundColor Green

# 2. Compile RAZSetupWizard.cs -> RAZBerrySetup.exe dengan embedded icon & resources
Write-Host "[RAZ-INSTALLER] Mengompilasi RAZSetupWizard.cs -> dist\RAZBerrySetup.exe..." -ForegroundColor Cyan
$cscArgs = @(
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
    "/resource:$LogoBerry,LogoRazBerry.png",
    "/resource:$LogoStudio,LogoRazStudio.png",
    "$SourceCs"
)
& $CscExe @cscArgs

if ($LASTEXITCODE -ne 0) {
    throw "Kompilasi csc.exe gagal!"
}

# 3. Salin alias razberry.installer.exe (sesuai nama asset download website)
Copy-Item -Path $OutputSetupExe -Destination $OutputAliasExe -Force

# 4. Bersihkan file payload zip sementara
if (Test-Path $PayloadZip) { Remove-Item $PayloadZip -Force }

$FinalSizeMB = [math]::Round(((Get-Item $OutputSetupExe).Length / 1MB), 2)
Write-Host "[RAZ-INSTALLER] SUKSES! Installer siap: $OutputSetupExe ($FinalSizeMB MB)" -ForegroundColor Green
Write-Host "[RAZ-INSTALLER] Alias release siap: $OutputAliasExe" -ForegroundColor Green
