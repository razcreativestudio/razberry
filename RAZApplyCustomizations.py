"""
==============================================================================
Metadata & Header File
Proyek        : RAZBerry Browser
File          : RAZApplyCustomizations.py
Dibuat Pada   : 2026-11-24
Author        : RAZ Creative Studio
Deskripsi     : Skrip otomatisasi penerapan kustomisasi lengkap RAZBerry:
                1. Mematikan seluruh mekanisme Auto-Update Zen Browser
                2. Mengubah tema visual menjadi Solid Raspberry Red (#C72C48)
                   dan mematikan Mica / Glassmorphism / Acrylic / Blur
                3. Mengubah nama folder awal space menjadi "razberrys"
                4. Mengubah URL Welcome ke https://razberry.it-raz.com/welcome/
                   dan Privacy Policy ke https://razberry.it-raz.com/privacy-policy/
                5. Mengganti defaultFavicon.svg dan favicon.svg dengan logo RAZBerry
==============================================================================
"""

import os
import shutil
import zipfile
import re
import base64

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist", "RAZBerry")
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
LOGO_PNG = os.path.join(BASE_DIR, "razberry-logo.png")

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_file(filepath: str):
    if os.path.exists(filepath):
        dest = os.path.join(BACKUP_DIR, os.path.basename(filepath))
        shutil.copy2(filepath, dest)
        print(f"[RAZ] Backup diamankan: {dest}")

