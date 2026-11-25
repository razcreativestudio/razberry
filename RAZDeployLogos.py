# ==============================================================================
# RAZDeployLogos.py
# Waktu Pembuatan: 2026-11-24 18:42 WIB
# Author          : RAZ Creative Studio
# Deskripsi       : Skrip komprehensif untuk memproses dan menyebarkan logo baru:
#                   1. razberry-logo.png (Icon/Favicon/PE Exe/Window Titlebar)
#                   2. logo-razberry.png (Wordmark/About/Welcome/Website/BlankTab/Settings)
#                   3. Memperbaiki masalah -brand-shorter-name (BOM removal & FTL sync)
# ==============================================================================

import os
import io
import re
import math
import base64
import shutil
import zipfile
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
DIST_DIR = os.path.join(BASE_DIR, "dist", "RAZBerry")
WWW_DIR = os.path.join(BASE_DIR, "razberry-www")
BRANDING_DIR = os.path.join(BASE_DIR, "razberry", "configs", "branding", "release")
CONTENT_DIR = os.path.join(BRANDING_DIR, "content")

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(CONTENT_DIR, exist_ok=True)

def backup_file(file_path):
    """Menyimpan salinan backup file sebelum dimodifikasi sesuai protokol RAZ."""
    if os.path.exists(file_path):
        rel = os.path.relpath(file_path, BASE_DIR).replace(os.sep, "_")
        target = os.path.join(BACKUP_DIR, f"{rel}.bak")
        shutil.copy2(file_path, target)

def process_icon_logo():
    """Memproses razberry-logo.png untuk ikon aplikasi, favicon, titlebar, dan about icon."""
    icon_path = os.path.join(BASE_DIR, "razberry-logo.png")
    if not os.path.exists(icon_path):
        print(f"[!] {icon_path} tidak ditemukan!")
        return False
        
    print(f"[RAZ] Memproses ikon master: {icon_path}")
    im = Image.open(icon_path).convert("RGBA")
    w, h = im.size
    
    # Pastikan aspect ratio 1:1 (square canvas) agar tidak distorsi
    max_dim = max(w, h)
    square_im = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    offset_x = (max_dim - w) // 2
    offset_y = (max_dim - h) // 2
    square_im.paste(im, (offset_x, offset_y))
    
    # 1. Generate about-logo.png (512x512) & about-logo@2x.png (1024x1024)
    logo_512 = square_im.resize((512, 512), Image.Resampling.LANCZOS)
    logo_1024 = square_im.resize((1024, 1024), Image.Resampling.LANCZOS)
    
    logo_512.save(os.path.join(CONTENT_DIR, "about-logo.png"), "PNG")
    logo_512.save(os.path.join(CONTENT_DIR, "about-logo-private.png"), "PNG")
    logo_1024.save(os.path.join(CONTENT_DIR, "about-logo@2x.png"), "PNG")
    logo_1024.save(os.path.join(CONTENT_DIR, "about-logo-private@2x.png"), "PNG")
    
    # 2. Generate standard icon sizes di branding release
    for sz in [16, 22, 24, 32, 48, 64, 128, 256, 512, 1024]:
        resized = square_im.resize((sz, sz), Image.Resampling.LANCZOS)
        resized.save(os.path.join(BRANDING_DIR, f"logo{sz}.png"), "PNG")
        if sz in [16, 32, 48, 64, 128]:
            resized.save(os.path.join(CONTENT_DIR, f"icon{sz}.png"), "PNG")
            
    square_im.save(os.path.join(BRANDING_DIR, "logo.png"), "PNG")
    square_im.save(os.path.join(BRANDING_DIR, "logo-mac.png"), "PNG")
    
    # 3. Generate SVG version dari about-logo
    buf = io.BytesIO()
    logo_512.save(buf, format="PNG")
    b64_icon = base64.b64encode(buf.getvalue()).decode("ascii")
    about_logo_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="512" height="512" viewBox="0 0 512 512">
  <image width="512" height="512" xlink:href="data:image/png;base64,{b64_icon}" />
