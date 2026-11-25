# ==============================================================================
# RAZUpdateProfileAndTabs.py
# Modul Pembaruan Session Profile, Folder Space, & URL Tab Default RAZBerry
# Mengubah folder "zen basics" -> "razberry" dan mengganti URL tab Zen
# (Welcome & Privacy Policy) ke domain resmi https://razberry.it-raz.com/.
# Dibuat oleh: Senior Software Engineer & RAZ Specialist
# Timestamp: 2026-11-25
# ==============================================================================

import json
import os
import shutil
import struct
import zipfile
import lz4.block

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
PROFILE_DIR = os.path.expandvars(r"%APPDATA%\razberry\Profiles\dsph9rup.Default (release)")


def log(msg):
    print(f"[RAZ-TAB-UPDATE] {msg}")


def read_mozlz4(path):
    """Membaca dan mendekode berkas .jsonlz4 format Mozilla (header mozLz40\\0)."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"mozLz40\x00":
        raise ValueError(f"Header tidak valid pada {path}")
    raw = lz4.block.decompress(data[8:])
    return json.loads(raw.decode("utf-8"))


def write_mozlz4(path, obj):
    """Mengompresi dan menulis objek JSON kembali ke format .jsonlz4 Mozilla."""
    raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    compressed = lz4.block.compress(raw, store_size=True)
    with open(path, "wb") as f:
        f.write(b"mozLz40\x00" + compressed)


def transform_session_node(node):
    """
    Menjelajahi struktur JSON session secara rekursif untuk:
    1. Mengubah nama folder/group 'zen basics' -> 'razberry'.
    2. Mengubah URL zen-browser.app/welcome & privacy-policy -> razberry.it-raz.com.
    3. Menghapus cache favicon SVG Zen lama & policyContainer lama pada tab yang diubah.
    """
    changed = False

    if isinstance(node, list):
        for item in node:
            if transform_session_node(item):
                changed = True
        return changed

    if isinstance(node, dict):
        # 1. Ubah nama folder / group "zen basics" -> "razberry"
        if node.get("name") == "zen basics":
            node["name"] = "razberry"
            changed = True

        # 2. Ubah URL & Title pada entry tab
        url = node.get("url")
        if isinstance(url, str):
            new_url = None
            if "zen-browser.app/welcome" in url:
                new_url = "https://razberry.it-raz.com/welcome/"
                if node.get("title") in ("Welcome!", "Welcome to Zen"):
                    node["title"] = "Welcome to RAZBerry Browser"
            elif "zen-browser.app/privacy-policy" in url:
                new_url = "https://razberry.it-raz.com/privacy-policy/"
                if node.get("title") in ("Privacy Policy - Zen", "Privacy Policy"):
                    node["title"] = "Privacy Policy - RAZBerry"

            if new_url and new_url != url:
                node["url"] = new_url
                # Hapus principal/policyContainer lama agar origin baru razberry.it-raz.com bersih
                for key in ("policyContainer", "principalToInherit_base64", "children"):
                    if key in node:
                        del node[key]
                changed = True

        # 3. Ubah title langsung pada wrapper tab jika masih ada label Zen
        if node.get("title") == "Privacy Policy - Zen":
            node["title"] = "Privacy Policy - RAZBerry"
            changed = True

        # 4. Hapus cache favicon SVG Zen lama (lingkaran konsentris #F76F53)
        img = node.get("image")
        if isinstance(img, str) and ("RjJGMEUz" in img or "Rjc2RjUz" in img or "zen-browser.app" in img):
            node["image"] = None
            changed = True

        for key, val in list(node.items()):
            if isinstance(val, (dict, list)):
                if transform_session_node(val):
                    changed = True

    return changed


def update_profile_sessions():
    """Memperbarui semua berkas session .jsonlz4 pada profil RAZBerry aktif."""
    if not os.path.exists(PROFILE_DIR):
        log(f"Direktori profil tidak ditemukan: {PROFILE_DIR}")
        return

    prof_backup = os.path.join(BACKUP_DIR, "profile_dsph9rup")
    os.makedirs(prof_backup, exist_ok=True)

    target_files = [
        "zen-sessions.jsonlz4",
        "sessionstore.jsonlz4",
        os.path.join("sessionstore-backups", "recovery.jsonlz4"),
        os.path.join("sessionstore-backups", "recovery.baklz4"),
        os.path.join("sessionstore-backups", "previous.jsonlz4"),
        os.path.join("zen-sessions-backup", "clean.jsonlz4"),
        os.path.join("zen-sessions-backup", "recovery.baklz4"),
    ]

    for rel_path in target_files:
        full_path = os.path.join(PROFILE_DIR, rel_path)
        if not os.path.exists(full_path):
            continue

        # Backup sebelum modifikasi
        bak_dest = os.path.join(prof_backup, rel_path.replace(os.sep, "_"))
        if not os.path.exists(bak_dest):
            shutil.copy2(full_path, bak_dest)
            log(f"Backup dibuat: {bak_dest}")

        try:
            obj = read_mozlz4(full_path)
            if transform_session_node(obj):
                write_mozlz4(full_path, obj)
                log(f"Berhasil diperbarui: {rel_path}")
            else:
                log(f"Sudah bersih (tidak ada perubahan): {rel_path}")
        except Exception as e:
            log(f"Gagal memproses {rel_path}: {e}")


def update_omni_and_source():
    """Memperbarui ZenWelcome.mjs & aboutDialog.xhtml di omni.ja serta source files."""
    omni_path = os.path.join(BASE_DIR, "dist", "RAZBerry", "browser", "omni.ja")
    temp_omni = omni_path + ".tab_tmp"
    bak_omni = os.path.join(BACKUP_DIR, "omni.ja.tab_update.bak")

    if os.path.exists(omni_path):
        if not os.path.exists(bak_omni):
            shutil.copy2(omni_path, bak_omni)
            log(f"Backup omni.ja dibuat: {bak_omni}")

        modified = 0
        with zipfile.ZipFile(omni_path, "r") as zin, zipfile.ZipFile(temp_omni, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)

                if item.filename == "chrome/browser/content/browser/zen-components/ZenWelcome.mjs":
                    text = content.decode("utf-8", errors="replace")
                    if 'label: "razberrys"' in text:
                        text = text.replace('label: "razberrys"', 'label: "razberry"')
                        content = text.encode("utf-8")
                        modified += 1
                        log("ZenWelcome.mjs di omni.ja diperbarui: label -> 'razberry'")

                elif item.filename == "chrome/browser/content/browser/aboutDialog.xhtml":
                    text = content.decode("utf-8", errors="replace")
                    new_text = text.replace("https://www.zen-browser.app/privacy-policy/", "https://razberry.it-raz.com/privacy-policy/")
                    new_text = new_text.replace("https://zen-browser.app/about", "https://razberry.it-raz.com/about/")
                    if new_text != text:
                        content = new_text.encode("utf-8")
                        modified += 1
                        log("aboutDialog.xhtml di omni.ja diperbarui ke URL razberry.it-raz.com")

                zout.writestr(item, content)

        if modified > 0:
            shutil.move(temp_omni, omni_path)
            log(f"omni.ja sukses diperbarui ({modified} berkas).")
        else:
            if os.path.exists(temp_omni):
                os.remove(temp_omni)

    # Perbarui source files di razberry/src/ jika ada
    about_inc = os.path.join(BASE_DIR, "razberry", "src", "zen", "about", "zen-about.inc.xhtml")
    if os.path.exists(about_inc):
        with open(about_inc, "r", encoding="utf-8") as f:
            txt = f.read()
        if "https://www.zen-browser.app/privacy-policy/" in txt:
            bak_inc = os.path.join(BACKUP_DIR, "zen-about.inc.xhtml.bak")
            if not os.path.exists(bak_inc):
                shutil.copy2(about_inc, bak_inc)
            txt = txt.replace("https://www.zen-browser.app/privacy-policy/", "https://razberry.it-raz.com/privacy-policy/")
            with open(about_inc, "w", encoding="utf-8") as f:
                f.write(txt)
            log("Source zen-about.inc.xhtml diperbarui ke https://razberry.it-raz.com/privacy-policy/")


if __name__ == "__main__":
    log("Memulai pembaruan tab URL dan folder Space RAZBerry...")
    update_profile_sessions()
    update_omni_and_source()
    log("Selesai! Silakan buka kembali RAZBerry Browser untuk melihat hasilnya.")
