# ==============================================================================
# RAZCreateTransparentLogo.py
# Waktu Pembuatan: 2026-11-24 18:02 WIB
# Deskripsi: Skrip untuk mengonversi RAZ_Creative_Studio_Identik.svg menjadi aset
#            logo transparan (tanpa background) dalam format PNG dan SVG beresolusi tinggi,
#            serta menyalinnya ke direktori branding browser RAZBerry.
# ==============================================================================

import os
import re
import math
import base64
import shutil
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
os.makedirs(BACKUP_DIR, exist_ok=True)

def create_transparent_logo():
    """Mengekstrak logo dari RAZ_Creative_Studio_Identik.svg dan menghapus background hitamnya."""
    svg_source = os.path.join(BASE_DIR, "RAZ_Creative_Studio_Identik.svg")
    if not os.path.exists(svg_source):
        print(f"[ERROR] File {svg_source} tidak ditemukan!")
        return False

    print("[RAZ] Membaca sumber SVG:", svg_source)
    with open(svg_source, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Ekstrak data base64 JPEG
    m = re.search(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)', svg_content)
    if not m:
        print("[ERROR] Base64 JPEG tidak ditemukan di dalam SVG!")
        return False

    b64_data = m.group(1)
    raw_bytes = base64.b64decode(b64_data)

    # Simpan backup sementara
    raw_jpg_path = os.path.join(BACKUP_DIR, "RAZ_Creative_Studio_Raw.jpg")
    with open(raw_jpg_path, "wb") as f:
        f.write(raw_bytes)

    # Buka gambar menggunakan PIL
    im = Image.open(raw_jpg_path).convert("RGB")
    w, h = im.size
    print(f"[RAZ] Dimensi gambar: {w}x{h}")

    # Warna background dominan sekitar RGB(26, 28, 27)
    bg_r, bg_g, bg_b = 26, 28, 27
    rgba_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    src_pix = im.load()
    dst_pix = rgba_im.load()

    # Interpolasi alpha yang sangat mulus (anti-aliasing terjaga, bebas pinggiran hitam)
    for y in range(h):
        for x in range(w):
            r, g, b = src_pix[x, y]
            dist = math.sqrt((r - bg_r)**2 + (g - bg_g)**2 + (b - bg_b)**2)
            if dist <= 18.0:
                # Background murni -> 100% transparan
                dst_pix[x, y] = (0, 0, 0, 0)
            elif dist >= 40.0:
                # Konten murni -> 100% solid
                dst_pix[x, y] = (r, g, b, 255)
            else:
                # Gradasi transisi tepi halus
                alpha = int(255.0 * (dist - 18.0) / (40.0 - 18.0))
                dst_pix[x, y] = (r, g, b, alpha)

    # Bounding box konten
    bbox = rgba_im.getbbox()
    print(f"[RAZ] Bounding box konten: {bbox}")
    cropped_im = rgba_im.crop(bbox)

    # 1. Simpan PNG transparan di root
    out_png_root = os.path.join(BASE_DIR, "RAZ_Creative_Studio_Transparent.png")
    cropped_im.save(out_png_root, "PNG")
    print(f"[RAZ] Berhasil dibuat: {out_png_root} ({cropped_im.size})")

    # 2. Buat SVG transparan di root
    with open(out_png_root, "rb") as f:
        png_b64 = base64.b64encode(f.read()).decode("ascii")

    cw, ch = cropped_im.size
    svg_transparent_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{cw}" height="{ch}" viewBox="0 0 994 315" role="img" aria-label="RAZ Creative Studio Logo Tanpa Background">
  <image width="994" height="315" xlink:href="data:image/png;base64,{png_b64}" />
</svg>'''
    
    out_svg_root = os.path.join(BASE_DIR, "RAZ_Creative_Studio_Transparent.svg")
    with open(out_svg_root, "w", encoding="utf-8") as f:
        f.write(svg_transparent_content)
    print(f"[RAZ] Berhasil dibuat: {out_svg_root}")

    # 3. Salin juga ke direktori branding browser di razberry/configs/branding/release/content/
    branding_dir = os.path.join(BASE_DIR, "razberry", "configs", "branding", "release", "content")
    os.makedirs(branding_dir, exist_ok=True)

    branding_png = os.path.join(branding_dir, "raz-studio-logo.png")
    cropped_im.save(branding_png, "PNG")
    print(f"[RAZ] Disalin ke branding: {branding_png}")

    branding_svg = os.path.join(branding_dir, "raz-studio-logo.svg")
    with open(branding_svg, "w", encoding="utf-8") as f:
        f.write(svg_transparent_content)
    print(f"[RAZ] Disalin ke branding: {branding_svg}")

    # Hapus file raw sementara
    if os.path.exists(raw_jpg_path):
        os.remove(raw_jpg_path)

    return True

if __name__ == "__main__":
    create_transparent_logo()
