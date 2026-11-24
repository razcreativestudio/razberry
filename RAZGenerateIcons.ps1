<#
 ==============================================================================
 Metadata & Header File
 Proyek        : RAZBerry Browser (Zen Browser Rebranding)
 File          : RAZGenerateIcons.ps1
 Dibuat Pada   : 2026-11-24
 Deskripsi     : Skrip otomatisasi untuk me-resize logo sumber RAZBerry ke
                 berbagai dimensi ikon (PNG & multi-resolution ICO) dan
                 menyimpannya ke direktori branding release & twilight.
 ==============================================================================
#>

Add-Type -AssemblyName System.Drawing

# Path file logo utama transparan (500x500 ARGB)
$sourceLogoPath = "razberry-logo.png"

if (-not (Test-Path $sourceLogoPath)) {
    Write-Error "File logo sumber '$sourceLogoPath' tidak ditemukan!"
    exit 1
}

Write-Host "[RAZBerry] Membaca logo sumber: $sourceLogoPath..." -ForegroundColor Cyan
$sourceImg = [System.Drawing.Image]::FromFile((Resolve-Path $sourceLogoPath).Path)

# Fungsi edukatif untuk me-resize gambar dengan kualitas interpolasi tinggi (Bicubic)
function Resize-Image {
    param (
        [System.Drawing.Image]$img,
        [int]$width,
        [int]$height
    )
    $destRect = New-Object System.Drawing.Rectangle(0, 0, $width, $height)
    $destImage = New-Object System.Drawing.Bitmap($width, $height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $destImage.SetResolution($img.HorizontalResolution, $img.VerticalResolution)

    $graphics = [System.Drawing.Graphics]::FromImage($destImage)
    $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceOver
    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

    $wrapMode = New-Object System.Drawing.Imaging.ImageAttributes
    $wrapMode.SetWrapMode([System.Drawing.Drawing2D.WrapMode]::TileFlipXY)
    $graphics.DrawImage($img, $destRect, 0, 0, $img.Width, $img.Height, [System.Drawing.GraphicsUnit]::Pixel, $wrapMode)
    $graphics.Dispose()

    return $destImage
}

# Fungsi untuk menghasilkan file ICO modern berbasis format payload PNG multi-resolusi
function New-IcoFile {
    param (
        [string]$outputPath,
        [int[]]$sizes,
        [System.Drawing.Image]$source
    )
    
    $pngBytesList = @()
    foreach ($sz in $sizes) {
        $resized = Resize-Image -img $source -width $sz -height $sz
        $ms = New-Object System.IO.MemoryStream
        $resized.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
        $pngBytesList += ,@($sz, $ms.ToArray())
        $ms.Dispose()
        $resized.Dispose()
    }

    $fs = [System.IO.File]::Create($outputPath)
    $bw = New-Object System.IO.BinaryWriter($fs)

    # Tulis ICO Header: Reserved (2 bytes), Type (2 bytes = 1 for icon), Count (2 bytes)
    $bw.Write([uint16]0)
    $bw.Write([uint16]1)
    $bw.Write([uint16]$pngBytesList.Count)

    # Hitung offset data gambar pertama (Header 6 bytes + 16 bytes per item)
    $offset = 6 + (16 * $pngBytesList.Count)

    # Tulis Entry Directory
    foreach ($item in $pngBytesList) {
        $sz = $item[0]
        $bytes = $item[1]
        
        $wByte = if ($sz -ge 256) { [byte]0 } else { [byte]$sz }
        $hByte = if ($sz -ge 256) { [byte]0 } else { [byte]$sz }

        $bw.Write($wByte)                 # Width
        $bw.Write($hByte)                 # Height
        $bw.Write([byte]0)                # Colors in palette
        $bw.Write([byte]0)                # Reserved
        $bw.Write([uint16]1)              # Color planes
        $bw.Write([uint16]32)             # Bits per pixel
        $bw.Write([uint32]$bytes.Length)  # Image data size
        $bw.Write([uint32]$offset)        # Image data offset

        $offset += $bytes.Length
    }

    # Tulis Raw PNG Payload
    foreach ($item in $pngBytesList) {
        $bytes = $item[1]
        $bw.Write($bytes)
    }

    $bw.Flush()
    $bw.Close()
    $fs.Close()
    Write-Host "  -> Generated ICO: $outputPath ($($sizes -join ', ') px)" -ForegroundColor Green
}

# Target folder branding
$brandingDirs = @(
    "razberry\configs\branding\release",
    "razberry\configs\branding\twilight"
)

# Ukuran logo PNG standar yang dibutuhkan browser
$pngSizes = @(16, 22, 24, 32, 48, 64, 128, 256, 512, 1024)

foreach ($dir in $brandingDirs) {
    Write-Host "[RAZBerry] Memproses direktori: $dir" -ForegroundColor Yellow

    # Generate setiap ukuran PNG
    foreach ($s in $pngSizes) {
        $bmp = Resize-Image -img $sourceImg -width $s -height $s
        $targetFile = Join-Path $dir "logo$s.png"
        $bmp.Save($targetFile, [System.Drawing.Imaging.ImageFormat]::Png)
        $bmp.Dispose()
    }

    # Generate logo.png dan logo-mac.png (1024x1024)
    $bmp1024 = Resize-Image -img $sourceImg -width 1024 -height 1024
    $bmp1024.Save((Join-Path $dir "logo.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp1024.Save((Join-Path $dir "logo-mac.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp1024.Save((Join-Path $dir "VisualElements_150.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp1024.Save((Join-Path $dir "VisualElements_70.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp1024.Dispose()

    # Generate Content Logos (About Page)
    $contentDir = Join-Path $dir "content"
    if (Test-Path $contentDir) {
        $aboutLogo512 = Resize-Image -img $sourceImg -width 512 -height 512
        $aboutLogo512.Save((Join-Path $contentDir "about-logo.png"), [System.Drawing.Imaging.ImageFormat]::Png)
        $aboutLogo512.Save((Join-Path $contentDir "about-logo-private.png"), [System.Drawing.Imaging.ImageFormat]::Png)
        $aboutLogo512.Dispose()

        $aboutLogo1024 = Resize-Image -img $sourceImg -width 1024 -height 1024
        $aboutLogo1024.Save((Join-Path $contentDir "about-logo@2x.png"), [System.Drawing.Imaging.ImageFormat]::Png)
        $aboutLogo1024.Save((Join-Path $contentDir "about-logo-private@2x.png"), [System.Drawing.Imaging.ImageFormat]::Png)
        $aboutLogo1024.Dispose()
    }

    # Generate File ICO (Multi-Resolution 16, 24, 32, 48, 64, 128, 256)
    $icoFiles = @(
        "firefox.ico",
        "firefox64.ico",
        "document.ico",
        "document_pdf.ico",
        "pbmode.ico"
    )
    $icoSizes = @(16, 24, 32, 48, 64, 128, 256)
    foreach ($ico in $icoFiles) {
        $icoPath = Join-Path $dir $ico
        New-IcoFile -outputPath $icoPath -sizes $icoSizes -source $sourceImg
    }
}

$sourceImg.Dispose()
Write-Host "[RAZBerry] Pembuatan semua aset ikon sukses!" -ForegroundColor Green
