# RAZBerry Browser - Panduan Lengkap

**Versi**: 0.8.1  
**Tanggal Update**: 2026-11-24  
**Author**: RAZ Creative Studio

---

## 📖 Daftar Isi

1. [Tentang RAZBerry](#-tentang-razberry)
2. [Prasyarat Sistem](#-prasyarat-sistem)
3. [Alur Branding & Regenerasi Ikon](#-alur-branding--regenerasi-ikon)
4. [Cara Build & Menjalankan Browser](#-cara-build--menjalankan-browser)
5. [Menjalankan Website Resmi (RAZBerry Web)](#-menjalankan-website-resmi-razberry-web)
6. [Struktur Kustomisasi Tema & Tampilan](#-struktur-kustomisasi-tema--tampilan)
7. [Troubleshooting & FAQ](#-troubleshooting--faq)

---

## 🍓 Tentang RAZBerry

**RAZBerry** adalah peramban web modern tingkat enterprise yang dibangun di atas fondasi **Zen Browser** (Firefox Engine). RAZBerry menggabungkan:
- ✅ **Kekuatan Produktivitas**: Tab vertikal cerdas, multi split-view, dan pengelompokan ruang kerja (spaces) dengan folder default `"razberrys"`.
- ✅ **Tema Solid Raspberry Red**: Antarmuka solid Raspberry Red (`#C72C48`) dan Dark Berry (`#1A0508`) tanpa efek glassmorphism, blur, acrylic, maupun Windows Mica.
- ✅ **Privasi & Proteksi Mutlak**: Auto-updater upstream Zen dinonaktifkan total sehingga kustomisasi peramban tidak akan pernah tertimpa.
- ✅ **Akurasi Ikon Tingkat Rendah**: 28 slot Win32 PE Resource pada `razberry.exe` di-patch secara presisi agar Taskbar, Alt-Tab, dan Titlebar konsisten menampilkan logo RAZBerry.
- ✅ **Ekosistem Web Terintegrasi**: Terhubung ke portal resmi `https://razberry.it-raz.com` dengan welcome onboarding di `/welcome/` dan privacy policy di `/privacy-policy/`.

---

## 💻 Prasyarat Sistem

Untuk pengembangan dan proses build lokal di Windows:
1. **Node.js** (v20+ atau v25+) dan **pnpm** / **npm**.
2. **Python 3.10+** (dengan library `pefile` dan `Pillow`).
3. **PowerShell 5.1+** (atau PowerShell Core).
4. **Git for Windows**.

---

## 🎨 Alur Branding & Regenerasi Ikon

Semua aset visual dan logo RAZBerry dikelola melalui skrip otomatisasi [`RAZGenerateIcons.ps1`](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/RAZGenerateIcons.ps1).

### Cara Memperbarui Logo:
1. Masukkan berkas logo baru berformat PNG transparan dengan nama `razberry-logo.png` di root folder.
2. Jalankan perintah:
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File .\RAZGenerateIcons.ps1
   ```
3. Skrip akan secara otomatis memproduksi seluruh ukuran PNG (16px sampai 1024px) serta multi-resolution Windows `.ico` (`firefox.ico`, `firefox64.ico`, `document.ico`, `pbmode.ico`) dan menempatkannya di:
   - `razberry/configs/branding/release/`
   - `razberry/configs/branding/twilight/`

---

## 🚀 Cara Build & Menjalankan Browser

### Metode 1: Build Otomatis Distribusi Standalone (Direkomendasikan)
Jalankan skrip build utama:
```powershell
powershell.exe -ExecutionPolicy Bypass -File .\RAZBuildBrowser.ps1
```
Skrip ini secara otomatis:
1. Menyalin engine runtime dari `C:\Program Files\Zen Browser`.
2. Melakukan rebranding executable ke `razberry.exe` dan menyelaraskan `application.ini`.
3. Menginjeksi branding FTL, properties, dan SVG ke `browser/omni.ja`.
4. Menjalankan [`RAZApplyCustomizations.py`](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/RAZApplyCustomizations.py) untuk menyuntikkan tema solid raspberry, mematikan auto-updater, mengganti default folder space menjadi `"razberrys"`, mengarahkan Welcome URL ke `https://razberry.it-raz.com/welcome/`, serta mengganti favicon SVG.
5. Menjalankan [`RAZPatchExeIcons.py`](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/RAZPatchExeIcons.py) untuk mem-patch seluruh 28 slot Win32 PE Resource icon pada `razberry.exe`.
6. Memasang ikon window native di `chrome/icons/default/` (`main-window.ico`, `default.ico`, `about.ico`).
7. Menghasilkan shortcut Windows `RAZBerry.lnk` dan batch launcher `RAZBerry.bat`.

### Cara Menjalankan:
Cukup klik ganda **`RAZBerry.lnk`** di root folder atau jalankan **`RAZBerry.bat`**.

---

## 🌐 Menjalankan Website Resmi (RAZBerry Web)

Website resmi RAZBerry berada di sub-folder `razberry-www/`.

### 1. Masuk ke direktori website:
```bash
cd razberry-www
```

### 2. Install dependensi & jalankan server lokal:
```bash
pnpm install
pnpm dev
```
Buka browser pada alamat `http://localhost:3000` untuk melihat:
- **Landing Page**: `http://localhost:3000/`
- **Welcome Page**: `http://localhost:3000/welcome`
- **Privacy Policy**: `http://localhost:3000/privacy-policy`

---

## 🎨 Struktur Kustomisasi Tema & Tampilan

- **Welcome Screen Onboarding Dual Logo**:
  - Teks sambutan: *"Welcome to RAZBerry Browser By RAZ Creative Studio"*.
  - Menampilkan **Logo RAZBerry** dan **Logo RAZ Creative Studio** transparan tanpa latar belakang (`RAZCreateTransparentLogo.py`).
  - Latar belakang layar onboarding berupa gradien radial solid Dark Berry (`#23060c` ke `#120305`) tanpa video background.
  - Tombol mulai (`#zen-welcome-start-button`) berbalut warna aksen Raspberry Red (`#C72C48`) dengan border radius oval dan shadow lembut.
- **Palet Warna Raspberry Red**:
  - Primary Accent: `#C72C48`
  - Dark Berry Canvas: `#120305` & `#1A0508`
  - Tertiary / Urlbar: `#26080F`
  - Text Light: `#F8BBD9`
- **Penonaktifan Glassmorphism**:
  - `widget.windows.mica = false`
  - `zen.theme.acrylic-sidebar = false`
  - `zen.theme.acrylic-urlbar = false`
  - `backdrop-filter: none !important` diinjeksikan langsung ke stylesheet inti.

---

## ❓ Troubleshooting & FAQ

1. **Bagaimana jika browser ter-update otomatis dan menimpa branding?**  
   Hal ini sudah dicegah 100% pada versi 0.4.0 melalui penguncian `update-settings.ini` dan preferensi `app.update.enabled = false`. Jika ingin rebuild ulang, cukup jalankan `powershell -ExecutionPolicy Bypass -File .\RAZBuildBrowser.ps1`.

2. **Ikon di taskbar Windows masih menampilkan ikon lama?**  
   Windows meng-cache icon pada explorer. Jika shortcut lama ter-pin di taskbar, unpin terlebih dahulu shortcut lama, lalu jalankan `RAZBerry.lnk` yang baru dan pin kembali ke taskbar. Seluruh resource `RT_ICON` pada `razberry.exe` sudah 100% menggunakan logo RAZBerry.
