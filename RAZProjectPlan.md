# RAZBerry Browser Project Plan
**Versi**: 0.9.0  
**Tanggal Update**: 2026-11-24  
**Author**: RAZ Creative Studio

---

## 🍓 Deskripsi Project

**RAZBerry** adalah web browser custom modern dan elegan berbasis **Zen Browser** (Firefox Engine) dengan branding eksklusif dari RAZ Creative Studio. Browser ini menggabungkan fitur produktivitas mutakhir (vertical tabs, split views, workspaces, privacy-first) dengan tampilan tema solid visual khas **Raspberry Pink** (`#D81B60` dan `#FF4081`) yang lulus kontras WCAG AA/AAA tanpa glassmorphism/acrylic, didukung oleh ekosistem website resmi **RAZBerry Web** (`https://razberry.it-raz.com`).

---

## 🎯 Tujuan

1. **Branding Custom Penuh** - Mengubah identitas browser menjadi RAZBerry (nama, logo, ikon, wordmark, metadata).
2. **Tema Solid Raspberry Pink** - Menetapkan nuansa solid merah raspberry (`#D81B60`) dan vibrant pink (`#FF4081`) tanpa efek blur/mica/glassmorphism.
3. **Privasi & Proteksi Mandiri** - Mematikan auto-updater upstream Zen (`MOZ_UPDATER: false`, Enterprise Policies) agar kustomisasi tidak tertimpa dan menjaga privasi mutlak.
4. **Website Resmi Terpadu** - Membangun website resmi RAZBerry berbasis Astro & Tailwind (`razberry-www`) dengan landing page, welcome page onboarding (`/welcome/`), dan privacy policy (`/privacy-policy/`).
5. **Ikon Native Presisi** - Memastikan ikon aplikasi muncul tajam di Taskbar (32 slot PE resource patched), Titlebar dialog XUL, dan Favicon SVG.
6. **Troubleshooting Support Akurat** - Memastikan `about:support` menampilkan `Name: RAZBerry` secara permanen.

---

## 🎨 Identitas Brand

| Element | Value |
|---------|-------|
| **Nama Browser** | RAZBerry |
| **Nama Lengkap** | RAZBerry Browser |
| **Company / Vendor** | RAZ Creative Studio |
| **App ID / Binary** | razberry |
| **Domain Resmi** | `https://razberry.it-raz.com` |
| **Warna Utama** | Raspberry Red (`#C72C48`) |
| **Warna Latar** | Dark Berry (`#120305` & `#1A0508`) |
| **Warna Kolom** | Maroon Berry (`#26080F`) |
| **Logo Utama** | `razberry-logo.png` (transparent ARGB) |

---

## 📁 Struktur Project

```
RAZBerry/
├── backup/                     # Backup files terpusat sebelum modifikasi
├── dist/                       # Hasil build distribusi mandiri RAZBerry
│   └── RAZBerry/
│       ├── razberry.exe        # Eksekutabel utama RAZBerry (28 patched PE icons)
│       ├── RAZBerry.bat        # Batch launcher standalone
│       ├── RAZBerry.lnk        # Shortcut siap pakai
│       ├── chrome/icons/       # Ikon window native XUL (main-window, default, about)
│       └── browser/omni.ja     # Mesin UI terinjeksi tema solid berry & anti-update
├── docs/                       # Dokumentasi & histori harian
│   ├── RAZUpdateHistory_2026-01-06.md
│   └── RAZUpdateHistory_2026-11-24.md
├── razberry/                   # Basis utama codebase RAZBerry (desktop)
│   ├── configs/branding/       # Aset logo, ikon ICO, dan SVG RAZBerry
│   ├── src/                    # Custom UI & engine extensions
│   ├── prefs/                  # Konfigurasi preferensi default (warna & fitur)
│   ├── surfer.json             # Konfigurasi metadata & identitas aplikasi
│   └── package.json            # Toolchain konfigurasi build
├── razberry-www/               # Repositori website resmi RAZBerry (Astro + Tailwind)
│   ├── src/pages/              # Index, Welcome (/welcome/), Privacy Policy
│   ├── src/components/         # Komponen UI Logo, Hero, NavBar bertema raspberry
│   └── public/                 # Favicon, logo.png, dan aset statis website
├── razberry-logo.png           # Logo utama (transparent)
├── RAZApplyCustomizations.py   # Skrip injeksi kustomisasi tema, update, & URLs
├── RAZPatchExeIcons.py         # Skrip injeksi 28 embedded icons pada razberry.exe
├── RAZRebrandWebsite.py        # Skrip otomatisasi rebranding website Astro
├── RAZBuildBrowser.ps1         # Skrip build & packaging distribusi RAZBerry
├── RAZGenerateIcons.ps1        # Otomasi resize logo & generator ICO multi-resolusi
├── RAZBerry.bat                # Launcher cepat di root
├── RAZBerry.lnk                # Shortcut berikon di root
├── RAZGuide.md                 # Panduan teknis & build
├── RAZProjectStructure.md      # Rincian struktur berkas proyek
├── RAZProjectPlan.md           # Rencana proyek ini
└── README.md                   # Single source of truth proyek
```