def generate_svg_favicon(png_path: str) -> str:
    """Membuat SVG favicon yang membungkus gambar logo RAZBerry secara tajam."""
    with open(png_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="16" height="16">
  <image width="32" height="32" href="data:image/png;base64,{b64}"/>
</svg>'''

def update_ini_files():
    """Perbarui application.ini dan browser/application.ini agar konsisten dengan identitas RAZBerry."""
    for rel_path in ["application.ini", os.path.join("browser", "application.ini")]:
        ini_path = os.path.join(DIST_DIR, rel_path)
        if not os.path.exists(ini_path):
            continue
        backup_file(ini_path)
        with open(ini_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = re.sub(r"(?m)^Vendor=.*", "Vendor=RAZ Creative Studio", content)
        content = re.sub(r"(?m)^Name=.*", "Name=RAZBerry", content)
        content = re.sub(r"(?m)^RemotingName=.*", "RemotingName=razberry", content)
        content = re.sub(r"(?m)^Version=.*", "Version=1.0.0", content)
        content = re.sub(r"(?m)^Profile=.*", "Profile=razberry", content)
        # Matikan URL update di application.ini
        content = re.sub(r"(?m)^URL=.*", "URL=", content)
        
        with open(ini_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[RAZ] application.ini diperbarui: {rel_path}")

def update_prefs():
    """Tulis preferensi default RAZBerry untuk mematikan update & glassmorphism."""
    pref_dir = os.path.join(DIST_DIR, "defaults", "pref")
    os.makedirs(pref_dir, exist_ok=True)
    pref_file = os.path.join(pref_dir, "razberry-prefs.js")
    
    prefs_content = """// ==============================================================================
// Preferensi Default RAZBerry Browser - RAZ Creative Studio
// ==============================================================================

// 1. Identitas & Tema Solid Raspberry Red (Matikan Glassmorphism & Mica)
pref("zen.theme.accent-color", "#C72C48");
pref("widget.windows.mica", false);
pref("widget.windows.mica.toplevel-backdrop", 0);
pref("zen.theme.acrylic-sidebar", false);
pref("zen.theme.acrylic-urlbar", false);
pref("zen.widget.linux.transparency", false);
pref("browser.tabs.warnOnClose", false);

// 2. Matikan Total Background Auto-Update Zen Browser
pref("app.update.enabled", false);
pref("app.update.auto", false);
pref("app.update.mode", 0);
pref("app.update.service.enabled", false);
pref("app.update.silent", false);
pref("app.update.staging.enabled", false);
pref("app.update.doorhanger", false);
pref("app.update.badge", false);
pref("app.update.url", "");
pref("app.update.url.details", "");
pref("app.update.url.manual", "https://razberry.it-raz.com/download/");
pref("app.update.interval", 999999999);

// 3. Konfigurasi Welcome URL & Homepage RAZBerry
pref("zen.welcome-screen.seen", false);
pref("startup.homepage_welcome_url", "https://razberry.it-raz.com/welcome/");
pref("startup.homepage_welcome_url.additional", "https://razberry.it-raz.com/privacy-policy/");
pref("startup.homepage_override_url", "https://razberry.it-raz.com/whatsnew/");
pref("app.releaseNotesURL", "https://razberry.it-raz.com/whatsnew/");
pref("app.releaseNotesURL.aboutDialog", "https://razberry.it-raz.com/release-notes/");
"""
    with open(pref_file, "w", encoding="utf-8") as f:
        f.write(prefs_content)
    print(f"[RAZ] razberry-prefs.js diperbarui di {pref_file}")

def update_update_settings():
    """Kosongkan accepted channel di update-settings.ini agar tidak download build zen."""
    update_ini = os.path.join(DIST_DIR, "update-settings.ini")
    if os.path.exists(update_ini):
        backup_file(update_ini)
        with open(update_ini, "w", encoding="utf-8") as f:
            f.write("; Updates disabled for RAZBerry standalone\n[Settings]\nACCEPTED_MAR_CHANNEL_IDS=\n")
        print("[RAZ] update-settings.ini dikunci.")

def update_browser_omni():
    """Injeksi kustomisasi ke dalam dist/RAZBerry/browser/omni.ja."""
    omni_path = os.path.join(DIST_DIR, "browser", "omni.ja")
    if not os.path.exists(omni_path):
        print(f"[!] {omni_path} tidak ditemukan, lewati.")
        return
        
    backup_file(omni_path)
    svg_favicon = generate_svg_favicon(LOGO_PNG)
    
    # CSS Solid Raspberry Red Theme Override
    theme_override_css = """
/* ========================================================================== */
/* RAZBerry Browser - Solid Raspberry Red Theme (No Glassmorphism / Acrylic)  */
/* ========================================================================== */
:root,
#main-window,
#main-window[windowtype="navigator:browser"]:not([popup-window]) {
  --zen-primary-color: #C72C48 !important;
  --zen-themed-toolbar-bg: #1A0508 !important;
  --zen-themed-toolbar-bg-transparent: #1A0508 !important;
  --zen-colors-primary: #120305 !important;
  --zen-colors-secondary: #1A0508 !important;
  --zen-colors-tertiary: #26080F !important;
  --toolbar-bgcolor: #1A0508 !important;
  --zen-background-opacity: 1 !important;
  background: #120305 !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

#browser,
#navigator-toolbox,
#sidebar-box,
.zen-sidebar,
#zen-sidebar-web-panel,
#tabbrowser-tabpanels {
  background: #1A0508 !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

#urlbar,
#urlbar-background,
#urlbar[breakout-extend] {
  background: #26080F !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border-color: #C72C48 !important;
}
"""

    # Aset logo transparan RAZ Creative Studio
    raz_studio_png = os.path.join(BASE_DIR, "razberry", "configs", "branding", "release", "content", "raz-studio-logo.png")
    raz_studio_svg = os.path.join(BASE_DIR, "razberry", "configs", "branding", "release", "content", "raz-studio-logo.svg")
    
    src_welcome_mjs = os.path.join(BASE_DIR, "razberry", "src", "zen", "welcome", "ZenWelcome.mjs")
    src_welcome_css = os.path.join(BASE_DIR, "razberry", "src", "zen", "welcome", "zen-welcome.css")

    temp_omni = omni_path + ".tmp"
    with zipfile.ZipFile(omni_path, "r") as zin:
        with zipfile.ZipFile(temp_omni, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                
                # 1. ZenWelcome.mjs -> Injeksi kode welcome screen lengkap dengan kedua logo
                if item.filename.endswith("zen-components/ZenWelcome.mjs"):
                    if os.path.exists(src_welcome_mjs):
                        with open(src_welcome_mjs, "rb") as f:
                            data = f.read()
                        print("  [+] Diperbarui: ZenWelcome.mjs (Dual logo & RAZBerry welcome logic)")
                    else:
                        text = data.decode("utf-8", errors="ignore")
                        text = text.replace('label: "zen basics"', 'label: "razberrys"')
                        data = text.encode("utf-8")
                        print("  [+] Diperbarui: ZenWelcome.mjs (label -> 'razberrys')")
                        
                # 2. zen-welcome.css -> Injeksi styling welcome screen baru tanpa background video & dual logo
                elif item.filename.endswith("zen-styles/zen-welcome.css"):
                    if os.path.exists(src_welcome_css):
                        with open(src_welcome_css, "rb") as f:
                            data = f.read()
                        print("  [+] Diperbarui: zen-welcome.css (Styling dual logo, radial dark berry & no video)")

                # 3. zen-welcome.ftl -> Ubah teks judul sambutan
                elif item.filename.endswith("zen-welcome.ftl"):
                    text = data.decode("utf-8", errors="ignore")
                    text = text.replace("zen-welcome-title-line1 = Welcome to", "zen-welcome-title-line1 = Welcome to RAZBerry Browser")
                    text = text.replace("zen-welcome-title-line2 = a calmer internet", "zen-welcome-title-line2 = By RAZ Creative Studio")
                    data = text.encode("utf-8")
                    
                # 4. firefox-branding.js -> ganti URL zen-browser.app ke razberry.it-raz.com
                elif item.filename == "defaults/preferences/firefox-branding.js":
                    text = data.decode("utf-8", errors="ignore")
                    text = text.replace("https://zen-browser.app/welcome/", "https://razberry.it-raz.com/welcome/")
                    text = text.replace("https://zen-browser.app/privacy-policy/", "https://razberry.it-raz.com/privacy-policy/")
                    text = text.replace("https://zen-browser.app/whatsnew", "https://razberry.it-raz.com/whatsnew")
                    text = text.replace("https://zen-browser.app/download/", "https://razberry.it-raz.com/download/")
                    text = text.replace("https://zen-browser.app/release-notes/", "https://razberry.it-raz.com/release-notes/")
                    text = text.replace("https://www.zen-browser.app/release-notes/", "https://razberry.it-raz.com/release-notes/")
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: firefox-branding.js (URLs -> razberry.it-raz.com)")
                    
                # 5. zen-about.xhtml -> sembunyikan update & update tautan legal
                elif item.filename.endswith("zen-about.xhtml"):
                    text = data.decode("utf-8", errors="ignore")
                    text = text.replace('id="zen-about-update" data-state="never-checked"', 'id="zen-about-update" hidden="true" data-state="never-checked"')
                    text = text.replace("https://www.zen-browser.app/privacy-policy/", "https://razberry.it-raz.com/privacy-policy/")
                    text = text.replace("https://www.zen-browser.app/donate", "https://razberry.it-raz.com/donate")
                    text = text.replace("https://github.com/zen-browser/desktop", "https://razberry.it-raz.com")
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: zen-about.xhtml (Update disembunyikan & URLs diperbarui)")
                    
                # 6. zen-theme.css -> sisipkan tema solid raspberry
                elif item.filename == "chrome/browser/content/browser/zen-styles/zen-theme.css":
                    text = data.decode("utf-8", errors="ignore")
                    text = text.replace("--zen-primary-color: AccentColor;", "--zen-primary-color: #C72C48;")
                    text += "\n" + theme_override_css
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: zen-theme.css (Solid Raspberry Theme diinjeksi)")
                    
                # 7. privatebrowsing/favicon.svg
                elif item.filename.endswith("privatebrowsing/favicon.svg"):
                    data = svg_favicon.encode("utf-8")
                    print("  [+] Diperbarui: privatebrowsing/favicon.svg")
                    
                # 8. Skip logo branding agar tidak duplikat saat dijalankan berulang
                elif item.filename in ("chrome/browser/content/branding/raz-studio-logo.png", "chrome/browser/content/branding/raz-studio-logo.svg"):
                    continue
                    
                zout.writestr(item, data)
                
            # Tambahkan aset logo transparan RAZ Creative Studio ke dalam browser/omni.ja
            if os.path.exists(raz_studio_png):
                with open(raz_studio_png, "rb") as f:
                    zout.writestr("chrome/browser/content/branding/raz-studio-logo.png", f.read())
                print("  [+] Ditambahkan: chrome/browser/content/branding/raz-studio-logo.png")
            if os.path.exists(raz_studio_svg):
                with open(raz_studio_svg, "rb") as f:
                    zout.writestr("chrome/browser/content/branding/raz-studio-logo.svg", f.read())
                print("  [+] Ditambahkan: chrome/browser/content/branding/raz-studio-logo.svg")
                
    if os.path.exists(temp_omni):
        os.replace(temp_omni, omni_path)
    print(f"[RAZ] browser/omni.ja berhasil diperbarui.")

def update_root_omni():
    """Injeksi defaultFavicon.svg ke dalam dist/RAZBerry/omni.ja."""
    omni_path = os.path.join(DIST_DIR, "omni.ja")
    if not os.path.exists(omni_path):
        print(f"[!] {omni_path} tidak ditemukan, lewati.")
        return
        
    backup_file(omni_path)
    svg_favicon = generate_svg_favicon(LOGO_PNG)
    
    temp_omni = omni_path + ".tmp"
    with zipfile.ZipFile(omni_path, "r") as zin:
        with zipfile.ZipFile(temp_omni, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "chrome/toolkit/skin/classic/global/icons/defaultFavicon.svg":
                    data = svg_favicon.encode("utf-8")
                    print("  [+] Diperbarui: root omni.ja defaultFavicon.svg")
                zout.writestr(item, data)
                
    if os.path.exists(temp_omni):
        os.replace(temp_omni, omni_path)
    print(f"[RAZ] root omni.ja berhasil diperbarui.")

def update_source_files():
    """Sinkronkan perubahan juga ke dalam file repositori sumber razberry/."""
    # 1. ZenWelcome.mjs
    src_welcome = os.path.join(BASE_DIR, "razberry", "src", "zen", "welcome", "ZenWelcome.mjs")
    if os.path.exists(src_welcome):
        backup_file(src_welcome)
        with open(src_welcome, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('label: "zen basics"', 'label: "razberrys"')
        with open(src_welcome, "w", encoding="utf-8") as f:
            f.write(content)
        print("[RAZ] razberry/src/zen/welcome/ZenWelcome.mjs diselaraskan.")
        
    # 2. theme.yaml
    src_theme_yaml = os.path.join(BASE_DIR, "razberry", "prefs", "zen", "theme.yaml")
    if os.path.exists(src_theme_yaml):
        backup_file(src_theme_yaml)
        with open(src_theme_yaml, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r"- name: zen\.theme\.acrylic-urlbar\s*\n\s*value: true", "- name: zen.theme.acrylic-urlbar\n  value: false", content)
        content = re.sub(r"- name: zen\.theme\.acrylic-sidebar\s*\n\s*value: .*", "- name: zen.theme.acrylic-sidebar\n  value: false", content)
        with open(src_theme_yaml, "w", encoding="utf-8") as f:
            f.write(content)
        print("[RAZ] razberry/prefs/zen/theme.yaml diselaraskan.")
        
    # 3. windows.yaml
    src_win_yaml = os.path.join(BASE_DIR, "razberry", "prefs", "zen", "windows.yaml")
    if os.path.exists(src_win_yaml):
        backup_file(src_win_yaml)
        with open(src_win_yaml, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r"- name: widget\.windows\.mica\s*\n\s*value: true", "- name: widget.windows.mica\n  value: false", content)
        with open(src_win_yaml, "w", encoding="utf-8") as f:
            f.write(content)
        print("[RAZ] razberry/prefs/zen/windows.yaml diselaraskan.")

if __name__ == "__main__":
    print("============================================================")
    print("  🍓 RAZBerry Browser - Customization Application System")
    print("============================================================")
    update_ini_files()
    update_prefs()
    update_update_settings()
    update_browser_omni()
    update_root_omni()
    update_source_files()
    print("============================================================")
    print("  ✅ Seluruh kustomisasi RAZBerry berhasil diaplikasikan!")
    print("============================================================")
