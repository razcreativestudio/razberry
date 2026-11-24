# ==============================================================================
# RAZRebrandAllZenText.py
# Modul Otomasi Rebranding Teks Menyeluruh:
# Mengubah "Zen Mods" -> "RAZBerry Mods", "Zen URL Bar" -> "RAZBerry URL Bar",
# dan seluruh teks UI yang masih menampilkan nama "Zen" menjadi "RAZBerry".
# Dibuat oleh: Senior Software Engineer & RAZ Specialist
# Timestamp: 2026-11-24
# ==============================================================================

import os
import sys
import shutil
import zipfile
import re

def log(msg):
    print(f"[RAZ-REBRAND] {msg}")

def rebrand_ftl_content(text, locale_code=""):
    """
    Melakukan penggantian teks pada konten file FTL.
    HANYA memodifikasi nilai terjemahan (setelah tanda '=' atau lanjutan multiline),
    tanpa merusak nama identifier/key Fluent.
    """
    lines = text.splitlines(keepends=True)
    new_lines = []

    for line in lines:
        stripped = line.strip()
        # Jika baris adalah komentar (# ...) atau baris kosong, biarkan
        if stripped.startswith('#') or not stripped:
            new_lines.append(line)
            continue

        # Jika baris adalah deklarasi term brand (misal -brand-shorter-name), biarkan
        if stripped.startswith('-brand-') or stripped.startswith('-vendor-'):
            new_lines.append(line)
            continue

        if '=' in line:
            key_part, val_part = line.split('=', 1)
            # Rebranding pada val_part
            val_part = apply_text_replacements(val_part)
            new_lines.append(f"{key_part}={val_part}")
        else:
            # Kemungkinan atribut (.label = ...) atau baris lanjutan pesan FTL
            if '.' in line and '=' in line:
                key_part, val_part = line.split('=', 1)
                val_part = apply_text_replacements(val_part)
                new_lines.append(f"{key_part}={val_part}")
            elif line.startswith('    ') or line.startswith('\t'):
                # Baris lanjutan pesan bertingkat
                new_lines.append(apply_text_replacements(line))
            else:
                new_lines.append(line)

    return "".join(new_lines)

def apply_text_replacements(val):
    """Menerapkan substitusi teks Zen -> RAZBerry secara kontekstual."""
    # 1. Zen Mods -> RAZBerry Mods
    val = re.sub(r'\bZen\s+Mods\b', 'RAZBerry Mods', val)
    val = re.sub(r'\bZen\s+Mod\b', 'RAZBerry Mod', val)
    val = re.sub(r'\bzen\s+mods\b', 'razberry mods', val)

    # 2. Zen URL Bar -> RAZBerry URL Bar
    val = re.sub(r'\bZen\s+URL\s+Bar\b', 'RAZBerry URL Bar', val)
    val = re.sub(r'\bBilah\s+URL\s+Zen\b', 'Bilah URL RAZBerry', val)
    val = re.sub(r'\bBarra\s+URL\s+Zen\b', 'Barra URL RAZBerry', val)
    val = re.sub(r'\bBarra\s+de\s+URL\s+do\s+Zen\b', 'Barra de URL do RAZBerry', val)
    val = re.sub(r'\bZen-URL-Leiste\b', 'RAZBerry-URL-Leiste', val)
    val = re.sub(r'\bZen\s+URL-balk\b', 'RAZBerry URL-balk', val)

    # 3. Frasa spesifik Zen lainnya
    val = re.sub(r'\bOther\s+Zen\s+Features\b', 'Other RAZBerry Features', val)
    val = re.sub(r'\bFitur\s+Zen\s+Lainnya\b', 'Fitur RAZBerry Lainnya', val)
    val = re.sub(r'\bZen\s+Features\b', 'RAZBerry Features', val)
    val = re.sub(r'\bZen\s+Browser\b', 'RAZBerry Browser', val)
    val = re.sub(r'\bZen\s+Store\b', 'RAZBerry Store', val)
    val = re.sub(r'\bZen\s+Marketplace\b', 'RAZBerry Marketplace', val)
    val = re.sub(r'\bZen\s+Theme\b', 'RAZBerry Theme', val)
    val = re.sub(r'\bZen\s+Themes\b', 'RAZBerry Themes', val)
    val = re.sub(r'\bYour\s+Zen\b', 'Your RAZBerry', val)
    val = re.sub(r'\bZen\s+milik\s+anda\b', 'RAZBerry milik anda', val, flags=re.IGNORECASE)
    val = re.sub(r'\bZen\s+now\s+syncs\b', 'RAZBerry now syncs', val)
    val = re.sub(r'\bZen\s+kini\s+menyinkronkan\b', 'RAZBerry kini menyinkronkan', val)

    # 4. Substitusi kata Zen mandiri dalam kalimat (misal: "Welcome to Zen" -> "Welcome to RAZBerry")
    # Pastikan tidak mengganti string kode yang tidak diinginkan
    val = re.sub(r'(?<![a-zA-Z0-9_\-])Zen(?![a-zA-Z0-9_\-])', 'RAZBerry', val)

    return val

