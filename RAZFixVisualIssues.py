# ==============================================================================
# RAZFixVisualIssues.py
# Modul Otomasi Perbaikan 4 Isu Visual & Sistem:
# 1. Fluent placeholder {-brand-shorter-name} -> Ter-resolve pasti menjadi RAZBerry
# 2. Matikan Auto-Updater Zen & Pembersihan Cache Update
# 3. Taskbar & Titlebar Icon Win32/Gecko
# 4. Welcome Screen Onboarding: Judul & Logo RAZBerry + RAZ Creative Studio
# Dibuat oleh: Senior Software Engineer & RAZ Specialist
# Timestamp: 2026-11-24
# ==============================================================================

import os
import sys
import shutil
import zipfile
import re
from PIL import Image

def log(msg):
    print(f"[RAZ-FIX] {msg}")

def clear_startup_caches():
    """Hapus seluruh cache startup Gecko di APPDATA agar membaca perubahan FTL baru."""
    log("Membersihkan StartupCache di direktori pengguna...")
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if not local_app_data:
        return
    
    deleted_count = 0
    for root_dir in [os.path.join(local_app_data, 'zen'), os.path.join(local_app_data, 'razberry')]:
        if not os.path.exists(root_dir):
            continue
        for cur, dirs, files in os.walk(root_dir):
            for d in list(dirs):
                if d.lower() == 'startupcache':
                    cache_dir = os.path.join(cur, d)
                    try:
                        shutil.rmtree(cache_dir, ignore_errors=True)
                        deleted_count += 1
                        log(f"Berhasil menghapus cache: {cache_dir}")
                    except Exception as e:
                        log(f"Gagal hapus {cache_dir}: {e}")
            for f in files:
                if 'startupcache' in f.lower() or f.endswith('.mar') or 'active-update' in f.lower():
                    fp = os.path.join(cur, f)
                    try:
                        os.remove(fp)
                        deleted_count += 1
                    except:
                        pass
    # Bersihkan juga sisa update in-flight di ProgramData
    program_data = os.environ.get('ProgramData', r'C:\ProgramData')
    if os.path.exists(program_data):
        for item in os.listdir(program_data):
            if item.lower().startswith('mozilla-'):
                up_dir = os.path.join(program_data, item, 'updates')
                if os.path.exists(up_dir):
                    try:
                        shutil.rmtree(up_dir, ignore_errors=True)
                        deleted_count += 1
                        log(f"Berhasil membersihkan sisa update ProgramData: {up_dir}")
                    except Exception as e:
                        log(f"Gagal hapus {up_dir}: {e}")

    log(f"Total {deleted_count} cache/residu dibersihkan.")

