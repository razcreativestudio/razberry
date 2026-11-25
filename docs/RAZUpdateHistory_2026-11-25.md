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

---

### 🚀 [11:36 WIB] - GitHub Release Action (`RAZReleaseBrowser.yml`) & Migrasi Penuh Link Download/GitHub

- **GitHub Actions Release Pipeline**: Membuat `.github/workflows/RAZReleaseBrowser.yml` dengan trigger tag `v*` dan `workflow_dispatch`, pengemasan aset rilis resmi, SHA-256 checksums, dan publikasi otomatis via `softprops/action-gh-release@v2` ke `razcreativestudio/razberry/releases`.
- **Link Download & Checksum**: Memperbarui `release-data.ts` dan `githubChecksums.ts` agar seluruh unduhan Windows, macOS, dan Linux mengarah ke `https://github.com/razcreativestudio/razberry/releases/latest/download/...`.
- **Migrasi Link GitHub & i18n**: Memperbarui `about.astro`, `feed.xml.ts`, `ReleaseNoteItem.astro`, `en/translation.json`, dan `ja/translation.json` (sekaligus menambal missing translation key `tryRAZBerryMods`) ke repositori `razcreativestudio/razberry`.

---

### 📦 [11:46 WIB] - Pembuatan Installer Standalone `RAZBerrySetup.exe` (Floating Banner Chrome Style)

- **Source Wizard (`RAZSetupWizard.cs`)**:
  - Tampilan *floating borderless banner* ala Google Chrome Installer dengan tema Black-Pink Raspberry (`#110A0E`, `#D81B60`, `#FF4081`) selaras dengan Welcome Screen RAZBerry (menampilkan Logo RAZBerry & Logo RAZ Creative Studio sejajar tanpa background).
  - Alur 3 tahap bersih:
    1. **Ready**: Opsi checkbox shortcut + tombol **Install** & **Cancel**.
    2. **Installing**: Custom gradient Pink Progress Bar real-time (`0% - 100%`) mengekstrak payload ke `%LocalAppData%\RAZBerry`, membuat shortcut Desktop & Start Menu, serta mendaftarkan entri Uninstall Windows.
    3. **Completed**: Tombol **Finish & Open** untuk langsung meluncurkan `razberry.exe` + tombol **Close**.
- **Build Pipeline (`RAZBuildInstaller.ps1`)**:
  - Mengompres `dist/RAZBerry` dan mengompilasinya bersama logo serta `RAZBerry.ico` via `.NET Framework csc.exe` menjadi single-file executable `dist/RAZBerrySetup.exe` & `dist/razberry.installer.exe`.

---

### 🗑️ [11:53 WIB] - Penambahan Folder Start Menu `RAZBerry` & `Uninstall RAZBerry.exe`

- **Standalone Uninstaller (`RAZUninstaller.cs`)**:
  - Membuat uninstaller GUI bertema Black-Pink Raspberry (`dist/Uninstall RAZBerry.exe`) dengan opsi penghapusan profil opsional, pembersihan shortcut Desktop, penghapusan folder Start Menu `RAZBerry`, pembersihan Registry Uninstall, dan self-delete folder instalasi.
- **Integrasi Start Menu Folder (`RAZSetupWizard.cs`)**:
  - Menempatkan shortcut `RAZBerry` dan `Uninstall RAZBerry` ke dalam subfolder Start Menu `Programs\RAZBerry\` (sekaligus membersihkan shortcut lama di root Programs agar tampil rapi dalam satu folder).
  - Mendaftarkan `UninstallString`, `QuietUninstallString`, `EstimatedSize` (KB), `NoModify`, dan `NoRepair` di Registry `HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\RAZBerry` agar tombol **Uninstall** dan ukuran aplikasi tampil aktif di **Windows Settings > Apps > Installed apps**.

---

### 🩹 [12:05 WIB] - Perbaikan Welcome Screen Blank & Auto-Open `razberry.it-raz.com/welcome/`

- **Perbaikan `ZenWelcome.mjs` & `zen-welcome.css` (`RAZFixWelcomeAndLaunch.py`)**:
  - Menghapus `opacity: 0` permanen di `zen-welcome.css` pada `#zen-welcome-brand-logos`, `#zen-welcome-start-button`, dan `.zen-welcome-char` agar Welcome Screen tidak pernah tampil kosong jika animasi JS tertunda/gagal.
  - Menambahkan fallback l10n (`Welcome to RAZBerry Browser` / `By RAZ Creative Studio`) serta memasang event listener tombol start **sebelum** animasi dijalankan.
  - Memastikan fungsi `finish()` langsung membuka tab aktif `https://razberry.it-raz.com/welcome/` tepat setelah jendela utama RAZBerry Browser terbuka.
- **Perbaikan Launch Flag (`RAZSetupWizard.cs`)**:
  - Menghapus flag `-app browser\application.ini` saat meluncurkan `razberry.exe` dari *Finish & Open* maupun shortcut Desktop/Start Menu agar browser berjalan dalam mode native normal.

---

### 🧩 [12:16 WIB] - Perbaikan Halaman Migration / Import & Seluruh FTL Welcome Wizard

- **Penambalan 41 File Locale `zen-welcome.ftl`**:
  - Menambahkan seluruh key yang hilang (`zen-generic-next`, `zen-welcome-import-description`, `zen-welcome-import-no`, `zen-welcome-block-ads-*`, `zen-welcome-essentials-*`, `zen-welcome-default-browser-*`, `zen-welcome-back`, `zen-welcome-skip`) sehingga keterangan penjelasan di sidebar kiri dan tombol **Next** / **Skip** tampil lengkap.
- **Perbaikan `ZenWelcome.mjs` & `zen-welcome.css`**:
  - Menghapus referensi `browser/zen-migration.ftl` yang tidak ada di `omni.ja`.
  - Menambahkan fallback nama browser (`Google Chrome`, `Microsoft Edge`, `Brave Browser`, `Mozilla Firefox`, `Opera`, `Vivaldi`) agar tidak menampilkan raw l10n key.
  - Menghapus `opacity: 0` pada `#zen-welcome-pages`, `.zen-welcome-page`, dan `.zen-welcome-text > *` serta menambahkan proteksi fallback pada `#renderText()` dan `updateButtons()`.