---

## 🔧 Status Tahapan Pengerjaan

### Phase 1: Rebranding & Asset Integration (Selesai ✅)
- [x] Clone upstream repository Zen Browser ke `razberry/`
- [x] Amankan backup file orisinil ke `backup/`
- [x] Generate ikon multi-resolusi PNG (16-1024px) & ICO modern (`RAZGenerateIcons.ps1`)
- [x] Deploy aset branding ke `configs/branding/release/` & `twilight/`
- [x] Update SVG wordmark & logo
- [x] Rebranding metadata di `surfer.json`, `mozconfig`, `package.json`
- [x] Integrasi palet warna Raspberry Red (`#C72C48`) ke `zen-theme.css` & `theme.yaml`

### Phase 2: Build & Standalone Distribution (Selesai ✅)
- [x] Buat skrip otomatisasi build [RAZBuildBrowser.ps1](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/RAZBuildBrowser.ps1)
- [x] Ekstraksi & modifikasi runtime binary engine
- [x] Injeksi branding, FTL, properties, dan CSS ke `omni.ja`
- [x] Konfigurasi default preferences (`zen.theme.accent-color = #C72C48`)
- [x] Pembuatan binary `razberry.exe`, batch launcher, dan Windows shortcut `RAZBerry.lnk`
- [x] Verifikasi eksekusi binary (`RAZ Creative Studio RAZBerry 1.19.8b`)

### Phase 3: Customization Hardening & Official Website (Selesai ✅)
- [x] Patching 28 slot Win32 PE Resource Icons di `razberry.exe` (`RAZPatchExeIcons.py`)
- [x] Pemasangan window icons native XUL di `chrome/icons/default/` (`main-window.ico`, `default.ico`, `about.ico`)
- [x] Penggantian favicon SVG `defaultFavicon.svg` dan `favicon.svg` dengan logo RAZBerry
- [x] Penonaktifan total background updater upstream Zen (`app.update.enabled = false`, kunci `update-settings.ini`)
- [x] Eliminasi glassmorphism, acrylic, blur, dan Windows Mica menjadi Solid Raspberry Red
- [x] Pengubahan nama default space folder pertama menjadi `"razberrys"`
- [x] Pengarahan Welcome URL ke `https://razberry.it-raz.com/welcome/` & Privacy Policy ke `https://razberry.it-raz.com/privacy-policy/`
- [x] Clone dan rebranding repositori website upstream [zen-browser/www](https://github.com/zen-browser/www) menjadi `razberry-www` (`RAZRebrandWebsite.py`)
- [x] Integrasi penuh seluruh proses ke dalam [RAZBuildBrowser.ps1](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/RAZBuildBrowser.ps1)

### Phase 4: Welcome Screen & Dual Logo Customization (Selesai ✅)
- [x] Ekstraksi logo identik RAZ Creative Studio dari `RAZ_Creative_Studio_Identik.svg` (`RAZCreateTransparentLogo.py`)
- [x] Pembuatan aset logo transparan murni tanpa background: `RAZ_Creative_Studio_Transparent.png` dan `.svg`
- [x] Integrasi dual logo di atas judul welcome screen onboarding (`ZenWelcome.mjs`)
- [x] Perubahan teks sambutan: "Welcome to RAZBerry Browser By RAZ Creative Studio" (`zen-welcome.ftl`)
- [x] Styling visual welcome screen: hilangkan video background, gradien radial solid dark berry (`#23060c` ke `#120305`), tombol aksen raspberry red (`#C72C48`) (`zen-welcome.css`)
- [x] Injeksi aset transparan dan logika welcome screen ke dalam `omni.ja` dan pipeline build otomatis [RAZBuildBrowser.ps1](file:///c:/Users/Administrator/Documents/DATA%20ZUL/RAZ/RAZBerry/RAZBuildBrowser.ps1)

### Phase 5: Packaging & Distribution (Dalam Perencanaan 📋)
- [ ] Pengujian visual interface browser secara menyeluruh oleh pengguna
- [ ] Pengujian build produksi website `razberry-www` (`pnpm build`)
- [ ] Pembuatan script installer NSIS / InnoSetup untuk distribusi installer Windows
