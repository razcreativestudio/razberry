# RAZBerry Browser

<p align="center">
  <img src="razberry-logo.png" alt="RAZBerry Browser Logo" width="150" />
</p>

<p align="center">
  <strong>Browser Modern yang Cepat, Fokus, dan Menjaga Privasi — Dibuat oleh RAZ Creative Studio</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Versi-1.1.0-D81B60.svg" alt="Versi" />
  <img src="https://img.shields.io/badge/Engine-Firefox%20%2F%20Gecko-BA1257.svg" alt="Engine" />
  <img src="https://img.shields.io/badge/Platform-Windows%2010%2F11-FF4081.svg" alt="Platform" />
  <img src="https://img.shields.io/badge/Website-razberry.it--raz.com-D81B60.svg" alt="Website" />
  <img src="https://img.shields.io/badge/CI%2FCD-Passing-brightgreen.svg" alt="CI/CD" />
</p>

---

## Apa Itu RAZBerry Browser?

**RAZBerry Browser** adalah browser web modern bertema **Black-Pink Raspberry** yang dibuat oleh **RAZ Creative Studio** (`raz.web.id`). Browser ini dirancang buat kamu yang butuh kerja cepat, tampilan bersih tanpa gangguan visual, serta privasi penuh tanpa pelacakan (zero telemetry).

