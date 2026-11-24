"""
==============================================================================
Metadata & Header File
Proyek        : RAZBerry Browser
File          : RAZPatchExeIcons.py
Dibuat Pada   : 2026-11-24
Author        : RAZ Creative Studio
Deskripsi     : Skrip otomatisasi injeksi resource icon Win32 PE pada razberry.exe.
                Mengganti seluruh embedded icon Zen Browser dengan ikon RAZBerry
                pada RT_GROUP_ICON 1, 2, 5, 6, dan 32512 agar icon di Taskbar,
                Window Titlebar, Alt-Tab, dan File Explorer 100% konsisten.
==============================================================================
"""

import os
import sys
import shutil
import struct
import io
from PIL import Image
import pefile

def make_dib_icon(img: Image.Image, size: int) -> bytes:
    """
    Membuat byte stream format DIB icon (32-bit RGBA) untuk Windows PE.
    Struktur DIB:
    - 40 byte BITMAPINFOHEADER (tinggi dikali 2 untuk XOR + AND mask)
    - Data piksel bottom-up dalam format BGRA
    - 1-bit per pixel AND mask (baris di-pad ke kelipatan 4 byte / 32-bit DWORD)
    """
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    rgba = resized.convert('RGBA')
    
    # 1. Header DIB
    bi_size = 40
    bi_width = size
    bi_height = size * 2  # DIB icon menyimpan 2x tinggi (XOR mask + AND mask)
    bi_planes = 1
    bi_bit_count = 32
    bi_compression = 0    # BI_RGB
    bi_size_image = size * size * 4
    bi_xpels_per_meter = 0
    bi_ypels_per_meter = 0
    bi_clr_used = 0
    bi_clr_important = 0
    
    header = struct.pack(
        '<IIIHHIIIIII',
        bi_size, bi_width, bi_height, bi_planes, bi_bit_count,
        bi_compression, bi_size_image, bi_xpels_per_meter,
        bi_ypels_per_meter, bi_clr_used, bi_clr_important
    )
    
    # 2. Piksel BGRA bottom-up
    pixels = bytearray()
    for y in reversed(range(size)):
        for x in range(size):
            r, g, b, a = rgba.getpixel((x, y))
            pixels.extend([b, g, r, a])
            
    # 3. AND mask (1 bit per piksel, baris di-pad ke 4 byte)
    mask_stride = ((size + 31) // 32) * 4
    and_mask = bytearray(mask_stride * size) # Seluruh piksel transparan di-handle oleh alpha channel 32-bit
    
    return header + bytes(pixels) + bytes(and_mask)

def make_png_icon(img: Image.Image, size: int = 256, max_bytes: int = 6000) -> bytes:
    """
    Membuat PNG berukuran 256x256 terkompresi optimal agar muat dalam slot resource.
    """
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    rgba = resized.convert('RGBA')
    
    # Coba kompresi dengan quantize warna bertingkat
    for colors in [128, 96, 64, 48, 32, 24, 16, 12, 8, 4]:
        for dither in [Image.Dither.FLOYDSTEINBERG, Image.Dither.NONE]:
            buf = io.BytesIO()
            rgba.quantize(colors=colors, dither=dither).save(buf, format='PNG', optimize=True, compress_level=9)
            data = buf.getvalue()
            if len(data) <= max_bytes:
                return data
            
    return data

def patch_executable_icons(exe_path: str, logo_path: str, backup_dir: str):
    print(f"[RAZ] Memulai patching PE icons: {exe_path}")
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"File {exe_path} tidak ditemukan!")
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo {logo_path} tidak ditemukan!")
        
    # Backup file exe
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, os.path.basename(exe_path))
    shutil.copy2(exe_path, backup_file)
    print(f"[RAZ] Backup berhasil dibuat: {backup_file}")
    
    source_img = Image.open(logo_path).convert('RGBA')
    
    # 0. Buat ikon multi-resolusi (16, 24, 32, 48, 64, 128, 256) pada canvas persegi
    square_canvas = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    temp_thumb = source_img.copy()
    temp_thumb.thumbnail((256, 256), Image.Resampling.LANCZOS)
    ox = (256 - temp_thumb.width) // 2
    oy = (256 - temp_thumb.height) // 2
    square_canvas.paste(temp_thumb, (ox, oy))
    
    multi_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    dist_dir = os.path.dirname(exe_path)
    for ico_name in ['RAZBerry.ico', 'razberry.ico']:
        ico_dest = os.path.join(dist_dir, ico_name)
        square_canvas.save(ico_dest, sizes=multi_sizes)
        print(f"[RAZ] Multi-resolution ICO tersimpan: {ico_dest}")

    # Salin ke folder chrome/icons/default dan browser/chrome/icons/default
    icon_variants = ['main-window.ico', 'default.ico', 'about.ico', 'aboutDialog.ico', 'Browser_About.ico', 'zen.ico', 'razberry.ico']
    for icon_sub in [os.path.join(dist_dir, 'chrome', 'icons', 'default'), os.path.join(dist_dir, 'browser', 'chrome', 'icons', 'default')]:
        os.makedirs(icon_sub, exist_ok=True)
        for iv in icon_variants:
            square_canvas.save(os.path.join(icon_sub, iv), sizes=multi_sizes)

    # Buat cache aset ikon per resolusi
    png_256 = make_png_icon(source_img, 256, max_bytes=6200)
    dib_128 = make_dib_icon(source_img, 128)
    dib_64  = make_dib_icon(source_img, 64)
    dib_48  = make_dib_icon(source_img, 48)
    dib_32  = make_dib_icon(source_img, 32)
    dib_16  = make_dib_icon(source_img, 16)
    
    # Pemetaan Icon ID ke byte data pengganti
    # Sesuai pemetaan pefile dari razberry.exe
    icon_replacement_map = {
        # Group 1 (IDI_APPICON - Main App)
        1: png_256,
        2: dib_64,
        3: dib_48,
        4: dib_32,
        5: dib_16,
        
        # Group 2 (Document icon)
        6: dib_16,
        7: dib_32,
        8: dib_48,
        9: dib_64,
        10: dib_128,
        11: png_256,
        
        # Group 32512 (IDI_APPLICATION - Windows Taskbar & System Dialogs)
        12: png_256,
        13: dib_64,
        14: dib_48,
        15: dib_32,
        16: dib_16,
        
        # Group 3 (Dialogs / Window icons - Titlebar & Dialog default)
        17: dib_16,
        18: dib_32,
        
        # Group 4 (Dialogs / Window icons - Titlebar & Dialog alternative)
        19: dib_16,
        20: dib_32,
        
        # Group 5 (Document PDF)
        21: dib_16,
        22: dib_32,
        23: dib_48,
        24: dib_64,
        25: dib_128,
        26: png_256,
        
        # Group 6 (Secondary Document)
        27: dib_16,
        28: dib_32,
        29: dib_48,
        30: dib_64,
        31: dib_128,
        32: png_256,
    }
    
    # Buka dan modifikasi raw binary
    with open(exe_path, 'rb') as f:
        exe_bytes = bytearray(f.read())
        
    pe = pefile.PE(data=exe_bytes)
    
    patched_count = 0
    for type_entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if type_entry.struct.Id == 3: # RT_ICON
            for icon_entry in type_entry.directory.entries:
                icon_id = icon_entry.struct.Id
                if icon_id in icon_replacement_map:
                    data_rva = icon_entry.directory.entries[0].data.struct.OffsetToData
                    data_size = icon_entry.directory.entries[0].data.struct.Size
                    offset = pe.get_offset_from_rva(data_rva)
                    
                    if icon_id in (1, 11, 26, 32):
                        new_data = make_png_icon(source_img, 256, max_bytes=data_size)
                    else:
                        new_data = icon_replacement_map[icon_id]
                    
                    if len(new_data) <= data_size:
                        # Tulis new_data dan padding jika ada sisa ruang (untuk PNG)
                        padded = new_data.ljust(data_size, b'\x00')
                        exe_bytes[offset:offset+data_size] = padded
                        patched_count += 1
                        print(f"  [+] Patched RT_ICON ID {icon_id:2d}: {len(new_data)} bytes pada offset {offset}")
                    else:
                        print(f"  [!] Peringatan: Data icon {icon_id} ({len(new_data)} bytes) melebihi kapasitas ({data_size} bytes)")
                        
    with open(exe_path, 'wb') as f:
        f.write(exe_bytes)
        
    print(f"[RAZ] Sukses memperbarui {patched_count} ikon di dalam binary {exe_path}!")

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    target_exe = os.path.join(base_dir, 'dist', 'RAZBerry', 'razberry.exe')
    logo_file = os.path.join(base_dir, 'razberry-logo.png')
    backup_folder = os.path.join(base_dir, 'backup')
    
    patch_executable_icons(target_exe, logo_file, backup_folder)
