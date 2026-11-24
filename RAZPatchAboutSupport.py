# ==============================================================================
# RAZPatchAboutSupport.py
# Modul Otomasi Perbaikan about:support dan AppConstants:
# Mengubah 'Name Zen' menjadi 'Name RAZBerry' pada halaman Troubleshooting Information.
# Dibuat oleh: Senior Software Engineer & RAZ Specialist
# Timestamp: 2026-11-24
# ==============================================================================

import os
import sys
import shutil
import zipfile
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_OMNI = os.path.join(BASE_DIR, "dist", "RAZBerry", "omni.ja")
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

def log(msg):
    print(f"[RAZ-SUPPORT] {msg}")

def patch_root_omni():
    """Melakukan patching pada root dist/RAZBerry/omni.ja."""
    if not os.path.exists(ROOT_OMNI):
        log(f"File {ROOT_OMNI} tidak ditemukan!")
        return False

    os.makedirs(BACKUP_DIR, exist_ok=True)
    bak_file = os.path.join(BACKUP_DIR, "omni.ja.root.support.bak")
    if not os.path.exists(bak_file):
        shutil.copy2(ROOT_OMNI, bak_file)
        log(f"Backup root omni.ja tersimpan di: {bak_file}")

    temp_omni = ROOT_OMNI + ".tmp"
    patched_count = 0

    with zipfile.ZipFile(ROOT_OMNI, "r") as zin, zipfile.ZipFile(temp_omni, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)

            # 1. Patch modules/Troubleshoot.sys.mjs
            if item.filename == "modules/Troubleshoot.sys.mjs":
                text = content.decode("utf-8", errors="replace")
                old_str = "name: Services.appinfo.name,"
                new_str = 'name: "RAZBerry",'
                if old_str in text:
                    text = text.replace(old_str, new_str)
                    content = text.encode("utf-8")
                    patched_count += 1
                    log("Troubleshoot.sys.mjs berhasil di-patch: name -> RAZBerry")

            # 2. Patch chrome/toolkit/content/global/aboutSupport.js
            elif item.filename == "chrome/toolkit/content/global/aboutSupport.js":
                text = content.decode("utf-8", errors="replace")
                old_str = '$("application-box").textContent = data.name;'
                new_str = '$("application-box").textContent = (data.name === "Zen" || !data.name) ? "RAZBerry" : data.name;'
                if old_str in text:
                    text = text.replace(old_str, new_str)
                    content = text.encode("utf-8")
                    patched_count += 1
                    log("aboutSupport.js berhasil di-patch: application-box -> RAZBerry")

            # 3. Patch modules/AppConstants.sys.mjs
            elif item.filename == "modules/AppConstants.sys.mjs":
                text = content.decode("utf-8", errors="replace")
                text = text.replace('MOZ_APP_BASENAME: "Zen",', 'MOZ_APP_BASENAME: "RAZBerry",')
                text = text.replace('MOZ_APP_DISPLAYNAME_DO_NOT_USE: "Zen",', 'MOZ_APP_DISPLAYNAME_DO_NOT_USE: "RAZBerry",')
                text = text.replace('MOZ_UPDATER: true,', 'MOZ_UPDATER: false,')
                content = text.encode("utf-8")
                patched_count += 1
                log("AppConstants.sys.mjs berhasil di-patch: MOZ_APP_BASENAME -> RAZBerry & MOZ_UPDATER -> false")

            zout.writestr(item, content)

    shutil.move(temp_omni, ROOT_OMNI)
    log(f"Root omni.ja sukses diperbarui ({patched_count} berkas termodifikasi)!")
    return True

if __name__ == "__main__":
    patch_root_omni()