</svg>'''
    with open(os.path.join(CONTENT_DIR, "about-logo.svg"), "w", encoding="utf-8") as f:
        f.write(about_logo_svg)
    with open(os.path.join(CONTENT_DIR, "about-logo-private.svg"), "w", encoding="utf-8") as f:
        f.write(about_logo_svg)
        
    # 4. Update favicon di website razberry-www/public
    if os.path.exists(WWW_DIR):
        www_pub = os.path.join(WWW_DIR, "public")
        os.makedirs(www_pub, exist_ok=True)
        square_im.save(os.path.join(www_pub, "logo.png"), "PNG")
        square_im.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(www_pub, "favicon.png"), "PNG")
        with open(os.path.join(www_pub, "favicon.svg"), "w", encoding="utf-8") as f:
            f.write(about_logo_svg)
        print("  [+] Website public icons diperbarui (logo.png, favicon.png, favicon.svg)")

    print("[RAZ] Seluruh varian ikon razberry-logo.png berhasil dibuat.")
    return True

def process_wordmark_logo():
    """Memproses logo-razberry.png untuk wordmark, About, Welcome Screen, Blank Tab, & Settings."""
    wordmark_path = os.path.join(BASE_DIR, "logo-razberry.png")
    if not os.path.exists(wordmark_path):
        print(f"[!] {wordmark_path} tidak ditemukan!")
        return False
        
    print(f"[RAZ] Memproses logo horizontal wordmark: {wordmark_path}")
    im = Image.open(wordmark_path).convert("RGBA")
    
    # Crop ke bounding box konten aktif
    bbox = im.getbbox()
    cropped = im.crop(bbox)
    w, h = cropped.size
    print(f"  -> Dimensi cropped logo: {w}x{h}")
    
    # 1. Simpan versi resolusi tinggi di branding content
    cropped.save(os.path.join(CONTENT_DIR, "logo-razberry.png"), "PNG")
    
    # 2. Buat SVG wordmark yang tajam dan teroptimasi
    target_w = 1100
    target_h = int(h * (target_w / w))
    resized_wm = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    buf = io.BytesIO()
    resized_wm.save(buf, format="PNG", optimize=True)
    b64_wm = base64.b64encode(buf.getvalue()).decode("ascii")
    
    wordmark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {target_w} {target_h}" width="{target_w}" height="{target_h}">
  <image width="{target_w}" height="{target_h}" xlink:href="data:image/png;base64,{b64_wm}" />
</svg>'''

    with open(os.path.join(CONTENT_DIR, "about-wordmark.svg"), "w", encoding="utf-8") as f:
        f.write(wordmark_svg)
    with open(os.path.join(CONTENT_DIR, "firefox-wordmark.svg"), "w", encoding="utf-8") as f:
        f.write(wordmark_svg)
    print("  [+] about-wordmark.svg dan firefox-wordmark.svg berhasil dibuat.")
    
    # 3. Salin juga ke website razberry-www/public
    if os.path.exists(WWW_DIR):
        www_pub = os.path.join(WWW_DIR, "public")
        cropped.save(os.path.join(www_pub, "logo-razberry.png"), "PNG")
        cropped.save(os.path.join(www_pub, "logo-wordmark.png"), "PNG")
        print("  [+] Website logo-razberry.png dan logo-wordmark.png diperbarui.")
        
    return True

def fix_brand_ftl_and_properties():
    """Memperbaiki masalah -brand-shorter-name dengan menghapus UTF-8 BOM dan menyelaraskan FTL."""
    print("[RAZ] Memperbaiki variabel -brand-shorter-name dan menghapus BOM...")
    
    clean_ftl_content = """-brand-shorter-name = RAZBerry
-brand-short-name = RAZBerry
-brand-full-name = RAZBerry Browser
-brand-product-name = RAZBerry Browser
-vendor-short-name = RAZ Creative Studio
trademarkInfo = { " " }
"""
    clean_properties_content = """brandShorterName=RAZBerry
brandShortName=RAZBerry
brandFullName=RAZBerry Browser
vendorShortName=RAZ Creative Studio
"""
    # 1. Update di razberry/locales/
    locales_dir = os.path.join(BASE_DIR, "razberry", "locales")
    if os.path.exists(locales_dir):
        for root, dirs, files in os.walk(locales_dir):
            for f in files:
                if f == "brand.ftl":
                    p = os.path.join(root, f)
                    with open(p, "wb") as fp:
                        fp.write(clean_ftl_content.encode("utf-8")) # Tanpa BOM!
                elif f == "brand.properties":
                    p = os.path.join(root, f)
                    with open(p, "wb") as fp:
                        fp.write(clean_properties_content.encode("utf-8"))
        print("  [+] Seluruh brand.ftl & brand.properties di razberry/locales diperbarui tanpa BOM.")
        
    return clean_ftl_content, clean_properties_content

