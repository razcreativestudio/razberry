# RAZBerry Browser Project Structure

**Versi Dokumen**: 0.9.0  
**Tanggal Update**: 2026-11-24  
**Author**: RAZ Creative Studio  

Dokumen ini menjelaskan struktur direktori, organisasi berkas, dan fungsi setiap komponen dalam proyek **RAZBerry Browser**.

---

## 🌳 Pohon Direktori Utama

```
RAZBerry/
│
├── backup/                                # Direktori backup terpusat sebelum modifikasi
│   ├── branding_release/                  # Backup aset branding release orisinil
│   ├── branding_twilight/                 # Backup aset branding twilight orisinil
│   ├── surfer.json                        # Backup file surfer.json
│   ├── mozconfig                          # Backup file konfigurasi mozconfig
│   ├── zen-theme.css                      # Backup styling tema css
│   ├── theme.yaml                         # Backup preferensi tema yaml
│   ├── windows.yaml                       # Backup preferensi windows mica
│   ├── application.ini                    # Backup file manifest aplikasi
│   ├── omni.ja                            # Backup arsip mesin UI omni.ja
│   └── ...                                # Backup lainnya
│
├── dist/                                  # Hasil build distribusi mandiri RAZBerry
│   └── RAZBerry/
│       ├── razberry.exe                   # Eksekutabel peramban dengan 28 patched PE icons
│       ├── RAZBerry.bat                   # Batch launcher standalone
│       ├── RAZBerry.lnk                   # Windows shortcut siap pakai
│       ├── chrome/icons/default/          # Ikon native XUL (main-window, default, about)
│       ├── browser/chrome/icons/default/  # Ikon native XUL browser level
│       ├── browser/omni.ja                # Mesin UI browser terinjeksi tema & branding
│       ├── omni.ja                        # Mesin toolkit terinjeksi defaultFavicon.svg
│       └── defaults/pref/razberry-prefs.js # Preferensi default solid berry & anti-update
│
├── docs/                                  # Dokumentasi dan riwayat pembaruan harian
│   ├── RAZUpdateHistory_2026-01-06.md     # Riwayat update inisialisasi awal
│   └── RAZUpdateHistory_2026-11-24.md     # Riwayat update clone, rebranding, & hardening
│
├── razberry/                              # Sub-repositori basis RAZBerry (berbasis mesin Zen/Firefox)
│   ├── configs/
│   │   ├── branding/
│   │   │   ├── release/                   # Aset branding utama (logo, ico, svg)
│   │   │   │   ├── content/               # Aset halaman About & Wordmark SVG
│   │   │   │   └── ...                    # Ikon PNG berbagai ukuran & file ICO
│   │   │   └── twilight/                  # Aset branding kanal preview/twilight
│   │   ├── common/
│   │   │   └── mozconfig                  # Konfigurasi build engine Mozilla
│   │   └── windows/                       # Konfigurasi platform Windows
│   ├── src/                               # Implementasi antarmuka dan modul kustom
│   │   ├── browser/                       # Komponen browser UI
│   │   └── zen/                           # Gaya tema, tokens, dan script Zen
│   │       ├── common/styles/             # Berkas CSS termasuk zen-theme.css
│   │       └── welcome/ZenWelcome.mjs     # Space folder default ("razberrys")
│   ├── prefs/                             # Berkas preferensi default (YAML)
│   │   ├── zen/theme.yaml                 # Preferensi tema default (#C72C48)
│   │   └── zen/windows.yaml               # Preferensi windows mica (false)
│   ├── surfer.json                        # Pengaturan identitas aplikasi & build
│   └── package.json                       # Dependensi dan script build npm
│
├── razberry-www/                          # Repositori website resmi RAZBerry (Astro + Tailwind)
│   ├── src/
│   │   ├── pages/                         # Index, Welcome (/welcome/), Privacy Policy
│   │   ├── components/                    # Komponen Logo.astro, Hero, NavBar bertema berry
│   │   ├── styles/global.css              # Tema styling warna Raspberry Red (#C72C48)
│   │   └── i18n/                          # File lokalisasi teks translation.json
│   ├── public/                            # Favicon, logo.png, share-pic.png
│   └── astro.config.mjs                   # Konfigurasi Astro website (https://razberry.it-raz.com)
│
├── razberry-logo.png                      # Logo primer RAZBerry (500x500 ARGB transparan)
├── logo-razberry.png                      # Logo sekunder dengan teks RAZBerry
├── logorazberry.png                       # Alternatif logo visual
├── RAZ_Creative_Studio_Identik.svg        # Aset orisinil logo RAZ Studio (JPEG embedded)
├── RAZ_Creative_Studio_Transparent.png    # Aset logo RAZ Studio transparan tanpa background (994x315)
├── RAZ_Creative_Studio_Transparent.svg    # Aset vektor logo RAZ Studio transparan
│
├── RAZCreateTransparentLogo.py            # Skrip ekstraksi & pembuatan logo transparan RAZ Studio
├── RAZApplyCustomizations.py              # Skrip injeksi kustomisasi tema, welcome screen, & URLs
├── RAZPatchExeIcons.py                    # Skrip injeksi 32 embedded icons pada razberry.exe
├── RAZPatchAboutSupport.py                # Skrip patching about:support (Name: RAZBerry) & AppConstants
├── RAZFixVisualIssues.py                  # Skrip pembersihan cache, enterprise policies, & FTL fallback
├── RAZRebrandAllZenText.py                # Skrip lokalisasi teks Zen Mods -> RAZBerry Mods & URL Bar
├── RAZApplyPinkTheme.py                   # Skrip penerapan tema solid raspberry pink (WCAG AA/AAA)
├── RAZRebrandWebsite.py                   # Skrip otomatisasi rebranding website Astro
├── RAZBuildBrowser.ps1                    # Skrip otomatisasi build & packaging distribusi
├── RAZGenerateIcons.ps1                   # Skrip otomatisasi generate semua varian ikon
├── RAZBerry.bat                           # Launcher cepat di root direktori
├── RAZBerry.lnk                           # Shortcut berikon di root direktori
├── RAZGuide.md                            # Panduan teknis pengembangan dan build
├── RAZProjectPlan.md                      # Rencana dan roadmap pengembangan proyek
├── RAZProjectStructure.md                 # Berkas dokumentasi struktur ini
└── README.md                              # Single source of truth proyek
```

