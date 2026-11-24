# ==============================================================================
# RAZApplyPinkTheme.py
# Modul Penerapan Tema Utama Raspberry Pink (Solid, High-Contrast & Accessible)
# Mematuhi Aturan /antislop-human, /antislop-ui, /antislop, dan /antigravity-guide.
# Menjamin Kontras Sempurna di Light Mode & Dark Mode sesuai Standar WCAG AA/AAA.
# Dibuat oleh: Senior Software Engineer & RAZ Specialist
# Timestamp: 2026-11-24
# ==============================================================================

import os
import shutil
import zipfile

def log(msg):
    print(f"[RAZ-THEME] {msg}")

def update_preferences():
    """Perbarui file preferensi default RAZBerry untuk menggunakan aksen pink logo."""
    pref_file = 'dist/RAZBerry/defaults/pref/razberry-prefs.js'
    if not os.path.exists(pref_file):
        log(f"{pref_file} tidak ditemukan!")
        return

    log("Memperbarui preferensi warna default di razberry-prefs.js...")
    with open(pref_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ubah accent color default dari #C72C48 ke #D81B60
    content = content.replace('#C72C48', '#D81B60')
    
    with open(pref_file, 'w', encoding='utf-8') as f:
        f.write(content)
    log("Preferensi warna razberry-prefs.js berhasil diselaraskan ke #D81B60.")

def update_source_yaml():
    """Perbarui theme.yaml di repositori sumber."""
    yaml_file = 'razberry/prefs/zen/theme.yaml'
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('#C72C48', '#D81B60')
        with open(yaml_file, 'w', encoding='utf-8') as f:
            f.write(c)
        log("razberry/prefs/zen/theme.yaml berhasil diperbarui.")

def build_pink_theme_css():
    """
    Menghasilkan CSS tema solid Raspberry Pink berstandar antislop-ui & antislop-human.
    Mendukung Light Mode dan Dark Mode secara independen dengan kontras terverifikasi WCAG AA/AAA.
    """
    return """
/* ==============================================================================
 * RAZBerry Browser - Solid Raspberry Pink Enterprise Theme
 * Dirancang khusus berdasarkan logo RAZBerry (Pink Raspberry & Vibrant Ring)
 * Mematuhi Standar WCAG AA/AAA, antislop-human (kontras tinggi), & antislop-ui
 * ============================================================================== */

:root {
  /* 1. Brand Color Core */
  --razberry-pink-primary: #D81B60;
  --razberry-pink-vibrant: #FF4081;
  --razberry-pink-deep: #BA1257;

  /* 2. Light Mode Tokens (WCAG Contrast: Text 17.75:1, Accent 4.95:1) */
  --razberry-light-bg: #FDF7F9;
  --razberry-light-surface: #FFFFFF;
  --razberry-light-input: #FAECF2;
  --razberry-light-border: #F1CCD9;
  --razberry-light-text: #1F0B17;
  --razberry-light-text-muted: #634554;
  --razberry-light-tab-active: #FCE6EF;

  /* 3. Dark Mode Tokens (WCAG Contrast: Text 17.65:1, Accent 5.87:1) */
  --razberry-dark-bg: #130910;
  --razberry-dark-surface: #1B0C16;
  --razberry-dark-input: #261220;
  --razberry-dark-border: #3E1C31;
  --razberry-dark-text: #FDF0F5;
  --razberry-dark-text-muted: #D4B0C3;
  --razberry-dark-tab-active: #341529;

  /* 4. Adaptive Variables (Mengikuti Light/Dark Mode Native) */
  --zen-primary-color: var(--razberry-pink-primary) !important;
  --color-accent-primary: var(--razberry-pink-primary) !important;
  --focus-outline-color: var(--razberry-pink-primary) !important;

  /* Matikan total efek blur/glassmorphism bertumpuk (Sesuai antislop-ui R-10) */
  --zen-background-opacity: 1 !important;
  backdrop-filter: none !important;
}

/* Penataan Khusus LIGHT MODE */
@media (prefers-color-scheme: light) {
  :root {
    --toolbar-bgcolor: var(--razberry-light-surface) !important;
    --zen-themed-toolbar-bg: var(--razberry-light-surface) !important;
    --zen-themed-toolbar-bg-transparent: var(--razberry-light-surface) !important;
    --zen-main-browser-background: var(--razberry-light-bg) !important;
    --zen-colors-primary: var(--razberry-light-surface) !important;
    --zen-colors-secondary: var(--razberry-light-input) !important;
    --zen-colors-tertiary: var(--razberry-light-bg) !important;
    --zen-colors-border: var(--razberry-light-border) !important;
    --toolbox-textcolor: var(--razberry-light-text) !important;
    --toolbar-color: var(--razberry-light-text) !important;
    --in-content-page-background: var(--razberry-light-bg) !important;
    --in-content-page-color: var(--razberry-light-text) !important;
  }

  #navigator-toolbox,
  #sidebar-box,
  #zen-sidebar-box {
    background-color: var(--razberry-light-surface) !important;
    color: var(--razberry-light-text) !important;
    border-color: var(--razberry-light-border) !important;
  }

  #urlbar-background,
  .urlbar-background {
    background-color: var(--razberry-light-input) !important;
    border: 1px solid var(--razberry-light-border) !important;
    box-shadow: none !important;
  }

  #urlbar[focused="true"] #urlbar-background {
    border-color: var(--razberry-pink-primary) !important;
    box-shadow: 0 0 0 2px rgba(216, 27, 96, 0.25) !important;
  }

  .tabbrowser-tab[selected="true"] .tab-background {
    background-color: var(--razberry-light-tab-active) !important;
    border: 1px solid var(--razberry-pink-primary) !important;
  }

  /* Tombol Utama & Teks Terang */
  button.primary,
  .button-primary,
  #zen-welcome-start-button {
    background-color: var(--razberry-pink-primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
  }
}

/* Penataan Khusus DARK MODE */
@media (prefers-color-scheme: dark) {
  :root {
    --toolbar-bgcolor: var(--razberry-dark-surface) !important;
    --zen-themed-toolbar-bg: var(--razberry-dark-surface) !important;
    --zen-themed-toolbar-bg-transparent: var(--razberry-dark-surface) !important;
    --zen-main-browser-background: var(--razberry-dark-bg) !important;
    --zen-colors-primary: var(--razberry-dark-surface) !important;
    --zen-colors-secondary: var(--razberry-dark-input) !important;
    --zen-colors-tertiary: var(--razberry-dark-bg) !important;
    --zen-colors-border: var(--razberry-dark-border) !important;
    --toolbox-textcolor: var(--razberry-dark-text) !important;
    --toolbar-color: var(--razberry-dark-text) !important;
    --in-content-page-background: var(--razberry-dark-bg) !important;
    --in-content-page-color: var(--razberry-dark-text) !important;
  }

  #navigator-toolbox,
  #sidebar-box,
  #zen-sidebar-box {
    background-color: var(--razberry-dark-surface) !important;
    color: var(--razberry-dark-text) !important;
    border-color: var(--razberry-dark-border) !important;
  }

  #urlbar-background,
  .urlbar-background {
    background-color: var(--razberry-dark-input) !important;
    border: 1px solid var(--razberry-dark-border) !important;
    box-shadow: none !important;
  }

  #urlbar[focused="true"] #urlbar-background {
    border-color: var(--razberry-pink-vibrant) !important;
    box-shadow: 0 0 0 2px rgba(255, 64, 129, 0.3) !important;
  }

  .tabbrowser-tab[selected="true"] .tab-background {
    background-color: var(--razberry-dark-tab-active) !important;
    border: 1px solid var(--razberry-pink-vibrant) !important;
  }

  button.primary,
  .button-primary,
  #zen-welcome-start-button {
    background-color: var(--razberry-pink-primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
  }
}
"""

def patch_theme_in_omni_ja():
    """Suntikkan CSS tema Raspberry Pink baru ke dalam omni.ja."""
    omni_path = 'dist/RAZBerry/browser/omni.ja'
    temp_omni = 'dist/RAZBerry/browser/omni.ja.theme_tmp'

    if not os.path.exists(omni_path):
        log(f"{omni_path} tidak ditemukan!")
        return

    theme_css_code = build_pink_theme_css()
    log("Menyuntikkan tema Raspberry Pink ke dalam browser/omni.ja...")

    with zipfile.ZipFile(omni_path, 'r') as zin, zipfile.ZipFile(temp_omni, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            if item.filename == 'chrome/browser/content/browser/zen-styles/zen-theme.css':
                # Tambahkan CSS tema solid di akhir file
                text = content.decode('utf-8', errors='ignore')
                text = text + "\n" + theme_css_code
                content = text.encode('utf-8')
                log("zen-theme.css berhasil di-patch dengan tema solid pink.")
            zout.writestr(item, content)

    shutil.move(temp_omni, omni_path)
    log("Injeksi omni.ja selesai 100%!")

def update_website_theme():
    """Selaraskan palet Tailwind CSS di website razberry-www agar seragam dengan browser."""
    tailwind_file = 'razberry-www/tailwind.config.mjs'
    if not os.path.exists(tailwind_file):
        log(f"{tailwind_file} tidak ditemukan!")
        return

    log("Memperbarui palet warna di razberry-www/tailwind.config.mjs...")
    with open(tailwind_file, 'r', encoding='utf-8') as f:
        tw = f.read()

    # Ganti accent color lama (#C72C48) dengan #D81B60
    tw = tw.replace('#C72C48', '#D81B60')
    tw = tw.replace('#c72c48', '#D81B60')

    with open(tailwind_file, 'w', encoding='utf-8') as f:
        f.write(tw)
    log("tailwind.config.mjs berhasil diperbarui dengan aksen #D81B60.")

if __name__ == '__main__':
    log("Memulai penerapan tema Raspberry Pink...")
    update_preferences()
    update_source_yaml()
    patch_theme_in_omni_ja()
    update_website_theme()
    log("Penerapan tema Raspberry Pink selesai dengan sukses 100%!")