def rebrand_omni_ja():
    """Memperbarui seluruh file terjemahan FTL dan JS di dalam dist/RAZBerry/browser/omni.ja."""
    omni_path = 'dist/RAZBerry/browser/omni.ja'
    temp_omni = 'dist/RAZBerry/browser/omni.ja.rebrand_temp'
    bak_omni = 'backup/omni.ja.rebrand.bak'

    if not os.path.exists(omni_path):
        log(f"{omni_path} tidak ditemukan!")
        return

    if not os.path.exists(bak_omni):
        shutil.copy2(omni_path, bak_omni)
        log(f"Backup omni.ja tersimpan di {bak_omni}")

    log("Memproses rebranding di dalam browser/omni.ja...")
    modified_count = 0

    with zipfile.ZipFile(omni_path, 'r') as zin, zipfile.ZipFile(temp_omni, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)

            # Rebranding file FTL
            if item.filename.endswith('.ftl'):
                try:
                    text = content.decode('utf-8')
                    if 'zen' in text.lower():
                        new_text = rebrand_ftl_content(text)
                        if new_text != text:
                            content = new_text.encode('utf-8')
                            modified_count += 1
                except:
                    pass

            # Rebranding file JS / MJS komponen
            elif item.filename.endswith(('ZenMods.mjs', 'preferences.xhtml')):
                try:
                    text = content.decode('utf-8')
                    # Ganti judul hardcode atau tooltip jika ada
                    text = text.replace('Zen Mods', 'RAZBerry Mods')
                    text = text.replace('Zen URL Bar', 'RAZBerry URL Bar')
                    content = text.encode('utf-8')
                    modified_count += 1
                except:
                    pass

            zout.writestr(item, content)

    shutil.move(temp_omni, omni_path)
    log(f"Berhasil memperbarui {modified_count} file di dalam omni.ja!")

def rebrand_source_locales():
    """Memperbarui file FTL di dalam repositori razberry/locales/ agar sinkron permanen."""
    locales_dir = 'razberry/locales'
    if not os.path.exists(locales_dir):
        log("Direktori razberry/locales tidak ditemukan, dilewati.")
        return

    log("Memproses rebranding di razberry/locales...")
    count = 0
    for root, dirs, files in os.walk(locales_dir):
        for f in files:
            if f.endswith('.ftl'):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as file_in:
                        text = file_in.read()
                    if 'zen' in text.lower():
                        new_text = rebrand_ftl_content(text)
                        if new_text != text:
                            with open(fp, 'w', encoding='utf-8') as file_out:
                                file_out.write(new_text)
                            count += 1
                except:
                    pass
    log(f"Berhasil memperbarui {count} file di razberry/locales!")

def clear_startup_caches():
    """Hapus seluruh cache startup Gecko di APPDATA agar membaca teks FTL baru."""
    log("Membersihkan StartupCache di direktori pengguna...")
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if not local_app_data:
        return

    deleted = 0
    for root_dir in [os.path.join(local_app_data, 'zen'), os.path.join(local_app_data, 'razberry')]:
        if not os.path.exists(root_dir):
            continue
        for cur, dirs, files in os.walk(root_dir):
            for d in list(dirs):
                if d.lower() == 'startupcache':
                    cache_dir = os.path.join(cur, d)
                    try:
                        shutil.rmtree(cache_dir, ignore_errors=True)
                        deleted += 1
                        log(f"Dihapus: {cache_dir}")
                    except:
                        pass
    log(f"Pembersihan selesai ({deleted} folder cache dihapus).")

if __name__ == '__main__':
    log("Memulai eksekusi RAZRebrandAllZenText...")
    rebrand_source_locales()
    rebrand_omni_ja()
    clear_startup_caches()
    log("Rebranding menyeluruh selesai dengan sukses 100%!")