---

## 📌 Penjelasan Berkas Kunci

1. **`RAZCreateTransparentLogo.py`**  
   Skrip otomatisasi Python untuk memproses file `RAZ_Creative_Studio_Identik.svg`, menghilangkan latar belakang hitam `RGB(26, 28, 27)` secara presisi melalui algoritma *color distance*, dan mengekstrak aset PNG & SVG transparan murni untuk disematkan pada layar Welcome Onboarding browser.

2. **`RAZPatchExeIcons.py`**  
   Skrip otomatisasi Python untuk membedah dan memodifikasi struktur Win32 PE Resource pada `dist/RAZBerry/razberry.exe`. Mengganti seluruh 28 slot `RT_ICON` pada IDI_APPICON, IDI_APPLICATION (taskbar & system dialogs), Group 2 (Document), Group 5 (PDF), dan Group 6 sehingga icon Windows Taskbar dan Alt-Tab 100% konsisten berlogo RAZBerry.

3. **`RAZApplyCustomizations.py`**  
   Skrip otomatisasi Python yang mengunci konfigurasi peramban: menyuntikkan layar sambutan baru ("Welcome to RAZBerry Browser By RAZ Creative Studio" dengan dual logo transparan), mematikan background auto-update Zen, mematikan Mica/Acrylic/Glassmorphism dan menerapkan tema solid Raspberry Red, mengganti nama default folder space pertama menjadi `"razberrys"`, mengarahkan Welcome URL ke `https://razberry.it-raz.com/welcome/`, serta mengganti favicon SVG global.

3. **`RAZRebrandWebsite.py`**  
   Skrip otomatisasi rebranding website Astro (`razberry-www`) yang mengonversi kode sumber website upstream `zen-browser/www` menjadi website resmi RAZBerry dengan halaman utama, welcome onboarding, dan privacy policy yang disesuaikan.

4. **`RAZBuildBrowser.ps1`**  
   Skrip orkestrasi build utama berbasis PowerShell yang mengintegrasikan seluruh tahapan build runtime, injeksi omni.ja, preferensi, patching ikon PE, dan pembuatan shortcut launcher.

5. **`RAZGenerateIcons.ps1`**  
   Skrip otomatisasi konversi gambar berbasis .NET System.Drawing untuk merender semua varian PNG (16px - 1024px) dan multi-resolusi `.ico` dari master logo `razberry-logo.png`.
