// ==============================================================================
// RAZSetupWizard.cs
// Installer Wizard Standalone RAZBerry Browser (Gaya Floating Banner Chrome)
// Tema: Black-Pink Raspberry (Selaras dengan Welcome Screen RAZBerry)
// Author: RAZ Creative Studio
// Timestamp: 2026-11-25
// ==============================================================================

using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Win32;

namespace RAZBerrySetup
{
    internal static class Program
    {
        [DllImport("user32.dll")]
        private static extern bool SetProcessDPIAware();

        [STAThread]
        private static void Main()
        {
            if (Environment.OSVersion.Version.Major >= 6)
            {
                SetProcessDPIAware();
            }
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new FloatingInstallerForm());
        }
    }

    public sealed class FloatingInstallerForm : Form
    {
        // --- Palet Warna Black-Pink Raspberry ---
        private static readonly Color BgDark = Color.FromArgb(17, 10, 14);         // #110A0E
        private static readonly Color SurfaceDark = Color.FromArgb(26, 16, 22);    // #1A1016
        private static readonly Color PinkPrimary = Color.FromArgb(216, 27, 96);   // #D81B60
        private static readonly Color PinkVibrant = Color.FromArgb(255, 64, 129);  // #FF4081
        private static readonly Color BorderPink = Color.FromArgb(95, 34, 62);
        private static readonly Color TextPrimary = Color.FromArgb(253, 240, 245); // #FDF0F5
        private static readonly Color TextMuted = Color.FromArgb(196, 168, 182);

        // --- Win32 Rounded Corner & Dragging ---
        [DllImport("Gdi32.dll", EntryPoint = "CreateRoundRectRgn")]
        private static extern IntPtr CreateRoundRectRgn(int nLeftRect, int nTopRect, int nRightRect, int nBottomRect, int nWidthEllipse, int nHeightEllipse);

        [DllImport("user32.dll")]
        private static extern bool ReleaseCapture();

        [DllImport("user32.dll")]
        private static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);

        private const int WM_NCLBUTTONDOWN = 0xA1;
        private const int HT_CAPTION = 0x2;

        // --- Komponen UI ---
        private PictureBox _pbRazBerry;
        private PictureBox _pbRazStudio;
        private Label _lblTitle;
        private Label _lblSubtitle;
        private Label _lblStatus;
        private CheckBox _chkShortcut;
        private PinkProgressBar _progressBar;
        private Label _lblPercent;
        private Button _btnInstall;
        private Button _btnCancel;
        private Button _btnFinishOpen;
        private Button _btnClose;
        private Label _btnTopClose;

        private readonly string _installDir;
        private readonly BackgroundWorker _worker;
        private bool _isInstalling = false;

        public FloatingInstallerForm()
        {
            _installDir = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "RAZBerry"
            );

            InitializeForm();
            InitializeControls();

            _worker = new BackgroundWorker
            {
                WorkerReportsProgress = true,
                WorkerSupportsCancellation = true
            };
            _worker.DoWork += Worker_DoWork;
            _worker.ProgressChanged += Worker_ProgressChanged;
            _worker.RunWorkerCompleted += Worker_RunWorkerCompleted;
        }

        private void InitializeForm()
        {
            Text = "RAZBerry Browser Setup";
            Size = new Size(540, 390);
            StartPosition = FormStartPosition.CenterScreen;
            FormBorderStyle = FormBorderStyle.None;
            BackColor = BgDark;
            DoubleBuffered = true;
            Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Width, Height, 22, 22));

            try
            {
                Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath);
            }
            catch { }

            MouseDown += Form_MouseDown;
            Paint += Form_Paint;
        }

        private void Form_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                ReleaseCapture();
                SendMessage(Handle, WM_NCLBUTTONDOWN, HT_CAPTION, 0);
            }
        }

        private void Form_Paint(object sender, PaintEventArgs e)
        {
            e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
            // Bingkai luar glowing tipis raspberry pink
            using (var pen = new Pen(BorderPink, 2f))
            {
                e.Graphics.DrawPath(pen, GetRoundedPath(new Rectangle(1, 1, Width - 3, Height - 3), 20));
            }
        }

        private static GraphicsPath GetRoundedPath(Rectangle rect, int radius)
        {
            var path = new GraphicsPath();
            int d = radius * 2;
            path.AddArc(rect.X, rect.Y, d, d, 180, 90);
            path.AddArc(rect.Right - d, rect.Y, d, d, 270, 90);
            path.AddArc(rect.Right - d, rect.Bottom - d, d, d, 0, 90);
            path.AddArc(rect.X, rect.Bottom - d, d, d, 90, 90);
            path.CloseFigure();
            return path;
        }

        private Image LoadEmbeddedImage(string resourceName)
        {
            var asm = Assembly.GetExecutingAssembly();
            using (var stream = asm.GetManifestResourceStream(resourceName))
            {
                if (stream != null)
                {
                    return Image.FromStream(stream);
                }
            }
            return null;
        }

        private void InitializeControls()
        {
            // Tombol X pojok kanan atas
            _btnTopClose = new Label
            {
                Text = "✕",
                Font = new Font("Segoe UI", 11F, FontStyle.Bold),
                ForeColor = TextMuted,
                BackColor = Color.Transparent,
                Size = new Size(32, 32),
                Location = new Point(Width - 42, 10),
                TextAlign = ContentAlignment.MiddleCenter,
                Cursor = Cursors.Hand
            };
            _btnTopClose.Click += (s, e) =>
            {
                if (!_isInstalling) Close();
            };
            _btnTopClose.MouseEnter += (s, e) => { if (!_isInstalling) _btnTopClose.ForeColor = PinkVibrant; };
            _btnTopClose.MouseLeave += (s, e) => { _btnTopClose.ForeColor = TextMuted; };
            Controls.Add(_btnTopClose);

            // Logo RAZBerry & Logo RAZ Creative Studio (sejajar tanpa background)
            _pbRazBerry = new PictureBox
            {
                Size = new Size(76, 76),
                Location = new Point(164, 34),
                SizeMode = PictureBoxSizeMode.Zoom,
                BackColor = Color.Transparent,
                Image = LoadEmbeddedImage("LogoRazBerry.png")
            };
            _pbRazBerry.MouseDown += Form_MouseDown;
            Controls.Add(_pbRazBerry);

            var divider = new Panel
            {
                Size = new Size(1, 46),
                Location = new Point(254, 49),
                BackColor = BorderPink
            };
            Controls.Add(divider);

            _pbRazStudio = new PictureBox
            {
                Size = new Size(118, 62),
                Location = new Point(268, 41),
                SizeMode = PictureBoxSizeMode.Zoom,
                BackColor = Color.Transparent,
                Image = LoadEmbeddedImage("LogoRazStudio.png")
            };
            _pbRazStudio.MouseDown += Form_MouseDown;
            Controls.Add(_pbRazStudio);

            // Headline Welcome
            _lblTitle = new Label
            {
                Text = "Welcome to RAZBerry Browser",
                Font = new Font("Segoe UI", 17.5F, FontStyle.Bold),
                ForeColor = TextPrimary,
                BackColor = Color.Transparent,
                Size = new Size(Width - 40, 34),
                Location = new Point(20, 128),
                TextAlign = ContentAlignment.MiddleCenter
            };
            _lblTitle.MouseDown += Form_MouseDown;
            Controls.Add(_lblTitle);

            _lblSubtitle = new Label
            {
                Text = "By RAZ Creative Studio",
                Font = new Font("Segoe UI", 10.5F, FontStyle.Bold),
                ForeColor = PinkVibrant,
                BackColor = Color.Transparent,
                Size = new Size(Width - 40, 24),
                Location = new Point(20, 162),
                TextAlign = ContentAlignment.MiddleCenter
            };
            _lblSubtitle.MouseDown += Form_MouseDown;
            Controls.Add(_lblSubtitle);

            // Status / Deskripsi
            _lblStatus = new Label
            {
                Text = "Siap memasang RAZBerry Browser secara cepat, bersih, dan aman.\nLokasi: " + _installDir,
                Font = new Font("Segoe UI", 9F, FontStyle.Regular),
                ForeColor = TextMuted,
                BackColor = Color.Transparent,
                Size = new Size(Width - 64, 42),
                Location = new Point(32, 198),
                TextAlign = ContentAlignment.MiddleCenter
            };
            _lblStatus.MouseDown += Form_MouseDown;
            Controls.Add(_lblStatus);

            // Checkbox Shortcut
            _chkShortcut = new CheckBox
            {
                Text = "Buat shortcut di Desktop & Start Menu",
                Checked = true,
                Font = new Font("Segoe UI", 9F, FontStyle.Regular),
                ForeColor = TextPrimary,
                BackColor = Color.Transparent,
                AutoSize = true,
                Location = new Point(156, 252),
                Cursor = Cursors.Hand
            };
            Controls.Add(_chkShortcut);

            // Progress Bar & Persentase (tersembunyi pada tahap awal)
            _progressBar = new PinkProgressBar
            {
                Size = new Size(420, 14),
                Location = new Point(60, 256),
                Visible = false,
                Value = 0
            };
            Controls.Add(_progressBar);

            _lblPercent = new Label
            {
                Text = "0%",
                Font = new Font("Segoe UI", 9F, FontStyle.Bold),
                ForeColor = PinkVibrant,
                BackColor = Color.Transparent,
                Size = new Size(420, 22),
                Location = new Point(60, 276),
                TextAlign = ContentAlignment.MiddleCenter,
                Visible = false
            };
            Controls.Add(_lblPercent);

            // Tombol Tahap 1: Install & Cancel
            _btnInstall = CreateStyledButton("Install", true, new Point(132, 314), new Size(134, 42));
            _btnInstall.Click += BtnInstall_Click;
            Controls.Add(_btnInstall);

            _btnCancel = CreateStyledButton("Cancel", false, new Point(276, 314), new Size(134, 42));
            _btnCancel.Click += (s, e) => Close();
            Controls.Add(_btnCancel);

            // Tombol Tahap 3: Finish & Open + Close
            _btnFinishOpen = CreateStyledButton("Finish && Open", true, new Point(122, 314), new Size(164, 42));
            _btnFinishOpen.Visible = false;
            _btnFinishOpen.Click += BtnFinishOpen_Click;
            Controls.Add(_btnFinishOpen);

            _btnClose = CreateStyledButton("Close", false, new Point(296, 314), new Size(122, 42));
            _btnClose.Visible = false;
            _btnClose.Click += (s, e) => Close();
            Controls.Add(_btnClose);
        }

        private Button CreateStyledButton(string text, bool isPrimary, Point loc, Size size)
        {
            var btn = new Button
            {
                Text = text,
                Location = loc,
                Size = size,
                FlatStyle = FlatStyle.Flat,
                Font = new Font("Segoe UI", 9.5F, FontStyle.Bold),
                Cursor = Cursors.Hand,
                BackColor = isPrimary ? PinkPrimary : SurfaceDark,
                ForeColor = TextPrimary
            };
            btn.FlatAppearance.BorderSize = isPrimary ? 0 : 1;
            btn.FlatAppearance.BorderColor = isPrimary ? PinkPrimary : BorderPink;
            btn.FlatAppearance.MouseOverBackColor = isPrimary ? PinkVibrant : Color.FromArgb(46, 24, 36);
            btn.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, size.Width, size.Height, 10, 10));
            return btn;
        }

        private void BtnInstall_Click(object sender, EventArgs e)
        {
            _isInstalling = true;
            _btnInstall.Visible = false;
            _btnCancel.Visible = false;
            _chkShortcut.Visible = false;
            _btnTopClose.Enabled = false;

            _progressBar.Visible = true;
            _lblPercent.Visible = true;
            _lblStatus.Text = "Mempersiapkan pemasangan RAZBerry Browser...";

            _worker.RunWorkerAsync(_chkShortcut.Checked);
        }

        private void Worker_DoWork(object sender, DoWorkEventArgs e)
        {
            bool createShortcuts = (bool)e.Argument;
            var asm = Assembly.GetExecutingAssembly();

            // 1. Tutup instance razberry.exe yang sedang berjalan agar file tidak terkunci
            _worker.ReportProgress(3, "Memeriksa proses aktif...");
            foreach (var proc in Process.GetProcessesByName("razberry"))
            {
                try { proc.Kill(); proc.WaitForExit(3000); } catch { }
            }

            // 2. Siapkan folder target
            Directory.CreateDirectory(_installDir);

            // 3. Ekstrak RAZBerryPayload.zip dengan pelaporan progress real-time
            using (var stream = asm.GetManifestResourceStream("RAZBerryPayload.zip"))
            {
                if (stream == null)
                {
                    throw new InvalidOperationException("Payload instalasi RAZBerryPayload.zip tidak ditemukan.");
                }

                using (var archive = new ZipArchive(stream, ZipArchiveMode.Read))
                {
                    int total = archive.Entries.Count;
                    int current = 0;

                    foreach (var entry in archive.Entries)
                    {
                        current++;
                        string destPath = Path.GetFullPath(Path.Combine(_installDir, entry.FullName));

                        if (!destPath.StartsWith(_installDir, StringComparison.OrdinalIgnoreCase))
                            continue;

                        if (string.IsNullOrEmpty(entry.Name))
                        {
                            Directory.CreateDirectory(destPath);
                        }
                        else
                        {
                            Directory.CreateDirectory(Path.GetDirectoryName(destPath));
                            entry.ExtractToFile(destPath, overwrite: true);
                        }

                        if (current % 15 == 0 || current == total)
                        {
                            int pct = 5 + (int)(current * 85.0 / Math.Max(1, total));
                            _worker.ReportProgress(pct, string.Format("Memasang berkas RAZBerry ({0}/{1})...", current, total));
                        }
                    }
                }
            }

            // 4. Ekstrak Uninstall RAZBerry.exe ke direktori instalasi
            _worker.ReportProgress(91, "Memasang Uninstall RAZBerry.exe...");
            string uninstallerPath = Path.Combine(_installDir, "Uninstall RAZBerry.exe");
            using (var uStream = asm.GetManifestResourceStream("UninstallRAZBerry.exe"))
            {
                if (uStream != null)
                {
                    using (var fs = new FileStream(uninstallerPath, FileMode.Create, FileAccess.Write))
                    {
                        uStream.CopyTo(fs);
                    }
                }
            }

            // 5. Buat Shortcut Desktop & Folder Start Menu RAZBerry
            if (createShortcuts)
            {
                _worker.ReportProgress(94, "Membuat shortcut Desktop & folder Start Menu RAZBerry...");
                string exePath = Path.Combine(_installDir, "razberry.exe");
                string icoPath = Path.Combine(_installDir, "RAZBerry.ico");

                // Desktop shortcut
                CreateShortcut(
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory), "RAZBerry.lnk"),
                    exePath, "", _installDir, icoPath,
                    "RAZBerry Browser - By RAZ Creative Studio"
                );

                // Start Menu: hapus shortcut lama di root Programs agar masuk rapi ke folder RAZBerry
                string programsDir = Environment.GetFolderPath(Environment.SpecialFolder.Programs);
                string oldRootLnk = Path.Combine(programsDir, "RAZBerry.lnk");
                if (File.Exists(oldRootLnk))
                {
                    try { File.Delete(oldRootLnk); } catch { }
                }

                string startMenuFolder = Path.Combine(programsDir, "RAZBerry");
                Directory.CreateDirectory(startMenuFolder);

                CreateShortcut(
                    Path.Combine(startMenuFolder, "RAZBerry.lnk"),
                    exePath, "", _installDir, icoPath,
                    "RAZBerry Browser - By RAZ Creative Studio"
                );

                if (File.Exists(uninstallerPath))
                {
                    CreateShortcut(
                        Path.Combine(startMenuFolder, "Uninstall RAZBerry.lnk"),
                        uninstallerPath, "", _installDir, icoPath,
                        "Hapus RAZBerry Browser dari perangkat ini"
                    );
                }
            }

            // 6. Daftarkan aplikasi & Uninstaller ke Windows Registry (Add/Remove Programs)
            _worker.ReportProgress(97, "Mendaftarkan aplikasi di sistem Windows...");
            RegisterApplication(uninstallerPath);

            Thread.Sleep(250);
            _worker.ReportProgress(100, "RAZBerry Browser berhasil dipasang dan siap digunakan!");
        }

        private void CreateShortcut(string shortcutPath, string targetExe, string arguments, string workDir, string iconPath, string description)
        {
            try
            {
                Type shellType = Type.GetTypeFromProgID("WScript.Shell");
                dynamic shell = Activator.CreateInstance(shellType);
                dynamic sc = shell.CreateShortcut(shortcutPath);
                sc.TargetPath = targetExe;
                if (!string.IsNullOrEmpty(arguments))
                {
                    sc.Arguments = arguments;
                }
                sc.WorkingDirectory = workDir;
                sc.IconLocation = iconPath + ", 0";
                sc.Description = description;
                sc.Save();
            }
            catch { }
        }

        private void RegisterApplication(string uninstallerPath)
        {
            try
            {
                int estimatedSizeKb = 387000;
                try
                {
                    long totalBytes = 0;
                    foreach (string file in Directory.GetFiles(_installDir, "*", SearchOption.AllDirectories))
                    {
                        totalBytes += new FileInfo(file).Length;
                    }
                    estimatedSizeKb = (int)Math.Max(1, totalBytes / 1024);
                }
                catch { }

                using (var key = Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Uninstall\RAZBerry"))
                {
                    if (key != null)
                    {
                        key.SetValue("DisplayName", "RAZBerry Browser");
                        key.SetValue("DisplayVersion", "1.19.8b");
                        key.SetValue("Publisher", "RAZ Creative Studio");
                        key.SetValue("DisplayIcon", Path.Combine(_installDir, "RAZBerry.ico"));
                        key.SetValue("InstallLocation", _installDir);
                        key.SetValue("InstallDate", DateTime.Now.ToString("yyyyMMdd"));
                        key.SetValue("UninstallString", "\"" + uninstallerPath + "\"");
                        key.SetValue("QuietUninstallString", "\"" + uninstallerPath + "\"");
                        key.SetValue("EstimatedSize", estimatedSizeKb, RegistryValueKind.DWord);
                        key.SetValue("URLInfoAbout", "https://razberry.it-raz.com/");
                        key.SetValue("NoModify", 1, RegistryValueKind.DWord);
                        key.SetValue("NoRepair", 1, RegistryValueKind.DWord);
                    }
                }
            }
            catch { }
        }

        private void Worker_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            _progressBar.Value = Math.Min(100, Math.Max(0, e.ProgressPercentage));
            _lblPercent.Text = _progressBar.Value + "%";
            if (e.UserState != null)
            {
                _lblStatus.Text = e.UserState.ToString();
            }
        }

        private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            _isInstalling = false;
            _btnTopClose.Enabled = true;

            if (e.Error != null)
            {
                _lblStatus.Text = "Terjadi kendala: " + e.Error.Message;
                _lblStatus.ForeColor = PinkVibrant;
                _btnClose.Visible = true;
                _btnClose.Location = new Point((Width - _btnClose.Width) / 2, 314);
                return;
            }

            _progressBar.Value = 100;
            _lblPercent.Text = "100% — Selesai!";
            _lblStatus.Text = "RAZBerry Browser berhasil terpasang di:\n" + _installDir;
            _btnFinishOpen.Visible = true;
            _btnClose.Visible = true;
        }

        private void BtnFinishOpen_Click(object sender, EventArgs e)
        {
            string exePath = Path.Combine(_installDir, "razberry.exe");
            if (File.Exists(exePath))
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = exePath,
                    WorkingDirectory = _installDir,
                    UseShellExecute = true
                });
            }
            Close();
        }
    }

    /// <summary>
    /// Kontrol Progress Bar kustom dengan gradasi Black-Pink Raspberry.
    /// </summary>
    public sealed class PinkProgressBar : Control
    {
        private int _value;
        public int Value
        {
            get { return _value; }
            set
            {
                _value = Math.Min(100, Math.Max(0, value));
                Invalidate();
            }
        }

        public PinkProgressBar()
        {
            DoubleBuffered = true;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
            var trackRect = new Rectangle(0, 0, Width - 1, Height - 1);

            using (var trackBrush = new SolidBrush(Color.FromArgb(40, 22, 32)))
            {
                e.Graphics.FillRectangle(trackBrush, trackRect);
            }

            if (_value > 0)
            {
                int fillWidth = Math.Max(6, (int)(Width * (_value / 100.0)));
                var fillRect = new Rectangle(0, 0, fillWidth, Height);
                using (var grad = new LinearGradientBrush(
                    fillRect,
                    Color.FromArgb(216, 27, 96),
                    Color.FromArgb(255, 64, 129),
                    LinearGradientMode.Horizontal))
                {
                    e.Graphics.FillRectangle(grad, fillRect);
                }
            }

            using (var borderPen = new Pen(Color.FromArgb(95, 34, 62), 1f))
            {
                e.Graphics.DrawRectangle(borderPen, trackRect);
            }
        }
    }
}