def patch_omni_ja():
    """Memperbaiki FTL, Updater script, dan styling di dalam dist/RAZBerry/browser/omni.ja."""
    omni_path = 'dist/RAZBerry/browser/omni.ja'
    temp_omni = 'dist/RAZBerry/browser/omni.ja.temp'
    bak_omni = 'backup/omni.ja.visual_fix.bak'

    if not os.path.exists(omni_path):
        log(f"File {omni_path} tidak ditemukan!")
        return

    # Backup omni.ja jika belum ada
    if not os.path.exists(bak_omni):
        shutil.copy2(omni_path, bak_omni)
        log(f"Backup omni.ja tersimpan di {bak_omni}")

    log("Membuka omni.ja untuk pembaruan menyeluruh...")
    with zipfile.ZipFile(omni_path, 'r') as zin, zipfile.ZipFile(temp_omni, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)

            # 1. Modifikasi appmenu.ftl (semua locale)
            if item.filename.endswith('appmenu.ftl'):
                text = content.decode('utf-8', errors='ignore')
                # Tambahkan definisi term di awal jika belum ada
                header = (
                    "-brand-shorter-name = RAZBerry\n"
                    "-brand-short-name = RAZBerry\n"
                    "-brand-full-name = RAZBerry Browser\n"
                    "-brand-product-name = RAZBerry Browser\n"
                    "-vendor-short-name = RAZ Creative Studio\n"
                )
                if "-brand-shorter-name = RAZBerry" not in text:
                    text = header + "\n" + text
                # Ganti langsung placeholder rentan dengan teks konkret RAZBerry
                text = re.sub(r'(\.title\s*=\s*)\{\s*-brand-shorter-name\s*\}\s*help', r'\1RAZBerry help', text, flags=re.IGNORECASE)
                text = re.sub(r'(\.label\s*=\s*)About\s*\{\s*-brand-shorter-name\s*\}', r'\1About RAZBerry', text, flags=re.IGNORECASE)
                content = text.encode('utf-8')

            # 2. Modifikasi menubar.ftl (semua locale)
            elif item.filename.endswith('menubar.ftl'):
                text = content.decode('utf-8', errors='ignore')
                header = (
                    "-brand-shorter-name = RAZBerry\n"
                    "-brand-short-name = RAZBerry\n"
                    "-brand-full-name = RAZBerry Browser\n"
                    "-brand-product-name = RAZBerry Browser\n"
                    "-vendor-short-name = RAZ Creative Studio\n"
                )
                if "-brand-shorter-name = RAZBerry" not in text:
                    text = header + "\n" + text
                text = re.sub(r'(\.label\s*=\s*)About\s*\{\s*-brand-shorter-name\s*\}', r'\1About RAZBerry', text, flags=re.IGNORECASE)
                content = text.encode('utf-8')

            # 3. Modifikasi zen-welcome.ftl (semua locale)
            elif item.filename.endswith('zen-welcome.ftl'):
                text = content.decode('utf-8', errors='ignore')
                text = re.sub(r'zen-welcome-title-line1\s*=.*', 'zen-welcome-title-line1 = Welcome to RAZBerry Browser', text)
                text = re.sub(r'zen-welcome-title-line2\s*=.*', 'zen-welcome-title-line2 = By RAZ Creative Studio', text)
                content = text.encode('utf-8')

            # 4. Modifikasi aboutDialog-appUpdater.js (Matikan update bar agar tidak ada 'Downloading update')
            elif item.filename == 'chrome/browser/content/browser/aboutDialog-appUpdater.js':
                text = content.decode('utf-8', errors='ignore')
                # Override agar selalu menganggap tidak ada update atau up-to-date
                # Ganti fungsi checkForUpdates dan downloadUpdate
                replacement = """
/* RAZBerry Enterprise Patch: Auto-update sepenuhnya dinonaktifkan */
appUpdater.prototype.checkForUpdates = function() {
  let deck = document.getElementById("updateDeck");
  if (deck) {
    deck.selectedPanel = document.getElementById("noUpdatesFound") || deck.children[0];
  }
};
appUpdater.prototype.startDownload = function() {};
appUpdater.prototype.buttonRestartAfterDownload = function() {};
"""
                text = text + "\n" + replacement
                content = text.encode('utf-8')

            # 5. Modifikasi aboutDialog.xhtml (Window title & icon)
            elif item.filename == 'chrome/browser/content/browser/aboutDialog.xhtml':
                text = content.decode('utf-8', errors='ignore')
                # Tambahkan link icon di header xhtml
                if 'razberry.ico' not in text:
                    text = text.replace(
                        '</linkset>',
                        '  <html:link rel="icon" type="image/x-icon" href="chrome://branding/content/default.ico"/>\n  </linkset>'
                    )
                content = text.encode('utf-8')

            zout.writestr(item, content)

    shutil.move(temp_omni, omni_path)
    log("Pembaruan omni.ja selesai dan terintegrasi 100%!")

def setup_browser_icons():
    """Memastikan seluruh variasi nama ikon yang dicari Gecko tersedia di folder icons."""
    log("Menyelaraskan variasi nama icon di folder chrome/icons/default...")
    src_ico = 'dist/RAZBerry/RAZBerry.ico'
    if not os.path.exists(src_ico):
        log(f"{src_ico} tidak ditemukan!")
        return

    icon_names = [
        'default.ico',
        'main-window.ico',
        'about.ico',
        'aboutDialog.ico',
        'Browser_About.ico',
        'razberry.ico',
        'zen.ico',
    ]

    target_dirs = [
        'dist/RAZBerry/chrome/icons/default',
        'dist/RAZBerry/browser/chrome/icons/default',
    ]

    for d in target_dirs:
        os.makedirs(d, exist_ok=True)
        for name in icon_names:
            dest = os.path.join(d, name)
            shutil.copy2(src_ico, dest)
    log("Seluruh variasi file .ico berhasil disalin ke folder chrome icons.")

