# RAZBerry Update History - 2026-11-25

**Project**: RAZBerry Browser  
**Version**: 0.9.3  
**Date**: 2026-11-25  
**Author**: RAZ Creative Studio

---

## Kegiatan Hari Ini

### 🔧 [11:00 WIB] - Pembaruan Folder Space (`zen basics` -> `razberry`) & URL Tab Bawaan ke Website Resmi

#### 🚀 Latar Belakang & Permintaan Pengguna
1. Mengganti nama folder pertama pada Space dari `zen basics` menjadi `razberry`.
2. Mengganti tab bawaan (`Welcome!` dan `Privacy Policy - Zen`) agar mengarah ke URL website resmi RAZBerry (`https://razberry.it-raz.com/welcome/` dan `https://razberry.it-raz.com/privacy-policy/`).

#### 🛠️ Tindakan Solutif & Implementasi
1. **Pembaruan Session Profil Aktif (`RAZUpdateProfileAndTabs.py`)**:
   - Membuat backup terpusat seluruh berkas session profil `dsph9rup.Default (release)` ke `backup/profile_dsph9rup/`.
   - Mengubah nama folder & group pada `zen-sessions.jsonlz4`, `sessionstore.jsonlz4`, `sessionstore-backups/*`, dan `zen-sessions-backup/*` dari `zen basics` menjadi **`razberry`**.
   - Mengganti URL tab Welcome (`https://zen-browser.app/welcome/` -> `https://razberry.it-raz.com/welcome/`) dan Privacy Policy (`https://zen-browser.app/privacy-policy/` -> `https://razberry.it-raz.com/privacy-policy/`).
   - Membersihkan cache favicon SVG Zen lama dan `policyContainer` lama pada tab terkait agar browser memuat favicon RAZBerry terbaru secara otomatis.
2. **Pembaruan `browser/omni.ja` & Source Code**:
   - Menyelaraskan `ZenWelcome.mjs` agar pembuatan folder pertama untuk profil baru juga menggunakan nama `razberry`.
   - Memperbarui tautan `aboutDialog.xhtml` dan `razberry/src/zen/about/zen-about.inc.xhtml` ke `https://razberry.it-raz.com/privacy-policy/` dan `https://razberry.it-raz.com/about/`.

#### ✅ Verifikasi
- `zen-sessions.jsonlz4` terverifikasi memiliki folder `razberry` dan tab `https://razberry.it-raz.com/welcome/` serta `https://razberry.it-raz.com/privacy-policy/`.

---

### 🎨 [11:15 WIB] - Redesign Website `razberry-www` Mengadopsi Style Web Utama RAZ Creative Studio (Tema Black-Pink Raspberry)

#### 🚀 Latar Belakang & Permintaan Pengguna
- Mengadopsi style visual, layout, animasi partikel, header glassmorphic, card, dan footer dari website utama **RAZ Creative Studio** (`webraz`), namun menggunakan tema warna **Black-Pink Raspberry** (`#0a0a0a` + `#FF4081` / `#D81B60`) serta seluruh isi, data, video, mods, dan halaman dari **RAZBerry Browser**.

#### 🛠️ Implementasi
1. **Design System `RAZBerryTheme.css` & `global.css`**:
   - Token Black-Pink Raspberry (`#0a0a0a`, `#141013`, `#FF4081`, `#D81B60`, `#BA1257`) di Dark Mode (default) dan Soft Berry Cream (`#fdf7f9`, `#ffffff`, `#D81B60`) di Light Mode.
   - Tipografi `Inter` + `Poppins`, shimmer gradient pink, section label bergaris pink, dan `.raz-card` dengan hover glow pink.
2. **Komponen Inti (`Layout.astro`, `NavBar.astro`, `Footer.astro`, `Button.astro`, `Hero.astro`, `Features.astro`)**:
   - `Hero.astro`: Canvas partikel node pink interaktif (`#raz-hero-canvas`), floating keywords, `.raz-hero-badge`, dual CTA buttons, dan video showcase di dalam bingkai browser RAZBerry.
   - `NavBar.astro` & `Footer.astro`: Header fixed glassmorphic dan 4-kolom footer terhubung ke ekosistem RAZ Creative Studio.
3. **Seluruh Halaman (`index.astro`, `welcome.astro`, `about.astro`, `privacy-policy.astro`, `donate.astro`, `download.astro`)**:
   - Disesuaikan menyeluruh dengan palet Black-Pink Raspberry dan layout responsif.

---

### 📱 [11:20 WIB] - Penyelarasan Sosial Media, Email, & Kontak Resmi RAZ Creative Studio

- Seluruh tautan komunitas dan kontak pada `SocialMediaStrip.astro`, `Community.astro`, `MobileMenu.astro`, `Footer.astro`, `privacy-policy.astro`, `whatsnew.astro`, dan `donate.astro` telah diselaraskan dengan web utama **RAZ Creative Studio** (`https://raz.web.id/`):
  - **Instagram**: `https://www.instagram.com/raz_studio.id/`
  - **YouTube**: `https://www.youtube.com/@razcreativestudio`
  - **TikTok**: `https://www.tiktok.com/@razcreativestudio`
  - **GitHub**: `https://github.com/razcreativestudio/razberry`
  - **Email Resmi**: `razcreativestudio@gmail.com`
  - **WhatsApp / Telepon**: `+62 831 7300 2527` (`https://wa.me/6283173002527`)
  - **Halaman Kontak**: `https://raz.web.id/hubungi-raz.html`
