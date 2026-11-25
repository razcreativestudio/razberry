<#
 ==============================================================================
 Metadata & Header File
 Proyek        : RAZBerry Browser
 File          : RAZBuildBrowser.ps1
 Dibuat Pada   : 2026-11-24
 Author        : RAZ Creative Studio
 Deskripsi     : Skrip otomatisasi build & packaging distribusi standalone/portable
                 RAZBerry Browser. Mengintegrasikan binary engine Firefox/Zen
                 dengan seluruh aset identitas, logo, konfigurasi, dan tema
                 Raspberry Red (#C72C48) milik RAZBerry.
 ==============================================================================
#>

param (
    [string]$SourceDir = "C:\Program Files\Zen Browser",
    [string]$OutputDir = "$PSScriptRoot\dist\RAZBerry"
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "  RAZBerry Browser - Build & Packaging System" -ForegroundColor Cyan
Write-Host "  Author : RAZ Creative Studio" -ForegroundColor Gray
Write-Host "  Target : $OutputDir" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Magenta

# 1. Validasi Keberadaan Source Runtime
if (-not (Test-Path $SourceDir)) {
    Write-Error "Direktori sumber '$SourceDir' tidak ditemukan!"
    exit 1
}

# 2. Persiapan Direktori Output Distribusi
if (Test-Path $OutputDir) {
    Write-Host "[1/7] Membersihkan direktori output lama..." -ForegroundColor Yellow
    Remove-Item -Path $OutputDir -Recurse -Force
}
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
Write-Host "[1/7] Direktori distribusi siap: $OutputDir" -ForegroundColor Green

# 3. Menyalin Berkas Binary Engine (Menggunakan robocopy untuk kecepatan & stabilitas)
Write-Host "[2/7] Menyalin runtime binary engine..." -ForegroundColor Yellow
$roboArgs = @(
    $SourceDir,
    $OutputDir,
    "/E",
    "/XD", "uninstall",
    "/XF", "install.log", "installation_telemetry.json",
    "/NFL", "/NDL", "/NJH", "/NJS", "/nc", "/ns", "/np"
)
& robocopy.exe @roboArgs | Out-Null
Write-Host "      Runtime binary berhasil disalin." -ForegroundColor Green

# 4. Rebranding Executable & Manifest
Write-Host "[3/7] Memperbarui executable binary dan metadata manifest..." -ForegroundColor Yellow

# Rename zen.exe -> razberry.exe
$oldExe = Join-Path $OutputDir "zen.exe"
$newExe = Join-Path $OutputDir "razberry.exe"
if (Test-Path $oldExe) {
    Move-Item -Path $oldExe -Destination $newExe -Force
}

# Update application.ini
$appIniPath = Join-Path $OutputDir "application.ini"
if (Test-Path $appIniPath) {
    $iniContent = Get-Content $appIniPath -Raw
    $iniContent = $iniContent -replace "(?m)^Vendor=.*", "Vendor=RAZ Creative Studio"
    $iniContent = $iniContent -replace "(?m)^Name=.*", "Name=RAZBerry"
    $iniContent = $iniContent -replace "(?m)^RemotingName=.*", "RemotingName=razberry"
    $iniContent = $iniContent -replace "(?m)^Version=.*", "Version=1.0.0"
    $iniContent = $iniContent -replace "(?m)^Profile=.*", "Profile=razberry"
    Set-Content -Path $appIniPath -Value $iniContent -Encoding UTF8
    
    # Salin juga ke browser/application.ini agar dibaca engine
    $browserDir = Join-Path $OutputDir "browser"
    if (Test-Path $browserDir) {
        Copy-Item -Path $appIniPath -Destination (Join-Path $browserDir "application.ini") -Force
    }
}

# Update VisualElements
$brandingSrcDir = "$PSScriptRoot\razberry\configs\branding\release"
$visualElementsDir = Join-Path $OutputDir "browser\VisualElements"
if ((Test-Path $visualElementsDir) -and (Test-Path $brandingSrcDir)) {
    Copy-Item (Join-Path $brandingSrcDir "VisualElements_150.png") -Destination $visualElementsDir -Force
    Copy-Item (Join-Path $brandingSrcDir "VisualElements_70.png") -Destination $visualElementsDir -Force
}

# 5. Injeksi Branding & Tema ke Dalam browser/omni.ja
Write-Host "[4/7] Menginjeksi aset branding & palet warna ke dalam omni.ja..." -ForegroundColor Yellow
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$omniPath = Join-Path $OutputDir "browser\omni.ja"
if (Test-Path $omniPath) {
    $zip = [System.IO.Compression.ZipFile]::Open($omniPath, [System.IO.Compression.ZipArchiveMode]::Update)

    # Fungsi pembantu untuk replace entry dalam zip
    function Set-ZipTextEntry {
        param ($zipArchive, $entryPath, $textContent)
        $oldEntry = $zipArchive.GetEntry($entryPath)
        if ($oldEntry) { $oldEntry.Delete() }
        $newEntry = $zipArchive.CreateEntry($entryPath, [System.IO.Compression.CompressionLevel]::Optimal)
        # Gunakan UTF8 tanpa BOM ($false) agar parser Mozilla Fluent tidak error pada -brand-shorter-name
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        $writer = New-Object System.IO.StreamWriter($newEntry.Open(), $utf8NoBom)
        $writer.Write($textContent)
        $writer.Flush()
        $writer.Close()
    }

    function Set-ZipBinaryEntry {
        param ($zipArchive, $entryPath, $sourceFilePath)
        if (-not (Test-Path $sourceFilePath)) { return }
        $oldEntry = $zipArchive.GetEntry($entryPath)
        if ($oldEntry) { $oldEntry.Delete() }
        $newEntry = $zipArchive.CreateEntry($entryPath, [System.IO.Compression.CompressionLevel]::Optimal)
        $entryStream = $newEntry.Open()
        $fileStream = [System.IO.File]::OpenRead($sourceFilePath)
        $fileStream.CopyTo($entryStream)
        $fileStream.Close()
        $entryStream.Flush()
        $entryStream.Close()
    }

    # Brand FTL Definition untuk RAZBerry
    $brandFtlContent = @"
-brand-shorter-name = RAZBerry
-brand-short-name = RAZBerry
-brand-full-name = RAZBerry Browser
-brand-product-name = RAZBerry Browser
-vendor-short-name = RAZ Creative Studio
trademarkInfo = { " " }
"@

    # Injeksi brand.ftl ke seluruh bahasa yang tersedia di omni.ja
    $brandFtlEntries = @($zip.Entries | Where-Object { $_.FullName -like "localization/*/branding/brand.ftl" } | ForEach-Object { $_.FullName })
    foreach ($ftlPath in $brandFtlEntries) {
        Set-ZipTextEntry -zipArchive $zip -entryPath $ftlPath -textContent $brandFtlContent
    }

    # Injeksi brand.properties
    $brandPropContent = @"
brandShorterName=RAZBerry
brandShortName=RAZBerry
brandFullName=RAZBerry Browser
vendorShortName=RAZ Creative Studio
"@
    $brandPropEntries = @($zip.Entries | Where-Object { $_.FullName -like "chrome/*/locale/branding/brand.properties" } | ForEach-Object { $_.FullName })
    foreach ($propPath in $brandPropEntries) {
        Set-ZipTextEntry -zipArchive $zip -entryPath $propPath -textContent $brandPropContent
    }

    # Injeksi Warna Tema Utama ke zen-theme.css
    $themeCssEntry = $zip.GetEntry("chrome/browser/content/browser/zen-styles/zen-theme.css")
    if ($themeCssEntry) {
        $reader = New-Object System.IO.StreamReader($themeCssEntry.Open(), [System.Text.Encoding]::UTF8)
        $themeCss = $reader.ReadToEnd()
        $reader.Close()

        # Override primary color menjadi Raspberry Red #C72C48
        $themeCss = $themeCss -replace "--zen-primary-color:\s*AccentColor;", "--zen-primary-color: #C72C48;"
        Set-ZipTextEntry -zipArchive $zip -entryPath "chrome/browser/content/browser/zen-styles/zen-theme.css" -textContent $themeCss
    }

    # Injeksi Gambar & SVG Logo Baru
    $brandingRelease = "$PSScriptRoot\razberry\configs\branding\release"
    $brandingContent = "$brandingRelease\content"

    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/about-logo.png" -sourceFilePath "$brandingContent\about-logo.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/about-logo@2x.png" -sourceFilePath "$brandingContent\about-logo@2x.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/about-logo-private.png" -sourceFilePath "$brandingContent\about-logo-private.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/about-logo-private@2x.png" -sourceFilePath "$brandingContent\about-logo-private@2x.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/about-logo.svg" -sourceFilePath "$brandingContent\about-logo.svg"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/about-wordmark.svg" -sourceFilePath "$brandingContent\about-wordmark.svg"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/firefox-wordmark.svg" -sourceFilePath "$brandingContent\firefox-wordmark.svg"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/logo-razberry.png" -sourceFilePath "$brandingContent\logo-razberry.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/about.png" -sourceFilePath "$brandingContent\about-logo.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/icon16.png" -sourceFilePath "$brandingRelease\logo16.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/icon32.png" -sourceFilePath "$brandingRelease\logo32.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/icon48.png" -sourceFilePath "$brandingRelease\logo48.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/icon64.png" -sourceFilePath "$brandingRelease\logo64.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/icon128.png" -sourceFilePath "$brandingRelease\logo128.png"
    Set-ZipBinaryEntry -zipArchive $zip -entryPath "chrome/browser/content/branding/document.ico" -sourceFilePath "$brandingRelease\document.ico"

    $zip.Dispose()
    Write-Host "      Injeksi omni.ja selesai dengan sukses." -ForegroundColor Green
}

# 6. Preferensi Default & Kustomisasi RAZBerry (Update, Tema Solid Raspberry, URLs, Space Folder, Welcome Screen, Brand Logos)
Write-Host "[5/7] Menerapkan kustomisasi sistem, tema solid raspberry, welcome screen, & deployment logo..." -ForegroundColor Yellow
if (Test-Path "$PSScriptRoot\RAZCreateTransparentLogo.py") {
    & python.exe "$PSScriptRoot\RAZCreateTransparentLogo.py"
}
if (Test-Path "$PSScriptRoot\RAZDeployLogos.py") {
    & python.exe "$PSScriptRoot\RAZDeployLogos.py"
}
& python.exe "$PSScriptRoot\RAZApplyCustomizations.py"

# 7. Patching Embedded PE Resource Icons & Window Icons
Write-Host "[6/7] Melakukan patching Win32 PE icons & window icons..." -ForegroundColor Yellow
& python.exe "$PSScriptRoot\RAZPatchExeIcons.py"

# Salin Ikon Aplikasi ke Root Direktori Build
$rootIco = Join-Path $OutputDir "razberry.ico"
Copy-Item "$brandingSrcDir\firefox.ico" -Destination $rootIco -Force

# Salin juga ikon window ke chrome/icons/default agar dialog XUL menggunakan ikon RAZBerry
$iconDirs = @(
    (Join-Path $OutputDir "chrome\icons\default"),
    (Join-Path $OutputDir "browser\chrome\icons\default")
)
foreach ($iDir in $iconDirs) {
    if (-not (Test-Path $iDir)) { New-Item -ItemType Directory -Path $iDir -Force | Out-Null }
    Copy-Item $rootIco -Destination (Join-Path $iDir "main-window.ico") -Force
    Copy-Item $rootIco -Destination (Join-Path $iDir "default.ico") -Force
    Copy-Item $rootIco -Destination (Join-Path $iDir "about.ico") -Force
}

# 8. Membuat Shortcut Windows & Batch Launcher
Write-Host "[7/7] Membuat shortcut RAZBerry.lnk dan launcher..." -ForegroundColor Yellow
$wsh = New-Object -ComObject WScript.Shell
$shortcutPath = Join-Path $OutputDir "RAZBerry.lnk"
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $newExe
$shortcut.Arguments = "-app browser\application.ini"
$shortcut.WorkingDirectory = $OutputDir
$shortcut.IconLocation = (Join-Path $OutputDir "razberry.ico")
$shortcut.Description = "RAZBerry Browser oleh RAZ Creative Studio"
$shortcut.Save()

# Shortcut di root proyek juga agar mudah diakses
$rootShortcutPath = "$PSScriptRoot\RAZBerry.lnk"
$rootShortcut = $wsh.CreateShortcut($rootShortcutPath)
$rootShortcut.TargetPath = $newExe
$rootShortcut.Arguments = "-app browser\application.ini"
$rootShortcut.WorkingDirectory = $OutputDir
$rootShortcut.IconLocation = (Join-Path $OutputDir "razberry.ico")
$rootShortcut.Description = "RAZBerry Browser oleh RAZ Creative Studio"
$rootShortcut.Save()

# Batch Launcher di folder output
$distBatPath = Join-Path $OutputDir "RAZBerry.bat"
$batContent = "@echo off`r`nstart `"`" `"%~dp0razberry.exe`" -app browser\application.ini %*"
Set-Content -Path $distBatPath -Value $batContent -Encoding ASCII

# 9. Menjalankan Rebranding Menyeluruh Teks Zen -> RAZBerry
Write-Host "[8/11] Menjalankan RAZRebrandAllZenText (Rebranding Zen Mods, URL Bar, UI text)..." -ForegroundColor Yellow
python "$PSScriptRoot\RAZRebrandAllZenText.py"

# 10. Menerapkan Tema Solid Raspberry Pink (Light & Dark Mode Accessible)
Write-Host "[9/11] Menjalankan RAZApplyPinkTheme (Accessible Pink Theme, WCAG AA/AAA)..." -ForegroundColor Yellow
python "$PSScriptRoot\RAZApplyPinkTheme.py"

# 11. Menjalankan Patch about:support & AppConstants (Name: RAZBerry & Matikan Updater Subsystem)
Write-Host "[10/11] Menjalankan RAZPatchAboutSupport (Name: RAZBerry di about:support & MOZ_UPDATER: false)..." -ForegroundColor Yellow
python "$PSScriptRoot\RAZPatchAboutSupport.py"

# Pastikan preferensi default browser/defaults/preferences terpasang
$browserPrefDir = Join-Path $OutputDir "browser\defaults\preferences"
if (-not (Test-Path $browserPrefDir)) { New-Item -ItemType Directory -Path $browserPrefDir -Force | Out-Null }
$prefSrc = "$OutputDir\defaults\pref\razberry-prefs.js"
if (Test-Path $prefSrc) {
    Copy-Item $prefSrc -Destination (Join-Path $browserPrefDir "razberry-prefs.js") -Force
}

# 12. Menjalankan Perbaikan Visual & Sistem RAZFixVisualIssues
Write-Host "[11/11] Menjalankan RAZFixVisualIssues (Cache flush, FTL fallback, Policies)..." -ForegroundColor Yellow
python "$PSScriptRoot\RAZFixVisualIssues.py"

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "  ✅ BUILD RAZBERRY BROWSER SUKSES DIPRODUKSI!" -ForegroundColor Green
Write-Host "  Lokasi Eksekutabel : $newExe" -ForegroundColor Cyan
Write-Host "  Shortcut Utama     : $rootShortcutPath" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Magenta
