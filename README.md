# RAZBerry Browser

<p align="center">
  <img src="razberry-logo.png" alt="RAZBerry Logo" width="160" />
</p>

<p align="center">
  <strong>Peramban Web Modern, Produktif & Berpusat pada Privasi oleh RAZ Creative Studio</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Versi-1.1.0-D81B60.svg" alt="Versi" />
  <img src="https://img.shields.io/badge/Engine-Firefox%20%2F%20Zen-BA1257.svg" alt="Engine" />
  <img src="https://img.shields.io/badge/Build-Ready%20to%20Run-success.svg" alt="Build" />
  <img src="https://img.shields.io/badge/Website-razberry.it--raz.com-FF4081.svg" alt="Website" />
  <img src="https://img.shields.io/badge/CI%2FCD-Passing-brightgreen.svg" alt="CI/CD" />
</p>

---

## 📖 Ringkasan Proyek

**RAZBerry** adalah peramban web custom yang dirancang untuk pengguna yang mengutamakan produktivitas tinggi, kenyamanan visual, dan privasi tanpa kompromi. Berbasiskan arsitektur modern **Zen Browser** (mesin Firefox), RAZBerry menghadirkan pengalaman navigasi multi-tab cerdas dengan balutan identitas visual eksklusif bertema **Solid Raspberry Pink** (`#D81B60`) dari RAZ Creative Studio.

Peramban ini didukung oleh portal website mandiri **RAZBerry Web** (`https://razberry.it-raz.com`) yang dibangun menggunakan Astro, Tailwind CSS, dan React, mencakup halaman utama, halaman Welcome onboarding (`/welcome/`), dan Privacy Policy (`/privacy-policy/`).

---

## ✨ Fitur Unggulan

- 🍇 **Tema Solid Raspberry Pink**: Tampilan bersih, kontras tinggi, dan elegan dengan warna khas Raspberry Pink (`#D81B60` dan `#FF4081`) yang telah terverifikasi 100% lulus standar aksesibilitas WCAG AA/AAA. Seluruh efek glassmorphism, blur berlebih, transparansi, dan Windows Mica dinonaktifkan secara total.
- 🚀 **Welcome Screen Onboarding Eksklusif**: Layar sambutan awal yang elegan menampilkan judul *"Welcome to RAZBerry Browser By RAZ Creative Studio"* dengan **Logo RAZBerry** dan **Logo RAZ Creative Studio** transparan tanpa background.
- 🖼️ **Ikon Konsisten & Presisi**: Ikon logo RAZBerry disuntikkan langsung ke 32 slot Win32 PE Resource pada `razberry.exe`, window title bar dialog XUL, taskbar grouping, dan favicon global.
- 🛠️ **Informasi Sistem Akurat (`about:support`)**: Nama peramban terkonfigurasi permanen sebagai **RAZBerry** pada tabel *Application Basics* di `about:support`.
- 🔒 **Proteksi Anti Auto-Update**: Seluruh mekanisme background updater upstream dinonaktifkan total (`MOZ_UPDATER: false`, cache ProgramData dibersihkan, Enterprise Policies) sehingga kustomisasi peramban tidak akan pernah tertimpa.
- 📁 **Space Folder "razberrys"**: Folder default pertama ruang kerja (spaces) dinamai `razberrys`.
- 🌐 **Ekosistem Web Terintegrasi**: Halaman welcome default mengarah ke `https://razberry.it-raz.com/welcome/` dan privacy policy ke `https://razberry.it-raz.com/privacy-policy/`.
- 📑 **Manajemen Tab Vertikal**: Penataan ruang layar yang jauh lebih lega untuk layar modern 16:9 dan ultra-wide.
- 🪟 **Built-in Split View**: Menampilkan dua halaman web berdampingan dalam satu jendela tanpa ekstensi tambahan.
- 🛡️ **Privasi Maksimal**: Zero telemetry, zero tracking, dan pelindung pelacakan bawaan.

---

## 🎨 Identitas Brand & Aset

| Komponen | Spesifikasi | Keterangan |
|----------|-------------|------------|
| **Nama Aplikasi** | RAZBerry | Ditampilkan di menu & title bar |
| **Vendor** | RAZ Creative Studio | Identitas pembuat |
| **App ID / Binary** | `razberry` | Nama proses & eksekusi |
| **Domain Resmi** | `https://razberry.it-raz.com` | Portal & welcome server |
| **Warna Utama** | `#C72C48` (Raspberry Red) | Aksen utama tema |
| **Warna Latar** | `#120305` & `#1A0508` (Dark Berry) | Kanvas solid tanpa blur |
| **Warna Urlbar** | `#26080F` (Maroon Berry) | Kontras kolom pencarian |
| **Aset Logo RAZBerry** | `razberry-logo.png` | Format 32-bit ARGB transparan |
| **Aset Logo RAZ Studio** | `RAZ_Creative_Studio_Transparent.png` / `.svg` | Format transparan tanpa latar belakang |

---

## 📁 Struktur Direktori

Informasi struktur lengkap dapat dibaca pada [RAZProjectStructure.md](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/RAZProjectStructure.md).

