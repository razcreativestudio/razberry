# Panduan Deployment Otomatis RAZBerry Web ke Hosting IDwebhost (Paket Tera)

**Proyek**: RAZBerry Browser & Web  
**Penulis**: RAZ Creative Studio  
**Target Hosting**: IDwebhost (Paket Tera / cPanel)  
**Domain**: `https://razberry.it-raz.com`  

---

## 📌 Ringkasan Sistem Deployment

Website `razberry-www` kini dilengkapi dengan dua metode deployment yang fleksibel, aman, dan mudah dioperasikan:

1. **Otomatis (CI/CD GitHub Actions)**: Setiap kali Anda melakukan `git push` ke repository GitHub `https://github.com/razcreativestudio/razberry`, GitHub Actions akan otomatis mengompilasi situs statis Astro dan menyinkronkan berkasnya langsung ke server hosting IDwebhost melalui FTPS terenkripsi.
2. **Mandiri (Local One-Click Script)**: Anda juga dapat melakukan deploy langsung dari komputer lokal kapan saja dengan menjalankan skrip PowerShell `RAZDeployToIDwebhost.ps1`.

---

## 🚀 Metode 1: Otomatisasi via GitHub Actions (Sangat Direkomendasikan)

### Langkah 1: Siapkan Kredensial FTP di cPanel IDwebhost
1. Masuk ke cPanel IDwebhost akun hosting Anda (biasanya melalui Member Area IDwebhost atau via port `:2083`).
2. Masuk ke menu **FTP Accounts** (Akun FTP).
3. Anda bisa menggunakan akun FTP utama cPanel atau membuat akun FTP baru khusus:
   - **Log in**: `razberry` (nama lengkap akun menjadi `razberry@it-raz.com` atau username cPanel Anda)
   - **Password**: Buat password yang kuat dan catat.
   - **Directory**: Arahkan ke folder web root subdomain Anda (misalnya: `public_html/` atau `public_html/razberry/` sesuai penataan subdomain di menu *Domains* cPanel).

### Langkah 2: Daftarkan Secrets di GitHub Repository
1. Buka repositori Anda di browser:  
   👉 [https://github.com/razcreativestudio/razberry](https://github.com/razcreativestudio/razberry)
2. Klik tab **Settings** di bagian atas repository.
3. Pada bilah menu samping kiri, klik **Secrets and variables** > pilih **Actions**.
4. Klik tombol hijau **New repository secret** dan tambahkan data berikut satu per satu:

| Nama Secret | Nilai / Keterangan | Contoh |
|---|---|---|
| `FTP_SERVER` | Alamat Host FTP IDwebhost (bisa domain atau Shared IP Server di cPanel) | `ftp.it-raz.com` atau IP cPanel Anda |
| `FTP_USERNAME` | Username FTP cPanel Anda | `razberry@it-raz.com` atau username cPanel |
| `FTP_PASSWORD` | Password FTP cPanel Anda | *(password akun FTP Anda)* |
| `FTP_REMOTE_DIR` | Folder tujuan di server hosting | `public_html/` atau `public_html/razberry/` |
| `FTP_PORT` *(Opsional)* | Port FTP standar | `21` |
| `FTP_PROTOCOL` *(Opsional)* | Protokol transfer aman | `ftps` (atau `ftp`) |

### Langkah 3: Eksekusi Otomatis & Monitoring
- **Otomatis**: Setiap kali Anda melakukan perubahan kode di folder `razberry-www` lalu menjalankan `git push`, pipeline akan otomatis aktif.
- **Manual (Satu Klik)**:
  1. Buka tab **Actions** di GitHub.
  2. Pilih alur kerja **Deploy RAZBerry Web to IDwebhost**.
  3. Klik tombol **Run workflow** > pilih branch `main` > klik **Run workflow**.
- Anda dapat memantau log proses build dan upload secara langsung di layar GitHub.

---

## 💻 Metode 2: Deploy Langsung dari Komputer Lokal

Jika Anda ingin mengunggah website secara langsung dari laptop/komputer tanpa menunggu GitHub:

1. Buat salinan file konfigurasi lokal:
   - Salin berkas `deploy_config.example.json` di root proyek menjadi `deploy_config.json`.
   - Buka `deploy_config.json` dan isi data FTP hosting Anda:
     ```json
     {
       "FTP_SERVER": "ftp.it-raz.com",
       "FTP_USERNAME": "razberry@it-raz.com",
       "FTP_PASSWORD": "PasswordFTPAndaDiSini",
       "FTP_PORT": 21,
       "FTP_REMOTE_DIR": "public_html/",
       "USE_TLS": true
     }
     ```
   *(Catatan: File `deploy_config.json` sudah otomatis dilindungi oleh `.gitignore` sehingga tidak akan pernah bocor ke GitHub).*

2. Jalankan skrip deployment di PowerShell:
   ```powershell
   .\RAZDeployToIDwebhost.ps1
   ```
3. Skrip akan otomatis:
   - Menjalankan `pnpm build` di `razberry-www`.
   - Mengunggah semua halaman HTML, CSS, JavaScript, dan aset gambar secara rekursif ke hosting IDwebhost Anda dengan laporan progres per berkas.

---

## 🔒 Keamanan & Praktik Terbaik (*Best Practices*)
- **FTPS Encryption**: Alur kerja menggunakan enkripsi TLS/SSL port 21 untuk memastikan kredensial dan data yang dikirim tidak terbaca oleh pihak ketiga di jaringan.
- **Incremental Sync**: Tindakan FTP ini mencatat checksum sehingga pada upload berikutnya, hanya berkas yang berubah saja yang akan dikirim (menghemat kuota bandwidth dan waktu deploy).
- **Zero Credentials in Code**: Semua password dilindungi melalui GitHub Encrypted Secrets dan file konfigurasi lokal yang masuk daftar abaikan Git.