def update_blank_tab():
    """Membuat tampilan blank tab (about:blank) elegan dengan watermark logo-razberry."""
    blank_html = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>RAZBerry</title>
    <meta name="color-scheme" content="light dark" />
    <meta
      http-equiv="Content-Security-Policy"
      content="default-src chrome: 'unsafe-inline'; img-src chrome: data:; style-src chrome: 'unsafe-inline'; object-src 'none'"
    />
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        width: 100vw;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at center, #23060c 0%, #120305 100%);
        overflow: hidden;
        user-select: none;
      }
      .razberry-watermark {
        max-width: 360px;
        width: 60vw;
        height: auto;
        opacity: 0.22;
        filter: drop-shadow(0 6px 20px rgba(199, 44, 72, 0.35));
        transition: opacity 0.3s ease, transform 0.3s ease;
      }
      .razberry-watermark:hover {
        opacity: 0.45;
        transform: scale(1.03);
      }
    </style>
  </head>
  <body>
    <img src="chrome://branding/content/about-wordmark.svg" alt="RAZBerry" class="razberry-watermark" />
  </body>
</html>
"""
    return blank_html

def inject_all_into_omni():
    """Menginjeksi seluruh aset dan perbaikan ke dalam dist/RAZBerry/browser/omni.ja dan omni.ja."""
    browser_omni = os.path.join(DIST_DIR, "browser", "omni.ja")
    if not os.path.exists(browser_omni):
        print(f"[!] {browser_omni} tidak ditemukan!")
        return False
        
    backup_file(browser_omni)
    
    # Siapkan data aset
    with open(os.path.join(CONTENT_DIR, "about-logo.png"), "rb") as f:
        data_about_logo_png = f.read()
    with open(os.path.join(CONTENT_DIR, "about-logo@2x.png"), "rb") as f:
        data_about_logo_2x_png = f.read()
    with open(os.path.join(CONTENT_DIR, "about-logo.svg"), "rb") as f:
        data_about_logo_svg = f.read()
    with open(os.path.join(CONTENT_DIR, "about-wordmark.svg"), "rb") as f:
        data_about_wordmark_svg = f.read()
    with open(os.path.join(CONTENT_DIR, "logo-razberry.png"), "rb") as f:
        data_logo_razberry_png = f.read()
        
    clean_ftl_bytes = """-brand-shorter-name = RAZBerry
-brand-short-name = RAZBerry
-brand-full-name = RAZBerry Browser
-brand-product-name = RAZBerry Browser
-vendor-short-name = RAZ Creative Studio
trademarkInfo = { " " }
""".encode("utf-8") # PURE UTF-8 TANPA BOM!

    clean_prop_bytes = """brandShorterName=RAZBerry
brandShortName=RAZBerry
brandFullName=RAZBerry Browser
vendorShortName=RAZ Creative Studio
""".encode("utf-8")

    blank_tab_bytes = update_blank_tab().encode("utf-8")
    
    # CSS injection untuk About Dialog & Settings Sidebar
    about_css_override = """
#aboutDialogContainer {
  background: radial-gradient(circle at center, #23060c 0%, #120305 100%) !important;
  color: #ffffff !important;
}
#leftBox {
  background-size: 140px auto !important;
  background-position: center 30px !important;
}
#rightBox {
  background-image: url("chrome://branding/content/about-wordmark.svg") !important;
  background-size: 260px auto !important;
  background-repeat: no-repeat !important;
  background-position: left 0 !important;
  padding-top: 75px !important;
}
"""
    # CSS injection untuk Settings Menu (about:preferences)
    zen_prefs_override = """
#categories {
  padding-top: 10px !important;
}
.navigation::before {
  content: "";
  display: block;
  width: 180px;
  height: 42px;
  margin: 16px auto 14px auto;
  background-image: url("chrome://branding/content/about-wordmark.svg");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  filter: drop-shadow(0 2px 8px rgba(199, 44, 72, 0.4));
}
"""
    # CSS New Tab Activity Stream Wordmark
    activity_stream_override = """