Website resmi: **[https://razberry.it-raz.com](https://razberry.it-raz.com)**

---

## Kemampuan & Fitur Utama

1. **Workspaces & Tab Vertikal**  
   Pisahkan tab kerja, riset, kuliah, dan hiburan ke ruang kerja masing-masing agar tidak menumpuk dan tetap rapi.
2. **Split View Bawaan**  
   Buka dan bandingkan dua halaman web atau lebih secara berdampingan dalam satu jendela tanpa perlu install ekstensi tambahan.
3. **Compact Mode & Glance**  
   Sembunyikan bar tab saat tidak dibutuhkan agar layar lebih lega, dan intip tab favorit dengan cepat lewat fitur Glance.
4. **Tema Eksklusif Black-Pink Raspberry**  
   Tampilan solid dengan kontras tinggi (`#120305` & `#D81B60`) yang nyaman di mata untuk pemakaian siang maupun malam, tanpa efek blur berat.
5. **RAZBerry Mods**  
   Bebas kustomisasi tampilan dan perilaku browser melalui koleksi Mods di `razberry.it-raz.com/mods`.
6. **Privasi Maksimal (Zero Telemetry)**  
   Semua telemetri dan pelacakan bawaan dimatikan. Riwayat, cookies, dan pengaturan tersimpan lokal di perangkatmu.
7. **Proteksi Anti Auto-Update Paksa**  
   Kustomisasi tema dan pengaturanmu aman karena mekanisme penimpaan otomatis sudah dinonaktifkan.

---

## Teknologi yang Digunakan

| Komponen | Teknologi | Fungsi |
|----------|-----------|--------|
| **Mesin Browser** | Firefox / Gecko + Zen UI | Rendering web cepat, aman, dan mendukung ekstensi Firefox |
| **Tema & Antarmuka** | CSS Tokens, XUL, Fluent (`.ftl`), JS Modules (`.mjs`) | Tema Black-Pink Raspberry, Welcome Onboarding, dan Migration Wizard |
| **Installer Windows** | C# WinForms (`.NET Framework 4.0+`) | `RAZBerrySetup.exe` & `Uninstall RAZBerry.exe` bergaya floating banner |
| **Website Resmi** | Astro, Tailwind CSS v4, React, TypeScript | Portal multi-bahasa (`Indo Oke`, `Indonesia`, `English`) |
| **CI/CD & Rilis** | GitHub Actions & GitHub Releases | Build otomatis, rilis binary, dan deploy ke `razberry.it-raz.com` |

---

## Cara Install (Windows 10 / 11)

1. Download installer terbaru **`RAZBerrySetup.exe`** (atau `razberry.installer.exe`) dari:
   - Website resmi: [https://razberry.it-raz.com/download](https://razberry.it-raz.com/download)
   - Halaman Rilis GitHub: [Latest Release](https://github.com/razcreativestudio/razberry/releases/latest)
2. Klik dua kali file `RAZBerrySetup.exe`.
3. Pada jendela **RAZBerry Setup Wizard**, klik tombol **Install**.
4. Tunggu progress bar selesai mengekstrak file ke `%LocalAppData%\RAZBerry`.
5. Setelah selesai, klik **Finish & Open** untuk langsung membuka RAZBerry Browser.

> **Catatan:** Installer otomatis membuat folder **RAZBerry** di Start Menu berisi shortcut `RAZBerry`, `RAZBerry Private Mode`, dan `Remove RAZBerry`, serta mendaftarkannya di *Windows Settings → Installed Apps*.

### Cara Uninstall
- Buka **Windows Settings → Apps → Installed Apps → RAZBerry Browser → Uninstall**, atau
- Buka **Start Menu → RAZBerry → Remove RAZBerry**.

---

## Cara Pakai Sehari-hari

- **Pertama Kali Buka**: Ikuti Welcome Screen dan Migration Wizard untuk memindahkan bookmark/data dari Chrome, Edge, atau Brave (atau klik **Skip** jika ingin mulai dari nol).
- **Membuat Workspace**: Klik ikon workspace di sidebar kiri untuk memisahkan grup tab kerja dan pribadi.
- **Membuka Split View**: Klik kanan pada beberapa tab yang ingin dibandingkan → pilih *Split Tabs*.
- **Mengaktifkan Compact Mode**: Tekan pintasan keyboard bawaan atau klik tombol sidebar untuk menyembunyikan/menampilkan bar tab secara otomatis.
- **Mode Privat**: Jalankan shortcut **RAZBerry Private Mode** dari Start Menu atau tekan `Ctrl + Shift + P`.

---

## Shortcut Key Bawaan

Kamu bisa memakai kombinasi tombol berikut di Windows (untuk macOS, ganti `Ctrl` dengan `Cmd`, dan Workspace memakai `Control + 1–0`). Versi web interaktif juga tersedia di [https://razberry.it-raz.com/shortcuts](https://razberry.it-raz.com/shortcuts).

### Compact Mode & Sidebar
| Fungsi | Shortcut |
|--------|----------|
| Aktifkan / matikan Compact Mode | `Ctrl + S` |
| Tampilkan / sembunyikan Sidebar di Compact Mode | `Ctrl + Alt + S` |
| Buka / tutup Library | `Alt + Shift + L` |

### Split View
| Fungsi | Shortcut |
|--------|----------|
| Split View Vertical (kiri-kanan) | `Ctrl + Alt + V` |
| Split View Horizontal (atas-bawah) | `Ctrl + Alt + H` |
| Split View Grid | `Ctrl + Alt + G` |
| Lepaskan Split View (Unsplit) | `Ctrl + Alt + U` |
| Buka Split View kosong baru | `Ctrl + Shift + *` |

### Workspaces & Tab
| Fungsi | Shortcut |
|--------|----------|
| Pindah langsung ke Workspace 1 – 10 | `Alt + 1` s/d `Alt + 0` |
| Pindah ke Workspace berikutnya | `Ctrl + Alt + →` |
| Pindah ke Workspace sebelumnya | `Ctrl + Alt + ←` |
| Pin / Unpin tab aktif | `Ctrl + Shift + D` |
| Tutup semua tab yang tidak di-pin | `Ctrl + Shift + K` |

### Glance, URL & Window
| Fungsi | Shortcut |
|--------|----------|
| Perbesar pratinjau Glance | `Ctrl + O` |
| Copy URL halaman saat ini | `Ctrl + Shift + C` |
| Copy URL sebagai Markdown | `Ctrl + Alt + Shift + C` |
| Buka window baru tanpa sync | `Ctrl + Shift + N` |
| Buka Little Window | `Ctrl + Alt + N` |
| Buka jendela Private Mode | `Ctrl + Shift + P` |

> **Tips:** Semua shortcut dapat diubah atau ditambah sesuai kebutuhan lewat **Settings → Keyboard Shortcuts** di dalam RAZBerry Browser.

---

## Cara Build Sendiri (Untuk Developer)

Jika ingin membangun ulang browser, installer, atau website dari source code:

### 1. Clone Repository
```bash
git clone https://github.com/razcreativestudio/razberry.git
cd razberry
```

### 2. Build Browser Distribution (Windows)
```powershell
.\RAZBuildBrowser.ps1
```
Script ini menyiapkan folder distribusi di `dist\RAZBerry\`, menyalin branding, preferensi tema, dan mem-patch `omni.ja`.

### 3. Compile Installer & Uninstaller (`RAZBerrySetup.exe`)
Memerlukan Windows dengan `.NET Framework 4.0+` (`csc.exe`):
```powershell
.\RAZBuildInstaller.ps1
```
Output dihasilkan di:
- `dist\RAZBerrySetup.exe`
- `dist\razberry.installer.exe`
- `dist\Uninstall RAZBerry.exe`

### 4. Build Website (`razberry-www`)
Memerlukan Node.js 20+:
```bash
cd razberry-www
npm install
npm run build
```
Hasil build statis berada di `razberry-www/dist/` dengan dukungan 3 bahasa: **Indo Oke** (`/`), **Indonesia** (`/id/`), dan **English** (`/en/`).

---

## Ekosistem & Kontak RAZ Creative Studio

- **Website Studio**: [https://raz.web.id](https://raz.web.id)
- **Website RAZBerry**: [https://razberry.it-raz.com](https://razberry.it-raz.com)
- **RAZ Download Manager**: [https://dm.it-raz.com](https://dm.it-raz.com)
- **Email Resmi**: `razcreativestudio@gmail.com`
- **WhatsApp**: `+62 831 7300 2527`
- **Sosial Media**: Instagram `@raz_studio.id` • YouTube `@razcreativestudio` • TikTok `@razcreativestudio`

---

<p align="center">
  Dibuat dengan dedikasi oleh <strong>RAZ Creative Studio</strong>
</p>