```
RAZBerry/
├── backup/                 # Salinan backup aman sebelum modifikasi file
├── dist/                   # Hasil build distribusi mandiri RAZBerry
│   └── RAZBerry/
│       ├── razberry.exe    # Eksekutabel peramban dengan 28 patched Win32 PE icons
│       ├── RAZBerry.bat    # Batch launcher
│       ├── RAZBerry.lnk    # Shortcut peramban Windows
│       ├── chrome/icons/   # Ikon window native XUL (main-window, default, about)
│       └── browser/omni.ja # Mesin UI terinjeksi tema solid raspberry, dual logo & prefs
├── docs/                   # Log harian dan histori update proyek
│   ├── RAZUpdateHistory_2026-01-06.md
│   └── RAZUpdateHistory_2026-11-24.md
├── razberry/               # Base repository RAZBerry Desktop
│   ├── configs/branding/   # Aset logo, ICO multi-resolusi, dan SVG RAZBerry
│   ├── src/                # Kode sumber UI dan ekstensi antarmuka
│   └── locales/            # File lokalisasi (en-US, id, dll) dengan teks sambutan RAZBerry
├── razberry-www/           # Source code website resmi RAZBerry (Astro + Tailwind CSS)
├── RAZ_Creative_Studio_Transparent.png  # Aset logo RAZ Studio transparan
├── RAZ_Creative_Studio_Transparent.svg  # Aset vektor RAZ Studio transparan
├── RAZCreateTransparentLogo.py          # Skrip pembuatan logo transparan
├── RAZApplyCustomizations.py            # Skrip injeksi kustomisasi & branding
├── RAZBuildBrowser.ps1                  # Otomatisasi build & packaging lengkap
├── RAZPatchExeIcons.py                  # Skrip patching Win32 PE resources
└── RAZRebrandWebsite.py                 # Skrip rebranding website resmi
│   ├── prefs/              # Pengaturan preferensi default browser
│   ├── surfer.json         # Konfigurasi identitas aplikasi RAZBerry
│   └── package.json        # Toolchain build npm & surfer
├── razberry-www/           # Repositori website resmi RAZBerry (Astro + Tailwind)
│   ├── src/pages/          # Halaman index, welcome, privacy-policy
│   ├── src/components/     # Komponen UI Logo, Hero, NavBar bertema raspberry
│   └── public/             # Favicon, logo.png, dan aset statis website
├── razberry-logo.png       # Master icon RAZBerry transparan
├── RAZApplyCustomizations.py # Skrip injeksi kustomisasi tema, update, & URLs
├── RAZPatchExeIcons.py     # Skrip injeksi 28 embedded icons pada razberry.exe
├── RAZRebrandWebsite.py    # Skrip otomatisasi rebranding website Astro
├── RAZBuildBrowser.ps1     # Skrip otomatisasi build & packaging distribusi
├── RAZGenerateIcons.ps1    # Skrip otomatisasi konversi & generate aset ikon
├── RAZBerry.bat            # Launcher cepat di root direktori
├── RAZBerry.lnk            # Shortcut berikon di root direktori
├── RAZGuide.md             # Panduan instalasi dan build lengkap
├── RAZProjectPlan.md       # Roadmap dan status tahapan proyek
├── RAZProjectStructure.md  # Rincian organisasi berkas
└── README.md               # Pusat dokumentasi ini (Single Source of Truth)
```

---

## 🚀 Cara Menjalankan & Membangun

### 1. Menjalankan RAZBerry Browser
Cukup buka salah satu file berikut di root direktori:
- Klik ganda **`RAZBerry.lnk`** (Shortcut Windows resmi dengan ikon Raspberry), ATAU
- Jalankan **`RAZBerry.bat`**.

### 2. Membangun / Memperbarui Build Browser
Jalankan skrip PowerShell otomatis:
```powershell
powershell -ExecutionPolicy Bypass -File .\RAZBuildBrowser.ps1
```
Skrip ini akan secara otomatis:
1. Menyalin runtime binary engine dari `C:\Program Files\Zen Browser`.
2. Melakukan patching 28 slot icon Win32 PE pada `razberry.exe`.
3. Memasang window icons native di `chrome/icons/default/`.
4. Menginjeksi branding, tema Solid Raspberry Red, anti auto-update, dan welcome URLs ke dalam `omni.ja`.
5. Mengonfigurasi `defaults/pref/razberry-prefs.js`.
6. Membuat launcher batch dan shortcut Windows.

### 3. Menjalankan Website Resmi RAZBerry
Masuk ke direktori `razberry-www` dan jalankan:
```bash
cd razberry-www
pnpm install
pnpm dev
```
Website akan berjalan di `http://localhost:3000`.

### 4. Deployment Otomatis ke Hosting IDwebhost (Paket Tera)
Proyek ini mendukung CI/CD otomatis via GitHub Actions dan deploy lokal:
- **GitHub Actions (Auto-Deploy)**: Setiap push ke branch `main` pada `razberry-www` akan otomatis mengompilasi dan mengunggah website ke cPanel IDwebhost melalui FTPS.
- **Local Deploy**: Jalankan `.\RAZDeployToIDwebhost.ps1` untuk deploy instan satu klik dari komputer Anda.
- Panduan lengkap konfigurasi secrets dan kredensial hosting dapat dilihat di [docs/RAZHostingDeployGuide.md](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/docs/RAZHostingDeployGuide.md).

---

## 📜 Lisensi & Atribusi

- **RAZBerry Browser**: Berdasarkan Mozilla Public License v2.0 (MPL-2.0).
- **Aset & Identitas Brand**: © 2026 RAZ Creative Studio. Hak Cipta Dilindungi Undang-Undang.
