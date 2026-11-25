# ==============================================================================
# RAZFixWelcomeAndLaunch.py
# Memperbaiki seluruh tahap Welcome Screen & Migration Wizard di browser/omni.ja:
# 1. Menghapus opacity: 0 yang menyebabkan blank screen pada #zen-welcome-start & #zen-welcome-pages.
# 2. Menambal seluruh key FTL yang hilang di zen-welcome.ftl (Next, Back, Skip, Import, Essentials, dll).
# 3. Memperbaiki getImportableBrowsers() agar nama Chrome/Edge/Brave tampil rapi (bukan raw l10n key).
# 4. Otomatis membuka https://razberry.it-raz.com/welcome/ setelah Welcome Screen selesai.
# Author: RAZ Creative Studio
# Timestamp: 2026-11-25
# ==============================================================================

import os
import re
import shutil
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OMNI_PATH = os.path.join(BASE_DIR, "dist", "RAZBerry", "browser", "omni.ja")
BACKUP_PATH = os.path.join(BASE_DIR, "backup", "omni.ja.welcome_fix.bak")

MISSING_FTL_DEFS = {
    "zen-generic-next": "Next",
    "zen-welcome-back": "Back",
    "zen-welcome-skip": "Skip",
    "zen-welcome-import-title": "Import Data dari Browser Lain",
    "zen-welcome-import-description": "Pilih browser sebelumnya (Chrome, Edge, Brave, dll) untuk memindahkan bookmark, riwayat, dan kata sandi ke RAZBerry Browser—atau pilih mulai dari awal lalu klik Next.",
    "zen-welcome-import-no": "Mulai dari awal (Jangan import apa pun)",
    "zen-welcome-block-ads-title": "Perlindungan Iklan & Pelacak",
    "zen-welcome-block-ads-description": "Aktifkan pemblokir iklan & pelacak bawaan agar penjelajahan di RAZBerry lebih cepat, ringan, dan bebas gangguan.",
    "zen-welcome-block-ads-yes": "Ya, blokir iklan & pelacak",
    "zen-welcome-block-ads-no": "Tidak, biarkan standar",
    "zen-welcome-essentials-title": "Aplikasi Favorit (Essentials)",
    "zen-welcome-essentials-description": "Pilih aplikasi web favorit Anda untuk disematkan di bagian atas sidebar RAZBerry agar mudah diakses kapan saja.",
    "zen-welcome-default-browser-title": "Jadikan RAZBerry Browser Utama",
    "zen-welcome-default-browser-description": "Jadikan RAZBerry sebagai browser default agar setiap tautan terbuka otomatis dengan cepat dan aman.",
}


def log(msg):
    print(f"[RAZ-WELCOME-FIX] {msg}")


def ensure_ftl_keys(text):
    """Menambahkan key FTL yang hilang tanpa menimpa key yang sudah ada."""
    additions = []
    for key, val in MISSING_FTL_DEFS.items():
        if not re.search(rf"^\s*{re.escape(key)}\s*=", text, flags=re.MULTILINE):
            additions.append(f"{key} = {val}")
    if additions:
        text = text.rstrip() + "\n\n# --- RAZBerry Welcome & Migration Additions ---\n" + "\n".join(additions) + "\n"
    return text


