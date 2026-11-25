# ==============================================================================
# RAZFixWelcomeAndLaunch.py
# Memperbaiki Welcome Screen blank pada ZenWelcome.mjs & zen-welcome.css:
# 1. Menghapus opacity: 0 yang menyebabkan blank screen jika motion gagal.
# 2. Menambahkan fallback aman l10n & pemasangan listener tombol sebelum animasi.
# 3. Otomatis membuka https://razberry.it-raz.com/welcome/ setelah Welcome Screen selesai.
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


def log(msg):
    print(f"[RAZ-WELCOME-FIX] {msg}")


def patch_welcome():
    if not os.path.exists(OMNI_PATH):
        raise FileNotFoundError(f"Tidak ditemukan: {OMNI_PATH}")

    os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
    if not os.path.exists(BACKUP_PATH):
        shutil.copy2(OMNI_PATH, BACKUP_PATH)
        log(f"Backup dibuat: {BACKUP_PATH}")

    temp_omni = OMNI_PATH + ".wfix_tmp"
    patched = 0

    with zipfile.ZipFile(OMNI_PATH, "r") as zin, zipfile.ZipFile(temp_omni, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)

            # 1. Patch zen-welcome.css: pastikan brand-logos, start-button, & chars selalu visible (opacity: 1)
            if item.filename == "chrome/browser/content/browser/zen-styles/zen-welcome.css":
                css = content.decode("utf-8", errors="replace")
                # Ganti opacity: 0 pada #zen-welcome-brand-logos, #zen-welcome-start-button, dan .zen-welcome-char
                css = re.sub(
                    r"(#zen-welcome-brand-logos\s*\{[^}]*?)opacity:\s*0;",
                    r"\1opacity: 1;",
                    css,
                    flags=re.DOTALL,
                )
                css = re.sub(
                    r"(#zen-welcome-start-button\s*\{[^}]*?)opacity:\s*0;",
                    r"\1opacity: 1;",
                    css,
                    flags=re.DOTALL,
                )
                css = re.sub(
                    r"(\.zen-welcome-char\s*\{[^}]*?)opacity:\s*0;",
                    r"\1opacity: 1;",
                    css,
                    flags=re.DOTALL,
                )
                content = css.encode("utf-8")
                patched += 1
                log("zen-welcome.css diperbarui: opacity default -> 1 (anti blank screen)")

            # 2. Patch ZenWelcome.mjs: anti-blank animateInitialStage + buka https://razberry.it-raz.com/welcome/ saat finish
            elif item.filename == "chrome/browser/content/browser/zen-components/ZenWelcome.mjs":
                mjs = content.decode("utf-8", errors="replace").replace("\r\n", "\n")

                # A. Ganti animateInitialStage agar anti-blank dan tombol selalu bisa diklik
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
                    log("animateInitialStage() di ZenWelcome.mjs diperbarui (anti-blank + fallback aman)")

                # B. Di finish(), buka otomatis https://razberry.it-raz.com/welcome/ setelah browser tampil
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
                    log("finish() di ZenWelcome.mjs diperbarui: auto-open https://razberry.it-raz.com/welcome/")

                content = mjs.encode("utf-8")
                patched += 1

            zout.writestr(item, content)

    shutil.move(temp_omni, OMNI_PATH)
    log(f"Selesai! {patched} berkas berhasil diperbarui di omni.ja.")


if __name__ == "__main__":
    patch_welcome()