.logo-and-wordmark .logo {
  background-image: url("chrome://branding/content/about-logo.png") !important;
  background-size: contain !important;
}
.logo-and-wordmark .wordmark {
  background-image: url("chrome://branding/content/about-wordmark.svg") !important;
  background-size: contain !important;
  width: 240px !important;
  height: 55px !important;
}
"""

    temp_omni = browser_omni + ".tmp"
    with zipfile.ZipFile(browser_omni, "r") as zin:
        with zipfile.ZipFile(temp_omni, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                fname = item.filename
                data = zin.read(fname)
                
                # 1. brand.ftl di seluruh bahasa (HAPUS BOM)
                if fname.startswith("localization/") and fname.endswith("/branding/brand.ftl"):
                    data = clean_ftl_bytes
                elif fname.startswith("chrome/") and fname.endswith("/branding/brand.properties"):
                    data = clean_prop_bytes
                    
                # 2. Wordmark & Logos
                elif fname == "chrome/browser/content/branding/about-logo.png":
                    data = data_about_logo_png
                elif fname == "chrome/browser/content/branding/about-logo@2x.png":
                    data = data_about_logo_2x_png
                elif fname == "chrome/browser/content/branding/about-logo.svg":
                    data = data_about_logo_svg
                elif fname == "chrome/browser/content/branding/about-wordmark.svg":
                    data = data_about_wordmark_svg
                elif fname == "chrome/browser/content/branding/firefox-wordmark.svg":
                    data = data_about_wordmark_svg
                elif fname == "chrome/browser/content/branding/about-logo-private.png":
                    data = data_about_logo_png
                elif fname == "chrome/browser/content/branding/about-logo-private.svg":
                    data = data_about_logo_svg
                    
                # 3. Blank Tab
                elif fname == "chrome/browser/content/browser/blanktab.html":
                    data = blank_tab_bytes
                    print("  [+] Diperbarui: blanktab.html dengan watermark RAZBerry")
                    
                # 4. About Dialog CSS
                elif fname == "chrome/browser/content/browser/aboutDialog.css":
                    text = data.decode("utf-8", errors="ignore")
                    text += "\n" + about_css_override
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: aboutDialog.css dengan wordmark logo-razberry")
                    
                # 5. Settings Menu CSS (zen-preferences.css)
                elif fname == "chrome/browser/skin/classic/browser/preferences/zen-preferences.css":
                    text = data.decode("utf-8", errors="ignore")
                    text += "\n" + zen_prefs_override
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: zen-preferences.css dengan logo header Settings")
                    
                # 6. New Tab Activity Stream CSS
                elif fname == "chrome/browser/builtin-addons/newtab/data/css/activity-stream.css":
                    text = data.decode("utf-8", errors="ignore")
                    text += "\n" + activity_stream_override
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: activity-stream.css NewTab dengan logo-razberry")
                    
                # 7. Welcome screen: pasang wordmark logo-razberry di welcome
                elif fname.endswith("zen-components/ZenWelcome.mjs"):
                    text = data.decode("utf-8", errors="ignore")
                    text = text.replace('src="chrome://branding/content/about-logo.png"', 'src="chrome://branding/content/about-wordmark.svg"')
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: ZenWelcome.mjs menggunakan about-wordmark.svg")
                    
                elif fname.endswith("zen-styles/zen-welcome.css"):
                    text = data.decode("utf-8", errors="ignore")
                    # Update ukuran logo welcome agar proporsional untuk wordmark horizontal
                    text = text.replace('height: 90px;\n      width: auto;\n      max-width: 140px;', 'height: 62px;\n      width: auto;\n      max-width: 320px;')
                    data = text.encode("utf-8")
                    print("  [+] Diperbarui: zen-welcome.css ukuran wordmark proporsional")
                    
                elif fname == "chrome/browser/content/branding/logo-razberry.png":
                    continue
                    
                zout.writestr(item, data)
                
            # Tambahkan file logo-razberry.png langsung
            zout.writestr("chrome/browser/content/branding/logo-razberry.png", data_logo_razberry_png)
            
    if os.path.exists(temp_omni):
        os.replace(temp_omni, browser_omni)
    print("[RAZ] Injeksi omni.ja berhasil 100%!")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("  RAZBerry Browser - Logo & Brand Deployment System")
    print("=" * 60)
    process_icon_logo()
    process_wordmark_logo()
    fix_brand_ftl_and_properties()
    inject_all_into_omni()
    print("=" * 60)
    print("  ✅ Deployment Aset Logo & Perbaikan Brand Selesai!")
    print("=" * 60)
