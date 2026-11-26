# RAZBerry Browser — Update History (2026-11-26)

## Ringkasan Pembaruan

### 08:43 WIB — Perbaikan Timeout CI/CD Deployment (`RAZDeployHosting.yml`)
- Menaikkan `timeout-minutes` dari `15` menjadi `45` menit pada `.github/workflows/RAZDeployHosting.yml` agar sinkronisasi FTPS untuk 438+ halaman statis (3 bahasa) ke IDwebhost tidak terhenti di tengah jalan.

### 09:42 WIB — Penambahan Halaman Shortcut Key Website (`/shortcuts`)
- **Halaman Baru (`razberry-www/src/pages/[...locale]/shortcuts.astro`)**:
  - Menampilkan seluruh daftar pintasan keyboard resmi RAZBerry Browser berdasarkan `zen-keysets.inc.xhtml` (*Compact Mode & Sidebar*, *Split View*, *Workspaces & Tab*, *Glance, URL & Window*).
  - Dilengkapi fitur pencarian cepat (filter real-time client-side) serta dukungan 3 bahasa (`id-oke`, `id`, `en`).
- **Terjemahan & Navigasi**:
  - Menambahkan key `routes.shortcuts`, `layout.shortcuts`, serta `components.nav.menu.shortcuts` & `shortcutsDesc` pada `id-oke/translation.json`, `id/translation.json`, dan `en/translation.json`.
  - Menambahkan tautan menu **Shortcut Key** di `NavBar.astro`, `MobileMenu.astro`, dan `Footer.astro`.
- **Pembaruan `README.md`**:
  - Menambahkan tabel lengkap **Shortcut Key Bawaan** (Compact Mode & Sidebar, Split View, Workspaces & Tab, serta Glance, URL & Window) langsung di `README.md`.
