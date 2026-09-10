using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Microsoft.Web.WebView2.Core;
using TangyuanDolaStudio.Dialogs;
using TangyuanDolaStudio.Models;
using TangyuanDolaStudio.Services;

namespace TangyuanDolaStudio;

public partial class MainWindow : Window
{
    private readonly ProfileStore _profileStore = new();
    private readonly BrowserInstanceManager _browserManager;
    private readonly ObservableCollection<ProfileItem> _profiles = new();

    private ProfileItem? _activeProfile;
    private bool _isBusy;

    public MainWindow()
    {
        InitializeComponent();
        _browserManager = new BrowserInstanceManager(_profileStore);
        ProfilesList.ItemsSource = _profiles;

        DolaBrowserHost.StatusChanged += BrowserHost_StatusChanged;
        DolaBrowserHost.AddressChanged += BrowserHost_AddressChanged;
        DolaBrowserHost.RunningChanged += BrowserHost_RunningChanged;

        Loaded += MainWindow_Loaded;
        Closing += MainWindow_Closing;
    }

    private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
    {
        try
        {
            DetectRuntime();

            var loaded = await _profileStore.LoadAsync();
            foreach (var profile in loaded)
            {
                _profileStore.EnsureProfileFolders(profile);
                _profiles.Add(profile);
            }

            if (_profiles.Count == 0)
            {
                var a = NewProfile("Dola-001");
                var b = NewProfile("Dola-002");
                _profileStore.EnsureProfileFolders(a);
                _profileStore.EnsureProfileFolders(b);
                _profiles.Add(a);
                _profiles.Add(b);
            }

            await SaveProfilesAsync();
            ProfilesList.SelectedIndex = 0;
            StatusText.Text = "P1.1 Ready：先测试添加实例，再打开 Dola。";
            AppLogger.Info($"Main window initialized with {_profiles.Count} profile(s).");
        }
        catch (Exception ex)
        {
            AppLogger.Error("MainWindow initialization failed", ex);
            MessageBox.Show(this, $"初始化失败：\n{ex.Message}\n\n日志：{AppLogger.LogFile}", "Tangyuan Dola Studio",
                MessageBoxButton.OK, MessageBoxImage.Error);
            StatusText.Text = "初始化失败";
        }
    }

    private void DetectRuntime()
    {
        try
        {
            var version = CoreWebView2Environment.GetAvailableBrowserVersionString();
            RuntimeText.Text = $"WebView2：{version}";
            AppLogger.Info($"Detected WebView2 Runtime: {version}");
        }
        catch (Exception ex)
        {
            RuntimeText.Text = "WebView2：未检测到";
            AppLogger.Error("WebView2 runtime detection failed", ex);
        }
    }

    private void MainWindow_Closing(object? sender, CancelEventArgs e)
    {
        DolaBrowserHost.Close();
    }

    private ProfileItem NewProfile(string displayName) => new()
    {
        Id = Guid.NewGuid().ToString("N"),
        DisplayName = displayName,
        HomeUrl = "https://www.dola.com/chat/",
        CreatedAt = DateTimeOffset.Now
    };

    private Task SaveProfilesAsync() => _profileStore.SaveAsync(_profiles);

    private ProfileItem? SelectedProfile => ProfilesList.SelectedItem as ProfileItem;