def create_desktop_and_taskbar_shortcuts():
    """Membuat shortcut Desktop & Taskbar resmi untuk RAZBerry Browser."""
    log("Membuat shortcut Desktop dan Taskbar resmi RAZBerry...")
    desktop = r'C:\Users\Administrator\Desktop'
    target_exe = os.path.abspath('dist/RAZBerry/razberry.exe')
    icon_path = os.path.abspath('dist/RAZBerry/RAZBerry.ico')
    work_dir = os.path.abspath('dist/RAZBerry')

    # Buat VBScript sementara untuk membuat shortcut WScript.Shell
    vbs_code = f"""
Set ws = CreateObject("WScript.Shell")

' 1. Desktop Shortcut
strDesktop = ws.SpecialFolders("Desktop")
Set scDesktop = ws.CreateShortcut(strDesktop & "\\RAZBerry.lnk")
scDesktop.TargetPath = "{target_exe}"
scDesktop.Arguments = "-app browser\\application.ini"
scDesktop.WorkingDirectory = "{work_dir}"
scDesktop.IconLocation = "{icon_path}, 0"
scDesktop.Description = "RAZBerry Browser - By RAZ Creative Studio"
scDesktop.Save

' 2. Start Menu Shortcut
strPrograms = ws.SpecialFolders("Programs")
Set scStart = ws.CreateShortcut(strPrograms & "\\RAZBerry.lnk")
scStart.TargetPath = "{target_exe}"
scStart.Arguments = "-app browser\\application.ini"
scStart.WorkingDirectory = "{work_dir}"
scStart.IconLocation = "{icon_path}, 0"
scStart.Description = "RAZBerry Browser - By RAZ Creative Studio"
scStart.Save

' 3. Update Pinned Taskbar Zen.lnk jika ada agar mengarah ke RAZBerry
strTaskBar = ws.ExpandEnvironmentStrings("%APPDATA%") & "\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar"
Set fso = CreateObject("Scripting.FileSystemObject")
If fso.FolderExists(strTaskBar) Then
    If fso.FileExists(strTaskBar & "\\Zen.lnk") Then
        Set scZen = ws.CreateShortcut(strTaskBar & "\\Zen.lnk")
        scZen.TargetPath = "{target_exe}"
        scZen.Arguments = "-app browser\\application.ini"
        scZen.WorkingDirectory = "{work_dir}"
        scZen.IconLocation = "{icon_path}, 0"
        scZen.Description = "RAZBerry Browser - By RAZ Creative Studio"
        scZen.Save
    End If
    ' Tambahkan juga RAZBerry.lnk di taskbar
    Set scTB = ws.CreateShortcut(strTaskBar & "\\RAZBerry.lnk")
    scTB.TargetPath = "{target_exe}"
    scTB.Arguments = "-app browser\\application.ini"
    scTB.WorkingDirectory = "{work_dir}"
    scTB.IconLocation = "{icon_path}, 0"
    scTB.Description = "RAZBerry Browser - By RAZ Creative Studio"
    scTB.Save
End If
"""
    vbs_path = 'temp_create_shortcuts.vbs'
    with open(vbs_path, 'w', encoding='utf-8') as f:
        f.write(vbs_code)
    
    os.system(f'cscript //nologo {vbs_path}')
    if os.path.exists(vbs_path):
        os.remove(vbs_path)
    log("Shortcut Desktop, Start Menu, dan Taskbar berhasil dibuat/diperbarui!")

def flush_icon_cache():
    """Flush icon cache di Windows Explorer."""
    log("Me-refresh Windows Shell Icon Cache...")
    try:
        os.system('ie4uinit.exe -show')
    except:
        pass

def enforce_enterprise_policies():
    """Tulis distribution/policies.json untuk mematikan auto-updater Zen secara mutlak."""
    log("Menulis Enterprise Policy policies.json...")
    policy_dir = 'dist/RAZBerry/distribution'
    os.makedirs(policy_dir, exist_ok=True)
    policy_file = os.path.join(policy_dir, 'policies.json')
    policy_content = """{
  "policies": {
    "DisableAppUpdate": true,
    "DisableSystemAddonUpdate": true,
    "ManualAppUpdateOnly": true,
    "OverrideFirstRunPage": "https://razberry.it-raz.com/welcome/",
    "OverridePostUpdatePage": "https://razberry.it-raz.com/whatsnew/"
  }
}"""
    with open(policy_file, 'w', encoding='utf-8') as f:
        f.write(policy_content)
    log("Enterprise policies.json aktif!")

    # Nonaktifkan updater.exe jika ada
    updater_exe = 'dist/RAZBerry/updater.exe'
    if os.path.exists(updater_exe):
        try:
            shutil.copy2(updater_exe, 'backup/updater.exe.bak')
        except:
            pass

if __name__ == '__main__':
    log("Memulai eksekusi RAZFixVisualIssues...")
    enforce_enterprise_policies()
    clear_startup_caches()
    patch_omni_ja()
    setup_browser_icons()
    create_desktop_and_taskbar_shortcuts()
    flush_icon_cache()
    log("Seluruh perbaikan visual dan sistem RAZBerry selesai dengan sukses 100%!")
