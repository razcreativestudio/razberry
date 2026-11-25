"""
==============================================================================
Metadata & Header File
Proyek        : RAZBerry Browser
File          : RAZRebrandWebsite.py
Dibuat Pada   : 2026-11-24
Author        : RAZ Creative Studio
Deskripsi     : Skrip otomatisasi rebranding website resmi RAZBerry:
                - Mengonversi source code website zen-browser/www menjadi
                  website resmi RAZBerry (https://razberry.it-raz.com).
                - Memperbarui halaman utama (/), welcome (/welcome/), dan
                  privacy policy (/privacy-policy/).
                - Menyematkan aset logo, favicon, dan tema warna Raspberry Red.
==============================================================================
"""

import os
import shutil
import json
import base64
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WWW_DIR = os.path.join(BASE_DIR, "razberry-www")
LOGO_PNG = os.path.join(BASE_DIR, "razberry-logo.png")
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

def rebrand_assets():
    print("[1/6] Menyalin aset logo & favicon ke public/...")
    public_dir = os.path.join(WWW_DIR, "public")
    os.makedirs(public_dir, exist_ok=True)
    
    # Salin logo png
    shutil.copy2(LOGO_PNG, os.path.join(public_dir, "logo.png"))
    shutil.copy2(LOGO_PNG, os.path.join(public_dir, "favicon.png"))
    shutil.copy2(LOGO_PNG, os.path.join(public_dir, "share-pic.png"))
    
    # Salin razberry.ico
    ico_src = os.path.join(BASE_DIR, "dist", "RAZBerry", "razberry.ico")
    if os.path.exists(ico_src):
        shutil.copy2(ico_src, os.path.join(public_dir, "favicon.ico"))
        
    # Buat favicon.svg
    with open(LOGO_PNG, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
        
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <image width="32" height="32" href="data:image/png;base64,{b64}"/>
</svg>'''
    with open(os.path.join(public_dir, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("      Aset public/ berhasil diperbarui.")

def rebrand_astro_config():
    print("[2/6] Memperbarui astro.config.mjs...")
    cfg_path = os.path.join(WWW_DIR, "astro.config.mjs")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("https://zen-browser.app", "https://razberry.it-raz.com")
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("      astro.config.mjs domain diubah ke https://razberry.it-raz.com")

def rebrand_logo_component():
    print("[3/6] Memperbarui Logo.astro...")
    logo_component = os.path.join(WWW_DIR, "src", "components", "Logo.astro")
    if os.path.exists(logo_component):
        new_logo_astro = """---
const { class: className } = Astro.props
---

<img
  src="/logo.png"
  alt="RAZBerry Logo"
  class={className}
  width="32"
  height="32"
  style="object-fit: contain;"
/>
"""
        with open(logo_component, "w", encoding="utf-8") as f:
            f.write(new_logo_astro)
        print("      Logo.astro diarahkan ke /logo.png")

def rebrand_styles():
    print("[4/6] Menyesuaikan tema warna di src/styles/global.css...")
    global_css = os.path.join(WWW_DIR, "src", "styles", "global.css")
    if os.path.exists(global_css):
        with open(global_css, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Ganti accent color coral ke Raspberry Red #C72C48
        content = content.replace("--color-coral: #f76f53;", "--color-coral: #C72C48;")
        content = content.replace("--color-zen-blue: #6287f5;", "--color-zen-blue: #C72C48;")
        
        with open(global_css, "w", encoding="utf-8") as f:
            f.write(content)
        print("      Warna aksen global diset ke Raspberry Red #C72C48.")

def rebrand_translations():
    print("[5/6] Memperbarui teks & i18n translation.json...")
    en_trans_path = os.path.join(WWW_DIR, "src", "i18n", "en", "translation.json")
    if os.path.exists(en_trans_path):
        with open(en_trans_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        # Rebranding istilah Zen -> RAZBerry
        text = text.replace("Zen Browser", "RAZBerry Browser")
        text = text.replace("Zen browser", "RAZBerry browser")
        text = text.replace("zen browser", "razberry browser")
        text = text.replace("Zen", "RAZBerry")
        text = text.replace("zen-browser.app", "razberry.it-raz.com")
        text = text.replace("https://www.zen-browser.app", "https://razberry.it-raz.com")
        text = text.replace("github.com/zen-browser", "github.com/it-raz")
        
        # Load JSON untuk custom tuning khusus welcome & privacy policy
        data = json.loads(text)
        
        # Welcome Page
        if "layout" in data and "welcome" in data["layout"]:
            data["layout"]["welcome"]["title"] = "Welcome to RAZBerry!"
            data["layout"]["welcome"]["description"] = "Welcome to RAZBerry Browser by RAZ Creative Studio!"
        if "routes" in data and "welcome" in data["routes"]:
            data["routes"]["welcome"]["title"] = ["Welcome ", "to ", "RAZBerry!"]
            
        # Privacy Policy Page
        if "layout" in data and "privacyPolicy" in data["layout"]:
            data["layout"]["privacyPolicy"]["title"] = "Privacy Policy - RAZBerry"
            data["layout"]["privacyPolicy"]["description"] = "Privacy is a fundamental right. RAZBerry collects zero telemetry, zero analytics, and protects your browsing data."
        if "routes" in data and "privacyPolicy" in data["routes"]:
            data["routes"]["privacyPolicy"]["title"] = "Privacy Policy"
            data["routes"]["privacyPolicy"]["lastUpdated"] = "Last Updated: November 24, 2026"
            if "sections" in data["routes"]["privacyPolicy"]:
                sec = data["routes"]["privacyPolicy"]["sections"]
                if "introduction" in sec:
                    sec["introduction"]["title"] = "Introduction"
                    sec["introduction"]["body"] = "RAZBerry Browser is created by RAZ Creative Studio with an absolute commitment to privacy. We believe that what you do on the Web is entirely your own business. RAZBerry does not track you, does not harvest telemetry, and does not sell your data."
                    sec["introduction"]["summary"] = "Zero telemetry. Zero tracking. 100% open, private, and customizable."
                    
        # Home & Nav
        if "components" in data and "nav" in data["components"]:
            data["components"]["nav"]["brand"] = "RAZBerry"
            
        with open(en_trans_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("      en/translation.json berhasil di-rebrand secara komprehensif.")

def rebrand_package_json():
    print("[6/6] Memperbarui package.json & README.md...")
    pkg_path = os.path.join(WWW_DIR, "package.json")
    if os.path.exists(pkg_path):
        with open(pkg_path, "r", encoding="utf-8") as f:
            pkg = json.load(f)
        pkg["name"] = "razberry-www"
        pkg["description"] = "Official Website for RAZBerry Browser by RAZ Creative Studio"
        with open(pkg_path, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2)
            
    readme_path = os.path.join(WWW_DIR, "README.md")
    readme_content = """# RAZBerry Official Website

Repositori website resmi **RAZBerry Browser** (`https://razberry.it-raz.com`).

Dibangun menggunakan **Astro**, **React**, dan **Tailwind CSS**.

## Halaman Utama
- Landing Page: `/`
- Welcome Page: `/welcome` -> `https://razberry.it-raz.com/welcome/`
- Privacy Policy: `/privacy-policy` -> `https://razberry.it-raz.com/privacy-policy/`
- Download: `/download`

## Lisensi
MPL 2.0 - RAZ Creative Studio
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("      package.json & README.md berhasil diperbarui.")

if __name__ == "__main__":
    print("============================================================")
    print("  RAZBerry Website - Rebranding & Setup System")
    print("============================================================")
    rebrand_assets()
    rebrand_astro_config()
    rebrand_logo_component()
    rebrand_styles()
    rebrand_translations()
    rebrand_package_json()
    print("============================================================")
    print("  ✅ Rebranding website RAZBerry selesai!")
    print("============================================================")