    private void ProfilesList_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        RefreshProfileDetails(SelectedProfile);
    }

    private async void AddProfile_Click(object sender, RoutedEventArgs e)
    {
        if (_isBusy)
            return;

        try
        {
            var defaultName = $"Dola-{_profiles.Count + 1:000}";
            var dialog = new ProfileEditorDialog("添加账号实例", "给这个 Dola 实例起一个名称：", defaultName)
            {
                Owner = this
            };

            if (dialog.ShowDialog() != true)
                return;

            SetBusy(true, "正在创建账号实例...");
            var profile = NewProfile(dialog.ProfileName);
            _profileStore.EnsureProfileFolders(profile);
            _profiles.Add(profile);
            await SaveProfilesAsync();
            ProfilesList.SelectedItem = profile;

            AppLogger.Info($"Profile created: {profile.DisplayName} / {profile.Id}");
            StatusText.Text = $"已创建 {profile.DisplayName}。现在可点击“打开 / 切换账号”。";
        }
        catch (Exception ex)
        {
            AppLogger.Error("Add profile failed", ex);
            MessageBox.Show(this,
                $"添加账号实例失败，但程序不会退出。\n\n{ex.Message}\n\n日志：{AppLogger.LogFile}",
                "添加账号实例失败", MessageBoxButton.OK, MessageBoxImage.Error);
            StatusText.Text = "添加账号实例失败";
        }
        finally
        {
            SetBusy(false);
        }
    }

    private async void RenameProfile_Click(object sender, RoutedEventArgs e)
    {
        var profile = SelectedProfile;
        if (profile is null || _isBusy)
            return;

        try
        {
            var dialog = new ProfileEditorDialog("重命名账号实例", "新的实例名称：", profile.DisplayName)
            {
                Owner = this
            };

            if (dialog.ShowDialog() != true || dialog.ProfileName == profile.DisplayName)
                return;

            SetBusy(true, "正在保存实例名称...");
            profile.DisplayName = dialog.ProfileName;
            await SaveProfilesAsync();
            ProfilesList.Items.Refresh();
            RefreshProfileDetails(profile);
            StatusText.Text = "实例已重命名。";
        }
        catch (Exception ex)
        {
            AppLogger.Error("Rename profile failed", ex);
            ShowOperationError("重命名失败", ex);
        }
        finally
        {
            SetBusy(false);
        }
    }

    private async void DeleteProfile_Click(object sender, RoutedEventArgs e)
    {
        var profile = SelectedProfile;
        if (profile is null || _isBusy)
            return;

        var result = MessageBox.Show(this,
            $"删除实例“{profile.DisplayName}”？\n\n这会删除该实例的本地浏览器 Session 和下载目录。",
            "删除账号实例", MessageBoxButton.YesNo, MessageBoxImage.Warning);

        if (result != MessageBoxResult.Yes)
            return;

        try
        {
            SetBusy(true, "正在删除账号实例...");

            if (_activeProfile?.Id == profile.Id)
            {
                DolaBrowserHost.Close();
                _activeProfile = null;
            }

            _browserManager.Forget(profile);
            _profiles.Remove(profile);
            await SaveProfilesAsync();

            try
            {
                _profileStore.DeleteProfileData(profile);
            }
            catch (Exception ex)
            {
                AppLogger.Warn($"Profile data cleanup deferred: {ex.Message}");
            }

            ProfilesList.SelectedIndex = _profiles.Count > 0 ? 0 : -1;
            StatusText.Text = $"已删除 {profile.DisplayName}。";
        }
        catch (Exception ex)
        {
            AppLogger.Error("Delete profile failed", ex);
            ShowOperationError("删除失败", ex);
        }
        finally
        {
            SetBusy(false);
        }
    }

    private async void OpenProfile_Click(object sender, RoutedEventArgs e)
    {
        var profile = SelectedProfile;
        if (profile is null)
        {
            StatusText.Text = "请先选择一个账号实例。";
            return;
        }

        if (_isBusy)
            return;

        await OpenProfileAsync(profile);
    }

    private async Task OpenProfileAsync(ProfileItem profile)
    {
        SetBusy(true, $"正在启动 {profile.DisplayName} 的独立 WebView2 Session...");

        try
        {
            DolaBrowserHost.Close();
            _activeProfile = null;

            var environment = await _browserManager.GetEnvironmentAsync(profile);
            var downloads = _browserManager.GetDownloadsFolder(profile);

            await DolaBrowserHost.OpenAsync(environment, profile.HomeUrl, downloads);

            _activeProfile = profile;
            profile.LastOpenedAt = DateTimeOffset.Now;
            await SaveProfilesAsync();

            TopProfileText.Text = $"{profile.DisplayName} · 独立 Session";
            SessionStateText.Text = "浏览器：运行中";
            RefreshProfileDetails(profile);
            StatusText.Text = $"{profile.DisplayName} 已打开 Dola。首次请由你本人正常登录。";
            AppLogger.Info($"Profile opened: {profile.DisplayName} / {profile.Id}");
        }
        catch (WebView2RuntimeNotFoundException ex)
        {
            AppLogger.Error("WebView2 runtime not found", ex);
            DolaBrowserHost.Close();
            _activeProfile = null;
            MessageBox.Show(this,
                "未检测到 Microsoft Edge WebView2 Runtime。请先安装/更新 WebView2 Runtime。",
                "缺少 WebView2 Runtime", MessageBoxButton.OK, MessageBoxImage.Warning);
            StatusText.Text = "WebView2 Runtime 不可用";
        }
        catch (Exception ex)
        {
            AppLogger.Error($"Open profile failed: {profile.DisplayName}", ex);
            DolaBrowserHost.Close();
            _activeProfile = null;
            ShowOperationError("启动 Dola 浏览器失败", ex);
            StatusText.Text = "浏览器启动失败";
        }
        finally
        {
            SetBusy(false);
            RefreshProfileDetails(SelectedProfile);
        }
    }

    private void StopBrowser_Click(object sender, RoutedEventArgs e)
    {
        DolaBrowserHost.Close();
        _activeProfile = null;
        TopProfileText.Text = "未打开账号";
        RefreshProfileDetails(SelectedProfile);
        StatusText.Text = "当前浏览器已停止；Profile Session 数据仍保留。";
    }

    private void RefreshProfileDetails(ProfileItem? profile)
    {
        if (profile is null)
        {
            ProfileNameText.Text = "未选择";
            ProfileIdText.Text = "-";
            SessionStateText.Text = "浏览器：未启动";
            return;
        }

        ProfileNameText.Text = profile.DisplayName;
        ProfileIdText.Text = $"ID: {profile.Id}\nUDF: {_profileStore.GetWebViewDataFolder(profile)}";
        SessionStateText.Text = _activeProfile?.Id == profile.Id && DolaBrowserHost.IsRunning
            ? "浏览器：运行中"
            : "浏览器：未启动";
    }

    private void BrowserHost_StatusChanged(object? sender, string message)
    {
        if (!Dispatcher.CheckAccess())
        {
            Dispatcher.Invoke(() => BrowserHost_StatusChanged(sender, message));
            return;
        }

        StatusText.Text = message;
    }

    private void BrowserHost_AddressChanged(object? sender, string address)
    {
        if (!Dispatcher.CheckAccess())
        {
            Dispatcher.Invoke(() => BrowserHost_AddressChanged(sender, address));
            return;
        }

        AddressBox.Text = address;
    }

    private void BrowserHost_RunningChanged(object? sender, bool running)
    {
        if (!Dispatcher.CheckAccess())
        {
            Dispatcher.Invoke(() => BrowserHost_RunningChanged(sender, running));
            return;
        }

        SessionStateText.Text = running ? "浏览器：运行中" : "浏览器：未启动";
    }

    private void Home_Click(object sender, RoutedEventArgs e)
    {
        NavigateSafe(_activeProfile?.HomeUrl ?? SelectedProfile?.HomeUrl ?? "https://www.dola.com/chat/");
    }

    private void Back_Click(object sender, RoutedEventArgs e) => DolaBrowserHost.GoBack();
    private void Forward_Click(object sender, RoutedEventArgs e) => DolaBrowserHost.GoForward();
    private void Refresh_Click(object sender, RoutedEventArgs e) => DolaBrowserHost.Reload();
    private void Navigate_Click(object sender, RoutedEventArgs e) => NavigateSafe(AddressBox.Text);

    private void AddressBox_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter)
            NavigateSafe(AddressBox.Text);
    }

    private void NavigateSafe(string? input)
    {
        try
        {
            DolaBrowserHost.Navigate(input ?? string.Empty);
        }
        catch (Exception ex)
        {
            AppLogger.Error("Navigation failed", ex);
            StatusText.Text = ex.Message;
        }
    }

    private void OpenDownloads_Click(object sender, RoutedEventArgs e)
    {
        var profile = _activeProfile ?? SelectedProfile;
        if (profile is null)
        {
            StatusText.Text = "请先选择账号实例。";
            return;
        }

        try
        {
            var folder = _browserManager.GetDownloadsFolder(profile);
            Process.Start(new ProcessStartInfo("explorer.exe", folder) { UseShellExecute = true });
        }
        catch (Exception ex)
        {
            AppLogger.Error("Open downloads folder failed", ex);
            ShowOperationError("打开下载目录失败", ex);
        }
    }

    private void OpenLogs_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            Directory.CreateDirectory(AppLogger.LogDirectory);
            Process.Start(new ProcessStartInfo("explorer.exe", AppLogger.LogDirectory) { UseShellExecute = true });
        }
        catch (Exception ex)
        {
            AppLogger.Error("Open log folder failed", ex);
            ShowOperationError("打开日志目录失败", ex);
        }
    }

    private void SetBusy(bool busy, string? message = null)
    {
        _isBusy = busy;
        AddProfileButton.IsEnabled = !busy;
        OpenProfileButton.IsEnabled = !busy;
        ProfilesList.IsEnabled = !busy;
        Mouse.OverrideCursor = busy ? Cursors.Wait : null;
        if (!string.IsNullOrWhiteSpace(message))
            StatusText.Text = message;
    }

    private void ShowOperationError(string title, Exception ex)
    {
        MessageBox.Show(this,
            $"{title}：\n{ex.Message}\n\n日志：{AppLogger.LogFile}",
            title, MessageBoxButton.OK, MessageBoxImage.Error);
    }
}
