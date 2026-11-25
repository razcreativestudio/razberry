<#
 ==============================================================================
 Metadata & Header File
 Proyek        : RAZBerry Browser
 File          : RAZDeployToIDwebhost.ps1
 Dibuat Pada   : 2026-11-24
 Author        : RAZ Creative Studio
 Deskripsi     : Skrip otomatisasi build & upload razberry-www ke hosting IDwebhost
                 (Paket Tera). Mengompilasi situs statis Astro lalu mengunggahnya
                 melalui modul Python FTPS RAZDeployToIDwebhost.py.
 ==============================================================================
#>

param (
    [switch]$SkipBuild = $false
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "  RAZBerry Web - Deploy to IDwebhost Hosting" -ForegroundColor Cyan
Write-Host "  Author : RAZ Creative Studio" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Magenta

$wwwDir = Join-Path $PSScriptRoot "razberry-www"

# 1. Build Astro Website jika tidak di-skip
if (-not $SkipBuild) {
    Write-Host "[1/2] Mengompilasi razberry-www (Astro static build)..." -ForegroundColor Yellow
    Push-Location $wwwDir
    try {
        & pnpm build
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Gagal melakukan build Astro!"
            exit 1
        }
        Write-Host "      Kompilasi website sukses!" -ForegroundColor Green
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "[1/2] Melewati tahapan build (-SkipBuild aktif)..." -ForegroundColor Gray
}

# 2. Upload via Python FTPS Module
Write-Host "[2/2] Menjalankan sinkronisasi upload FTPS ke server IDwebhost..." -ForegroundColor Yellow
& python.exe "$PSScriptRoot\RAZDeployToIDwebhost.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host "============================================================" -ForegroundColor Magenta
    Write-Host "  ✅ DEPLOYMENT WEB RAZBERRY KE IDWEBHOST BERHASIL!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Magenta
}
else {
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "  ⚠️  Deployment gagal atau memerlukan konfigurasi kredensial." -ForegroundColor Yellow
    Write-Host "  Periksa file 'deploy_config.json' di direktori proyek." -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Red
}
