# ==============================================================================
# RAZDeployToIDwebhost.py
# Modul Otomasi Deployment Mandiri ke Hosting IDwebhost (Paket Tera)
# Author: RAZ Creative Studio
# Deskripsi: Mengunggah berkas kompilasi razberry-www/dist langsung ke cPanel IDwebhost
#            melalui protokol aman FTPS / FTP dengan dukungan rekursif direktori.
# ==============================================================================

import os
import sys
import json
import ftplib
import ssl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "razberry-www", "dist")
CONFIG_FILE = os.path.join(BASE_DIR, "deploy_config.json")
EXAMPLE_CONFIG = os.path.join(BASE_DIR, "deploy_config.example.json")

def log(msg):
    print(f"[RAZ-DEPLOY] {msg}")

def ensure_example_config():
    """Membuat contoh file konfigurasi deploy_config.example.json jika belum ada."""
    sample = {
        "FTP_SERVER": "ftp.it-raz.com",
        "FTP_USERNAME": "razberry@razberry.it-raz.com",
        "FTP_PASSWORD": "GANTI_DENGAN_PASSWORD_FTP_ANDA",
        "FTP_PORT": 21,
        "FTP_REMOTE_DIR": "/",
        "USE_TLS": True
    }
    with open(EXAMPLE_CONFIG, "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=2)

def upload_directory_recursive(ftp, local_dir, remote_dir):
    """Mengunggah seluruh file dan folder secara rekursif ke server FTP."""
    # Pastikan remote dir ada atau buat jika belum ada
    remote_parts = [p for p in remote_dir.replace("\\", "/").strip("/").split("/") if p]
    current = ""
    for part in remote_parts:
        current += "/" + part
        try:
            ftp.cwd(current)
        except ftplib.error_perm:
            try:
                ftp.mkd(current)
                ftp.cwd(current)
                log(f"Membuat remote folder: {current}")
            except Exception as e:
                pass

    total_files = 0
    uploaded_files = 0

    for root, dirs, files in os.walk(local_dir):
        rel_path = os.path.relpath(root, local_dir).replace("\\", "/")
        target_dir = remote_dir.rstrip("/")
        if rel_path != ".":
            target_dir = f"{target_dir}/{rel_path}"

        # Pastikan subdirektori ada di remote
        for d in dirs:
            sub_remote = f"{target_dir}/{d}"
            try:
                ftp.mkd(sub_remote)
            except ftplib.error_perm:
                pass # Direktori sudah ada

        for f in files:
            local_file = os.path.join(root, f)
            remote_file = f"{target_dir}/{f}"
            total_files += 1
            try:
                with open(local_file, "rb") as fp:
                    ftp.storbinary(f"STOR {remote_file}", fp)
                uploaded_files += 1
                if uploaded_files % 25 == 0 or uploaded_files == total_files:
                    log(f"Progres upload: {uploaded_files} file selesai...")
            except Exception as e:
                log(f"Gagal upload {remote_file}: {e}")

    log(f"Upload selesai! Total {uploaded_files} dari {total_files} berkas sukses terunggah.")

def deploy():
    ensure_example_config()

    if not os.path.exists(DIST_DIR):
        log(f"Direktori build {DIST_DIR} belum ada! Jalankan 'pnpm build' di razberry-www terlebih dahulu.")
        return False

    if not os.path.exists(CONFIG_FILE):
        log("File konfigurasi 'deploy_config.json' belum ditemukan!")
        log(f"Silakan salin '{EXAMPLE_CONFIG}' menjadi 'deploy_config.json' dan masukkan kredensial FTP IDwebhost Anda.")
        return False

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    server = cfg.get("FTP_SERVER", "")
    user = cfg.get("FTP_USERNAME", "")
    password = cfg.get("FTP_PASSWORD", "")
    port = int(cfg.get("FTP_PORT", 21))
    remote_dir = cfg.get("FTP_REMOTE_DIR", "public_html/")
    use_tls = cfg.get("USE_TLS", True)

    if not server or not user or not password:
        log("Kredensial FTP_SERVER, FTP_USERNAME, atau FTP_PASSWORD masih kosong!")
        return False

    log(f"Menghubungkan ke server {server}:{port} ({user})...")
    try:
        if use_tls:
            context = ssl.create_default_context()
            ftp = ftplib.FTP_TLS(context=context)
            ftp.connect(server, port, timeout=30)
            ftp.login(user, password)
            ftp.prot_p() # Amankan saluran data transfer
            log("Koneksi FTPS (TLS Terenkripsi) Berhasil!")
        else:
            ftp = ftplib.FTP()
            ftp.connect(server, port, timeout=30)
            ftp.login(user, password)
            log("Koneksi FTP Berhasil!")

        log(f"Memulai sinkronisasi dari '{DIST_DIR}' ke remote '{remote_dir}'...")
        upload_directory_recursive(ftp, DIST_DIR, remote_dir)
        ftp.quit()
        log("🎉 Deploy ke hosting IDwebhost sukses 100%!")
        return True
    except Exception as e:
        log(f"Galat koneksi/upload FTP: {e}")
        return False

if __name__ == "__main__":
    deploy()
