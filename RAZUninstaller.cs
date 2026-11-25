// ==============================================================================
// RAZUninstaller.cs
// Uninstaller Wizard Standalone RAZBerry Browser (Gaya Floating Banner)
// Tema: Black-Pink Raspberry (Selaras dengan RAZBerrySetup.exe)
// Author: RAZ Creative Studio
// Timestamp: 2026-11-25
// ==============================================================================

using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Win32;

namespace RAZBerryUninstaller
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
            Application.Run(new FloatingUninstallerForm());
        }
    }

    public sealed class FloatingUninstallerForm : Form
    {
        private static readonly Color BgDark = Color.FromArgb(17, 10, 14);
        private static readonly Color SurfaceDark = Color.FromArgb(26, 16, 22);
        private static readonly Color PinkPrimary = Color.FromArgb(216, 27, 96);
        private static readonly Color PinkVibrant = Color.FromArgb(255, 64, 129);
        private static readonly Color BorderPink = Color.FromArgb(95, 34, 62);
        private static readonly Color TextPrimary = Color.FromArgb(253, 240, 245);
        private static readonly Color TextMuted = Color.FromArgb(196, 168, 182);

        [DllImport("Gdi32.dll", EntryPoint = "CreateRoundRectRgn")]
        private static extern IntPtr CreateRoundRectRgn(int nLeftRect, int nTopRect, int nRightRect, int nBottomRect, int nWidthEllipse, int nHeightEllipse);

        [DllImport("user32.dll")]
        private static extern bool ReleaseCapture();

        [DllImport("user32.dll")]
        private static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);

        private const int WM_NCLBUTTONDOWN = 0xA1;
        private const int HT_CAPTION = 0x2;

        private Label _lblTitle;
        private Label _lblSubtitle;
        private Label _lblStatus;
        private CheckBox _chkRemoveProfile;
        private PinkProgressBar _progressBar;
        private Label _lblPercent;
        private Button _btnUninstall;
        private Button _btnCancel;
        private Button _btnFinish;
        private Label _btnTopClose;

        private readonly string _installDir;
        private readonly BackgroundWorker _worker;
        private bool _isUninstalling = false;
        private bool _uninstallDone = false;

        public FloatingUninstallerForm()
        {
            string exeDir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd(Path.DirectorySeparatorChar);
            string defaultDir = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "RAZBerry"
            );
            _installDir = File.Exists(Path.Combine(exeDir, "razberry.exe")) ? exeDir : defaultDir;

            InitializeForm();
            InitializeControls();

            _worker = new BackgroundWorker
            {
                WorkerReportsProgress = true
            };
            _worker.DoWork += Worker_DoWork;
            _worker.ProgressChanged += Worker_ProgressChanged;
            _worker.RunWorkerCompleted += Worker_RunWorkerCompleted;
        }

        private void InitializeForm()
        {
            Text = "Uninstall RAZBerry Browser";
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
            using (var pen = new Pen(BorderPink, 2f))
            {
                var path = new GraphicsPath();
                int r = 20 * 2;
                var rect = new Rectangle(1, 1, Width - 3, Height - 3);
                path.AddArc(rect.X, rect.Y, r, r, 180, 90);
                path.AddArc(rect.Right - r, rect.Y, r, r, 270, 90);
                path.AddArc(rect.Right - r, rect.Bottom - r, r, r, 0, 90);
                path.AddArc(rect.X, rect.Bottom - r, r, r, 90, 90);
                path.CloseFigure();
                e.Graphics.DrawPath(pen, path);
            }
        }

        private Image LoadEmbeddedImage(string resourceName)
        {
            var asm = Assembly.GetExecutingAssembly();
            using (var stream = asm.GetManifestResourceStream(resourceName))
            {
                if (stream != null) return Image.FromStream(stream);
            }
            return null;
        }

        private void InitializeControls()
        {
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
            _btnTopClose.Click += (s, e) => { if (!_isUninstalling) Close(); };
            _btnTopClose.MouseEnter += (s, e) => { if (!_isUninstalling) _btnTopClose.ForeColor = PinkVibrant; };
            _btnTopClose.MouseLeave += (s, e) => { _btnTopClose.ForeColor = TextMuted; };
            Controls.Add(_btnTopClose);

            var pbBerry = new PictureBox
            {
                Size = new Size(76, 76),
                Location = new Point(164, 34),
                SizeMode = PictureBoxSizeMode.Zoom,
                BackColor = Color.Transparent,
                Image = LoadEmbeddedImage("LogoRazBerry.png")
            };
            pbBerry.MouseDown += Form_MouseDown;
            Controls.Add(pbBerry);

            var divider = new Panel
            {
                Size = new Size(1, 46),
                Location = new Point(254, 49),
                BackColor = BorderPink
            };
            Controls.Add(divider);

            var pbStudio = new PictureBox
            {
                Size = new Size(118, 62),
                Location = new Point(268, 41),
                SizeMode = PictureBoxSizeMode.Zoom,
                BackColor = Color.Transparent,
                Image = LoadEmbeddedImage("LogoRazStudio.png")
            };
            pbStudio.MouseDown += Form_MouseDown;
            Controls.Add(pbStudio);

            _lblTitle = new Label
            {
                Text = "Uninstall RAZBerry Browser",
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

            _lblStatus = new Label
            {
                Text = "Apakah Anda yakin ingin menghapus RAZBerry Browser dari perangkat ini?\nLokasi: " + _installDir,
                Font = new Font("Segoe UI", 9F, FontStyle.Regular),
                ForeColor = TextMuted,
                BackColor = Color.Transparent,
                Size = new Size(Width - 64, 42),
                Location = new Point(32, 198),
                TextAlign = ContentAlignment.MiddleCenter
            };
            _lblStatus.MouseDown += Form_MouseDown;
            Controls.Add(_lblStatus);

            _chkRemoveProfile = new CheckBox
            {
                Text = "Hapus juga data profil, riwayat, & bookmark pengguna",
                Checked = false,
                Font = new Font("Segoe UI", 9F, FontStyle.Regular),
                ForeColor = TextPrimary,
                BackColor = Color.Transparent,
                AutoSize = true,
                Location = new Point(116, 252),
                Cursor = Cursors.Hand
            };
            Controls.Add(_chkRemoveProfile);

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

            _btnUninstall = CreateStyledButton("Uninstall", true, new Point(132, 314), new Size(134, 42));
            _btnUninstall.Click += BtnUninstall_Click;
            Controls.Add(_btnUninstall);

            _btnCancel = CreateStyledButton("Cancel", false, new Point(276, 314), new Size(134, 42));
            _btnCancel.Click += (s, e) => Close();
            Controls.Add(_btnCancel);

            _btnFinish = CreateStyledButton("Finish", true, new Point((Width - 150) / 2, 314), new Size(150, 42));
            _btnFinish.Visible = false;
            _btnFinish.Click += (s, e) => Close();
            Controls.Add(_btnFinish);
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

        private void BtnUninstall_Click(object sender, EventArgs e)
        {
            _isUninstalling = true;
            _btnUninstall.Visible = false;
            _btnCancel.Visible = false;
            _chkRemoveProfile.Visible = false;
            _btnTopClose.Enabled = false;

            _progressBar.Visible = true;
            _lblPercent.Visible = true;
            _lblStatus.Text = "Memulai proses penghapusan RAZBerry Browser...";

            _worker.RunWorkerAsync(_chkRemoveProfile.Checked);
        }

        private void Worker_DoWork(object sender, DoWorkEventArgs e)
        {
            bool removeProfile = (bool)e.Argument;

            // 1. Tutup proses razberry.exe
            _worker.ReportProgress(10, "Menutup proses RAZBerry Browser yang aktif...");
            foreach (var proc in Process.GetProcessesByName("razberry"))
            {
                try { proc.Kill(); proc.WaitForExit(3000); } catch { }
            }

            // 2. Hapus shortcut Desktop & folder Start Menu RAZBerry
            _worker.ReportProgress(25, "Menghapus shortcut Desktop & folder Start Menu RAZBerry...");
            try
            {
                string desktopLnk = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory), "RAZBerry.lnk");
                if (File.Exists(desktopLnk)) File.Delete(desktopLnk);

                string startMenuRoot = Environment.GetFolderPath(Environment.SpecialFolder.Programs);
                string startMenuOldLnk = Path.Combine(startMenuRoot, "RAZBerry.lnk");
                if (File.Exists(startMenuOldLnk)) File.Delete(startMenuOldLnk);

                string startMenuFolder = Path.Combine(startMenuRoot, "RAZBerry");
                if (Directory.Exists(startMenuFolder)) Directory.Delete(startMenuFolder, true);
            }
            catch { }

            // 3. Hapus Registry Uninstall entry
            _worker.ReportProgress(40, "Membersihkan registrasi sistem Windows...");
            try
            {
                Registry.CurrentUser.DeleteSubKeyTree(@"Software\Microsoft\Windows\CurrentVersion\Uninstall\RAZBerry", false);
            }
            catch { }

            // 4. Hapus file aplikasi di _installDir (kecuali self-executable yang sedang berjalan)
            _worker.ReportProgress(55, "Menghapus berkas aplikasi RAZBerry...");
            string selfPath = Application.ExecutablePath;
            if (Directory.Exists(_installDir))
            {
                try
                {
                    foreach (var dir in Directory.GetDirectories(_installDir))
                    {
                        try { Directory.Delete(dir, true); } catch { }
                    }
                    foreach (var file in Directory.GetFiles(_installDir))
                    {
                        if (string.Equals(Path.GetFullPath(file), Path.GetFullPath(selfPath), StringComparison.OrdinalIgnoreCase))
                            continue;
                        try { File.Delete(file); } catch { }
                    }
                }
                catch { }
            }

            // 5. Hapus data profil jika diminta
            if (removeProfile)
            {
                _worker.ReportProgress(85, "Menghapus data profil pengguna...");
                try
                {
                    string roamingProf = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "razberry");
                    string localProf = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "razberry");
                    if (Directory.Exists(roamingProf)) Directory.Delete(roamingProf, true);
                    if (Directory.Exists(localProf) && !string.Equals(Path.GetFullPath(localProf), Path.GetFullPath(_installDir), StringComparison.OrdinalIgnoreCase))
                        Directory.Delete(localProf, true);
                }
                catch { }
            }

            Thread.Sleep(250);
            _uninstallDone = true;
            _worker.ReportProgress(100, "RAZBerry Browser berhasil dihapus dari perangkat Anda.");
        }

        private void Worker_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            _progressBar.Value = Math.Min(100, Math.Max(0, e.ProgressPercentage));
            _lblPercent.Text = _progressBar.Value + "%";
            if (e.UserState != null) _lblStatus.Text = e.UserState.ToString();
        }

        private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            _isUninstalling = false;
            _btnTopClose.Enabled = true;
            _progressBar.Value = 100;
            _lblPercent.Text = "100% — Selesai!";
            _btnFinish.Visible = true;
        }

        protected override void OnFormClosed(FormClosedEventArgs e)
        {
            base.OnFormClosed(e);
            if (_uninstallDone && Directory.Exists(_installDir))
            {
                // Jadwalkan penghapusan diri & folder induk 2 detik setelah proses keluar
                try
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = "cmd.exe",
                        Arguments = string.Format("/C timeout /T 2 /NOBREAK > NUL & rmdir /S /Q \"{0}\"", _installDir),
                        WindowStyle = ProcessWindowStyle.Hidden,
                        CreateNoWindow = true
                    });
                }
                catch { }
            }
        }
    }

    public sealed class PinkProgressBar : Control
    {
        private int _value;
        public int Value
        {
            get { return _value; }
            set { _value = Math.Min(100, Math.Max(0, value)); Invalidate(); }
        }

        public PinkProgressBar() { DoubleBuffered = true; }

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
                using (var grad = new LinearGradientBrush(fillRect, Color.FromArgb(216, 27, 96), Color.FromArgb(255, 64, 129), LinearGradientMode.Horizontal))
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
