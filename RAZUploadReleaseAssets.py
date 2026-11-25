# ==============================================================================
# RAZUploadReleaseAssets.py
# Mengunggah binary installer RAZBerry (razberry.installer.exe, RAZBerrySetup.exe,
# Uninstall RAZBerry.exe) ke GitHub Releases (razcreativestudio/razberry).
# Menggunakan kredensial Git lokal tanpa menyimpan token di dalam kode.
# Author: RAZ Creative Studio
# Timestamp: 2026-11-25
# ==============================================================================

import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = "razcreativestudio/razberry"
TAG_NAME = "v1.19.8b-raz2"
RELEASE_NAME = "RAZBerry Browser 1.19.8b-raz2 (Windows Installer)"


def get_github_token():
    p = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\nusername=razcreativestudio\n\n",
        text=True,
        capture_output=True,
    )
    for line in p.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("Token GitHub tidak ditemukan di git credential helper.")


def api_request(url, token, method="GET", data=None, content_type="application/json"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "RAZBerry-Release-Uploader",
    }
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_release(token):
    try:
        _, rel = api_request(f"https://api.github.com/repos/{REPO}/releases/tags/{TAG_NAME}", token)
        print(f"[RAZ-RELEASE] Release {TAG_NAME} sudah ada (ID: {rel['id']}).")
        return rel
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise

    payload = json.dumps({
        "tag_name": TAG_NAME,
        "target_commitish": "main",
        "name": RELEASE_NAME,
        "prerelease": False,
        "draft": False,
        "body": (
            "## RAZBerry Browser `1.19.8b-raz2`\n"
            "**Designed by RAZ Creative Studio** — [razberry.it-raz.com](https://razberry.it-raz.com/)\n\n"
            "### ✨ Fitur Rilis Ini\n"
            "- Standalone Windows Installer (`razberry.installer.exe` / `RAZBerrySetup.exe`) bergaya floating banner Chrome dengan tema Black-Pink Raspberry.\n"
            "- Start Menu Folder `RAZBerry` berisi `RAZBerry`, `RAZBerry Private Mode`, dan `Remove RAZBerry`.\n"
            "- Terintegrasi dengan **Windows Settings > Apps > Installed apps** (`Uninstall RAZBerry.exe`).\n"
            "- Welcome Screen & Migration Wizard lengkap dengan auto-open `https://razberry.it-raz.com/welcome/`.\n"
        ),
    }).encode("utf-8")
    _, rel = api_request(f"https://api.github.com/repos/{REPO}/releases", token, method="POST", data=payload)
    print(f"[RAZ-RELEASE] Release {TAG_NAME} berhasil dibuat (ID: {rel['id']}).")
    return rel


def upload_asset(rel, token, local_path, asset_name):
    if not os.path.exists(local_path):
        print(f"[RAZ-RELEASE] File tidak ditemukan, lewati: {local_path}")
        return

    # Hapus asset lama dengan nama sama jika sudah ada
    for existing in rel.get("assets", []):
        if existing["name"] == asset_name:
            api_request(
                f"https://api.github.com/repos/{REPO}/releases/assets/{existing['id']}",
                token,
                method="DELETE",
            )
            print(f"[RAZ-RELEASE] Asset lama {asset_name} dihapus.")

    upload_base = rel["upload_url"].split("{")[0]
    upload_url = f"{upload_base}?name={urllib.parse.quote(asset_name)}"

    with open(local_path, "rb") as f:
        binary_data = f.read()

    print(f"[RAZ-RELEASE] Mengunggah {asset_name} ({len(binary_data) / (1024*1024):.2f} MB)...")
    status, asset = api_request(
        upload_url,
        token,
        method="POST",
        data=binary_data,
        content_type="application/octet-stream",
    )
    print(f"[RAZ-RELEASE] Sukses ({status}): {asset['browser_download_url']}")


def main():
    token = get_github_token()
    rel = ensure_release(token)

    files = [
        (os.path.join(BASE_DIR, "dist", "razberry.installer.exe"), "razberry.installer.exe"),
        (os.path.join(BASE_DIR, "dist", "RAZBerrySetup.exe"), "RAZBerrySetup.exe"),
        (os.path.join(BASE_DIR, "dist", "Uninstall RAZBerry.exe"), "Uninstall-RAZBerry.exe"),
    ]

    for local_path, asset_name in files:
        if os.path.exists(local_path):
            print(f"[RAZ-RELEASE] SHA-256 {asset_name}: {sha256_file(local_path)}")
        upload_asset(rel, token, local_path, asset_name)

    print(f"[RAZ-RELEASE] Selesai! Halaman rilis: {rel['html_url']}")


if __name__ == "__main__":
    main()