def patch_welcome():
    if not os.path.exists(OMNI_PATH):
        raise FileNotFoundError(f"Tidak ditemukan: {OMNI_PATH}")

    os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
    if not os.path.exists(BACKUP_PATH):
        shutil.copy2(OMNI_PATH, BACKUP_PATH)
        log(f"Backup dibuat: {BACKUP_PATH}")

    temp_omni = OMNI_PATH + ".wfix_tmp"
    patched_ftl = 0
    patched_core = 0

    with zipfile.ZipFile(OMNI_PATH, "r") as zin, zipfile.ZipFile(temp_omni, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)

            # 1. Patch zen-welcome.ftl untuk semua locale agar tidak pernah missing key
            if item.filename.endswith("browser/zen-welcome.ftl"):
                ftl = content.decode("utf-8", errors="replace").replace("\r\n", "\n")
                new_ftl = ensure_ftl_keys(ftl)
                if new_ftl != ftl:
                    content = new_ftl.encode("utf-8")
                    patched_ftl += 1

            # 2. Patch zen-welcome.css: pastikan semua container & teks welcome selalu visible
            elif item.filename == "chrome/browser/content/browser/zen-styles/zen-welcome.css":
                css = content.decode("utf-8", errors="replace").replace("\r\n", "\n")
                for sel in [
                    r"#zen-welcome-brand-logos",
                    r"#zen-welcome-start-button",
                    r"\.zen-welcome-char",
                    r"#zen-welcome-pages",
                    r"\.zen-welcome-page",
                    r"& > \*",
                ]:
                    css = re.sub(
                        rf"({sel}\s*\{{[^}}]*?)opacity:\s*0;",
                        r"\1opacity: 1;",
                        css,
                        flags=re.DOTALL,
                    )
                content = css.encode("utf-8")
                patched_core += 1
                log("zen-welcome.css diperbarui: semua panel & teks welcome visible (opacity: 1)")

            # 3. Patch ZenWelcome.mjs
            elif item.filename == "chrome/browser/content/browser/zen-components/ZenWelcome.mjs":
                mjs = content.decode("utf-8", errors="replace").replace("\r\n", "\n")

                # A. Hapus referensi zen-migration.ftl yang tidak ada agar bundle Fluent tidak gagal
                mjs = mjs.replace('    window.MozXULElement.insertFTLIfNeeded("browser/zen-migration.ftl");\n', '')
                mjs = mjs.replace('      "browser/zen-migration.ftl",\n', '')

                # B. Tambahkan fallback nama browser yang rapi di getImportableBrowsers()
                old_name_block = """          const nameId = migrator.constructor.displayNameL10nID;
          let displayName = nameId;
          try {
            displayName = (await l10n.formatValue(nameId)) || nameId;
          } catch {}"""
                new_name_block = """          const nameId = migrator.constructor.displayNameL10nID;
          const kBrowserFallbackNames = {
            chrome: "Google Chrome",
            "chromium-edge": "Microsoft Edge",
            brave: "Brave Browser",
            firefox: "Mozilla Firefox",
            opera: "Opera",
            vivaldi: "Vivaldi",
            safari: "Safari",
            ie: "Internet Explorer",
          };
          let displayName = kBrowserFallbackNames[key] || nameId;
          try {
            const localized = await l10n.formatValue(nameId);
            if (localized && !localized.startsWith("migration-wizard-")) {
              displayName = localized;
            }
          } catch {}"""
                if old_name_block in mjs:
                    mjs = mjs.replace(old_name_block, new_name_block, 1)
                    log("getImportableBrowsers() diperbarui dengan fallback nama browser yang jelas")

                # C. Bungkus translateFragment di #renderText & updateButtons dengan try/catch agar tidak pernah blank
                old_render_text = """      await document.l10n.translateFragment(text);
      if (token !== this.#renderToken) {
        return;
      }
      this.textContainer.appendChild(text);"""
                new_render_text = """      try {
        await document.l10n.translateFragment(text);
      } catch (e) {}
      if (token !== this.#renderToken) {
        return;
      }
      if (!title.textContent) {
        title.textContent = page.id === "import" ? "Import Data dari Browser Lain" : "RAZBerry Setup";
      }
      this.textContainer.appendChild(text);"""
                if old_render_text in mjs:
                    mjs = mjs.replace(old_render_text, new_render_text, 1)
                    log("#renderText() diperbarui dengan fallback aman")

                old_update_btns = """      await document.l10n.translateFragment(fragment);
      if (token === this.#buttonsToken) {
        this.buttonsContainer.replaceChildren(fragment);
      }"""
                new_update_btns = """      try {
        await document.l10n.translateFragment(fragment);
      } catch (e) {}
      for (const btn of fragment.querySelectorAll("button")) {
        if (!btn.textContent.trim()) {
          const l10nId = btn.getAttribute("data-l10n-id") || "";
          btn.textContent = l10nId.includes("skip") ? "Skip" : l10nId.includes("start") ? "Dive in!" : "Next";
        }
      }
      if (token === this.#buttonsToken) {
        this.buttonsContainer.replaceChildren(fragment);
      }"""
                if old_update_btns in mjs:
                    mjs = mjs.replace(old_update_btns, new_update_btns, 1)
                    log("updateButtons() diperbarui dengan fallback label tombol Next/Skip")

                # D. Pastikan animateInitialStage tidak blank
                old_stage_pattern = re.compile(
                    r"async function animateInitialStage\(\) \{.*?\n  \}\n\n  const kSizeLockProperties",
                    re.DOTALL,
                )
                new_stage_fn = """async function animateInitialStage() {
    let title1 = "Welcome to RAZBerry Browser";
    let title2 = "By RAZ Creative Studio";
    try {
      const vals = await document.l10n.formatValues([
        { id: "zen-welcome-title-line1" },
        { id: "zen-welcome-title-line2" },
      ]);
      if (vals[0]) title1 = vals[0];
      if (vals[1]) title2 = vals[1];
    } catch (e) {}

    const titleElement = document.getElementById("zen-welcome-title");
    if (titleElement) {
      titleElement.replaceChildren();
      for (const line of [title1, title2]) {
        const lineElement = document.createElement("span");
        for (const char of line) {
          if (char === " ") {
            lineElement.append(" ");
            continue;
          }
          const charElement = document.createElement("span");
          charElement.className = "zen-welcome-char";
          charElement.textContent = char;
          charElement.style.opacity = "1";
          lineElement.appendChild(charElement);
        }
        titleElement.appendChild(lineElement);
      }
    }

    const logos = document.getElementById("zen-welcome-brand-logos");
    if (logos) logos.style.opacity = "1";

    const button = document.getElementById("zen-welcome-start-button");
    if (button) {
      button.style.opacity = "1";
      button.addEventListener(
        "click",
        async () => {
          try {
            await animate(
              "#zen-welcome-brand-logos, #zen-welcome-title .zen-welcome-char, #zen-welcome-start-button",
              { opacity: [1, 0], y: [0, -14] },
              { duration: 0.25, ease: "easeIn" }
            );
          } catch (e) {}
          new nsZenWelcomePages(getWelcomePages());
        },
        { once: true }
      );
    }

    try {
      const chars = titleElement ? titleElement.querySelectorAll(".zen-welcome-char") : [];
      if (logos) {
        animate("#zen-welcome-brand-logos", { opacity: [0, 1], y: [20, 0] }, { duration: 0.5 });
      }
      if (chars.length) {
        await animate(chars, { opacity: [0, 1], y: [24, 0] }, { duration: 0.4, delay: getMotion().stagger(0.02) });
      }
      if (button) {
        await animate(button, { opacity: [0, 1], y: [14, 0] }, { duration: 0.35 });
      }
    } catch (e) {
      if (logos) logos.style.opacity = "1";
      if (button) button.style.opacity = "1";
    }
  }

  const kSizeLockProperties"""
                if old_stage_pattern.search(mjs):
                    mjs = old_stage_pattern.sub(new_stage_fn, mjs, count=1)

                # E. Pastikan finish() langsung buka https://razberry.it-raz.com/welcome/
                target_finish_end = """      _adBlocker = undefined;
      _startedInstalls.clear();
    }"""
                replacement_finish_end = """      _adBlocker = undefined;
      _startedInstalls.clear();
      try {
        const welcomeUrl = "https://razberry.it-raz.com/welcome/";
        const welcomeTab = window.gBrowser.addTrustedTab(welcomeUrl, {
          inBackground: false,
        });
        window.gBrowser.selectedTab = welcomeTab;
      } catch (e) {}
    }"""
                if "https://razberry.it-raz.com/welcome/" not in mjs and target_finish_end in mjs:
                    mjs = mjs.replace(target_finish_end, replacement_finish_end, 1)

                content = mjs.encode("utf-8")
                patched_core += 1

            zout.writestr(item, content)

    shutil.move(temp_omni, OMNI_PATH)
    log(f"Selesai! {patched_core} berkas inti & {patched_ftl} file FTL locale berhasil diperbarui.")


if __name__ == "__main__":
    patch_welcome()
